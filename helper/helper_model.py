class Helper_Model:
    def __init__(self):
        #  current time that user stopped
        self.__time = 0
        self.__time_id = 0
        self.__date = 0
        self.__seconds_of_time = 0
        self.__wpm = 0
        self.__page = 0
        self.__words = 0
        self.__words_entry_check = False
        self.__page_entry_check = False
        self.__gui_color = "orange red"
        self.__gui_color_text = "white"
        self.__gui_timer_font = ("Comic Sans MS", "44")
        self.__button_width = 11
        self.__button_height = 1
        self.__get_time = 0

    ##################################################################
    def calculate_wpm(self):
        return int((int(self.__words) / int(self.__seconds_of_time)) * 60)

    def set_seconds(self, seconds):
        self.__seconds_of_time = seconds

    def get_get_time(self):
        return self.__get_time

    def set_get_time(self, stop_time_get):
        self.__get_time = stop_time_get

    def gui_color_text(self):
        return self.__gui_color_text

    def get_button_width(self):
        return self.__button_width

    def get_button_height(self):
        return self.__button_height

    def set_page_count(self, page_count):
        self.__page = page_count

    def get_page_count(self):
        return self.__page

    def set_words_count(self, word_count):
        self.__words = word_count

    def get_words_count(self):
        return self.__words

    def get_gui_color(self):
        return self.__gui_color

    def get_gui_timer_font(self):
        return self.__gui_timer_font
