import airsim
import cv2
import time
import math
import numpy as np
import pprint
from pynput import keyboard


'''
    This script allows you to detect objects in Airsim, given their meshname &
    allows you to maneuver the drone using your computer's keyboard. 

    "w" - forward
    "s" - backward
    "a" - left
    "d" - right
    "x" - up
    "z" - down
    
'''


vx = 0
vy = 0
vz = 0

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
client.takeoffAsync().join()


# set camera name and image type to request images and detections
camera_name = "0"
image_type = airsim.ImageType.Scene

# set detection radius in [cm]
client.simSetDetectionFilterRadius(camera_name, image_type, 200 * 100)

def on_press(key):
    global vx, vy, vz

    try:
        if key == keyboard.Key.esc:
            # Stop the program if the 'Esc' key is pressed
            return False
        
        elif key.char == 'w':
            #forward
            vx = 5

        elif key.char == 's':
            #backward
            vx = -5 

        elif key.char == 'd':
            #right
           vy = 5

        elif key.char == 'a':
            #left
            vy = -5 

        elif key.char == 'x':
            #up
            vz = -5
        elif key.char == 'z':
            #down
            vz = 5

    except AttributeError:
        pass

def on_release(key):
    global vx, vy, vz
    try:
        if key.char == 'w' or key.char == 's':
            vx = 0
        elif key.char == 'd' or key.char == 'a':
            vy = 0
        elif key.char == 'x' or key.char == 'z':
            vz = 0
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def fetchDetectionsForMeshName(mesh_name):
    client.simAddDetectionFilterMeshName(camera_name, image_type, mesh_name)
    matches = client.simGetDetections(camera_name, image_type)
    client.simClearDetectionMeshNames(camera_name, image_type)
    return matches

def printDetections(mesh_name):
    objectList = fetchDetectionsForMeshName(mesh_name)
    if objectList:
        for obj in objectList:
            s = pprint.pformat(obj)
            print(f"{obj}" + ": %s" % s)

            cv2.rectangle(png,(int(obj.box2D.min.x_val),int(obj.box2D.min.y_val)),(int(obj.box2D.max.x_val),int(obj.box2D.max.y_val)),(255,0,0),2)
            cv2.putText(png, obj.name, (int(obj.box2D.min.x_val),int(obj.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))

while True:

    client.moveByVelocityBodyFrameAsync(vx, vy, vz, 12)
    time.sleep(0.1)
    
    rawImage = client.simGetImage(camera_name, image_type)
    if not rawImage:
        continue

    png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)

    #add objects you want to be detected here (wildcard format): 
    printDetections("BP_Human*")
    printDetections("BP_Buggy*")

    png = cv2.resize(png, (384, 216))
    cv2.imshow("AirSim", png)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('c'):   
        pass

    elif cv2.waitKey(1) & 0xFF == ord('a'):
        pass

cv2.destroyAllWindows()
