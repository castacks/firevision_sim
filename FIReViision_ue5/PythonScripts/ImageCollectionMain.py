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

BATCH_SIZE = 600

#Grabs Camera Actor
actors = unreal.EditorLevelLibrary.get_all_level_actors()
camera_actor = None
for actor in actors:
    if (actor.get_name() == 'CineCameraActor_1'):
        camera_actor = actor
        break

unreal.EditorLevelLibrary.pilot_level_actor(camera_actor)

# Grab our PP Thermal Material 
thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/FIReVision_Assets/FIReVision_FX/PP_Thermal_FX_Inst")

# # Initializes data management dataframe
df = pd.DataFrame(columns=pc.get_cols_from_test(TEST_MODE))#.reset_index(drop=True)

#Create images folder within our results folder
images_dir = os.path.join(RESULTS_FILE_PATH, "images")
if(not os.path.exists(images_dir)):
    os.mkdir(images_dir)

parameter_combinations = None

# if(TEST_MODE==1):
#     #START OF TEST MODE 1------------------------------------------------------------------------------------------------------------------
#     if(SEARCH_MODE=="LOW_FIDELITY"):
#         #Set the parameters
#         blend_weight_min=30
#         blend_weight_max=100
#         blend_weight_step=2
        
#         brightness_min=40
#         brightness_max=100
#         brightness_step=2
        
#         contrast_min=0
#         contrast_max=100
#         contrast_step=5
        
#         cold_brightness_multiplier_min=0
#         cold_brightness_multiplier_max=200
#         cold_brightness_multiplier_step=10
        
#         cold_power_min=-2
#         cold_power_max=2
#         cold_power_step=0.2
        
#         hot_brightness_multiplier_min=0
#         hot_brightness_multiplier_max=200
#         hot_brightness_multiplier_step=10
        
#         hot_power_min=-2
#         hot_power_max=2
#         hot_power_step=0.2
        
#         sky_heat_min=0 
#         sky_heat_max=0.2
#         sky_heat_step=0.05
                
#         fire_heat_min=0
#         fire_heat_max=1
#         fire_heat_step=0.05
        
#         ground_heat_correction_strength_min=0 
#         ground_heat_correction_strength_max=10000 
#         ground_heat_correction_strength_step=1000
        
#         ground_heat_offset_min=0
#         ground_heat_offset_max=1
#         ground_heat_offset_step=0.1
        
#         person_heat_multiplier_min=0 
#         person_heat_multiplier_max=25 
#         person_heat_multiplier_step=1
        
#         target_ground_heat_min=0
#         target_ground_heat_max=1
#         target_ground_heat_step=0.1
        
#         tree_correction_strength_min=0
#         tree_correction_strength_max=10000 
#         tree_correction_strength_step=1000
        
        
#         target_tree_heat_min=0
#         target_tree_heat_max=1
#         target_tree_heat_step=0.1
        
#         vehicle_heat_multiplier_min=0 
#         vehicle_heat_multiplier_max=25 
#         vehicle_heat_multiplier_step=1
        
#     elif(SEARCH_MODE=="HIGH_FIDELITY"):
#         #Set the parameters
#         blend_weight_min=30
#         blend_weight_max=100
#         blend_weight_step=0.5
        
#         brightness_min=40
#         brightness_max=100
#         brightness_step=1
        
#         contrast_min=0
#         contrast_max=100
#         contrast_step=1
        
#         cold_brightness_multiplier_min=0
#         cold_brightness_multiplier_max=200
#         cold_brightness_multiplier_step=1
        
#         cold_power_min=-2
#         cold_power_max=2
#         cold_power_step=0.1         
        
#         hot_brightness_multiplier_min=0
#         hot_brightness_multiplier_max=10
#         hot_brightness_multiplier_step=0.2
        
#         hot_power_min=-2
#         hot_power_max=2
#         hot_power_step=0.1
        
#         sky_heat_min=0 
#         sky_heat_max=0.2
#         sky_heat_step=0.01
                
#         fire_heat_min=0.8 
#         fire_heat_max=1
#         fire_heat_step=0.05
        
#         ground_heat_correction_strength_min=0 
#         ground_heat_correction_strength_max=10000 
#         ground_heat_correction_strength_step=10
        
#         ground_heat_offset_min=0 
#         ground_heat_offset_max=1 
#         ground_heat_offset_step=0.02
        
#         person_heat_multiplier_min=0 
#         person_heat_multiplier_max=25 
#         person_heat_multiplier_step=0.5
        
#         target_ground_heat_min=0 
#         target_ground_heat_max=1 
#         target_ground_heat_step=0.01
        
#         tree_correction_strength_min=0
#         tree_correction_strength_max=10000 
#         tree_correction_strength_step=10
        
        
#         target_tree_heat_min=0 
#         target_tree_heat_max=1 
#         target_tree_heat_step=0.01
        
