import json

import pprint

class cameraPose():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

with open('rendering_modeling_v1887_new.json') as file:
    data = json.load(file)

#Finding out how many vehicles there are in this json
numvehicles = 0

routes = []
for vehicle in data:
    if int(vehicle["id"]) == numvehicles + 1:
        routes.append([])
        numvehicles += 1
    else:
        break  


for vehicle in data:
    pose = cameraPose(float(vehicle["center_coords"]["center_x"]), 
               float(vehicle["center_coords"]["center_y"]), 
               float(vehicle["center_coords"]["center_z"]))

    print(int(vehicle["id"]) - 1)
    routes[int(vehicle["id"]) - 1].append(pose)

print(numvehicles)
print(route[0].x for route in routes)
