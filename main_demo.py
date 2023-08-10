import os
import sys
import time

import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from cv2 import aruco

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui

import msgpack as mp
import msgpack_numpy as mpn

from scipy import signal
import pickle



# from support.pymf import get_MF_devices as get_camera_list
from gui_box_v2 import Ui_MainWindow
from support.support_mp4 import generate_pdf
from pdf_py import run_analysis
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons


# mp_pose = mp.solutions.pose

"""open file dialog and path selection"""
calib_pth = ".//calibration//webcam_calibration.msgpack"
print(str(calib_pth))
# Check for camera calibration data
if not os.path.exists(calib_pth):
    print("You need to calibrate the camera you'll be using. See calibration project directory for details.")
    exit()
else:    
    with open(calib_pth, "rb") as f:
        webcam_calib = mp.Unpacker(f, object_hook=mpn.decode)
        _temp = next(webcam_calib)
        cameraMatrix = _temp[0]
        distCoeffs = _temp[1]
    if cameraMatrix is None or distCoeffs is None:
        print(
            "Calibration issue. Remove ./calibration/CameraCalibration.pckl and recalibrate your camera with calibration_ChAruco.py.")
        exit()

# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

# Create grid board object we're using in our stream
board = aruco.GridBoard_create(
    markersX=1,
    markersY=1,
    markerLength=0.045,
    markerSeparation=0.01,
    dictionary=ARUCO_DICT)

# Create vectors we'll be using for rotations and translations for postures
rotation_vectors, translation_vectors = None, None
axis = np.float32([[-.5, -.5, 0], [-.5, .5, 0], [.5, .5, 0], [.5, -.5, 0],
                   [-.5, -.5, 1], [-.5, .5, 1], [.5, .5, 1], [.5, -.5, 1]])


def find_peaks(data, threshold):
    count = 0
    trigger = True
    for i in data:
        if i > threshold and trigger:
            count += 1
            trigger = False
        if i < threshold and not trigger:
            trigger = True
    return count


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(QImage)
    progress = pyqtSignal(QImage)
    changePixmap = pyqtSignal(QImage)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            pass
        else:
            pass
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    xyRectPos = pyqtSignal(int)
    imageStatus = pyqtSignal(str)
    progress_callback = pyqtSignal(QImage)
    newPixmap = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        self.setupUi(self)
        self.threadpool = QThreadPool()

        self.t_vec = []
        self.r_vec = []

        self.pose = False
        self.data_points = np.nan
        self.data_points = np.array(self.data_points)

        self.disp_pose.stateChanged.connect(self.checkedcpp)
        self.start_button.clicked.connect(self.readImage)
        self.start_program.clicked.connect(self.start_process)
        self.set_orgin.clicked.connect(self.orign_set)

        self.start_p = False
        self.cur_time = 0
        self.time_count = 0
        self.res = []
        self.cl_names = ["time", "X", "Y", "Z"]

        # selecting the webcam
        self.capture_device = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.capture_device.set(cv2.CAP_PROP_FPS, 30)
        
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEventExit)
        self.close_button_pressed = False

        self.cam_space = pd.DataFrame(columns=self.cl_names)
        self.cam_space = self.cam_space.astype(np.float32)
        
    def closeEventExit(self):
        time.sleep(0.5)
        self.close_button_pressed = True
        self.capture_device.release()
        self.close()
        sys.exit()

    def orign_set(self):
        pass

    def checkedcpp(self, checked):
        if checked:
            self.pose = True
        else:
            self.pose = False

    def readImage(self):
        worker = Worker(self.runCam)
        worker.signals.progress.connect(self.set_image)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.result.connect(self.thread_complete)
        self.threadpool.start(worker)


    def start_process(self):
        self.start_p = True

    def do_nothing(self):
        pass

    def print_progress(self):
        pass

    def thread_complete(self):
        print("thread completed")
        self.cam.release()

    @pyqtSlot(QImage)
    def set_image(self, image):
        self.video_disp.setPixmap(QPixmap.fromImage(image))

    def runCam(self, progress_callback):
        tr = True
        self.peaks = 0

        count = 0
        ln = len(self.cam_space.columns)
        empt_list = []
        for i in range(ln):
            empt_list.append(np.nan)

        time_tr = True

        while True:

            # Capture frame-by-frame
            if self.close_button_pressed:
                break
            
            ret, frame = self.capture_device.read()
            if ret:
                # img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # image = img[yPos * 2:yPos * 2 + yRes, xPos * 2:xPos * 2 + xRes].copy()
                image = img.copy()

                self.colorImage = image

                if self.start_p and time_tr:
                    self.st_time = time.time()

                    time_tr = False

                if self.start_p:
                    self.cur_time = time.time()
                    self.time_count = int(self.cur_time - self.st_time)
                    self.time_float = self.cur_time - self.st_time

                if self.pose:
                    try:

                        gray = cv2.cvtColor(self.colorImage, cv2.COLOR_BGR2GRAY)
                        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT,
                                                                              parameters=ARUCO_PARAMETERS)
                        corners, ids, rejectedImgPoints, recoveredIds = aruco.refineDetectedMarkers(
                            image=gray,
                            board=board,
                            detectedCorners=corners,
                            detectedIds=ids,
                            rejectedCorners=rejectedImgPoints,
                            cameraMatrix=cameraMatrix,
                            distCoeffs=distCoeffs)

                        self.colorImage = aruco.drawDetectedMarkers(self.colorImage, corners, borderColor=(0, 0, 255))

                        # results = self.holistic.process(self.colorImage)
                        if self.start_p:
                            if ids is not None and len(ids) > 0:
                                # Estimate the posture per each Aruco marker
                                rotation_vectors, translation_vectors, _objPoints = aruco.estimatePoseSingleMarkers(
                                    corners, 0.04,
                                    cameraMatrix,
                                    distCoeffs)
                                for rvec, tvec in zip(rotation_vectors, translation_vectors):
                                    self.colorImage = aruco.drawAxis(self.colorImage, cameraMatrix, distCoeffs, rvec,
                                                                     tvec, 0.04)
                                    self.tvec_dist = tvec


                            else:
                                pass
                    except:
                        pass
                flpimg = self.colorImage
                flpimg = cv2.resize(flpimg, (960, 540))
                h1, w1, ch = flpimg.shape
                bytesPerLine = ch * w1
                convertToQtFormat = QImage(flpimg.data.tobytes(), w1, h1, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(960, 540, Qt.KeepAspectRatio)

                if self.start_p and tr:
                    img12 = cv2.cvtColor(self.colorImage, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(".//src//color.jpeg", img12)
                    tr = False

                if self.time_count >= 500 and self.start_p:
                    self.run_analysis()
                    self.start_p = False

                if self.start_p:
                    try:
                        self.label_x.setText(str(f"X {round(self.tvec_dist[0][0], 2)} m"))
                        self.label_y.setText(str(f"Y {round(self.tvec_dist[0][1], 2)} m"))
                        self.label_z.setText(str(f"Z {round(self.tvec_dist[0][2], 2)} m"))
                    except:
                        pass

                progress_callback.emit(p)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    # ImageUpdate()
    w.show()
    sys.exit(app.exec_())
