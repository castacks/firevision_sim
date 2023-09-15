# This python script is meant to be called in the Unreal Engine Python terminal.
# This file reads the parameters from a specified directory, and changes the current
# environment's materials, THIS SCRIPT DOES NOT TAKE AN IMAGE.


from datetime import datetime
import os
from pathlib import Path
import platform
from subprocess import Popen
import pandas as pd
import time

import unreal

TEST_MODE = "single_fire_test"
MUTEX_DIR = r"C:\Users\John\Downloads\temp_params\mutex_unlock.txt"
PARAMS_DIR = r"c:\Users\John\Downloads\temp_params\params.csv"
# TEST_MODE = "lightbulb_test"

# subsystems
EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
LevelEditorSubsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
UnrealEditorSubsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)


# thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/FIReVision_Assets/FIReVision_FX/PP_Thermal_FX_Inst")
thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/FIReVision_Assets/FIReVision_FX/PP_Thermal_Bondi__FX_Inst")


#Grabs Camera Actor
actors = unreal.EditorLevelLibrary.get_all_level_actors()
camera_actor = None
for actor in actors:
    if (actor.get_name() == 'CineCameraActor_1'):
        camera_actor = actor
        break
params = pd.read_csv(PARAMS_DIR)
row = params.iloc[0]

blend_weight = row["blend_weight"].item()
brightness = row["brightness"].item()
contrast = row["contrast"].item()
cold_brightness_multiplier = row["cold_brightness_multiplier"].item()
cold_power = row["cold_power"].item()
hot_brightness_multiplier = row["hot_brightness_multiplier"].item()
hot_power = row["hot_power"].item()

unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"blend_weight", blend_weight)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Brightness", brightness)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"Contrast", contrast)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_brightness_multiplier", cold_brightness_multiplier)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"cold_power", cold_power)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_brightness_multiplier", hot_brightness_multiplier)
unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"hot_power", hot_power)

if (TEST_MODE == "lightbulb_test"):
    light_bulb_heat_multiplier = row["light_bulb_heat_multiplier"].item()
    lamp_heat_multiplier = row["lamp_heat_multiplier"].item()

    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"light_bulb_heat_multiplier", light_bulb_heat_multiplier)
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,"lamp_heat_multiplier", lamp_heat_multiplier)

if(TEST_MODE == "single_fire_test"):
    sky_heat = row['sky_heat']
    ground_heat_correction = row['ground_heat_correction']
    tree_correction_strength = row['tree_correction_strength']
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,'sky_heat', hot_power)
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,'ground_heat_correction', cold_power)
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(thermal_mat_inst,'tree_correction_strength', hot_brightness_multiplier)
    
time.sleep(0.1)
f = open(MUTEX_DIR, "a")
f.write("Safe to take an image now!")
f.close()