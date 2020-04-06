import tkinter as tk 
from tkinter import ttk
import time
import csv
import pandas as pd
import datetime
from tkinter import messagebox as mb
from PIL import Image, ImageTk

class GUISHOW(tk.Frame):
    def __init__(self, csv_file_name,  master=None):
        self.csv_file_name = csv_file_name
        # inherit class 
        super().__init__(master)
        self.master = master
        self.csv_file_name = csv_file_name
        self.master["background"] = "orange red"
        self.master.title("ReadingTime")
        self.master.geometry("300x300")
        self.master.resizable(0,0)
        self.master.update()
        # configure cols and rows
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0, weight=1)
        # time configuration
        self.timerstr = tk.StringVar()
        self.elapsedTime = 0.0
        self.start = 0.0
        # this use boolean for reset,start,pause button
        self.running = False 
        #font
        self.TIME_FONT = ("Comic Sans MS", "44")
        self.button_width=11
        self.button_height=1
        # get values when the stop
        self.get_time = None
        # size and , current_date
        self.size = None
        # init gui and shows
        self.make_gui()
        # there is the error
        #self.master.pack(expand=False, fill=tk.BOTH)
        self.master.mainloop()
######################################################
# dialog box init
######################################################
    def show_message(self):
        mb.showinfo("No","New data is saved to:{}".format(self.size))
    def delete_values(self, get_data):
        v_time_id =get_data[0]
        ans = mb.askyesno('Delete data', 'Do you want to delete "{}"'.format(v_time_id))
        if ans:
            # delete data
            self.df_delete_values(v_time_id)
        else:
            # not delete data
            pass
        self.update_table_gui(False)

