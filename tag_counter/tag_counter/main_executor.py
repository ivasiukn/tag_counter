import sys
import getopt
import socket
from urllib import request, error
from tag_counter.HtmlCounter import HTMLCounter
from tag_counter.Tags import *
from tag_counter.services.AliasManager import AliasManager

socket.setdefaulttimeout(5)
alias_manager = AliasManager()


def main():
    try:
        commands, arguments = getopt.getopt(sys.argv[1:], "hg:v:a:p", ["help", "get=", "view=", "alias=" "print"])
        process_commands(dict(commands))
    except getopt.GetoptError as e:
        # TODO a nice warning
        print("Wrong usage: {}\n".format(e.msg))
        show_help_page()
        # raise e
    except Exception as e:
        # TODO Unknown exception handling
        raise e



def process_commands(commands):
    url = None
    alias = None
    print_tag_list = False

    if "-g" in commands.keys():
        url = commands["-g"]

    if "--get" in commands.keys():
        url = commands["--get"]

    if "-p" in commands.keys():
        print_tag_list = True

    if "--print" in commands.keys():
        print_tag_list = True

    if "-a" in commands.keys():
        alias = commands["-a"]

    if "--alias" in commands.keys():
        alias = commands["--alias"]



    if alias is not None:
        if url is not None:
            alias_manager.add_alias(alias, url)
        else:
            add_alias_manually(alias)

    if url is not None:
        get_html_by_url(url, print_tag_list)



def add_alias_manually(alias):
    url = input("Enter url for alias '{}':".format(alias))
    alias_manager.add_alias(alias, url)


def show_help_page():
    # TODO a good help page
    print("usage: tag_counter <command> <option>")
    print("commands:")
    print("-h (--help): show help page")
    print("-g (--get): count tags by url")
    print("-v (--view): get information about a site from the database by url")
    print("-p (--print): whether to print the list of tags of not")


def get_html_by_url(url, print_the_list):
    # EXAMPLE: http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm

    try:
        if alias_manager.get_alias(url) is not None:
            url = alias_manager.get_alias(url)

        if not url.startswith("http"):
            url = "http://{}".format(url)

        response = request.urlopen(url)
        content = response.read()
        html_counter = HTMLCounter()
        html_counter.feed(content.decode("utf-8"))
        tag_list = html_counter.tag_list

        if print_the_list:
            for tag in tag_list:
                print(tag)
            print("\n\n**********  RESULTS  **********")

        start_tags = 0
        end_tags = 0
        empty_tags = 0
        comment_tags = 0
        doctype_declaration_tags = 0
        unknown_declaration_tags = 0
        process_tags = 0
        html_data_count = 0

        for tag in tag_list:
            if type(tag) is StartTag: start_tags += 1
            elif type(tag) is EndTag: end_tags += 1
            elif type(tag) is EmptyTag: empty_tags += 1
            elif type(tag) is CommentTag: comment_tags += 1
            elif type(tag) is DoctypeDeclarationTag: doctype_declaration_tags += 1
            elif type(tag) is UnknownDeclarationTag: unknown_declaration_tags += 1
            elif type(tag) is ProcessTag: process_tags += 1
            elif type(tag) is HtmlData: html_data_count += 1


        print("Total tags: {}".format(start_tags + end_tags + empty_tags + comment_tags + doctype_declaration_tags + unknown_declaration_tags + process_tags))
        print("Start tags: {}".format(start_tags))
        print("End tags: {}".format(end_tags))
        print("Empty tags: {}".format(empty_tags))
        print("Comment tags: {}".format(comment_tags))
        print("Doctype Declaration tags: {}".format(doctype_declaration_tags))
        print("Unknown Declaration tags: {}".format(unknown_declaration_tags))
        print("Process tags: {}".format(process_tags))
        print("Tags with content: {}".format(html_data_count))

    except error.HTTPError as e:
        print("The server couldn\'t fulfill the request. HTTP response code: ".format(str(e.code)))
    except error.URLError as e:
        print("Failed to reach a server. Reason: ".format(str(e.reason)))

