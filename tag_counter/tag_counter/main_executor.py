import sys
import getopt
import logging
from tag_counter.services.SiteAuditor import SiteAuditor
from tag_counter.services.AliasManager import AliasManager
from tag_counter.services.SQLiteManager import SQLiteManager
from time import strftime, localtime



# logging.basicConfig(filename="tag_counter_log.log", level=logging.DEBUG)
alias_manager = AliasManager()

logger = logging.getLogger("file_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("tag_counter.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s: %(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    try:
        commands, arguments = getopt.getopt(sys.argv[1:], "hg:v:a:p", ["help", "get=", "view=", "alias=", "print"])
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

    if ("-g" in commands.keys() or "--get" in commands.keys()) and ("-v" in commands.keys() or "--view" in commands.keys()):
        show_help_page()
        sys.exit(0)

    get_url = None
    view_url = None
    print_full_tag_list = False
    alias = None


    if "-h" in commands.keys():
        show_help_page()
        sys.exit(0)

    if "--help" in commands.keys():
        show_help_page()
        sys.exit(0)

    if "-g" in commands.keys():
        get_url = commands["-g"]

    if "--get" in commands.keys():
        get_url = commands["--get"]

    if "-v" in commands.keys():
        view_url = commands["-v"]

    if "--view" in commands.keys():
        view_url = commands["--view"]

    if "-p" in commands.keys():
        print_full_tag_list = True

    if "--print" in commands.keys():
        print_full_tag_list = True

    if "-a" in commands.keys():
        alias = commands["-a"]

    if "--alias" in commands.keys():
        alias = commands["--alias"]



    if alias is not None:
        if get_url is not None:
            alias_manager.add_alias(alias, get_url)
        else:
            add_alias_manually(alias)

    if get_url is not None:
        if alias_manager.get_alias(get_url) is not None:
            print("Alias '{}' replaced with '{}'.".format(get_url, alias_manager.get_alias(get_url)))
            get_url = alias_manager.get_alias(get_url)

    if view_url is not None:
        if alias_manager.get_alias(view_url) is not None:
            print("Alias '{}' replaced with '{}'.".format(view_url, alias_manager.get_alias(view_url)))
            view_url = alias_manager.get_alias(view_url)


    # check site or get info from db
    if get_url is not None:
        try:
            audit_site(get_url, print_full_tag_list)
            logger.info("{}, check web site - success.".format(get_url))
        except Exception as e:
            print("An error occurred. See tag_counter.log")
            logger.exception("{}, check web site - fail.\n{}".format(get_url, str(e)))

    if view_url is not None:
        try:
            view_site_audit_from_db(view_url)
            logger.info("{}, check database - success.".format(view_url))
        except Exception as e:
            print("An error occurred. See tag_counter.log")
            logger.exception("{}, get info from database - fail.\n{}".format(view_url, str(e)))




def audit_site(url, print_full_tag_list):
    audit_date = strftime("%Y-%m-%d %H:%M:%S %z", localtime())
    site_name = None
    db_manager = None

    try:
        db_manager = SQLiteManager()
    except Exception as e:
        print("Something went wrong while creating connection to the database. Data won't be saved to the database.")
        print(str(e))

    if not url.startswith("http"):
        url = "http://{}".format(url)

    # main work is done here
    site_auditor = SiteAuditor(url)

    if print_full_tag_list:
        print_tag_list(site_auditor.get_tag_list())

    print_tag_stats(audit_date, site_auditor.get_tag_statistics())

    begin_index = url.find("://")
    if begin_index == -1:
        begin_index = 0
    else:
        begin_index += 3

    end_index = url.find("/", begin_index)
    if end_index == -1:
        end_index = url.find("?", begin_index)

    if end_index == -1:
        site_name = url[begin_index:]
    else:
        site_name = url[begin_index:end_index]

    if db_manager is not None:
        print("\nSaving audit statistics to the database...")
        try:
            # audit_id had to be used in writing data to tag_list table
            audit_id = db_manager.save_audit_statistics(url, site_name, audit_date, site_auditor.get_tag_statistics())
            print("Saved successfully.")
        except Exception as e:
            print("Failed to save audit statistics to the database. Error message:")
            print(str(e))



def view_site_audit_from_db(url):
    db_manager = None

    try:
        db_manager = SQLiteManager()
    except Exception as e:
        print("Something went wrong while creating connection to the database. Can't get information from the database.")
        print("See error message:")
        print(str(e))

    if not url.startswith("http"):
        url = "http://{}".format(url)

    audit_info = db_manager.get_audit_statistics(url)

    if audit_info is not None:
        print("Audition results of {}:".format(url))
        print_tag_stats(audit_info["audit_date"], audit_info["audit_stats"])
    else:
        print("There are no information in the database. Use 'tag_counter --get {}' command to check the real web site".format(url))




def print_tag_list(tag_list):
    if tag_list is not None:
        print("\nList of tags:\n")
        for tag in tag_list:
            print(tag)



def print_tag_stats(audit_date, tag_stats):
    print()
    print("Audit date: {}".format(audit_date))
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



def add_alias_manually(alias):
        site_url = input("Enter url for alias '{}':".format(alias))
        alias_manager.add_alias(alias, site_url)



def show_help_page():
    # TODO a good help page

    help_message = \
        "\nusage: tag_counter <command> <option>" \
        "\ncommands:" \
        "\n-h (--help): show help page (doesn't have any option)" \
        "\n-g (--get): count tags by url (accepts urls and aliases, can't be used with command '--view')" \
        "\n-v (--view): get information about a site from the database by url (accepts urls and aliases, can't be used with command '--get')" \
        "\n-a (--alias): create alias for given url (works only with command '--get')" \
        "\n-p (--print): whether to print the list of tags of not (doesn't have any option)" \
        "\n\nThere is a file with name 'aliases.yaml' somewhere there (in the execution or environment directory, i think)." \
        "\nAll created aliases are stored in that file in this format: <alias>: <url>. " \
        "\nYou can edit it but remember to leave an empty line in the end." \
        "\nLet your God/Gods help you."

    print(help_message)

    # A samurai went on a great battle
    # Demon of laziness was too strong
    # Disappointing...

