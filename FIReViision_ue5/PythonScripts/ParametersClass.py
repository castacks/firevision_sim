
import itertools
import numpy as np
import pandas as pd

FIRE_TEST = 1
LIGHTBULB_TEST = 2

# General Parameter indexes
BLEND_INDEX = 0
BRIGHTNESS_INDEX = 1
CONTRAST_INDEX = 2
COLD_BRIGHTNESS_MULTIPLIER_INDEX = 3
COLD_POWER_INDEX = 4
HOT_BRIGHTNESS_MULTIPLIER_INDEX = 5
HOT_POWER_INDEX = 6

# Fire test-specific parameter indexes
SKY_HEAT_INDEX = 7
FIRE_HEAT_INDEX = 8
GROUND_HEAT_CORRECTION_STRENGTH_INDEX = 9
GROUND_HEAT_OFFSET_INDEX = 10
PERSON_HEAT_MULTIPLIER_INDEX = 11
TARGET_GROUND_HEAT_INDEX = 12
TREE_CORRECTION_STRENGTH_INDEX = 13
TARGET_TREE_HEAT_INDEX = 14
VEHICLE_HEAT_MULTIPLIER_INDEX = 15

#Lightbulb test-specific parameter indexes
LIGHT_BULB_HEAT_MULTIPLIER_INDEX = 7


def test_name(test_mode):
    if(test_mode == FIRE_TEST):
        return "fire_test"
    if(test_mode == LIGHTBULB_TEST):
        return "lightbulb_test"

def get_cols_from_test(test_mode=FIRE_TEST):
    general_cols = ["image_index", "filename", "blend", "brightness", "contrast", "cold_brightness_multiplier",
                "cold_power", "hot_brightness_multiplier", "hot_power"]
    if(test_mode == FIRE_TEST):
        return general_cols + ["sky_heat", "fire_heat", "ground_heat_correction_strength",
            "ground_heat_offset","person_heat_multiplier",
            "target_ground_heat", "tree_correction_strength",
            "target_tree_heat", "vehicle_heat_multiplier"]
    elif(test_mode == LIGHTBULB_TEST):
        return general_cols + ["light_bulb_heat_multiplier"]
    else:
        print("Invalid test mode")
    return None

def create_row(test_mode, index, params, filename):
        row = {}
        
        blend = params[BLEND_INDEX]
        brightness = params[BRIGHTNESS_INDEX]
        contrast = params[CONTRAST_INDEX]
        cold_brightness_multiplier = params[COLD_BRIGHTNESS_MULTIPLIER_INDEX]
        cold_power = params[COLD_POWER_INDEX]
        hot_brightness_multiplier = params[HOT_BRIGHTNESS_MULTIPLIER_INDEX]
        hot_power = params[HOT_POWER_INDEX]
        
        if(test_mode == FIRE_TEST):
            sky_heat = params[SKY_HEAT_INDEX]
            fire_heat = params[FIRE_HEAT_INDEX]
            ground_heat_correction_strength = params[GROUND_HEAT_CORRECTION_STRENGTH_INDEX]
            ground_heat_offset = params[GROUND_HEAT_OFFSET_INDEX]
            person_heat_multiplier = params[PERSON_HEAT_MULTIPLIER_INDEX]
            target_ground_heat = params[TARGET_GROUND_HEAT_INDEX]
            tree_correction_strength = params[TREE_CORRECTION_STRENGTH_INDEX]
            target_tree_heat = params[TARGET_TREE_HEAT_INDEX]
            vehicle_heat_multiplier = params[VEHICLE_HEAT_MULTIPLIER_INDEX]
            row = {"image_index": index, "filename": filename, "blend": blend, "brightness": brightness, "contrast": contrast, "cold_brightness_multiplier": cold_brightness_multiplier,
                    "cold_power": cold_power, "hot_brightness_multiplier": hot_brightness_multiplier, "hot_power": hot_power,
                    "sky_heat": sky_heat, "fire_heat": fire_heat, "ground_heat_correction_strength": ground_heat_correction_strength,
                    "ground_heat_offset": ground_heat_offset, "person_heat_multiplier": person_heat_multiplier,
                    "target_ground_heat": target_ground_heat, "tree_correction_strength": tree_correction_strength,
                    "target_tree_heat": target_tree_heat, "vehicle_heat_multiplier": vehicle_heat_multiplier}
        elif(test_mode == LIGHTBULB_TEST):
            light_bulb_heat_multiplier = params[LIGHT_BULB_HEAT_MULTIPLIER_INDEX]
            row = {"image_index": index, "filename": filename, "blend": blend, "brightness": brightness, "contrast": contrast, "cold_brightness_multiplier": cold_brightness_multiplier,
                    "cold_power": cold_power, "hot_brightness_multiplier": hot_brightness_multiplier, "hot_power": hot_power,
                    "light_bulb_heat_multiplier": light_bulb_heat_multiplier}
        return pd.Series(row)
    
