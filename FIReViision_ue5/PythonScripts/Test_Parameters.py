import itertools
import numpy as np
import pandas as pd
import os
import ParametersClass as pc 


blend_weight_min=0
blend_weight_max=100
blend_weight_step=20

brightness_min=0
brightness_max=100
brightness_step=20

contrast_min=0
contrast_max=100
contrast_step=20

cold_brightness_multiplier_min=0
cold_brightness_multiplier_max=150
cold_brightness_multiplier_step=30

cold_power_min=-2
cold_power_max=2
cold_power_step=0.5

hot_brightness_multiplier_min=0
hot_brightness_multiplier_max=150
hot_brightness_multiplier_step=50

hot_power_min=-2
hot_power_max=2
hot_power_step=0.5

light_bulb_heat_multiplier_min=0 
light_bulb_heat_multiplier_max=1 
light_bulb_heat_multiplier_step=0.1

parameter_combinations = pc.Parameters(
    test_mode=2,
    
    blend_weight_min=blend_weight_min, 
    blend_weight_max=blend_weight_max, 
    blend_weight_step=blend_weight_step,
    
    brightness_min=brightness_min, 
    brightness_max=brightness_max, 
    brightness_step=brightness_step,
    
    contrast_min=contrast_min, 
    contrast_max=contrast_max, 
    contrast_step=contrast_step,
    
    cold_brightness_multiplier_min=cold_brightness_multiplier_min, 
    cold_brightness_multiplier_max=cold_brightness_multiplier_max, 
    cold_brightness_multiplier_step=cold_brightness_multiplier_step,
    
    cold_power_min=cold_power_min, 
    cold_power_max=cold_power_max, 
    cold_power_step=cold_power_step,
    
    hot_brightness_multiplier_min=hot_brightness_multiplier_min, 
    hot_brightness_multiplier_max=hot_brightness_multiplier_max, 
    hot_brightness_multiplier_step=hot_brightness_multiplier_step,
    
    hot_power_min=hot_power_min, 
    hot_power_max=hot_power_max, 
    hot_power_step=hot_power_step,
    
    light_bulb_heat_multiplier_min=light_bulb_heat_multiplier_min, 
    light_bulb_heat_multiplier_max=light_bulb_heat_multiplier_max, 
    light_bulb_heat_multiplier_step=light_bulb_heat_multiplier_step
    ).all_parameter_combinations()

print(len(parameter_combinations))