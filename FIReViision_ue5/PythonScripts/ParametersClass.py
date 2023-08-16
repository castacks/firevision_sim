
import itertools
import numpy as np

FIRE_TEST = 1
LIGHTBULB_TEST = 2

def get_cols_from_test(test_mode=FIRE_TEST):
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
            res = itertools.product(self.blend_range,
                                    self.brightness_range,
                                    self.contrast_range,
                                    self.cold_brightness_multiplier_range,
                                    self.cold_power_range,
                                    self.hot_brightness_multipler_range,
                                    self.hot_power_range,
                                    self.sky_heat_range,
                                    self.fire_heat_range,
                                    self.ground_heat_correction_strength_range,
                                    self.ground_heat_offset,
                                    self.person_heat_multiplier_range,
                                    self.target_ground_heat_range,
                                    self.tree_correction_strength_range,
                                    self.target_tree_heat_range,
                                    self.vehicle_heat_multiplier_range)
        elif(test_mode == LIGHTBULB_TEST):
            res = itertools.product(self.blend_range,
                                    self.brightness_range,
                                    self.contrast_range,
                                    self.cold_brightness_multiplier_range,
                                    self.cold_power_range,
                                    self.hot_brightness_multipler_range,
                                    self.light_bulb_heat_multiplier_range
                                    # Building heat stuff
                                    )
        #print(f'trying {len(res)} combinations')
        return res
    
    def get_pandas_row(self, params, index):
        test_mode = self.test_mode
        row = dict()
        if(test_mode == FIRE_TEST):
            blend = params[0]
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
            row = {"index": index, "blend": blend, "brightness": brightness, "contrast": contrast, "cold_brightness_multiplier": cold_brightness_multiplier,
                    "cold_power": cold_power, "hot_brightness_multiplier": hot_brightness_multiplier, "hot_power": hot_power,
                    "sky_heat": sky_heat, "fire_heat": fire_heat, "ground_heat_correction_strength": ground_heat_correction_strength,
                    "ground_heat_offset": ground_heat_offset, "person_heat_multiplier": person_heat_multiplier,
                    "target_ground_heat": target_ground_heat, "tree_correction_strength": tree_correction_strength,
                    "target_tree_heat": target_tree_heat, "vehicle_heat_multiplier": vehicle_heat_multiplier}
        elif(test_mode == LIGHTBULB_TEST):
            blend = params[0]
            brightness = params[1]
            contrast = params[2]
            cold_brightness_multiplier = params[3]
            cold_power = params[4]
            hot_brightness_multiplier = params[5]
            hot_power = params[6]
            light_bulb_heat_multiplier = params[7]
            row = {"index": index, "blend": blend, "brightness": brightness, "contrast": contrast, "cold_brightness_multiplier": cold_brightness_multiplier,
                    "cold_power": cold_power, "hot_brightness_multiplier": hot_brightness_multiplier, "hot_power": hot_power,
                    "light_bulb_heat_multiplier": light_bulb_heat_multiplier}
        return row
    

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









