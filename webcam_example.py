import os
import sys
import time

import cv2
import matplotlib.pyplot as plt

import msgpack as mp
import msgpack_numpy as mpn

from scipy import signal
from cv2 import aruco
import numpy as np

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



cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

ARUCO_PARAMETERS = aruco.DetectorParameters()
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
detector = aruco.ArucoDetector(ARUCO_DICT, ARUCO_PARAMETERS)
markerLength = 0.04
markerSeperation = 0.01

board = aruco.GridBoard(
        size= [1,1],
        markerLength=markerLength,
        markerSeparation=markerSeperation,
        dictionary=ARUCO_DICT)

# Create vectors we'll be using for rotations and translations for postures
rotation_vectors, translation_vectors = None, None
axis = np.float32([[-.5, -.5, 0], [-.5, .5, 0], [.5, .5, 0], [.5, -.5, 0],
                   [-.5, -.5, 1], [-.5, .5, 1], [.5, .5, 1], [.5, -.5, 1]])

marker_size = markerLength

marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                            [marker_size / 2, marker_size / 2, 0],
                            [marker_size / 2, -marker_size / 2, 0],
                            [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)

def my_estimatePoseSingleMarkers(corners, marker_points, mtx, distortion):
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, flags= cv2.SOLVEPNP_ITERATIVE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash


while cap.isOpened():
    
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected_image_points = detector.detectMarkers(gray)
        corners, ids, rejectedpoints,_ = detector.refineDetectedMarkers(image=gray,board=board ,detectedCorners=corners, detectedIds=ids, rejectedCorners=rejected_image_points, cameraMatrix=cameraMatrix, distCoeffs=distCoeffs)
        rvec, tvec,_  = my_estimatePoseSingleMarkers(corners, marker_points, cameraMatrix, distCoeffs)
        
        if ids is not None and len(ids) > 0:
            # Estimate the posture per each Aruco marker
            rotation_vectors, translation_vectors, _objPoints = my_estimatePoseSingleMarkers(corners, marker_points, cameraMatrix, distCoeffs)
            for rvec, tvec in zip(rotation_vectors, translation_vectors):
                frame = aruco.drawDetectedMarkers(frame, corners=corners, ids=ids)
                frame = cv2.drawFrameAxes(frame, cameraMatrix, distCoeffs, rvec, tvec, 0.05)
                tvec_dist = tvec

        else:
            pass
        
        cv2.imshow("aruco", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cv2.destroyAllWindows()