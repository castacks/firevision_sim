import math 
from cgi import test
import pandas as pd
import ParametersClass as pc
from skimage.metrics import structural_similarity
from skimage.transform import resize
import cv2
import os
import numpy as np

#Directory of test results folder
TEST_RESULTS_PATH = ""
IMAGES_PATH = os.path.join(TEST_RESULTS_PATH, "images")

#Directory of reference image
REFERENCE_IMAGEPATH = ""

#Directory of results output
OUTPUT_PATH = 'output/'

TEST_MODE = 1
TEST_NAME = pc.test_name(TEST_MODE)


def path_from_index(df, index):
    return df.loc[df['image_index'] == index]

def image_from_file(file):
    #Extract image from file
    return cv2.imread(file)

#Peak Signal-to-Noise Ratio function taken from https://www.geeksforgeeks.org/python-peak-signal-to-noise-ratio-psnr/
def PSNR(test_image, reference_image):
    mse = np.mean((test_image - reference_image) ** 2)
    #If no noise, then it's perfect?
    if (mse == 0): 
        return 100 
    #The max value for a pixel is 255 
    max_pixel = 255
    psnr = 20 * math.log10(max_pixel/math.sqrt(mse))
    return mse

def check_accuracy(test_image, reference_image):
    #Resize in case different dimensions 
    if (test_image.shape[0] != reference_image.shape[0]) or (test_image.shape[1] != reference_image.shape[1]):
        test_image = resize(test_image, (reference_image.shape[0], reference_image.shape[1]), anti_aliasing=True, preserve_range=True)  
    return structural_similarity(test_image, reference_image, channel_axis=2, multichannel=True, data_range=1)


def process_data(test_results_path, reference_imagepath, output_path, test_mode):
    data_df = pd.read_csv(test_results_path + "\\" + pc.test_name(test_mode) + "raw_data.xlsx")
    results_df = pd.DataFrame(columns=['accuracy', 'PSNR', 'image_index'])
    
    reference_image = image_from_file(reference_imagepath + 'reference.png')
    
    for i in data_df.image_index:
        filepath = path_from_index(data_df, i) #gets file path
        image = image_from_file(filepath) #gets image from file path
        accuracy = check_accuracy(image, reference_image) #gets accuracy
        psnr = PSNR(image,reference_image) #gets PSNR
        row = pd.Series({"accuracy": accuracy, "PSNR":psnr, "image_index": i}) #creates row
        
        pd.concat([results_df, row], ignore_index=True, in_place=True) #concats row to results_df

    # Merges results (with accuracies) and data (with params)
    results_df = results_df.merge(data_df, on='image_index')
    results_df.to_excel(output_path + "\\" + pc.test_name(test_mode) + "_results.xlsx", index=False)

def main():
    process_data(TEST_RESULTS_PATH, REFERENCE_IMAGEPATH, OUTPUT_PATH, TEST_MODE)
