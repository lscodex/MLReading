#!/usr/bin/python3
# coding="utf-8"


import time
import pandas as pd
import tkinter as tk
import os
import csv
import numpy as np
from csv import DictWriter
from  datetime import date
from helper.gui_shows import GUISHOW

# constant variables
gui = tk.Tk(className="MLReading")

#className="MLReading" file name
csv_file_name = "readingTime.csv"
######################################################
# create csv file on folder
######################################################
def create_csv_file():
    columns_list = ["time_id", "time", "date"] 
    if os.path.isfile(csv_file_name):
        print("File exists")
    else:
        print("File not exists") 
        # create file in folder
        with open(csv_file_name, "w", newline = '') as file:
            thewriter = csv.DictWriter(file, fieldnames=columns_list)
            thewriter.writeheader()

######################################################
# check to csv row 
######################################################
def checking_file():
    # create columns 
    columns_list = ('time','date','time_id')
    # read file
    df = pd.read_csv(csv_file_name)
    df.set_index("time_id", inplace=True)
    for col in columns_list:
        if col not in df.columns:
            df[col] = np.nan

######################################################
# main function 
######################################################
if __name__ == "__main__": 
    print("Working perfectly")
    # create csv file 
    create_csv_file()
    # edit header for index
    checking_file()
    # gui init
    app = GUISHOW(csv_file_name, gui)
