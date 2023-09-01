import unreal 
import numpy as np
import ParametersClass as pc
import CaptureImages as ci
import pandas as pd
import os
import airsim
import time
from multiprocessing import Process


TEST_MODE = 2
# SEARCH_MODE = "HIGH_FIDELITY"
SEARCH_MODE = "LOW_FIDELITY"
    
RESULTS_FILE_PATH = r"c:\Users\John\Downloads\test_images"
CAMERA_NAME = "bottom_forward_thermal"
SCREENSHOTS_DIR = r"c:\Users\John\Wildfire_Development\FIReVision2_0_0\Saved\Screenshots\WindowsEditor"

#Grabs Camera Actor
actors = unreal.EditorLevelLibrary.get_all_level_actors()
camera_actor = None
for actor in actors:
    if (actor.get_name() == 'CineCameraActor_1'):
        camera_actor = actor
        break
    print(actor)

# print(camera_actor)
unreal.EditorLevelLibrary.pilot_level_actor(camera_actor)

# Grab our PP Thermal Material 
thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/FIReVision_Assets/FIReVision_FX/PP_Thermal_FX_Inst")

# # Initializes data management dataframe
df = pd.DataFrame(columns=pc.get_cols_from_test(TEST_MODE))#.reset_index(drop=True)

#Create images folder within our results folder
images_dir = os.path.join(RESULTS_FILE_PATH, "images")
if(not os.path.exists(images_dir)):
    os.mkdir(images_dir)