#         vehicle_heat_multiplier_min=0 
#         vehicle_heat_multiplier_max=25 
#         vehicle_heat_multiplier_step=0.5
#     parameter_combinations = pc.Parameters(
#         test_mode=TEST_MODE,


#         blend_weight_min=blend_weight_min, 
#         blend_weight_max=blend_weight_max, 
#         blend_weight_step=blend_weight_step,
        
#         brightness_min=brightness_min, 
#         brightness_max=brightness_max, 
#         brightness_step=brightness_step,
        
#         contrast_min=contrast_min, 
#         contrast_max=contrast_max, 
#         contrast_step=contrast_step,
        
#         cold_brightness_multiplier_min=cold_brightness_multiplier_min, 
#         cold_brightness_multiplier_max=cold_brightness_multiplier_max, 
#         cold_brightness_multiplier_step=cold_brightness_multiplier_step,
        
#         cold_power_min=cold_power_min, 
#         cold_power_max=cold_power_max, 
#         cold_power_step=cold_power_step,
        
#         hot_brightness_multiplier_min=hot_brightness_multiplier_min, 
#         hot_brightness_multiplier_max=hot_brightness_multiplier_max, 
#         hot_brightness_multiplier_step=hot_brightness_multiplier_step,
        
#         hot_power_min=hot_power_min, 
#         hot_power_max=hot_power_max, 
#         hot_power_step=hot_power_step,
        
#         sky_heat_min=sky_heat_min, 
#         sky_heat_max=sky_heat_max, 
#         sky_heat_step=sky_heat_step,
        
#         fire_heat_min=fire_heat_min, 
#         fire_heat_max=fire_heat_max, 
#         fire_heat_step=fire_heat_step,
        
#         ground_heat_correction_strength_min=ground_heat_correction_strength_min, 
#         ground_heat_correction_strength_max=ground_heat_correction_strength_max, 
#         ground_heat_correction_strength_step=ground_heat_correction_strength_step,
        
#         ground_heat_offset_min=ground_heat_offset_min, 
#         ground_heat_offset_max=ground_heat_offset_max, 
#         ground_heat_offset_step=ground_heat_offset_step,
        
#         person_heat_multiplier_min=person_heat_multiplier_min, 
#         person_heat_multiplier_max=person_heat_multiplier_max, 
#         person_heat_multiplier_step=person_heat_multiplier_step,
        
#         target_ground_heat_min=target_ground_heat_min, 
#         target_ground_heat_max=target_ground_heat_max, 
#         target_ground_heat_step=target_ground_heat_step,
        
#         tree_correction_strength_min=tree_correction_strength_min, 
#         tree_correction_strength_max=tree_correction_strength_max, 
#         tree_correction_strength_step=tree_correction_strength_step,
        
#         target_tree_heat_min=target_tree_heat_min, 
#         target_tree_heat_max=target_tree_heat_max, 
#         target_tree_heat_step=target_tree_heat_step,
        
#         vehicle_heat_multiplier_min=vehicle_heat_multiplier_min, 
#         vehicle_heat_multiplier_max=vehicle_heat_multiplier_max, 
#         vehicle_heat_multiplier_step=vehicle_heat_multiplier_step
#         ).all_parameter_combinations()
# elif(TEST_MODE==2):
#     #START OF TEST MODE 2------------------------------------------------------------------------------------------------------------------
#     if(SEARCH_MODE=="LOW_FIDELITY"):
#         #Set the parameters
#         blend_weight_min=0
#         blend_weight_max=100
#         blend_weight_step=2
        
#         brightness_min=0
#         brightness_max=100
#         brightness_step=2
        
#         contrast_min=0
#         contrast_max=100
#         contrast_step=5
        
#         cold_brightness_multiplier_min=0
#         cold_brightness_multiplier_max=200
#         cold_brightness_multiplier_step=10
        
#         cold_power_min=-2
#         cold_power_max=2
#         cold_power_step=0.2
        
#         hot_brightness_multiplier_min=0
#         hot_brightness_multiplier_max=200
#         hot_brightness_multiplier_step=10
        
#         hot_power_min=-2
#         hot_power_max=2
#         hot_power_step=0.2
        
#         light_bulb_heat_multiplier_min=0 
#         light_bulb_heat_multiplier_max=1 
#         light_bulb_heat_multiplier_step=0.1
#     elif(SEARCH_MODE=="HIGH_FIDELITY"):
#         #Set the parameters
#         blend_weight_min=30
#         blend_weight_max=100
#         blend_weight_step=0.5
        
#         brightness_min=40
#         brightness_max=100
#         brightness_step=1
        
#         contrast_min=0
#         contrast_max=100
#         contrast_step=1
        
#         cold_brightness_multiplier_min=0
#         cold_brightness_multiplier_max=200
#         cold_brightness_multiplier_step=1
        
#         cold_power_min=-2
#         cold_power_max=2
#         cold_power_step=0.1         
        
#         hot_brightness_multiplier_min=0
#         hot_brightness_multiplier_max=10
#         hot_brightness_multiplier_step=0.2
        
