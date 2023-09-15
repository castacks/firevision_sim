import pyautogui
from datetime import datetime
import os
from pathlib import Path
import platform
from subprocess import Popen
import time
import pyautogui as pygui
import ImageComparisonProcessor as icp
from bayes_opt import BayesianOptimization
import pandas as pd
import cv2

# TEST_MODE = "single_fire_test"
TEST_MODE = "lightbulb_test"

PRIOR_RESULTS_DIR = r"c:\Users\John\Downloads\temp_params\results.csv"

LIGHTBULB_IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\current.png"
IMAGE_FOLDER = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor"
FIRE_IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\ScreenShot00000.png"
REF_LIGHTBULB_DIR = r"c:\Users\John\Downloads\Reference_Image\lightbulb_reference.png"
REF_SINGLE_FIRE_IMAGE = r"C:\Users\John\Downloads\Reference_Image\reference_single_fire.png"
TMP_PARAMS_DIR = r"c:\Users\John\Downloads\temp_params\params.csv"
MUTEX_DIR = r"C:\Users\John\Downloads\temp_params\mutex_unlock.txt"

# pyautogui.displayMousePosition()

#Compare Image
image = icp.image_from_file(LIGHTBULB_IMAGE_DIR)
cv2.imshow("image", image)
cv2.waitKey(0)
reference_image = icp.image_from_file(REF_LIGHTBULB_DIR)
cv2.imshow("Reference", reference_image)
cv2.waitKey(0)

# accuracy = icp.check_accuracy(image, reference_image) #gets accuracy
accuracy = icp.perceptualSimilarity(reference_image, image)
print(accuracy)