i = 0
if(TEST_MODE==1):
    #START OF TEST MODE 1------------------------------------------------------------------------------------------------------------------
    if(SEARCH_MODE=="LOW_FIDELITY"):
        #Set the parameters
        blend_weight_min=30
        blend_weight_max=100
        blend_weight_step=2
        
        brightness_min=40
        brightness_max=100
        brightness_step=2
        
        contrast_min=0
        contrast_max=100
        contrast_step=5
        
        cold_brightness_multiplier_min=0
        cold_brightness_multiplier_max=200
        cold_brightness_multiplier_step=10
        
        cold_power_min=-2
        cold_power_max=2
        cold_power_step=0.2
        
        hot_brightness_multiplier_min=0
        hot_brightness_multiplier_max=200
        hot_brightness_multiplier_step=10
        
        hot_power_min=-2
        hot_power_max=2
        hot_power_step=0.2
        
        sky_heat_min=0 
        sky_heat_max=0.2
        sky_heat_step=0.05
                
        fire_heat_min=0
        fire_heat_max=1
        fire_heat_step=0.05
        
        ground_heat_correction_strength_min=0 
        ground_heat_correction_strength_max=10000 
        ground_heat_correction_strength_step=1000
        
        ground_heat_offset_min=0
        ground_heat_offset_max=1
        ground_heat_offset_step=0.1
        
        person_heat_multiplier_min=0 
        person_heat_multiplier_max=25 
        person_heat_multiplier_step=1
        
        target_ground_heat_min=0
        target_ground_heat_max=1
        target_ground_heat_step=0.1
        
        tree_correction_strength_min=0
        tree_correction_strength_max=10000 
        tree_correction_strength_step=1000
        
        
        target_tree_heat_min=0
        target_tree_heat_max=1
        target_tree_heat_step=0.1
        
        vehicle_heat_multiplier_min=0 
        vehicle_heat_multiplier_max=25 
        vehicle_heat_multiplier_step=1
        
    elif(SEARCH_MODE=="HIGH_FIDELITY"):
        #Set the parameters
        blend_weight_min=30
        blend_weight_max=100
        blend_weight_step=0.5
        
        brightness_min=40
        brightness_max=100
        brightness_step=1
        
        contrast_min=0
        contrast_max=100
        contrast_step=1
        
        cold_brightness_multiplier_min=0
        cold_brightness_multiplier_max=200
        cold_brightness_multiplier_step=1
        
        cold_power_min=-2
        cold_power_max=2
        cold_power_step=0.1         
        
        hot_brightness_multiplier_min=0
        hot_brightness_multiplier_max=10
        hot_brightness_multiplier_step=0.2
        
        hot_power_min=-2
        hot_power_max=2
        hot_power_step=0.1
        
        sky_heat_min=0 
        sky_heat_max=0.2
        sky_heat_step=0.01
                
        fire_heat_min=0.8 
        fire_heat_max=1
        fire_heat_step=0.05
        
        ground_heat_correction_strength_min=0 
        ground_heat_correction_strength_max=10000 
        ground_heat_correction_strength_step=10
        
        ground_heat_offset_min=0 
        ground_heat_offset_max=1 
        ground_heat_offset_step=0.02
        
        person_heat_multiplier_min=0 
        person_heat_multiplier_max=25 
        person_heat_multiplier_step=0.5
        
        target_ground_heat_min=0 
        target_ground_heat_max=1 
        target_ground_heat_step=0.01
        
        tree_correction_strength_min=0
        tree_correction_strength_max=10000 
        tree_correction_strength_step=10
        
        
        target_tree_heat_min=0 
        target_tree_heat_max=1 
        target_tree_heat_step=0.01
        
        vehicle_heat_multiplier_min=0 
        vehicle_heat_multiplier_max=25 
        vehicle_heat_multiplier_step=0.5

    #Set the ranges
    blend_range = np.arange(blend_weight_min, blend_weight_max, blend_weight_step)
    brightness_range = np.arange(brightness_min, brightness_max, brightness_step)
    contrast_range = np.arange(contrast_min, contrast_max, contrast_step)
    cold_brightness_multiplier_range = np.arange(cold_brightness_multiplier_min, cold_brightness_multiplier_max, cold_brightness_multiplier_step)
    cold_power_range = np.arange(cold_power_min, cold_power_max, cold_power_step)
    hot_brightness_multiplier_range = np.arange(hot_brightness_multiplier_min, hot_brightness_multiplier_max, hot_brightness_multiplier_step)
    hot_power_range = np.arange(hot_power_min, hot_power_max, hot_power_step)
    sky_heat_range = np.arange(sky_heat_min, sky_heat_max, sky_heat_step)
    fire_heat_range = np.arange(fire_heat_min, fire_heat_max, fire_heat_step)
    ground_heat_correction_strength_range = np.arange(ground_heat_correction_strength_min, ground_heat_correction_strength_max, ground_heat_correction_strength_step)
    ground_heat_offset = np.arange(ground_heat_offset_min, ground_heat_offset_max, ground_heat_offset_step)
    person_heat_multiplier_range = np.arange(person_heat_multiplier_min, person_heat_multiplier_max, person_heat_multiplier_step)
    target_ground_heat_range = np.arange(target_ground_heat_min, target_ground_heat_max, target_ground_heat_step)
    tree_correction_strength_range = np.arange(tree_correction_strength_min, tree_correction_strength_max, tree_correction_strength_step)
    target_tree_heat_range = np.arange(target_tree_heat_min, target_tree_heat_max, target_tree_heat_step)
    vehicle_heat_multiplier_range = np.arange(vehicle_heat_multiplier_min, vehicle_heat_multiplier_max, vehicle_heat_multiplier_step)
    for blend_weight in blend_range:
        for brightness in brightness_range:
            for contrast in contrast_range: # contrast 3
                for cold_brightness_multiplier in cold_brightness_multiplier_range: # cold brightness multiplier 4
                    for cold_power in cold_power_range: # cold power 5
                        for hot_brightness_multiplier in hot_brightness_multiplier_range:
                            for hot_power in hot_power_range:
                                for sky_heat in sky_heat_range:
                                    for fire_heat in fire_heat_range:
                                        for ground_heat_correction_strength in ground_heat_correction_strength_range:
                                            for ground_heat_offset in ground_heat_offset:
                                                for person_heat_multiplier in person_heat_multiplier_range:
                                                    for target_ground_heat in target_ground_heat_range:
                                                        for tree_correction_strength in tree_correction_strength_range:
                                                            for target_tree_heat in target_tree_heat_range:
                                                                for vehicle_heat_multiplier in vehicle_heat_multiplier_range:
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"blend_weight", blend_weight.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Brightness", brightness.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Contrast", contrast.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_brightness_multiplier", cold_brightness_multiplier.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_power", cold_power.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_brightness_multiplier", hot_brightness_multiplier.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_power", hot_power.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"sky_heat", sky_heat.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Fire_Heat", fire_heat.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"ground_heat_correction_strength", ground_heat_correction_strength.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"ground_heat_offset", ground_heat_offset.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"person_heat_multiplier", person_heat_multiplier.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"target_ground_heat", target_ground_heat.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"tree_correction_strength", tree_correction_strength.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"target_tree_heat", target_tree_heat.item())
                                                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"vehicle_heat_multiplier", vehicle_heat_multiplier.item())        
                                                                    time.sleep(0.1)
                                                                    params = [blend_weight, brightness, contrast, cold_brightness_multiplier, cold_power, hot_brightness_multiplier, hot_power, sky_heat, fire_heat, ground_heat_correction_strength, ground_heat_offset, person_heat_multiplier, target_ground_heat, tree_correction_strength, target_tree_heat, vehicle_heat_multiplier]
                                                                    
                                                                    #Save row to dataframe
                                                                    row = pc.create_row(TEST_MODE, i, params, filename)
                                                                    df.loc[len(df.index)] = row 
                                                                                                    
                                                                    #Take Screen Shot
                                                                    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, filename, camera = camera_actor) 
                                                                    i += 1
