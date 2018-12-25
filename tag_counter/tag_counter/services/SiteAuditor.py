import sys
import getopt
import socket
from urllib import request, error
from tag_counter.HtmlCounter import HTMLCounter
from tag_counter.Tags import *


class SiteAuditor:

    __site_url = None
    __tag_list = None
    __tag_stats = None


    def __init__(self, site_url):

        if site_url is not str:
            raise TypeError("unsupported type for parameter [site_url]: '{}'. Only 'str' allowed.".format(type(site_url)))

        site_url = site_url.strip()

        if site_url is None or site_url == "":
            raise Exception("parameter [site_url] is None, empty or consists of whitespaces.")

        self.__site_url = site_url
        if not self.__site_url.startswith("http"):
            self.__site_url = "http://{}".format(site_url)


        self.__get_tag_list_by_url()
        self.__calculate_statistics()


    def get_tag_list(self):
        return self.__tag_list

    def get_tag_statistics(self):
        return self.__tag_stats

    def refresh_audit(self):
        self.__get_tag_list_by_url()
        self.__calculate_statistics()


    def __get_tag_list_by_url(self):
        # EXAMPLE: http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm
        try:
            response = request.urlopen(self.__site_url)
            content = response.read()
            html_counter = HTMLCounter()
            html_counter.feed(content.decode("utf-8"))
            self.__tag_list = html_counter.tag_list
        except error.HTTPError as e:
            print("The server couldn\'t fulfill the request. HTTP response code: ".format(str(e.code)))
        except error.URLError as e:
            print("Failed to reach a server. Reason: ".format(str(e.reason)))


    def __calculate_statistics(self):

        if len(self.__tag_list > 0):
            self.__tag_stats = {"start_tags": 0,
                                "end_tags": 0,
                                "empty_tags": 0,
                                "comment_tags": 0,
                                "doctype_declaration_tags": 0,
                                "unknown_declaration_tags": 0,
                                "process_tags": 0,
                                "html_data_count": 0}

        for tag in self.__tag_list:
            if type(tag) is StartTag:
                self.__tag_stats["start_tags"] += 1
            elif type(tag) is EndTag:
                self.__tag_stats["end_tags"] += 1
            elif type(tag) is EmptyTag:
                self.__tag_stats["empty_tags"] += 1
            elif type(tag) is CommentTag:
                self.__tag_stats["comment_tags"] += 1
            elif type(tag) is DoctypeDeclarationTag:
                self.__tag_stats["doctype_declaration_tags"] += 1
            elif type(tag) is UnknownDeclarationTag:
                self.__tag_stats["unknown_declaration_tags"] += 1
            elif type(tag) is ProcessTag:
                self.__tag_stats["process_tags"] += 1
            elif type(tag) is HtmlData:
                self.__tag_stats["html_data_count"] += 1
