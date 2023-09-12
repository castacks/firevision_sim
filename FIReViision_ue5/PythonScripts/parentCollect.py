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

TEST_MODE = "single_fire_test"
# TEST_MODE = "lightbulb_test"

PRIOR_RESULTS_DIR = r"c:\Users\John\Downloads\temp_params\results.csv"

LIGHTBULB_IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\current.png"
IMAGE_FOLDER = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor"
FIRE_IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\ScreenShot00000.png"
REF_LIGHTBULB_DIR = r"c:\Users\John\Downloads\Reference_Image\lightbulb_reference.png"
REF_SINGLE_FIRE_IMAGE = r"C:\Users\John\Downloads\Reference_Image\reference_single_fire.png"
TMP_PARAMS_DIR = r"c:\Users\John\Downloads\temp_params\params.csv"
MUTEX_DIR = r"C:\Users\John\Downloads\temp_params\mutex_unlock.txt"
# TAKE_IMAGE_SCRIPT = r"C:\Users\John\Wildfire_Development\firevision_sim\FIReViision_ue5\PythonScripts\TakeSingleImage.py"
image_index = 0

def black_box_function_lightbulb(blend_weight, brightness, contrast, cold_brightness_multiplier, cold_power, hot_brightness_multiplier, hot_power, light_bulb_heat_multiplier, lamp_heat_multiplier):
    if(os.path.exists(PRIOR_RESULTS_DIR)):
        prior_results = pd.read_csv(PRIOR_RESULTS_DIR)
        result_row = prior_results.loc[
            prior_results["blend_weight"] == blend_weight and 
            prior_results["brightness"] == brightness and 
            prior_results["contrast"] == contrast and 
            prior_results["cold_brightness_multiplier"] == cold_brightness_multiplier and 
            prior_results["cold_power"] == cold_power and 
            prior_results["hot_brightness_multiplier"] == hot_brightness_multiplier and 
            prior_results["hot_power"] == hot_power and 
            prior_results["light_bulb_heat_multiplier"] == light_bulb_heat_multiplier and 
            prior_results["lamp_heat_multiplier"] == lamp_heat_multiplier].target != 0
        if(result_row != None and result_row.target != 0):
            return result_row.target
    row ={
        "index" : "0",
        "blend_weight" :blend_weight,
        "brightness" : brightness,
        "contrast" : contrast,
        "cold_brightness_multiplier" : cold_brightness_multiplier,
        "cold_power" : cold_power,
        "hot_brightness_multiplier" : hot_brightness_multiplier,
        "hot_power" : hot_power,
        "light_bulb_heat_multiplier" : light_bulb_heat_multiplier,
        "lamp_heat_multiplier" : lamp_heat_multiplier
        }
    print(row)
    
    
    params = pd.DataFrame(row, index=[0])
    
    #Write Params to file
    params.to_csv(TMP_PARAMS_DIR)
    while(not os.path.exists(TMP_PARAMS_DIR)):
        time.sleep(0.1)
        
        
    #Mutes all scene symbols
    pygui.click(x=1131,y=515)
    pygui.press('g')
    
    #Generate Image
    pygui.click(x=433, y=1138)
    pygui.write("TakeSingleImage.py")
    pygui.press('enter')
    
    #Wait for image to be generated
    while(not os.path.exists(LIGHTBULB_IMAGE_DIR)):
        time.sleep(0.1)
    
    try:
        #Compare Image
        image = icp.image_from_file(LIGHTBULB_IMAGE_DIR)
        reference_image = icp.image_from_file(REF_LIGHTBULB_DIR)
        accuracy = icp.check_accuracy(image, reference_image) #gets accuracyg
    except:
        accuracy = 0    
    #Cleanup
    os.remove(TMP_PARAMS_DIR)
    os.remove(LIGHTBULB_IMAGE_DIR)
    
    print(accuracy)
    return accuracy