######################################################
# save the new time
######################################################
    def df_delete_values(self, num_of_delete):
        df = pd.read_csv(self.csv_file_name)
        # delete values from columns variable
        indexNames = df[df['time_id']==num_of_delete].index
        df.drop(indexNames,inplace=True)
        df.reset_index(drop=True, inplace=True) 
        df.to_csv(self.csv_file_name,index=False)

    def df_current_date(self): 
        return datetime.date.today()

    def df_size(self):
        df = pd.read_csv(self.csv_file_name)
        return len(df['time_id']), df
    
    def update_header(self):
        df = pd.read_csv(self.csv_file_name)
        df.set_index("time_id", inplace=True)

    # add new data
    def save_data_to_csv(self, time):
        self.size, df = self.df_size() 
        cur_date = self.df_current_date()
        # remove duplicated variable
        for i in df['time_id']:
            if self.size == i:
                self.size -= 1
                if self.size == i: 
                    self.size+= 2 
        fields = [self.size,time,cur_date]
        with open(self.csv_file_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

######################################################
#  callbacks
######################################################
    # timer callback method with trace
    def trace_callback_method(self, *args):
        if self.running:
            self.get_time = self.timerstr.get()
#################################################################################################################
#                                   ALL BUTTON INIT
######################################################
# start time row-1 column-1  
######################################################
    def handler_start_time(self):
        # time start with boolean for second start will not be running
        if not self.running: 
            self.start = time.time() - self.elapsedTime
            self.update()
            self.running = True 

    def start_time(self):
        self.play = tk.Button(self.frame_button, text="Start", \
                height=self.button_height, width=self.button_width,\
                command=lambda:self.handler_start_time()).pack(side=tk.LEFT)
######################################################
# pause time row-1 colunm-0
######################################################
    def handler_reset_time(self):
        # time start with boolean for second start will not be running
        self.start = time.time()
        self.elapsedTime = 0.0
        self.set_time(self.elapsedTime)
         
    def reset_time(self):
        self.reset = tk.Button(self.frame_button,text="Reset",\
                height=self.button_height,width=self.button_width, \
                command=lambda: self.handler_reset_time()).pack(side=tk.LEFT) 
######################################################
# stop time row-1 column-2 
######################################################
    def handler_stop_time(self):
        # time start with boolean for second start will not be running
        if self.running: 
            # self._timer is value in update() function that stop the timer
            self.master.after_cancel(self._timer)
            self.elapsedTime = time.time() - self.start
            self.set_time(self.elapsedTime)
            self.running = False

            # save file
            self.save_data_to_csv(self.get_time)
            self.update_header()
            self.update_table_gui(False)
            self.show_message()

    def stop_time(self):
        self.stop = tk.Button(self.frame_button,text="Stop",\
                height=self.button_height, width=self.button_width,  \
                command=lambda: self.handler_stop_time()).pack(side=tk.LEFT)
#################################################################################################################
######################################################
# create time 
######################################################
    def set_time(self, elap_time):
        minutes = int(elap_time/60)
        seconds = int (elap_time - minutes *60.0)
        hseconds = int((elap_time -minutes *60.0 - seconds)*100)
        self.timerstr.trace("w", self.trace_callback_method)
        self.timerstr.set('%02d:%02d:%02d' % (minutes,seconds,hseconds))
######################################################
# create timer and shows gui
######################################################
    def create_timer(self):
        self.label = tk.Label(self.frame_button,font=self.TIME_FONT,textvariable=self.timerstr,bg="orange red")
        self.label.config(anchor=tk.CENTER)
        self.set_time(self.elapsedTime)
        self.label.pack(fill=tk.X,side=tk.TOP)
######################################################
# update time  on label(stopwatch)
######################################################
    def update(self):
        self.elapsedTime = time.time() - self.start
        self.set_time(self.elapsedTime)
        self._timer = self.master.after(50,self.update)
######################################################
# create just csv header
######################################################
    def create_header_for_csv(self):
        # create just heqader for columns
        headers_getting=()
        df = pd.read_csv(self.csv_file_name, nrows=1)
        for i in range(0, len(df.columns)):
            self.tree["columns"] = (df.columns[i])
            self.tree.heading("#0", text="Name", anchor=tk.W)
            self.tree.heading(str(df.columns[i]), text=str(df.columns[i]),anchor=tk.W)
######################################################
# create csv filename
######################################################
    def create_csv_ongui(self):
        # insert values to csv file
        with open(self.csv_file_name, newline="") as file:
            reader = csv.reader(file)
            # skip header
            next(reader,None)
            r = 0 
            for i, val in enumerate(reader):
                self.tree.insert("",i,text="{}".format(val[0]),values=(val[0],val[1], val[2]))

    # gui update at desired location
    def update_table_gui(self, get_if_update):
        if get_if_update: 
            self.create_csv_ongui()
        else:
            for i in self.tree.get_children():
                self.tree.delete(i)
            self.create_csv_ongui()

######################################################
# button frame
######################################################
    def frame_for_button(self):
        self.frame_button = tk.Frame(self.master, background="orange red") 
        self.frame_button.configure(width=self.master.winfo_width())
        self.frame_button.pack(fill=tk.X)
        self.frame_button.update()
        self.create_timer()
        self.reset_time()
        self.start_time()
        self.stop_time()
######################################################
# update canvas
######################################################
    def delete_values_data(self,event):
        # get item for removing
        item = self.tree.selection()[0]
        values = self.tree.item(item).get("values")
        self.delete_values(values)

    def m_selection(self,event):
        self.tree.focus()
        if len(self.tree.selection()) > 0:
            item = self.tree.selection()[0]

    def frame_canvas(self):
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        # treeview init
        self.tree= tk.ttk.Treeview(self.master)
        self.tree["columns"] = ("time_id", "time", "date")
        self.tree.heading("time_id",text="time_id", anchor= tk.W)
        self.tree.heading("time", text="time", anchor=tk.W)
        self.tree.heading("date", text="date", anchor=tk.W)
        self.tree.column("time_id",width=50)
        self.tree.column("time",width=50)
        self.tree.column("date",width=50)
        self.create_csv_ongui()
        # not delete this, it remove #0 id columns in tkinter
        self.tree["show"] =" headings"

        # configuretion and callback
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree.bind("<Double-1>",self.delete_values_data)
        self.tree.bind("<Button-1>", self.m_selection)
        self.tree.pack(side=tk.TOP, fill=tk.X)
######################################################
# create graphic ui with widget
######################################################
    def make_gui(self): 
        # all functions are here.
        self.frame_for_button() 
        self.frame_canvas()
