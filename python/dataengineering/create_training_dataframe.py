# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:42:28 2025

@author: BRD5CLJ
"""

from utils import FileHandler
import os
import pandas as pd
import numpy as np
fh = FileHandler()
EXTRACTED_LENGTH = 179
main_dir_path = fh.select_directory()
column_names = [f"sample_{i}" for i in range(1,180)]
column_names.extend(["distance","angle","grid_x","grid_y","angle","real_x","real_y","label"])

dataset = pd.DataFrame(columns=column_names)
for obj_dir_name in os.listdir(main_dir_path):
   obj_dir_path = os.path.join(main_dir_path, obj_dir_name)
   for filename in os.listdir(obj_dir_path):
       if filename.endswith("filtered.csv"):
           measurement_path = os.path.join(obj_dir_path,filename)
           current_measurement = pd.read_csv(measurement_path)
           measurement_row = current_measurement["extracted_signal"][:EXTRACTED_LENGTH-1]
           distance = current_measurement["distance"][0]
           grid_x =  current_measurement["grid_x"][0]
           grid_y = current_measurement["grid_y"][0]
           angle = current_measurement["angle"][0]
           real_x = current_measurement["real_x"][0]
           real_y = current_measurement["real_y"][0]
           label = current_measurement["type"][0]
           measurement_row = pd.concat(measurement_row , pd.Series([distance,grid_x,grid_y,angle,real_x,real_y,label]) , axis=0)
           #measurement_row.append([current_measurement])