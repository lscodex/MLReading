import os
import pandas as pd
import csv
import numpy as np
from csv import DictWriter
class CreateCsvFile:
    def __init__(self):
        # constant path variable
        self.__csv_file_name = "readingTime.csv"
        self.__columns_list = ["time_id", "time", "date"] 
        self.__columns_tuple = ("time", "date", "time_id")
        self.__prepare_file_for_header()

######################################################
# check to csv row 
######################################################
    def __checking_file(self):
        # removing columns that beyond row
        df = pd.read_csv(self.__csv_file_name)
        df.set_index("time_id",inplace=True)
        for col in self.__columns_tuple:
            if col not in df.columns:
                df[col] = np.nan

######################################################
# create csv file on folder
######################################################
    def __prepare_file_for_header(self):
        if os.path.isfile(self.__csv_file_name):
            print("File is Exists")
        else:
            print("File is not Exists, The program is create it with succes")
            with open(self.__csv_file_name,"w", newline='') as file:
                thewriter = csv.DictWriter(file, fieldnames=self.__columns_tuple)
                thewriter.writeheader() 
        self.__checking_file()

    def get_path(self):
        return self.__csv_file_name
