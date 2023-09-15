from datetime import datetime
#
# This file runs on an infinite loop and waits until the 
# mutex file is created which "gives it permission" to 
# take and image using pyautogui to manually press "f9" 
# to take an image in the unreal editor
#
#


import os
from pathlib import Path
import platform
from subprocess import Popen
import pandas as pd
import pyautogui as pygui
import time

import unreal

IMAGE_PATH = r"c:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor"
IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\ScreenShot00000.png"

MUTEX_DIR = r"C:\Users\John\Downloads\temp_params\mutex_unlock.txt"

print("image taking is running")
while(True):
    if(os.path.exists(MUTEX_DIR)):
        #Generate Image
        pygui.click(x=465, y=374)
        pygui.hotkey('f9')
        time.sleep(0.3)
        os.remove(MUTEX_DIR)
        
    time.sleep(0.1)
    
print("should never get here")
