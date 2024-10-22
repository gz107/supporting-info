#-----------------------------------#
#Developed by Z.GAO
#Data 2022.5
#Function: get data from files
#----------------------------------#
import os
from pandas import read_excel
from pandas import DataFrame
import pandas as pd
import re
lines0 = input('What is the solving name?')
#Var_name=["Partial pressure","Average loading absolute [mol/kg framework]"]
Var_name=["Enthalpy of adsorption"]
Comp_num = int(input('Compoents number?'))
delay_num = 11;
read_num = 0;
key = 0;
Var_state=0;
pressure_list=os.listdir(lines0)
pnum=len(pressure_list)
tnum = []
temp_list=[[]];
sample_list=[[[]]];
out_data = [[],[],[]]
for i in range(len(Var_name)*Comp_num):
    out_data.append([])
    
for i in range(pnum):
    path_now=lines0+'\\'+pressure_list[i];
    temp_list[i]=os.listdir(path_now);
    temp_list.append([])
    sample_list.append([[]])
    for j in range(len(temp_list[i])):
        path_now=lines0+'\\'+pressure_list[i]+'\\'+temp_list[i][j];
        abc = os.listdir(path_now);
        sample_list[i][j]=abc[0:len(abc)-32]
        #sample_list[i][j]=abc[0:len(abc)]
        sample_list[i].append([])
        
        for k in range(len(sample_list[i][j])):
            out_data[0].append(pressure_list[i])
            out_data[1].append(temp_list[i][j])
            out_data[2].append(sample_list[i][j][k])
            path_now=lines0+'\\'+pressure_list[i]+'\\'+temp_list[i][j]+'\\'+sample_list[i][j][k];
            judge_list0 = os.listdir(path_now);
            if 'Output' in judge_list0:
                path_now=lines0+'\\'+pressure_list[i]+'\\'+temp_list[i][j]+'\\'+sample_list[i][j][k]+'\\Output\\System_0';
                filename = os.listdir(path_now)
                f = open(path_now+'\\'+filename[0], 'rb', )
                lines = f.readlines()
                for m in range(len(Var_name)):
                    for line in lines:
                        if Var_name[m].encode() in line:
                            #loc_num1 = re.search("\d", str(line)).span()
                            if Var_state < Comp_num:
                                key = 1;
                            else:
                                break
                        if key == 1:
                            read_num+=1;
                        if read_num == delay_num:
                            #loc_num1 = re.search("\d", str(line)).span()
                            loc_num1 = [0]
                            out_data[Comp_num*m+Var_state+3].append(str(line)[loc_num1[0]:len(str(line))-3])
                            Var_state=Var_state+1;
                            read_num = 0;
                            key =0                  
                    if Var_state == 0:
                        for n in range(Comp_num):
                            out_data[Comp_num*m+n+3].append('No this Variables');
                    elif Var_state < Comp_num:
                        for n in range(Comp_num-Var_state):
                            out_data[Comp_num*m+Var_state+n+3].append('No this Variables');
                        Var_state=0;
                    else:
                        Var_state=0;
            else:
                for m in range(len(Var_name)):
                    for n in range(Comp_num):
                            out_data[Comp_num*m+n+3].append('No Output');
                    
                            
    sample_list[i].remove([])
temp_list.remove([])
sample_list.remove([[]])
Var_name_real=[]
for m in range(len(Var_name)):
    for i in range(Comp_num):
        Var_name_real.append(Var_name[m]+'_Comp.'+str(i+1))
tot_name=["Pressure","Temperature","Sample Name"]+Var_name_real
out_data =[[row[i] for row in out_data] for i in range(len(out_data[0]))]
zaa = pd.DataFrame(out_data,columns=tot_name)
zaa.to_excel('cof.xlsx',index = False)
print("finished")
