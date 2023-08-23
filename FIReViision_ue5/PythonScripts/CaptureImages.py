import unreal
import time
from airsim import *
import airsim
import numpy as np
import os
import ParametersClass as pc
import pandas as pd
import ImageComparisonProcessor as icp


SAMPLING_RATE = 20

#Should possibly change to a path that we decide?
# dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "\SceneImages")

def set_params(params, test_mode, thermal_mat_inst):
    if (test_mode == 1):
        blend_weight = params[0]
        brightness = params[1]
        contrast = params[2]
        cold_brightness_multiplier = params[3]
        cold_power = params[4]
        hot_brightness_multiplier = params[5]
        hot_power = params[6]
        sky_heat = params[7]
        fire_heat = params[8]
        ground_heat_correction_strength = params[9]
        ground_heat_offset = params[10]
        person_heat_multiplier = params[11]
        target_ground_heat = params[12]
        tree_correction_strength = params[13]
        target_tree_heat = params[14]
        vehicle_heat_multiplier = params[15]
        #Set the parameters
        thermal_mat_inst.set_parameter_value("blend_weight", blend_weight)
        thermal_mat_inst.set_parameter_value("Brightness", brightness)
        thermal_mat_inst.set_parameter_value("Contrast", contrast)
        thermal_mat_inst.set_parameter_value("cold_brightness_multiplier", cold_brightness_multiplier)
        thermal_mat_inst.set_parameter_value("cold_power", cold_power)
        thermal_mat_inst.set_parameter_value("hot_brightness_multiplier", hot_brightness_multiplier)
        thermal_mat_inst.set_parameter_value("hot_power", hot_power)
        thermal_mat_inst.set_parameter_value("sky_heat", sky_heat)
        thermal_mat_inst.set_parameter_value("Fire_Heat", fire_heat)
        thermal_mat_inst.set_parameter_value("ground_heat_correction_strength", ground_heat_correction_strength)
        thermal_mat_inst.set_parameter_value("ground_heat_offset", ground_heat_offset)
        thermal_mat_inst.set_parameter_value("person_heat_multiplier", person_heat_multiplier)
        thermal_mat_inst.set_parameter_value("target_ground_heat", target_ground_heat)
        thermal_mat_inst.set_parameter_value("tree_correction_strength", tree_correction_strength)
        thermal_mat_inst.set_parameter_value("target_tree_heat", target_tree_heat)
        thermal_mat_inst.set_parameter_value("vehicle_heat_multiplier", vehicle_heat_multiplier)
    elif (test_mode == 2):
            blend_weight = params[0]
            brightness = params[1]
            contrast = params[2]
            cold_brightness_multiplier = params[3]
            cold_power = params[4]
            hot_brightness_multiplier = params[5]
            light_bulb_heat_multiplier = params[6]
            #Set the parameters
            thermal_mat_inst.set_parameter_value("blend_weight", blend_weight)
            thermal_mat_inst.set_parameter_value("Brightness", brightness)
            thermal_mat_inst.set_parameter_value("Contrast", contrast)
            thermal_mat_inst.set_parameter_value("cold_brightness_multiplier", cold_brightness_multiplier)
            thermal_mat_inst.set_parameter_value("cold_power", cold_power)
            thermal_mat_inst.set_parameter_value("hot_brightness_multiplier", hot_brightness_multiplier)
            #Unsure about the light bulb multiplier
            
    return 
    
def capture_image(camera_name, client, best_accuracies, reference_image, df, image_index, params, test_mode, dir):
    time.sleep(0.1)
    responses = client.simGetImages([ImageRequest(camera_name, 10, False, False)])
    print('Retrieved image: %d' % len(responses))
    print ("Saving images to %s" % dir)
    #Do the file naming with the -'s based on TEST_MODE
    filename = pc.test_name(test_mode) + "-" + str(image_index)
    file_path = dir + "\\" + filename 
    response = responses[0]
    
    # get numpy array
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    # reshape array to 4 channel image array H X W X 4
    img_rgb = img1d.reshape(response.height, response.width, 3)
    # original image is fliped vertically
    img_rgb = np.flipud(img_rgb)


    min_acc = np.min(best_accuracies.keys)
    current_acc = icp.check_accuracy(img_rgb, reference_image)
    if (current_acc > min_acc):
        del best_accuracies[min_acc]
        best_accuracies[current_acc] = [image_index, img_rgb]


    # write to png    
    if (image_index%SAMPLING_RATE == 0):
        airsim.write_png(os.path.normpath(file_path + '.png'), img_rgb)     
    
    
    #Save row to dataframe
    row = pc.create_row(test_mode, image_index, current_acc, params, filename)
    df = pd.concat([df, row])
    
    return