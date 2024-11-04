#---------------------------------------#
# Developed by Z.GAO
# Date: 2022.5
# Function: Get data from files
#---------------------------------------#

import os
import re
import pandas as pd

# Input Parameters
lines0 = input('What is the solving name?')
delete_num = 10  # The number of non-folder type files in the current directory
elx_name = "henry_coefficients.xlsx"

# Initialize the data structure, including seven empty lists
out_data = [[], [], [], [], [], [], []]  #Initial data structure, containing 7 columns

# Regular expression pattern for extracting Henry coefficient data
pattern = r"\[(\w+)\] Average Henry coefficient:\s+([\d.eE+-]+)\s+\+/-\s+([\d.eE+-]+)"

# Traverse the directory structure, read and process data
pressure_list = os.listdir(lines0)
for pressure in pressure_list:
    path_now = os.path.join(lines0, pressure)
    temp_list = os.listdir(path_now)

    for temp_folder in temp_list:
        path_now_j = os.path.join(path_now, temp_folder)
        abc = os.listdir(path_now_j)
        sample_list = abc[:-delete_num]  # Delete unnecessary files

        for sample in sample_list:
            out_data[0].append(pressure)  
            out_data[1].append(temp_folder)      
            out_data[2].append(sample)            

            path_now_k = os.path.join(path_now_j, sample)
            judge_list0 = os.listdir(path_now_k)

            if 'Output' in judge_list0:
                path_now_output = os.path.join(path_now_k, 'Output', 'System_0')
                filename = os.listdir(path_now_output)

                if filename:
                    for file_name in filename:
                        with open(os.path.join(path_now_output, file_name), 'r') as f:
                            lines = f.read()
                        
                       # Add file name
                        out_data[3].append(file_name)

                        # Use regular expressions to extract Henry coefficient data
                        results = re.findall(pattern, lines)
                        if results:
                            for gas, coeff, error in results:
                                out_data[4].append(gas)
                                out_data[5].append(float(coeff))
                                out_data[6].append(float(error))
                        else:
                            out_data[4].append("No Data")
                            out_data[5].append(None)
                            out_data[6].append(None)
            else:
                out_data[3].append('No Output folder')
                out_data[4].append("No Output")
                out_data[5].append(None)
                out_data[6].append(None)

# Generate column names in Excel
tot_name = ["Pressure", "Temperature", "Sample Name", "Filename", "Gas", "Average Henry Coefficient", "Error"]

# Convert data to DataFrame and save to Excel
out_data = list(zip(*out_data))  # Transpose the data structure to fit into a DataFrame
df = pd.DataFrame(out_data, columns=tot_name)
df.to_excel(elx_name, index=False)

print(f"Data has been successfully written to {elx_name}")
