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

IMAGE_DIR = r"C:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor\current.png"
REF_IMAGE_DIR = r"c:\Users\John\Downloads\Reference_Image\single_fire_reference.png"
TMP_PARAMS_DIR = r"c:\Users\John\Downloads\temp_params\params.csv"
# TAKE_IMAGE_SCRIPT = r"C:\Users\John\Wildfire_Development\firevision_sim\FIReViision_ue5\PythonScripts\TakeSingleImage.py"

def black_box_function(blend_weight, brightness, contrast, cold_brightness_multiplier, cold_power, hot_brightness_multiplier, hot_power, light_bulb_heat_multiplier, lamp_heat_multiplier):
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
        
    
    #Generate Image
    pygui.click(x=433, y=1138)
    pygui.write("TakeSingleImage.py")
    pygui.press('enter')
    
    #Wait for image to be generated
    while(not os.path.exists(IMAGE_DIR)):
        time.sleep(0.1)
        
    #Compare Image
    image = icp.image_from_file(IMAGE_DIR)
    reference_image = icp.image_from_file(REF_IMAGE_DIR)
    accuracy = icp.check_accuracy(image, reference_image) #gets accuracy
    
    #Cleanup
    os.remove(TMP_PARAMS_DIR)
    os.remove(IMAGE_DIR)
    
    print(accuracy)
    return accuracy    

def main():
    print("running")
    # Bounded region of parameter space
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
        f=black_box_function,
        pbounds=pbounds,
        random_state=1,
    )

    optimizer.maximize(
        init_points=2,
        n_iter=1000,
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