elif(TEST_MODE==2):
    #START OF TEST MODE 2------------------------------------------------------------------------------------------------------------------
    if(SEARCH_MODE=="LOW_FIDELITY"):
        #Set the parameters
        blend_weight_min=0
        blend_weight_max=100
        blend_weight_step=2
        
        brightness_min=0
        brightness_max=100
        brightness_step=2
        
        contrast_min=0
        contrast_max=100
        contrast_step=5
        
        cold_brightness_multiplier_min=0
        cold_brightness_multiplier_max=200
        cold_brightness_multiplier_step=10
        
        cold_power_min=-2
        cold_power_max=2
        cold_power_step=0.2
        
        hot_brightness_multiplier_min=0
        hot_brightness_multiplier_max=200
        hot_brightness_multiplier_step=10
        
        hot_power_min=-2
        hot_power_max=2
        hot_power_step=0.2
        
        light_bulb_heat_multiplier_min=0 
        light_bulb_heat_multiplier_max=1 
        light_bulb_heat_multiplier_step=0.1
    elif(SEARCH_MODE=="HIGH_FIDELITY"):
        #Set the parameters
        blend_weight_min=30
        blend_weight_max=100
        blend_weight_step=0.5
        
        brightness_min=40
        brightness_max=100
        brightness_step=1
        
        contrast_min=0
        contrast_max=100
        contrast_step=1
        
        cold_brightness_multiplier_min=0
        cold_brightness_multiplier_max=200
        cold_brightness_multiplier_step=1
        
        cold_power_min=-2
        cold_power_max=2
        cold_power_step=0.1         
        
        hot_brightness_multiplier_min=0
        hot_brightness_multiplier_max=10
        hot_brightness_multiplier_step=0.2
        
        hot_power_min=-2
        hot_power_max=2
        hot_power_step=0.1
        
        light_bulb_heat_multiplier_min=0 
        light_bulb_heat_multiplier_max=1 
        light_bulb_heat_multiplier_step=0.01

    blend_range = np.arange(blend_weight_min, blend_weight_max, blend_weight_step)
    brightness_range = np.arange(brightness_min, brightness_max, brightness_step)
    contrast_range = np.arange(contrast_min, contrast_max, contrast_step)
    cold_brightness_multiplier_range = np.arange(cold_brightness_multiplier_min, cold_brightness_multiplier_max, cold_brightness_multiplier_step)
    cold_power_range = np.arange(cold_power_min, cold_power_max, cold_power_step)
    hot_brightness_multiplier_range = np.arange(hot_brightness_multiplier_min, hot_brightness_multiplier_max, hot_brightness_multiplier_step)
    hot_power_range = np.arange(hot_power_min, hot_power_max, hot_power_step)
    light_bulb_heat_multiplier_range = np.arange(light_bulb_heat_multiplier_min, light_bulb_heat_multiplier_max, light_bulb_heat_multiplier_step)

    for blend_weight in blend_range:
        for brightness in brightness_range:
            for contrast in contrast_range: # contrast 3
                for cold_brightness_multiplier in cold_brightness_multiplier_range: # cold brightness multiplier 4
                    for cold_power in cold_power_range: # cold power 5
                        for hot_brightness_multiplier in hot_brightness_multiplier_range:
                            for hot_power in hot_power_range:
                                for light_bulb_heat_multiplier in light_bulb_heat_multiplier_range:
                                    #Strings together filename
                                    filename = pc.test_name(TEST_MODE) + "-" + str(i) + ".png"
                                    
                                    #Sets the parameters in unreal engine environment
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"blend_weight", blend_weight.item())
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Brightness", brightness.item())
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Contrast", contrast.item())
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_brightness_multiplier", cold_brightness_multiplier.item())
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_power", cold_power.item())
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_brightness_multiplier", hot_brightness_multiplier.item())
                                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_power", hot_power.item())
                                    
                                    #Wait for changes to occur
                                    time.sleep(0.1)
                                    
                                    #Save row to dataframe
                                    params = [blend_weight, brightness, contrast, cold_brightness_multiplier, cold_power, hot_brightness_multiplier, hot_power, light_bulb_heat_multiplier]
                                    row = pc.create_row(TEST_MODE, i, params, filename)
                                    df.loc[len(df.index)] = row 

                                    # print(df.to_string())
                                    
                                    #Take Screen Shot
                                    i += 1
                                    print("Line 365")
                                    unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, filename, camera = camera_actor)
                                    print("Line 366")
                                    # import code; code.interact(local=dict(globals(), **locals()))
                                    
                                    # print(i)
                                    #Just take 2 for testing
                                    if(i > 2):
                                        # print(df.columns)
                                        exit()

# pd.display(df)

# for file in df.filename:
#     if(os.path.exists(SCREENSHOTS_DIR + "\\" + file)):
#         os.rename(SCREENSHOTS_DIR + "\\" + file, RESULTS_FILE_PATH + "\\images\\" + file)


# # #Saves file information to excel file
# df.to_excel(RESULTS_FILE_PATH + "\\" + pc.test_name(TEST_MODE) + "raw_data.xlsx")