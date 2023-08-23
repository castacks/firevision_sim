import unreal 
import airsim
import ParametersClass as pc
import CaptureImages as ci
import pandas as pd
import os
import ImageComparisonProcessor as icp

TEST_MODE = 1
RESULTS_FILE_PATH = ""
CAMERA_NAME = "bottom_forward_thermal"
REFERNCE_IMAGE_PATH = ""

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
airsim.wait_key('Press any key to takeoff')
print("Taking off...")
client.armDisarm(True)
client.takeoffAsync().join()
airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
client.moveToPositionAsync(-10, 10, -10, 5).join()
client.hoverAsync().join()
state = client.getMultirotorState()
airsim.wait_key('Press any key to take images')

# Get all parameter combinations
params_obj = pc.Parameters(test_mode=TEST_MODE)
parameter_combinations = params_obj.all_parameter_combinations()

# Initializes data management dataframe
df = pd.DataFrame(columns=pc.get_cols_from_test(TEST_MODE)).reset_index(drop=True)

#Grab our PP Thermal Material 
thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/Thermal_FX/PP_Thermal_FX_Inst")

#Create images folder within our results folder
images_dir = os.path.join(RESULTS_FILE_PATH, "images")
os.mkdir(images_dir)

best_accs = {0 : [0,0]}
ref_image = icp.image_from_file(REFERNCE_IMAGE_PATH)
i = 0
for params in parameter_combinations:
    # Set parameters then capture image
    ci.set_params(params, TEST_MODE, thermal_mat_inst)
    #Captures and saves image name into dataframe
    ci.capture_image(CAMERA_NAME, client, best_accs, ref_image, df, i, params, TEST_MODE, images_dir)

for acc_key in best_accs:
    #Save the best images if they don't already exist
    if(not os.path.exists(os.path.normpath(images_dir + "\\" + str(acc_key) + '.png'))):
        airsim.write_png(os.path.normpath(images_dir + "\\" + str(acc_key) + '.png'), best_accs[acc_key][1])

#Saves file information to excel file
df.to_excel(RESULTS_FILE_PATH + "\\" + pc.test_name(TEST_MODE) + "raw_data.xlsx")

airsim.wait_key('Press any key to reset to original state')
client.reset()
client.armDisarm(False)
#End the image capturing
client.enableApiControl(False)