class Parameters:
    def __init__(self, test_mode=FIRE_TEST,
                    blend_weight_min=30, blend_weight_max=100, blend_weight_step=0.5,
                    brightness_min=40, brightness_max=100, brightness_step=1,
                    contrast_min=0, contrast_max=100, contrast_step=1,
                    cold_brightness_multiplier_min=0, cold_brightness_multipler_max=200, cold_brightness_multiplier_step=1,
                    cold_power_min=-2, cold_power_max=2, cold_power_step=0.1,         
                    hot_brightness_multipler_min=0, hot_brightness_multipler_max=10, hot_brightness_multipler_step=0.2,
                    hot_power_min=-2, hot_power_max=2, hot_power_step=0.1,
                    sky_heat_min=0, sky_heat_max=0.2, sky_heat_step=0.01,
                    fire_heat_min=0.8, fire_heat_max=1, fire_heat_step=0.05,
                    ground_heat_correction_strength_min=0, ground_heat_correction_strength_max=10000, ground_heat_correction_strength_step=10,
                    ground_heat_offset_min=0, ground_heat_offset_max=1, ground_heat_offset_step=0.02,
                    person_heat_multiplier_min=0, person_heat_multiplier_max=25, person_heat_multiplier_step=0.5,
                    target_ground_heat_min=0, target_ground_heat_max=1, target_ground_heat_step=0.01,
                    tree_correction_strength_min=0,tree_correction_strength_max=10000, tree_correction_strength_step=10,
                    target_tree_heat_min=0, target_tree_heat_max=1, target_tree_heat_step=0.01,
                    vehicle_heat_multiplier_min=0, vehicle_heat_multiplier_max=25, vehicle_heat_multiplier_step=0.5,
                    light_bulb_heat_multiplier_min=0, light_bulb_heat_multiplier_max=1, light_bulb_heat_multiplier_step=0.01
                    ):
        self.test_mode = test_mode
        self.blend_range = np.arange(blend_weight_min, blend_weight_max, blend_weight_step)
        self.brightness_range = np.arange(brightness_min, brightness_max, brightness_step)
        self.contrast_range = np.arange(contrast_min, contrast_max, contrast_step)
        self.cold_brightness_multiplier_range = np.arange(cold_brightness_multiplier_min,
                                                        cold_brightness_multipler_max,
                                                        cold_brightness_multiplier_step)
        self.cold_power_range = np.arange(cold_power_min, cold_power_max, cold_power_step)
        self.hot_brightness_multipler_range = np.arange(hot_brightness_multipler_min,
                                                    hot_brightness_multipler_max,
                                                    hot_brightness_multipler_step)
        self.hot_power_range = np.arange(hot_power_min, hot_power_max, hot_power_step)
        self.sky_heat_range = np.arange(sky_heat_min, sky_heat_max, sky_heat_step)
        self.fire_heat_range = np.arange(fire_heat_min, fire_heat_max, fire_heat_step)
        self.ground_heat_correction_strength_range = np.arange(ground_heat_correction_strength_min, ground_heat_correction_strength_max, ground_heat_correction_strength_step)
        self.ground_heat_offset = np.arange(ground_heat_offset_min, ground_heat_offset_max, ground_heat_offset_step)
        self.person_heat_multiplier_range = np.arange(person_heat_multiplier_min, person_heat_multiplier_max, person_heat_multiplier_step)
        self.target_ground_heat_range = np.arange(target_ground_heat_min, target_ground_heat_max, target_ground_heat_step)
        self.tree_correction_strength_range = np.arange(tree_correction_strength_min, tree_correction_strength_max, tree_correction_strength_step)
        self.target_tree_heat_range = np.arange(target_tree_heat_min, target_tree_heat_max, target_tree_heat_step)
        self.vehicle_heat_multiplier_range = np.arange(vehicle_heat_multiplier_min, vehicle_heat_multiplier_max, vehicle_heat_multiplier_step)
        self.light_bulb_heat_multiplier_range = np.arange(light_bulb_heat_multiplier_min, light_bulb_heat_multiplier_max, light_bulb_heat_multiplier_step)

    def all_parameter_combinations(self):
        test_mode = self.test_mode
        res = list()
        if(test_mode == FIRE_TEST):
            res = itertools.product(self.blend_range, # blend weight 1
                                    self.brightness_range, # brightness 2
                                    self.contrast_range, # contrast 3
                                    self.cold_brightness_multiplier_range, # cold brightness multiplier 4
                                    self.cold_power_range, # cold power 5
                                    self.hot_brightness_multipler_range, # hot brightness multiplier 6
                                    self.hot_power_range, # hot power 7
                                    self.sky_heat_range, # sky heat 8
                                    self.fire_heat_range, # fire heat 9
                                    self.ground_heat_correction_strength_range, # ground heat correction strength 10
                                    self.ground_heat_offset, # ground heat offset 11 
                                    self.person_heat_multiplier_range, # person heat multiplier 12
                                    self.target_ground_heat_range, # target ground heat 13
                                    self.tree_correction_strength_range, # tree correction strength 14
                                    self.target_tree_heat_range, # target tree heat 15
                                    self.vehicle_heat_multiplier_range # vehicle heat multiplier 16
                                    )
        elif(test_mode == LIGHTBULB_TEST):
            res = itertools.product(self.blend_range, # blend weight 1
                                    self.brightness_range, # brightness 2
                                    self.contrast_range, # contrast 3
                                    self.cold_brightness_multiplier_range, # cold brightness multiplier 4
                                    self.cold_power_range, # cold power 5
                                    self.hot_brightness_multipler_range, # hot brightness multiplier 6
                                    self.light_bulb_heat_multiplier_range # light bulb heat multiplier 7
                                    # Building heat stuff
                                    )
        #print(f'trying {len(res)} combinations')
        return res
    
    
    

    def get_test_cols(self):
        test_mode = self.test_mode

        if(test_mode == FIRE_TEST):
            return["blend", "brightness", "contrast", "cold_brightness_multiplier",
                "cold_power", "hot_brightness_multiplier", "hot_power",
                "sky_heat", "fire_heat", "ground_heat_correction_strength",
                "ground_heat_offset","person_heat_multiplier",
                "target_ground_heat", "tree_correction_strength",
                "target_tree_heat", "vehicle_heat_multiplier"]
        elif(test_mode == LIGHTBULB_TEST):
            return["blend", "brightness", "contrast", "cold_brightness_multiplier",
                "cold_power", "hot_brightness_multiplier", "hot_power",
                "sky_heat", "fire_heat", "ground_heat_correction_strength",
                "ground_heat_offset","person_heat_multiplier",
                "target_ground_heat", "tree_correction_strength",
                "target_tree_heat", "vehicle_heat_multiplier",
                "light_bulb_heat_multiplier"]
        print("Invalid test mode")
        return None









