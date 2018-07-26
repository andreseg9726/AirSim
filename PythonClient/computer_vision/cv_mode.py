# In settings.json first activate computer vision mode: 
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode

import setup_path 
import airsim

import pprint
import os
import time

import json
import math

pp = pprint.PrettyPrinter(indent=4)
 
client = airsim.VehicleClient()
client.confirmConnection()

# Class that keeps the position and orientation of a vehicle, use radians.
class cameraPose():
    def __init__(self, x, y, z, yaw, pitch, roll):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

# Reading from the json file
try:
    filename = input("Enter the name of the JSON file: ")
    with open(filename) as file:
        data = json.load(file)
except IOError:
    print("No file with that name found in your directory.")

# Finding out how many vehicles there are in this json and creating an empty 
# 2D array with that many spaces. Depends on vehicle positions listed in order.
numvehicles = 0
routes = []
for vehicle in data:
    if int(vehicle["id"]) == numvehicles + 1:
        routes.append([])
        numvehicles += 1
    else:
         break  
         
# Reading in the poses and filling the array         
for vehicle in data:
    pose = cameraPose(float(vehicle["center_coords"]["center_x"]), 
               float(vehicle["center_coords"]["center_y"]), 
               float(vehicle["center_coords"]["center_z"]),
               math.radians(float(vehicle["euler_angles"]["yaw"])),
               math.radians(float(vehicle["euler_angles"]["pitch"])),
               math.radians(float(vehicle["euler_angles"]["roll"])))

    routes[int(vehicle["id"]) - 1].append(pose)

# This loop will set the camera pose to the ones in the 2D array. Currently 
# only works for one vehicle
airsim.wait_key('Press any key to move')
for index, waypoint in enumerate(routes[0]):
    client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(routes[0][index].x, 
                                                         routes[0][index].y, 
                                                         routes[0][index].z), 
                             airsim.to_quaternion(routes[0][index].pitch, 
                                                  routes[0][index].roll, 
                                                  routes[0][index].yaw)), True) 
    print("Waypoint number: %d" % index)

    # Printing the pose for visualization purposes.
    pose = client.simGetVehiclePose()
    pp.pprint(pose)
    time.sleep(2)
    
#currently reset() doesn't work in CV mode. Below is the workaround
client.simSetPose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)