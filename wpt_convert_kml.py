from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd
import os
import re

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print("Imported "+filename)

# file = pd.read_csv(filename)
text_file = open(filename, "r")
data = text_file.read()
text_file.close()

numpy_array = np.array(data.split("\n"))
lat = []
long = []
names = []
index_list = []
reg = re.compile(r'[^\d.,-]+')

for i in range(len(numpy_array)):
#     if '<latitude>' in numpy_array[i]:
#         print(non_decimal.sub('',numpy_array[i]))
#     if '<longitude>' in numpy_array[i]:
#         print(non_decimal.sub('',numpy_array[i]))
    if '<coordinates>' in numpy_array[i]:
        # print(numpy_array[i])
        sub_coords = numpy_array[i].strip().split(' ')
        sub_lat = []
        sub_lon = []
        for coord in sub_coords:
            stripped_coord = reg.sub('',coord)
            lat_coord = stripped_coord.split(',')[1]
            lon_coord = stripped_coord.split(',')[0]
            sub_lat.append(lat_coord)
            sub_lon.append(lon_coord)
            # print("("+lat_coord+", "+lon_coord+")")
        lat.append(sub_lat)
        long.append(sub_lon)
    if '<name>' in numpy_array[i]:
        name = reg.sub('',numpy_array[i].strip())
        try:
            names.append(int(name))
        except ValueError:
            pass

names = np.array(names)
for i in range(len(names)):
    index = np.where(names == names.min())[0][0]
    # print(names[index])
    names[index]=10000000
    index_list.append(index)

lat_org = []
long_org = []

for j in range(len(lat)):
    i = index_list[j]
    if not i%2 == 0:
        lat[i].reverse()
        long[i].reverse()
        # print(lat[i])

    for j in range(len(lat[i])):
        lat_org.append(lat[i][j])
        long_org.append(long[i][j])

index = 0

# for i in range(len(lat)):
#     it = i%4
#     lat_org.append(lat[index])
#     long_org.append(long[index])
#     index+=org[it]

build_string = "format 1\nloop false\nwaypoints\n{\n"

# for i in range(len(lat)):
#     build_string+="waypoint\n\t{\n\t\tlatitude_deg "+lat[i]+"\n\t\tlongitude_deg "+long[i]+"\n\t\tspeed_knots 2.5\n\t\tloiterAtPoint false\n\t\tloiterRadius_ft 10\n\t\tloiterTimeUnlimited false\n\t\tloiterTime_s 240\n\t}\n\n"
# build_string+="}"

for i in range(len(lat_org)):
    build_string+="waypoint\n\t{\n\t\tlatitude_deg "+lat_org[i]+"\n\t\tlongitude_deg "+long_org[i]+"\n\t\tspeed_knots 2.5\n\t\tloiterAtPoint false\n\t\tloiterRadius_ft 10\n\t\tloiterTimeUnlimited false\n\t\tloiterTime_s 240\n\t}\n\n"
build_string+="}"
# print(build_string)

wpt_file = open("output.wpt", "w")
n = wpt_file.write(build_string)
wpt_file.close()

print(str(len(names))+" Lines Exported to File")
print(str(len(lat_org))+" Waypoints Exported to File")

print("File Exported to "+os.getcwd()+"\output.wpt")