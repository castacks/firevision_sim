import unreal
import os
unreal.log("Starting script")
#To interact with the unreal engine editor
editor_util = unreal.EditorUtilityLibrary()

#Grab the camera actor 
camera_actor = unreal.editor_util.find_actor_by_class(None, unreal.CameraActor, "ThermalCamera")
#To edit the material 
material_util = unreal.MaterialEditingLibrary()
#Grab our PP Thermal Material 
thermal_mat = "Game/Content/Thermal_FX/PP_Thermal_FX"
thermal_mat = unreal.load_asset(thermal_mat)

#Loop through range of values, create a material instance, edit a parameter, then take a screenshot
if camera_actor: 
    for i in range(0,5):
        thermal_inst = editor_util.create_transient_instance(thermal_mat)
        thermal_inst.set_parameter_value("Brightness", i*20)
        camera_actor.set_material(thermal_inst)
        unreal.log("Saving image " + str(i))
        unreal.GameplayStatics.captureViewport(camera_actor, True, os.path.dirname(os.path.abspath(__file__)) + "\SceneImages" + str(i) + ".png")
        unreal.log("Image saved")
unreal.log("Done")
