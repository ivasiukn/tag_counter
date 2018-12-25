import sys
import getopt
import socket
from tag_counter.Tags import *
from tag_counter.services.SiteAuditor import SiteAuditor
from tag_counter.services.AliasManager import AliasManager
from tag_counter.services.SQLiteManager import SQLiteManager
from time import strftime, localtime


socket.setdefaulttimeout(5)
alias_manager = AliasManager()


def main():
    try:
        audit_date = strftime("%Y-%m-%d %H:%M:%S %z", localtime())
        site_name = None
        db_manager = None

        try:
            db_manager = SQLiteManager()
        except Exception as e:
            print("Something went wrong while creating connection to the database. Data won't be saved to the database.")
            print("See error message:")
            print(str(e))


        commands, arguments = getopt.getopt(sys.argv[1:], "hg:v:a:p", ["help", "get=", "view=", "alias=" "print"])
        properties = process_commands(dict(commands))

        site_auditor = SiteAuditor(properties["url"])

        if properties["print_tag_list"]:
            print_tag_list(site_auditor.get_tag_list())

        print_tag_stats(site_auditor.get_tag_statistics())


        begin_index = properties["url"].find("://") + 3
        end_index = properties["url"].find("/", begin_index)

        if end_index == -1:
            end_index = properties["url"].find("?", begin_index)

        if end_index == -1:
            site_name = properties["url"][begin_index:]
        else:
            site_name = properties["url"][begin_index:end_index]

       # db_manager.







    except getopt.GetoptError as e:
        # TODO a nice warning
        print("Wrong usage: {}\n".format(e.msg))
        show_help_page()
        # raise e
    except Exception as e:
        # TODO Unknown exception handling
        raise e



def process_commands(commands):
    properties = {"url": None, "print_tag_list": False}
    alias = None

    if "-g" in commands.keys():
        properties["url"] = commands["-g"]

    if "--get" in commands.keys():
        properties["url"] = commands["--get"]

    if "-p" in commands.keys():
        properties["print_tag_list"] = True

    if "--print" in commands.keys():
        properties["print_tag_list"] = True

    if "-a" in commands.keys():
        alias = commands["-a"]

    if "--alias" in commands.keys():
        alias = commands["--alias"]



    if alias is not None:
        if properties["url"] is not None:
            alias_manager.add_alias(alias, properties["url"])
        else:
            add_alias_manually(alias)

    if properties["url"] is not None:
        if alias_manager.get_alias(properties["url"]) is not None:
            properties["url"] = alias_manager.get_alias(properties["url"])

    return properties



def print_tag_list(tag_list):
    if tag_list is not None:
        print("\nList of tags:\n")
        for tag in tag_list:
            print(tag)



def print_tag_stats(tag_stats):
    print()
    print("Total tags: {}".format(tag_stats["start_tags"] + tag_stats["end_tags"] + tag_stats["empty_tags"]
                                  + tag_stats["comment_tags"] + tag_stats["doctype_declaration_tags"]
                                  + tag_stats["unknown_declaration_tags"] + tag_stats["process_tags"]))
    print("Start tags: {}".format(tag_stats["start_tags"]))
    print("End tags: {}".format(tag_stats["end_tags"]))
    print("Empty tags: {}".format(tag_stats["empty_tags"]))
    print("Comment tags: {}".format(tag_stats["comment_tags"]))
    print("Doctype Declaration tags: {}".format(tag_stats["doctype_declaration_tags"]))
    print("Unknown Declaration tags: {}".format(tag_stats["unknown_declaration_tags"]))
    print("Process tags: {}".format(tag_stats["process_tags"]))
    print("Tags with content: {}".format(tag_stats["html_data_count"]))



def add_alias_manually(self, alias):
        self.site_url = input("Enter url for alias '{}':".format(alias))
        self.alias_manager.add_alias(alias, self.site_url)



def show_help_page():
    # TODO a good help page
    print("usage: tag_counter <command> <option>")
    print("commands:")
    print("-h (--help): show help page")
    print("-g (--get): count tags by url")
    print("-v (--view): get information about a site from the database by url")
    print("-p (--print): whether to print the list of tags of not")


