import unreal 
import ParametersClass as pc
import CaptureImages as ci
import pandas as pd
import os
import airsim
import time
import pyautogui as pygui
import ImageComparisonProcessor as icp


# actors = (actor for actor in unreal.EditorLevelLibrary.get_selected_level_actors())


TEST_MODE = 1
RESULTS_FILE_PATH = r"c:\Users\John\Downloads\test_images"
CAMERA_NAME = "bottom_forward_thermal"
REFERNCE_IMAGE_PATH = ""

#Grabs Camera Actor
actors = unreal.EditorLevelLibrary.get_all_level_actors()
camera_actor = None
for actor in actors:
    if (actor.get_name() == 'CineCameraActor_1'):
        camera_actor = actor
        break
    print(actor)

print(camera_actor)
unreal.EditorLevelLibrary.pilot_level_actor(camera_actor)

# options = unreal.AutomationScreenshotOptions(unreal.Vector2D(x=1920, y=1080), frame_delay = 2)
# print(options)

# latent_info = unreal.LatentActionInfo()
# print(latent_info)
# unreal.AutomationLibrary.take_automation_screenshot_at_camera(
#         camera_actor,
#         latent_info,
        
#         )

# Grab our PP Thermal Material 
thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/FIReVision_Assets/FIReVision_FX/PP_Thermal_FX_Inst")

# unreal.AutomationLibrary.take_high_res_screenshot(
#         1920,
#         1080,
#         "test.png",
#         camera = camera_actor
#         )


# Starts play mode
# unreal.EditorLevelLibrary().editor_play_simulate()
# pygui.hotkey('alt', 'p')


# print(type(thermal_mat_inst))
# print(thermal_mat_inst)


# # Get all parameter combinations
params_obj = pc.Parameters(test_mode=TEST_MODE)
parameter_combinations = params_obj.all_parameter_combinations()

# # Initializes data management dataframe
df = pd.DataFrame(columns=pc.get_cols_from_test(TEST_MODE)).reset_index(drop=True)

#Create images folder within our results folder
images_dir = os.path.join(RESULTS_FILE_PATH, "images")
if(not os.path.exists(images_dir)):
    os.mkdir(images_dir)

# best_accs = {0 : [0,0]}
# ref_image = icp.image_from_file(REFERNCE_IMAGE_PATH)
i = 0
for params in parameter_combinations:
    print(params)

# test_mode = TEST_MODE
# for params in parameter_combinations:
#     filename = pc.test_name(TEST_MODE) + "-" + str(i) + ".png"
#     # file_path = images_dir + "\\" + filename
#     # Set parameters then capture image
    
    
#     if (test_mode == 1):
#         blend_weight = params[0].item()
#         brightness = params[1].item()
#         contrast = params[2].item()
#         cold_brightness_multiplier = params[3].item()
#         cold_power = params[4].item()
#         hot_brightness_multiplier = params[5].item()
#         hot_power = params[6].item()
#         sky_heat = params[7].item()
#         fire_heat = params[8].item()
#         ground_heat_correction_strength = params[9].item()
#         ground_heat_offset = params[10].item()
#         person_heat_multiplier = params[11].item()
#         target_ground_heat = params[12].item()
#         tree_correction_strength = params[13].item()
#         target_tree_heat = params[14].item()
#         vehicle_heat_multiplier = params[15].item()
#         #Set the parameters
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"blend_weight", blend_weight)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Brightness", brightness)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Contrast", contrast)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_brightness_multiplier", cold_brightness_multiplier)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_power", cold_power)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_brightness_multiplier", hot_brightness_multiplier)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_power", hot_power)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"sky_heat", sky_heat)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Fire_Heat", fire_heat)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"ground_heat_correction_strength", ground_heat_correction_strength)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"ground_heat_offset", ground_heat_offset)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"person_heat_multiplier", person_heat_multiplier)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"target_ground_heat", target_ground_heat)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"tree_correction_strength", tree_correction_strength)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"target_tree_heat", target_tree_heat)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"vehicle_heat_multiplier", vehicle_heat_multiplier)
#     elif (test_mode == 2):
#         blend_weight = params[0].item()
#         brightness = params[1].item()
#         contrast = params[2].item()
#         cold_brightness_multiplier = params[3].item()
#         cold_power = params[4].item()
#         hot_brightness_multiplier = params[5].item()
#         light_bulb_heat_multiplier = params[6].item()
#         # Set the parameters
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"blend_weight", blend_weight)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Brightness", brightness)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Contrast", contrast)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_brightness_multiplier", cold_brightness_multiplier)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_power", cold_power)
#         unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_brightness_multiplier", hot_brightness_multiplier)
#         # Unsure about the light bulb multiplier
            

#     time.sleep(0.1)
    
#     # unreal.AutomationLibrary.take_high_res_screenshot(
#     #     1920,
#     #     1080,
#     #     filename,
#     #     camera = camera_actor
#     #     )
#     #Save row to dataframe
#     row = pc.create_row(TEST_MODE, i, params, filename)
#     df = pd.concat([df, row])
#     if(i > 5):
#         break
    
# pd.display(df)

# #Saves file information to excel file
# df.to_excel(RESULTS_FILE_PATH + "\\" + pc.test_name(TEST_MODE) + "raw_data.xlsx")