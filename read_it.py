#!/usr/bin/python3
# coding="utf-8"


import tkinter as tk
from helper.gui_shows import GUISHOW
from helper.create_file import CreateCsvFile

# constant variables
gui = tk.Tk(className="MLReading")

######################################################
# main function 
######################################################
if __name__ == "__main__": 
    print("Working perfectly")
    init_file = CreateCsvFile()
    # gui init
    app = GUISHOW(init_file.get_path(), gui)
