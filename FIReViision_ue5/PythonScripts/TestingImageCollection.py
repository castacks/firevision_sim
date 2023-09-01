# Tested using Unreal 5.3 Preview on Mac

from datetime import datetime
import os
from pathlib import Path
import platform
from subprocess import Popen

import unreal


# subsystems
EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
LevelEditorSubsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
UnrealEditorSubsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

#Grabs Camera Actor
actors = unreal.EditorLevelLibrary.get_all_level_actors()
camera_actor = None
for actor in actors:
    if (actor.get_name() == 'CineCameraActor_1'):
        camera_actor = actor
        break


class PyCapture:
    def __init__(self, file_num: int = 1):
        self.file_num = file_num

        # Register post tick command
        self.on_post_tick = unreal.register_slate_post_tick_callback(self.render_frame)

    def render_frame(self, ignore):
        # Render screenshot
        file_name = f"{self.file_num}.png"
        unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, file_name, camera_actor)
        unreal.unregister_slate_post_tick_callback(self.on_post_tick)


PyCapture(5)
flush()
PyCapture(6)
