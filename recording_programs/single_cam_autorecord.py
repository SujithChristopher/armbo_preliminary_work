import pyautogui
import pywinauto
import pygetwindow as gw
from time import sleep
import os
import getopt
import sys
import subprocess
import keyboard
from art import tprint


python_program = os.path.join(os.getcwd(), "recording_programs", "record_webcam_and_controller.py")

_parent_folder = "omni_sensor_feb_14_2023" # this is the parent folder name where the data will be saved
_base_pth = os.getcwd()
_base_pth = os.path.join(_base_pth, "recording_programs", "test_data")

_txt_pth = os.path.join(_base_pth, _parent_folder,"00_analysis", "record_folders.txt")

def focus_to_window(window_title=None, move = False, moveval = None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
        if move:
            window.moveTo(1033, 174) # change this to move to position of the screen

def get_file_names():
    file = open(_txt_pth, "r")
    file_names = file.readlines()
    file.close()
    return file_names

def start_mocap_recording(_name):
    focus_to_window("Motive")
    pyautogui.tripleClick(475, 1009)
    sleep(0.5)
    pyautogui.write(_name)
    sleep(2)
    pyautogui.click(879, 1009)

def stop_mocap_recording():
    sleep(0.5)
    pyautogui.click(879, 1009)

def main_process(file_name):
    # print(_parent_folder, file_name)
    tprint(file_name[8:])

    process = subprocess.Popen(["python", python_program, "-f", _parent_folder, "-n", file_name, "-c", "False", "-s", "True"])
    
    sleep(1)

    pyautogui.click(1006, 1062) # position of taskbar
    first_keypress = keyboard.read_key()
    if first_keypress == "s":
        # start the recording for mocap
        start_mocap_recording(file_name)
    sleep(1)
    focus_to_window("webcam", True, (1388, 306))

    second_keypress = keyboard.read_key()            

    if second_keypress == "r":
        # the recording is not okay retake in a different folder
        # stop the recording for mocap

        stop_mocap_recording()
        pass
    elif second_keypress == "q":
        # stop the recording for mocap
        stop_mocap_recording()
    
    # third_keypress = keyboard.read_key()
    # if third_keypress == "q":
    #     # stop the recording for mocap
    #     stop_mocap_recording()
    
    process.wait()


def main():
    file_names = get_file_names()
    for file_name in file_names:
        main_process(file_name)
        
if __name__ == '__main__':
    main()