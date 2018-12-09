from html.parser import HTMLParser
from tag_counter.Tags import *


class HTMLCounter(HTMLParser):
    def __init__(self):
        self.tag_list = []
        super().__init__()

    @property
    def tag_list(self):
        return self.__tag_list

    @tag_list.setter
    def tag_list(self, tag_list):
        self.__tag_list = tag_list


    def handle_starttag(self, tag, attrs):
        self.tag_list.append(StartTag(tag, attrs))

    def handle_data(self, data):
        self.tag_list[-1].content = data


