
class Helper_Model: 
    def __init__(self): 
        # current time that user stopped
        self.__time = time
        self.__time_id = time_id
        self.__date = date
        self.__wpm = 0
        self.__page = 0
        self.__words = 0 
        self.__words_entry_check = False
        self.__page_entry_check = False

    def set_page_count(self, page_count):
        self.__page = page_count
    def get_page_count(self):
        return.__page
    def set_words_count(self,word_count):
        self.__words = word_count
    def get_words_count(self):
        return self.__words

        

