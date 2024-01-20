# Code heavily, gratefully, borrows from: https://github.com/stevenkfirth/stevenfirth/blob/main/energyplus-simulation-and-analysis-using-python/EnergyPlus%20simulation%20and%20analysis%20using%20Python.ipynb?ref=stevenfirth.com

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os



energyplus_install_dir=r'C:\EnergyPlusV23-2-0'

folder_path = 'sim/idfs'
epw_file=r'sim\weather\CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw' # ASHRAE climate zone 6A
output_directory='sim\out'



def modify_timestep_in_idf(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified = False
    for i, line in enumerate(lines):
        if line.strip().startswith('Timestep,'):
            lines[i] = 'Timestep,\n12; !- Number of Timesteps per Hour\n'
            modified = True
            break

    if modified:
        with open(file_path, 'w') as file:
            file.writelines(lines)


# Command line string to run a simulation 
def run_energyplus(idf_file, epw_file, output_directory, energyplus_install_dir):
    command = [
        f'"{energyplus_install_dir}\\EnergyPlus"',
        '--readvars',
        f'--output-directory "{output_directory}"',
        f'--weather "{epw_file}"',
        f'"{idf_file}"'
    ]
    subprocess.run(' '.join(command), shell=True)


def process_idf_files(folder_path, epw_file, energyplus_install_dir):
    for filename in os.listdir(folder_path):
        if filename.endswith('.idf'):
            idf_file_path = os.path.join(folder_path, filename)
            modify_timestep_in_idf(idf_file_path)
            print(f"Updated timesteps in {filename}")

            output_directory = folder_path  
            run_energyplus(idf_file_path, epw_file, output_directory, energyplus_install_dir)
            print(f"Ran EnergyPlus simulation for {filename}")




process_idf_files(folder_path, epw_file, energyplus_install_dir)




 