#         hot_power_min=-2
#         hot_power_max=2
#         hot_power_step=0.1
        
#         light_bulb_heat_multiplier_min=0 
#         light_bulb_heat_multiplier_max=1 
#         light_bulb_heat_multiplier_step=0.01
        
#     parameter_combinations = pc.Parameters(
#         test_mode=TEST_MODE,
        
#         blend_weight_min=blend_weight_min, 
#         blend_weight_max=blend_weight_max, 
#         blend_weight_step=blend_weight_step,
        
#         brightness_min=brightness_min, 
#         brightness_max=brightness_max, 
#         brightness_step=brightness_step,
        
#         contrast_min=contrast_min, 
#         contrast_max=contrast_max, 
#         contrast_step=contrast_step,
        
#         cold_brightness_multiplier_min=cold_brightness_multiplier_min, 
#         cold_brightness_multiplier_max=cold_brightness_multiplier_max, 
#         cold_brightness_multiplier_step=cold_brightness_multiplier_step,
        
#         cold_power_min=cold_power_min, 
#         cold_power_max=cold_power_max, 
#         cold_power_step=cold_power_step,
        
#         hot_brightness_multiplier_min=hot_brightness_multiplier_min, 
#         hot_brightness_multiplier_max=hot_brightness_multiplier_max, 
#         hot_brightness_multiplier_step=hot_brightness_multiplier_step,
        
#         hot_power_min=hot_power_min, 
#         hot_power_max=hot_power_max, 
#         hot_power_step=hot_power_step,
        
#         light_bulb_heat_multiplier_min=light_bulb_heat_multiplier_min, 
#         light_bulb_heat_multiplier_max=light_bulb_heat_multiplier_max, 
#         light_bulb_heat_multiplier_step=light_bulb_heat_multiplier_step
#         ).all_parameter_combinations()

class capture(object):
    def __init__(self, batch_num):
        unreal.EditorLevelLibrary.editor_set_game_view(True)
        self.parameter_combinations = parameter_combinations
        self.count = 0
        self.batch_num = batch_num
        self.on_pre_tick = unreal.register_slate_pre_tick_callback(self.__pretick__)
        
    def finish_collection(self):
        
        pd.display(df)

        for file in df.filename:
            if(os.path.exists(SCREENSHOTS_DIR + "\\" + file)):
                os.rename(SCREENSHOTS_DIR + "\\" + file, RESULTS_FILE_PATH + "\\images\\" + file)

        # #Saves file information to excel file
        df.to_excel(RESULTS_FILE_PATH + "\\" + pc.test_name(TEST_MODE) + "_batch" + str(self.batch_num) + "raw_data.xlsx")
    
    def get_next_params(self):
        params = self.parameter_combinations[self.count]
        if(self.count >= len(self.parameter_combinations)):
            self.finish_collection()
            exit()
            
        self.count += 1
        return params
    
    def __pretick__(self, deltatime):
        try:
            self.count += 1
            print(self.count)
            # params = self.get_next_params()
            filename = pc.test_name(TEST_MODE) + "-" + str(self.count) + ".png"
            # row = pc.create_row(TEST_MODE, self.count, params, filename)
            # print(row)
            # blend_weight = row["blend"].item()
            # brightness = row["brightness"].item()
            # contrast = row["contrast"].item()
            # cold_brightness_multiplier = row["cold_brightness_multiplier"].item()
            # cold_power = row["cold_power"].item()
            # hot_brightness_multiplier = row["hot_brightness_multiplier"].item()
            # hot_power = row["hot_power"].item()
            # light_bulb_heat_multiplier = row["light_bulb_heat_multiplier"].item()
            # blend_weight = 0
            # brightness = 0
            # contrast = 0
            # cold_brightness_multiplier = 0
            # cold_power = 0
            # hot_brightness_multiplier = 0
            # hot_power = 0
            # light_bulb_heat_multiplier = 0

            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"blend_weight", blend_weight)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Brightness", brightness)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Contrast", contrast)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_brightness_multiplier", cold_brightness_multiplier)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_power", cold_power)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_brightness_multiplier", hot_brightness_multiplier)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_power", hot_power)
            # unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"light_bulb_heat_multiplier", light_bulb_heat_multiplier)
                        
            
            # df.loc[len(df.index)] = row 
            unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, filename, camera = camera_actor)
            unreal.register_slate_pre_tick_callback(self.on_pre_tick)

            print("attempted to take screenshot")
            
            if(self.count == 5): #TODO Delete later: For testing purposes
                print(error)
                print(df.to_string())
                unreal.register_slate_pre_tick_callback(self.on_pre_tick)
            
            
        except Exception as error:
            print(error)
            print(df.to_string())
            unreal.register_slate_pre_tick_callback(self.on_pre_tick)

unreal.EditorLevelLibrary.pilot_level_actor(camera_actor)
print("capured?")
instance = capture(0)
print("Yes!")

