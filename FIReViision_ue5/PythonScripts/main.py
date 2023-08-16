import unreal 
import airsim
import ParametersClass as pc
import CaptureImages as ci
TEST_MODE = 1
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
params_obj = pc.Parameters(test_mode=TEST_MODE)
parameter_combinations = params_obj.all_parameter_combinations()

#Grab our PP Thermal Material 
thermal_mat_inst = unreal.EditorAssetLibrary.load_asset("/Game/Thermal_FX/PP_Thermal_FX_Inst")
for params in parameter_combinations:
    ci.set_params("bottom_forward_thermal", params, TEST_MODE, thermal_mat_inst)
    ci.capture_image("bottom_forward_thermal", client, params)
airsim.wait_key('Press any key to reset to original state')
client.reset()
client.armDisarm(False)
#End the image capturing
client.enableApiControl(False)