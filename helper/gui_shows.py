import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
import time
import csv
import pandas as pd
import datetime
from tkinter import messagebox as mb
from helper.helper_model import Helper_Model


class GUISHOW(tk.Frame):
    def __init__(self, csv_file_name, master=None):

        # inherit class
        super().__init__(master)
        # init the helper model for configuration gui, or time etc..
        self.hm = Helper_Model()
        # musn't-change
        self.__csv_file_name = csv_file_name
        self.__master = master
        self.__master["background"] = self.hm.get_gui_color()
        # self.__master.iconbitmap("images/mlread.ico")
        self.__master.title("MLReading")
        self.__master.geometry("500x500")
        self.__master.resizable(0, 0)
        self.__master.update()
        # configure cols and rows
        self.__master.columnconfigure(0, weight=1)
        self.__master.rowconfigure(0, weight=1)
        # menus
        self.__menu = tk.Menu(self.__master)
        # treeview init
        self.__tree = tk.ttk.Treeview(self.__master)
        # labels
        self.__pages_labels = tk.Label(self.__master)
        self.__words_labels = tk.Label(self.__master)
        # entrys
        self.__pages_entry = tk.Entry(self.__master)
        self.__words_entry = tk.Entry(self.__master)
        # init all entry with configuration
        self.entries()
        # time configuration
        self.timerstr = tk.StringVar()
        self.elapsedTime = 0.0
        self.start = 0.0
        # this use boolean for reset,start,pause button
        self.running = False
        # font
        self.TIME_FONT = self.hm.get_gui_timer_font()
        # button size
        self.button_width = self.hm.get_button_width()
        self.button_height = self.hm.get_button_height()
        # get values when the stop
        # :self.__get_time = None
        # size and , current_date
        self.size = None
        # set menu
        self.get_cvs_file()
        # button frame
        self.__frame_button = tk.Frame(self.__master, background="orange red")
        self.__frame_button.configure(width=self.__master.winfo_width())
        self.__frame_button.place(relx=1.5, rely=1.5, anchor=tk.CENTER)
        self.__frame_button.pack()
        self.__frame_button.update()
        self.__frame_supply_button = tk.Frame(self.__master)
        # timer_showing in labels
        self.__label = tk.Label(self.__frame_button, font=self.TIME_FONT, textvariable=self.timerstr, bg="orange red")
        # init button
        self.__play = tk.Button(self.__frame_button, text="Start",
                                height=self.button_height, width=self.button_width,
                                state="disabled",
                                command=lambda: self.handler_start_time())
        self.__stop = tk.Button(self.__frame_button, text="Stop",
                                height=self.button_height, width=self.button_width,
                                state="disabled",
                                command=lambda: self.handler_stop_time())
        self.__reset = tk.Button(self.__frame_button, text="Reset",
                                 height=self.button_height, width=self.button_width,
                                 state="disabled",
                                 command=lambda: self.handler_reset_time())
        self.__add_all = tk.Button(self.__frame_supply_button, text="Enter",
                                   background="green", foreground="white", state="disabled",
                                   command=lambda: self.handler_apply_time())
        # init gui and shows
        self.make_gui()
        self.__master.mainloop()

    ######################################################
    # create menu bar for csv file open
    ######################################################
    def open_file(self):
        # open folder in mlread gui
        self.__master.getFile = tk.filedialog.askopenfilename(initialdir="",
                                                              title="select file",
                                                              filetypes=(("csv files", "*.csv"), "all files"))

    def ask_quit(self):
        if mb.askokcancel("Quit", "You want to quit now?"):
            self.__master.destroy()

    def quit_gui(self):
        self.__master.quit()

    # the first method we will calling the objects
    def get_cvs_file(self):
        # set file menu
        file_menu = tk.Menu(self.__menu)
        # getting file open
        file_menu.add_cascade(label="Open CSV FILE", command=self.open_file)
        # exit the program
        self.__menu.add_cascade(label="File", menu=file_menu)
        # TODO: will be added About menu
        # self.menu.add_cascade(label="About",command= )
        self.__menu.add_cascade(label="Exit", command=self.ask_quit)
        # with subtitle menu
        self.__master.config(menu=file_menu)
        # main menu
        self.__master.config(menu=self.__menu)

    ######################################################
    # dialog box init
    ######################################################
    def show_message(self):
        mb.showinfo("Success!", "New data is saved to:{}".format(self.size))

    def delete_values(self, get_data):
        v_time_id = get_data[0]
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
        df = pd.read_csv(self.__csv_file_name)
        # delete values from columns variable
        indexNames = df[df['time_id'] == num_of_delete].index
        df.drop(indexNames, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(self.__csv_file_name, index=False)

    def df_current_date(self):
        return datetime.date.today()

    def df_size(self):
        df = pd.read_csv(self.__csv_file_name)
        return len(df['time_id']), df

    def update_header(self):
        df = pd.read_csv(self.__csv_file_name)
        df.set_index("time_id", inplace=True)

    # add new data
    def save_data_to_csv(self, time, words, page):
        self.size, df = self.df_size()
        cur_date = self.df_current_date()
        # remove duplicated variable
        for i in df['time_id']:
            if self.size == i:
                self.size -= 1
                if self.size == i:
                    self.size += 2
        fields = [self.size, time, cur_date, str(self.hm.calculate_wpm()),  words, page]
        with open(self.__csv_file_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    ######################################################
    #  callbacks
    ######################################################
    # timer callback method with trace
    def trace_callback_method(self, *args):
        if self.running:
            # timerstr return string values
            type_of_seconds = self.timerstr.get().split(":")
            # there is the calculation error here
            #sum_of_seconds = (int(type_of_seconds[0]) * 60 * 60) + (int(type_of_seconds[1]) * 60) + (
                #int(type_of_seconds[2]))
            # information for type_fo_seconds[2] miliseconds so it does not multiply 60
            sum_of_seconds = (int(type_of_seconds[0])* 60) + (int(type_of_seconds[1]))
            #print("type-1: {}, type-2: {} , type_3:{}".format(type_of_seconds[0],type_of_seconds[1],type_of_seconds[2]));
            #print("sum_of_seconds: {}".format(sum_of_seconds))
            self.hm.set_seconds(sum_of_seconds)
            self.hm.set_get_time(self.timerstr.get())

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
        self.__play.pack(side=tk.LEFT)

    ######################################################
    # pause time row-1 colunm-0
    ######################################################
    def handler_reset_time(self):
        # time start with boolean for second start will not be running
        self.start = time.time()
        self.elapsedTime = 0.0
        self.set_time(self.elapsedTime)
        self.__play["state"] = "disabled"
        self.__stop["state"] = "disabled"
        self.__words_entry.delete(0,'end')
        self.__pages_entry.delete(0,'end')
        self.__words_entry.focus()
        self.__reset["state"] = "disabled"
        self.__pages_entry["state"] = "disabled"
        self.__add_all["state"] ="disabled"

    def reset_time(self):
        self.__reset.pack(side=tk.LEFT)

    ######################################################
    # stop time row-1 column-2
    ######################################################
    def handler_stop_time(self):
        # time start with boolean for second start will not be running
        if self.running:
            # self._timer is value in update() function that stop the timer
            self.__master.after_cancel(self._timer)
            self.elapsedTime = time.time() - self.start
            self.set_time(self.elapsedTime)
            self.running = False
            self.__play["state"] ="disabled"
            self.__stop["state"] = "disabled"
            self.__add_all["state"] ="normal"

    def stop_time(self):
        self.__stop.pack(side=tk.LEFT)

    ######################################################
    # apply all data
    ######################################################
    def handler_apply_time(self):
        # save file
        self.save_data_to_csv(self.hm.get_get_time(), self.hm.get_words_count(), self.hm.get_page_count())
        self.update_header()
        self.update_table_gui(False)
        self.show_message()

    def supply_to_pandas(self):
        self.__add_all.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.__add_all.pack(expand=False, fill="both")

    #################################################################################################################
    ######################################################
    # create time
    ######################################################
    def set_time(self, elap_time):
        minutes = int(elap_time / 60)
        seconds = int(elap_time - minutes * 60.0)
        hseconds = int((elap_time - minutes * 60.0 - seconds) * 100)
        self.timerstr.trace("w", self.trace_callback_method)
        self.timerstr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    ######################################################
    # create timer and shows gui
    ######################################################
    def create_timer(self):
        self.__label.config(anchor=tk.CENTER)
        self.set_time(self.elapsedTime)
        self.__label.pack(fill=tk.X, side=tk.TOP)

    ######################################################
    # update time  on label(stopwatch)
    ######################################################
    def update(self):
        self.elapsedTime = time.time() - self.start
        self.set_time(self.elapsedTime)
        self._timer = self.__master.after(50, self.update)

    ######################################################
    # create just csv header
    ######################################################
    def create_header_for_csv(self):
        # create just heqader for columns
        headers_getting = ()
        df = pd.read_csv(self.__csv_file_name, nrows=1)
        for i in range(0, len(df.columns)):
            self.__tree["columns"] = (df.columns[i])
            self.__tree.heading("#0", text="Name", anchor=tk.W)
            self.__tree.heading(str(df.columns[i]), text=str(df.columns[i]), anchor=tk.W)

    ######################################################
    # create csv filename
    ######################################################
    def create_csv_ongui(self):
        getting_values = []
        # insert values to csv file
        with open(self.__csv_file_name, newline="") as file:
            reader = csv.reader(file)
            # skip header
            next(reader)
            for i, val in enumerate(reader):
                if len(val) > 0:
                    getting_values.append(val)
            for i in range(0, len(getting_values)):
                self.__tree.insert("", i, text="{}".format(getting_values[i][0]),
                                   values=(getting_values[i][0],
                                           getting_values[i][1],
                                           getting_values[i][2],
                                           getting_values[i][3],
                                           getting_values[i][4],
                                           getting_values[i][5]))

    # gui update at desired location
    def update_table_gui(self, get_if_update):
        if get_if_update:
            self.create_csv_ongui()
        else:
            for i in self.__tree.get_children():
                self.__tree.delete(i)
            self.create_csv_ongui()

    ######################################################
    # button frame
    ######################################################

    def frame_for_button(self):
        # create timer button
        self.create_timer()
        # buttons
        self.reset_time()
        self.start_time()
        self.stop_time()

        # create supply button
        self.__frame_supply_button.pack(fill="both", expand=True)
        self.supply_to_pandas()

    ######################################################
    # update canvas
    ######################################################
    def delete_values_data(self, event):
        # get item for removing
        item = self.__tree.selection()[0]
        values = self.__tree.item(item).get("values")
        self.delete_values(values)

    def m_selection(self, event):
        self.__tree.focus()
        if len(self.__tree.selection()) > 0:
            item = self.__tree.selection()[0]

    def frame_canvas(self):
        self.scrollbar = tk.Scrollbar(self.__master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.__tree["columns"] = ("time_id", "time", "date", "wpm", "words", "pages")
        self.__tree.heading("time_id", text="id", anchor=tk.W)
        self.__tree.heading("time", text="time", anchor=tk.W)
        self.__tree.heading("date", text="date", anchor=tk.W)
        self.__tree.heading("wpm", text="wpm", anchor=tk.W)
        self.__tree.heading("pages", text="pages", anchor=tk.W)
        self.__tree.heading("words", text="words", anchor=tk.W)
        self.__tree.column("time_id", width=2)
        self.__tree.column("time", width=40)
        self.__tree.column("date", width=50)
        self.__tree.column("wpm", width=20)
        self.__tree.column("words", width=20)
        self.__tree.column("pages", width=20)
        self.update_table_gui(True)
        # not delete this, it remove #0 id columns in tkinter
        self.__tree["show"] = " headings"

        # configuretion and callback
        self.__tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.__tree.yview)
        self.__tree.bind("<Double-1>", self.delete_values_data)
        self.__tree.bind("<Button-1>", self.m_selection)
        self.__tree.pack(side=tk.TOP, fill=tk.X)

    ######################################################
    # create entry section for words and pages
    ######################################################
    def toggle_state(self, *_):
       #print(self.__words_entry.get())
       print("grep the words")

    def words_onclick(self, x):
        if len(self.__words_entry.get()) == 0:
            pass
        else:
            #print("here is the words entry", self.__words_entry.get())
            self.hm.set_words_count(self.__words_entry.get())
            self.__pages_entry["state"] = "normal"
            self.__pages_entry.focus()

    def pages_onclick(self, x):
        if len(self.__pages_entry.get()) == 0:
            pass
        else:
            self.hm.set_page_count(self.__pages_entry.get())
            # button clicked
            self.__play["state"] = "normal"
            self.__stop["state"] = "normal"
            self.__reset["state"] = "normal"
            self.__add_all["state"] = "normal"

    def entries(self):

        # pages entry disabled while pages button is not empty
        self.__pages_entry["state"] = "disabled"

        self.__words_entry.bind("<Return>", self.words_onclick)
        # label creating
        self.__words_labels["background"] = self.hm.get_gui_color()
        self.__words_labels["foreground"] = self.hm.gui_color_text()

        self.__words_labels["text"] = "Please, insert words count then press Enter!"
        self.__words_labels.pack(fill="both", expand=True)
        self.__words_entry.configure(justify="center")
        self.__words_entry.pack(fill="both", expand=True)

        self.__pages_labels["background"] = "orange red"
        self.__pages_labels["foreground"] = "white"
        self.__pages_labels["text"] = " Please, Enter the Pages Count"
        self.__pages_labels.pack(fill="both", expand=True)
        self.__pages_entry.configure(justify="center")
        self.__pages_entry.pack(fill="both", expand=True)
        self.__pages_entry.bind("<Return>", self.pages_onclick)

    ######################################################
    # create graphic ui with widget
    ######################################################
    def make_gui(self):
        # create entrys for pages and words
        # all functions are here.
        self.frame_for_button()
        self.frame_canvas()
