from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import os

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print("Imported "+filename)

file = pd.read_csv(filename)

numpy_array = np.array(file)
lat = []
long = []

for i in range(len(numpy_array)):
    if 'PT' in numpy_array[i][0]:
        sub_arr = numpy_array[i][0].split(" ")
        lat.append(sub_arr[1])
        long.append(sub_arr[2])

lat_org = []
long_org = []
org = [1,2,-1,2]

index = 0

for i in range(len(lat)):
    it = i%4
    lat_org.append(lat[index])
    long_org.append(long[index])
    index+=org[it]

build_string = "format 1\nloop false\nwaypoints\n{\n"

for i in range(len(lat_org)):
    build_string+="waypoint\n\t{\n\t\tlatitude_deg "+lat_org[i]+"\n\t\tlongitude_deg "+long_org[i]+"\n\t\tspeed_knots 2.5\n\t\tloiterAtPoint false\n\t\tloiterRadius_ft 10\n\t\tloiterTimeUnlimited false\n\t\tloiterTime_s 240\n\t}\n\n"
build_string+="}"

#print(build_string)

wpt_file = open("output.wpt", "w")
n = wpt_file.write(build_string)
wpt_file.close()

print("File Exported to "+os.getcwd()+"\output.wpt")