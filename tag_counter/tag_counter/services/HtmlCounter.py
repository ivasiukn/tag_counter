from html.parser import HTMLParser
from tag_counter.services.Tags import *


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

    def handle_endtag(self, tag):
        self.tag_list.append(EndTag(tag))

    def handle_startendtag(self, tag, attrs):
        self.tag_list.append(EmptyTag(tag, attrs))

    def handle_data(self, data):
        self.tag_list.append(HtmlData(data))

    def handle_comment(self, data):
        self.tag_list.append(CommentTag(data))

    def handle_decl(self, decl):
        self.tag_list.append(DoctypeDeclarationTag(decl))

    def unknown_decl(self, data):
        self.tag_list.append(UnknownDeclarationTag(data))

    def handle_pi(self, data):
        self.tag_list.append(ProcessTag(data))