def black_box_function_single_fire(blend_weight, brightness, contrast, cold_brightness_multiplier, cold_power, hot_brightness_multiplier, hot_power, sky_heat, ground_heat_correction, tree_correction_strength):
    row ={
        "index" : "0",
        "blend_weight" :blend_weight,
        "brightness" : brightness,
        "contrast" : contrast,
        "cold_brightness_multiplier" : cold_brightness_multiplier,
        "cold_power" : cold_power,
        "hot_brightness_multiplier" : hot_brightness_multiplier,
        "hot_power" : hot_power,
        "sky_heat" : sky_heat,
        "ground_heat_correction" : ground_heat_correction,
        "tree_correction_strength" : tree_correction_strength 
        }
    print(row)
    
    params = pd.DataFrame(row, index=[0])
    
    #Write Params to file
    params.to_csv(TMP_PARAMS_DIR)
    while(not os.path.exists(TMP_PARAMS_DIR)):
        time.sleep(0.1)
        
    
    #Generate Image
    pygui.click(x=433, y=1138)
    pygui.write("ChangeParams.py")
    pygui.press('enter')
    
    # path = r"c:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor"

    while(os.path.exists(MUTEX_DIR) or not os.path.exists(FIRE_IMAGE_DIR)):
        time.sleep(0.1)
                
    #Compare Image
    try:
        image = icp.image_from_file(FIRE_IMAGE_DIR)
        x, y, w, h = 519, 11, 557, 1019
        image = image[y:y+h, x:x+w]
        
        reference_image = icp.image_from_file(REF_SINGLE_FIRE_IMAGE)
        accuracy = icp.check_accuracy(image, reference_image) #gets accuracy
    except:
        print("error")
        accuracy = 0
    #Cleanup
    
        
    os.remove(TMP_PARAMS_DIR)
    
    for f in os.listdir(IMAGE_FOLDER):
        if(isinstance(f, str) and os.path.exists(os.path.join(IMAGE_FOLDER, f))):
            os.remove(os.path.join(IMAGE_FOLDER, f))
    return accuracy


def main():

    # Bounded region of parameter space
    pbounds = {}
    # optimizer = BayesianOptimization()
    if (TEST_MODE == "lightbulb_test"):
        pbounds = {'blend_weight': (50, 100), 
                'brightness': (50, 100), 
                'contrast': (50, 100), 
                'cold_brightness_multiplier': (0, 0.1), 
                'cold_power': (0.7, 1.3), 
                'hot_brightness_multiplier': (0.3, 0.5), 
                'hot_power': (-0.3, 0.3), 
                'light_bulb_heat_multiplier': (1, 2),
                'lamp_heat_multiplier': (1, 1.5)}
        
        optimizer = BayesianOptimization(
            f=black_box_function_lightbulb,
            pbounds=pbounds,
            random_state=1,
        )
        
    # if(TEST_MODE == "single_fire_test"):
    else:
        print("starting bounds")
        pbounds = {'blend_weight': (50, 100), 
                'brightness': (50, 100), 
                'contrast': (0, 100), 
                'cold_brightness_multiplier': (0, 0.1), 
                'cold_power': (0.7, 1.3), 
                'hot_brightness_multiplier': (0.3, 0.5), 
                'hot_power': (-0.3, 0.3), 
                "sky_heat" : (0, 0.1),
                "ground_heat_correction" : (0, 1),
                "tree_correction_strength" : (0, 1)}

        optimizer = BayesianOptimization(
            f=black_box_function_single_fire,
            pbounds=pbounds,
            random_state=1,
        )

    optimizer.maximize(
        init_points=2,
        n_iter = 500,
    )

    rows = {}
    
    for i, res in enumerate(optimizer.res):
        print("Iteration {}: \n\t{}".format(i, res))
        params_dict = {}
        params_dict['target'] = res['target']
        for key in res['params'].keys():
            params_dict[key] = res['params'][key]
        rows[i] = params_dict
        
    df = pd.DataFrame.from_dict(rows, orient='index')
    df.to_csv(r"c:\Users\John\Downloads\temp_params\results.csv")


if __name__ == "__main__":
    main()