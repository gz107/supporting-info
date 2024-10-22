#---------------------------------------#
# Developed by Z.GAO
# Date: 2022.5
# Function: Get data from files
#---------------------------------------#

import os
from pandas import DataFrame
import pandas as pd
import re

# Get input parameters
lines0 = input('What is the solving name?')
delete_num = 13 # How many non-folder type files are there in the current directory?
elx_name = "cof591_henry_single.xlsx"
Var_name = ["Average Henry coefficient:"]
delay_num = 7
Comp_num = int(input('Components number?'))

if Comp_num > 1:
    Comp_num += 1
    Var_name = ["Total enthalpy of adsorption"]
    delay_num = 10

# Initialize variables
read_num = 0
key = 0
Var_state = 0
pressure_list = os.listdir(lines0)
pnum = len(pressure_list)

temp_list = [[] for _ in range(pnum)]
sample_list = [[[] for _ in range(len(temp_list[i]))] for i in range(pnum)]
out_data = [[], [], []]

for i in range(len(Var_name) * Comp_num):
    out_data.append([])

out_data.append([])

# Read and process data
for i in range(pnum):
    path_now = os.path.join(lines0, pressure_list[i])
    temp_list[i] = os.listdir(path_now)
    sample_list.append([[]])

    for j in range(len(temp_list[i])):
        path_now = os.path.join(lines0, pressure_list[i], temp_list[i][j])
        abc = os.listdir(path_now)
        sample_list[i][j] = abc[0:len(abc)-delete_num]

        sample_list[i].append([])

        for k in range(len(sample_list[i][j])):
            out_data[0].append(pressure_list[i])
            out_data[1].append(temp_list[i][j])
            out_data[2].append(sample_list[i][j][k])
            path_now = os.path.join(lines0, pressure_list[i], temp_list[i][j], sample_list[i][j][k])
            judge_list0 = os.listdir(path_now)

            if 'Output' in judge_list0:
                path_now = os.path.join(path_now, 'Output', 'System_0')
                filename = os.listdir(path_now)

                if len(filename) != 0:
                    for In in range(len(filename)):
                        with open(os.path.join(path_now, filename[In]), 'rb') as f:
                            lines = f.readlines()

                            if In > 0:
                                out_data[0].append(pressure_list[i])
                                out_data[1].append(temp_list[i][j])
                                out_data[2].append(sample_list[i][j][k])

                            out_data[3].append(filename[In])

                            for m in range(len(Var_name)):
                                for line in lines:
                                    if Var_name[m].encode() in line:
                                        if Var_state < Comp_num:
                                            key = 1
                                    if key == 1:
                                        read_num += 1
                                    if read_num == delay_num:
                                        loc_num1 = [0]
                                        out_data[Comp_num * m + Var_state + 4].append(str(line)[loc_num1[0]:len(str(line))-3])
                                        Var_state += 1
                                        read_num = -3
                                    if Var_state >= Comp_num:
                                        key = 0
                                        break

                                if Var_state == 0:
                                    for n in range(Comp_num):
                                        out_data[Comp_num * m + n + 4].append('No this Variable')
                                elif Var_state < Comp_num:
                                    for n in range(Comp_num - Var_state):
                                        out_data[Comp_num * m + Var_state + n + 4].append('No this Variable')
                                    Var_state = 0
                                else:
                                    Var_state = 0
                            read_num = 0
            else:
                out_data[3].append('No Output folder')
                for m in range(len(Var_name)):
                    for n in range(Comp_num):
                        out_data[Comp_num * m + n + 4].append('No Output')

    sample_list[i].remove([])
temp_list.remove([])
sample_list.remove([[]])

# Generate variable names
Var_name_real = [f"{var_name}_Comp.{i+1}" for var_name in Var_name for i in range(Comp_num)]
tot_name = ["Pressure", "Temperature", "Sample Name", "Filename"] + Var_name_real

# Convert data to DataFrame and save to Excel
out_data = [[row[i] for row in out_data] for i in range(len(out_data[0]))]
zaa = pd.DataFrame(out_data, columns=tot_name)
zaa.to_excel(elx_name, index=False)

print("Finished")
