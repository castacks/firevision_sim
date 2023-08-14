import unreal
import os
unreal.log("Starting script")
#To interact with the unreal engine editor
editor_util = unreal.EditorUtilityLibrary()

#Grab the camera actor 
camera_actor = editor_util.get_actor_reference("ThermalCamera")

#Grab the world 
world = unreal.UnrealEditorSubsystem().get_game_world()

#To edit the material (may not be needed anymore) 
material_util = unreal.MaterialEditingLibrary()
#Grab our PP Thermal Material 
thermal_mat = "/Game/Thermal_FX/PP_Thermal_FX"
thermal_mat = unreal.EditorAssetLibrary.load_asset(thermal_mat)

#If the camera and material exists, proceed with the looping
if camera_actor and thermal_mat: 
    for i in range(0,5):
        thermal_inst = unreal.MaterialLibrary.create_dynamic_material_instance(world, thermal_mat)
        thermal_inst.set_parameter_value("Brightness", i*20)
        
        #Needs to be changed (Most likely doesn't work)
        camera_actor.set_material(thermal_inst)
        
        unreal.log("Saving image " + str(i))
        
        #Needs to be changed (Most likely doesn't work)
        unreal.GameplayStatics.captureViewport(camera_actor, True, os.path.dirname(os.path.abspath(__file__)) + "\SceneImages" + str(i) + ".png")
        
        unreal.log("Image saved")
unreal.log("Done")
