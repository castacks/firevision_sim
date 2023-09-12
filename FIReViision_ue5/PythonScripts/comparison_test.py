import math 
from cgi import test
import pandas as pd
import ParametersClass as pc
from skimage.metrics import structural_similarity
from skimage.transform import resize
import cv2
import os
import numpy as np
import ImageComparisonProcessor as icp

IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\current.png"
NEXT_IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\Next.png"

REF_IMAGE_DIR = r"c:\Users\John\Downloads\Reference_Image\lightbulb_reference.png"
TMP_PARAMS_DIR = r"c:\Users\John\Downloads\temp_params\params.csv"

image = icp.image_from_file(IMAGE_DIR)
reference_image = icp.image_from_file(REF_IMAGE_DIR)
accuracy = icp.check_accuracy(image, reference_image) #gets accuracy

next_image = icp.image_from_file(NEXT_IMAGE_DIR)

control_acc1 = icp.check_accuracy(image, image)
control_acc2 = icp.check_accuracy(reference_image, reference_image)
control_acc3 = icp.check_accuracy(image, next_image)

print(accuracy)
print(f"Control Accuracy 1: {control_acc1}")
print(f"Control Accuracy 2: {control_acc2}")
print(f"Control Accuracy 3: {control_acc3}")