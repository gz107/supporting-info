import os
import re
import pandas as pd

# 获取输入参数
lines0 = input('What is the solving name?')
delete_num = 10  # 当前目录中非文件夹类型的文件数量
elx_name = "henry_coefficients.xlsx"

# 初始化数据结构，包括七个空列表
out_data = [[], [], [], [], [], [], []]  # 初始数据结构，包含7列

# 正则表达式模式，用于提取Henry coefficient数据
pattern = r"\[(\w+)\] Average Henry coefficient:\s+([\d.eE+-]+)\s+\+/-\s+([\d.eE+-]+)"

# 遍历目录结构，读取和处理数据
pressure_list = os.listdir(lines0)
for pressure in pressure_list:
    path_now = os.path.join(lines0, pressure)
    temp_list = os.listdir(path_now)

    for temp_folder in temp_list:
        path_now_j = os.path.join(path_now, temp_folder)
        abc = os.listdir(path_now_j)
        sample_list = abc[:-delete_num]  # 删除多余文件

        for sample in sample_list:
            out_data[0].append(pressure)  # 压力值
            out_data[1].append(temp_folder)       # 温度值
            out_data[2].append(sample)            # 样本名称

            path_now_k = os.path.join(path_now_j, sample)
            judge_list0 = os.listdir(path_now_k)

            if 'Output' in judge_list0:
                path_now_output = os.path.join(path_now_k, 'Output', 'System_0')
                filename = os.listdir(path_now_output)

                if filename:
                    for file_name in filename:
                        with open(os.path.join(path_now_output, file_name), 'r') as f:
                            lines = f.read()
                        
                        # 添加文件名
                        out_data[3].append(file_name)

                        # 使用正则表达式提取Henry coefficient数据
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

# 生成 Excel 中的列名称
tot_name = ["Pressure", "Temperature", "Sample Name", "Filename", "Gas", "Average Henry Coefficient", "Error"]

# 将数据转换为 DataFrame 并保存到 Excel
out_data = list(zip(*out_data))  # 转置数据结构以适应 DataFrame
df = pd.DataFrame(out_data, columns=tot_name)
df.to_excel(elx_name, index=False)

print(f"数据已成功写入到 {elx_name}")
