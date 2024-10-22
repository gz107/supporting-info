#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
Function   :   diffusivity_calculation.py
Software   :   VSCode
"""
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def get_diffusivity_from_simulation_result_dir_single_comp(path_dir, path_save_data, molecule, times_range=[50, 380],
                                                           r2_threshold=0.95, columns=[0, 1]):
    """
    For some porous materials, MD cannot accurately simulate their diffusion coefficients. This code identifies 
    data from inaccurate simulations and marks them with a negative value (-1000000000). The code is suitable for 
    extracting single-component data.

    :param path_dir: Absolute path where all cif files and intermediate calculation results are located
    :param path_save_data: Path where the extracted results are saved, format: /**/**.xlsx. If the path does not 
                           exist, it will be created.
    :param molecule: Name of the molecule
    :param times_range: The time range for data sampling. If running 1 million cycles, it is recommended to use the 
                        default value. Default: [50, 380]
    :param r2_threshold: Threshold of the coefficient of determination. If the R² of time vs MSD linear fit is below 
                         this threshold, the calculation is considered unreliable. Default: 0.95
    :param columns: [0, 1] column indices for time and MSD
    :return: None
    """

    # Find all subdirectories
    list_all_file = os.listdir(path_dir)
    list_path_dir = [i for i in list_all_file if os.path.isdir(os.path.join(path_dir, i))]

    def __get_slope_value(path_msd, columns, times_range):
        """
        Calculate slope (diffusion coefficient) from MSD calculation results.

        :param path_msd: Path to the .dat file used to calculate the slope
        :param columns: Columns used to fit the data
        :param times_range: Time range used to fit the line, which gives the slope (in ps)
        :return: Slope of the fitted line (diffusion coefficient)
        """
        x, y = [], []
        # Sample (get x and y data for fitting)
        with open(path_msd, 'r') as f:
            for line in f.readlines():
                temp = line.split(' ')
                x.append(float(temp[columns[0]]))
                y.append(float(temp[columns[1]]))

        data = np.array([x, y]).T
        filtered_index = np.where((data[:, 0] >= times_range[0]) & (data[:, 0] <= times_range[1]))[0]
        data = data[filtered_index, :]
        x, y = data[:, 0], data[:, 1]

        # Fit and return the corresponding slope
        lr = LinearRegression()
        lr.fit(x.reshape(-1, 1), y)
        slope = lr.coef_[0]
        r2 = lr.score(x.reshape(-1, 1), y)

        return r2, slope

    list_slope = []
    for dir_name in list_path_dir:
        path_current_dir = os.path.join(path_dir, dir_name)
        path_result_dir = os.path.join(path_current_dir, 'MSDOrderN', 'System_0')

        try:
            count = 0
            os.chdir(path_result_dir)
            path_mol_file = f'msd_self_{molecule}_{count}.dat'
            r2, temp_slope = __get_slope_value(path_mol_file, columns, times_range)
            if columns[-1] == 1:
                temp_slope = 1 / (2 * 3) * temp_slope  # Adjust slope for single component
            if r2 < r2_threshold:
                temp_slope = -100000000  # Mark unreliable data
        except Exception:
            temp_slope = -100000000  # No calculation result
        list_slope.append(temp_slope)

    # Save the results
    list_cif = [cif + '.cif' for cif in list_path_dir]
    df = pd.DataFrame([list_cif, list_slope]).T
    df.columns = ['cif_name', f'self-diffusion coefficient of {molecule} /(10^-8 m^2/s)']

    # Ensure the save path exists, if not, create it
    path_save_data_dir = os.path.dirname(path_save_data)
    if not os.path.exists(path_save_data_dir):
        os.makedirs(path_save_data_dir)

    df.to_excel(path_save_data, index=None)


def get_diffusivity_from_simulation_result_dir_multi_comp(path_dir, path_save_data, molecules, times_range=[1000, 4000],
                                                          r2_threshold=0.95, columns=[0, 1]):
    """
    For some porous materials, MD cannot accurately simulate their diffusion coefficients. This code identifies 
    data from inaccurate simulations and marks them with a negative value (-1000000000). The code is suitable for 
    extracting multi-component data.

    :param path_dir: Absolute path where all cif files and intermediate calculation results are located
    :param path_save_data: Path where the extracted results are saved, format: /**/**.xlsx. If the path does not 
                           exist, it will be created.
    :param molecules: Names of the molecules
    :param times_range: The time range for data sampling. If running 1 million cycles, it is recommended to use the 
                        default value. Default: [50, 380]
    :param r2_threshold: Threshold of the coefficient of determination. If the R² of time vs MSD linear fit is below 
                         this threshold, the calculation is considered unreliable. Default: 0.95
    :param columns: [0, 1] column indices for time and MSD
    :return: None
    """

    # Find all subdirectories
    list_all_file = os.listdir(path_dir)
    list_path_dir = [i for i in list_all_file if os.path.isdir(os.path.join(path_dir, i))]

    def __get_slope_value(path_msd, columns, times_range):
        """
        Calculate slope (diffusion coefficient) from MSD calculation results.

        :param path_msd: Path to the .dat file used to calculate the slope
        :param columns: Columns used to fit the data
        :param times_range: Time range used to fit the line, which gives the slope (in ps)
        :return: Slope of the fitted line (diffusion coefficient)
        """
        x, y = [], []
        # Sample (get x and y data for fitting)
        with open(path_msd, 'r') as f:
            for line in f.readlines():
                temp = line.split(' ')
                x.append(float(temp[columns[0]]))
                y.append(float(temp[columns[1]]))

        data = np.array([x, y]).T
        filtered_index = np.where((data[:, 0] >= times_range[0]) & (data[:, 0] <= times_range[1]))[0]
        data = data[filtered_index, :]
        x, y = data[:, 0], data[:, 1]

        # Fit and return the corresponding slope
        lr = LinearRegression()
        lr.fit(x.reshape(-1, 1), y)
        slope = lr.coef_[0]
        r2 = lr.score(x.reshape(-1, 1), y)

        return r2, slope

    list_slope = []
    for dir_name in list_path_dir:
        path_current_dir = os.path.join(path_dir, dir_name)
        path_result_dir = os.path.join(path_current_dir, 'MSDOrderN', 'System_0')
        list_temp_slope = []
        count = 0
        for molecule in molecules:
            try:
                os.chdir(path_result_dir)
                path_mol_file = f'msd_self_{molecule}_{count}.dat'
                r2, temp_slope = __get_slope_value(path_mol_file, columns, times_range)
                if columns[-1] == 1:
                    temp_slope = 1 / (2 * 3) * temp_slope  # Adjust slope for multi-component system
                if r2 < r2_threshold:
                    temp_slope = -100000000  # Mark unreliable data
            except Exception:
                temp_slope = -100000000  # No calculation result
            count += 1
            list_temp_slope.append(temp_slope)
        list_slope.append(list_temp_slope)

    # Save the results
    list_cif = [cif + '.cif' for cif in list_path_dir]
    column_names = [f'self-diffusion coefficient of {mol} /(10^-8 m^2/s)' for mol in molecules]
    df = pd.DataFrame(list_slope, columns=column_names, index=list_cif)

    # Ensure the save path exists, if not, create it
    path_save_data_dir = os.path.dirname(path_save_data)
    if not os.path.exists(path_save_data_dir):
        os.makedirs(path_save_data_dir)

    df.to_excel(path_save_data)
