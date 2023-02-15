import pyautogui
import pywinauto
import pygetwindow as gw
from time import sleep
import os
import getopt
import sys
import subprocess

_parent_folder = "single_cam_dec_14"
_base_pth = os.path.dirname(os.getcwd())
_base_pth = os.path.join(_base_pth, "recording_programs", "test_data", _parent_folder)

_recorded_folder_list = os.listdir(os.path.join(_base_pth, _parent_folder))
_txt_pth = os.path.join(_base_pth, _parent_folder,"00_analysis", "record_folders.txt")

def focus_to_window(window_title=None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()

def get_file_names():
    file = open(_txt_pth, "r")
    file_names = file.readlines()
    file.close()
    return file_names

def main():
    file_names = get_file_names()
    for file_name in file_names:
        




    

if __name__ == '__main__':
    main()