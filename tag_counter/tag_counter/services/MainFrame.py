import tkinter
import sys
import getopt
import logging
import tkinter
from time import strftime, localtime
from tkinter.messagebox import showwarning
from tag_counter.services.SiteAuditor import SiteAuditor
from tag_counter.services.AliasManager import AliasManager
from tag_counter.services.SQLiteManager import SQLiteManager



alias_manager = AliasManager()

logger = logging.getLogger("file_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("tag_counter.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s: %(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MainFrame(tkinter.Frame):
    #site_entry = None
    #l3 = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Tag Counter")
        self.master.geometry("850x300")
        self.master.bind('<Return>', self.__audit_site)
        self.pack(expand=True, fill="both")
        self.__create_widgets()

    def __create_widgets(self):
        f1 = tkinter.Frame(self)
        f1.pack(side="top", fill="x")

        web_site_lable = tkinter.Label(f1, text="Web site:")
        web_site_lable.pack(side="left", anchor="n")

        self.site_entry = tkinter.Entry(f1, exportselection=0)
        self.site_entry.pack(side="left", anchor="nw", fill="x", expand=True)

        f2 = tkinter.Frame(self)
        f2.pack(side="top", fill="x")

        f2_1 = tkinter.Frame(f2)
        f2_2 = tkinter.Frame(f2)

        f2_1.grid(row=0, column=0, sticky="nsew")
        f2_2.grid(row=0, column=1, sticky="nsew")

        f2.grid_columnconfigure(0, weight=1, uniform="group1")
        f2.grid_columnconfigure(1, weight=1, uniform="group1")
        f2.grid_rowconfigure(0, weight=1)

        b1 = tkinter.Button(f2_1, text="DOWNLOAD", bg="light gray", command=self.__audit_site)
        b1.pack(expand=True, fill="both")

        b2 = tkinter.Button(f2_2, text="SHOW FROM DATABASE", bg="light gray", command=self.__show_audit_from_db)
        b2.pack(expand=True, fill="both")


        self.audit_date_frame = tkinter.Frame(self, bd=10)
        self.audit_date_frame.pack(side="top", fill="x")

        self.audit_date_label = tkinter.Label(self.audit_date_frame, text="")
        self.audit_date_label.pack(side="left", anchor="n")




        # Frame with tags statistics
        self.stats_frame = tkinter.Frame(self)
        self.stats_frame.pack(side="top", fill="x")

        self.total_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.total_tags_frame.grid(row=0, column=0, sticky="nsew")
        self.total_tags_label_1 = tkinter.Label(self.total_tags_frame, bd=3, bg="light gray", text="Total tags")
        self.total_tags_label_1.pack(side="top", fill="x", expand=True)
        self.total_tags_label_2 = tkinter.Label(self.total_tags_frame, bd=3, text="")
        self.total_tags_label_2.pack(side="top", fill="x", expand=True)

        self.start_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.start_tags_frame.grid(row=0, column=1, sticky="nsew")
        self.start_tags_label_1 = tkinter.Label(self.start_tags_frame, bd=3, text="Start tags")
        self.start_tags_label_1.pack(side="top", fill="x", expand=True)
        self.start_tags_label_2 = tkinter.Label(self.start_tags_frame, bd=3, text="")
        self.start_tags_label_2.pack(side="top", fill="x", expand=True)

        self.end_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.end_tags_frame.grid(row=0, column=2, sticky="nsew")
        self.end_tags_label_1 = tkinter.Label(self.end_tags_frame, bd=3, text="End tags")
        self.end_tags_label_1.pack(side="top", fill="x", expand=True)
        self.end_tags_label_2 = tkinter.Label(self.end_tags_frame, bd=3, text="")
        self.end_tags_label_2.pack(side="top", fill="x", expand=True)

        self.empty_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.empty_tags_frame.grid(row=0, column=3, sticky="nsew")
        self.empty_tags_label_1 = tkinter.Label(self.empty_tags_frame, bd=3, text="Empty tags")
        self.empty_tags_label_1.pack(side="top", fill="x", expand=True)
        self.empty_tags_label_2 = tkinter.Label(self.empty_tags_frame, bd=3, text="")
        self.empty_tags_label_2.pack(side="top", fill="x", expand=True)

        self.comment_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.comment_tags_frame.grid(row=0, column=4, sticky="nsew")
        self.comment_tags_label_1 = tkinter.Label(self.comment_tags_frame, bd=3, text="Comment_tags")
        self.comment_tags_label_1.pack(side="top", fill="x", expand=True)
        self.comment_tags_label_2 = tkinter.Label(self.comment_tags_frame, bd=3, text="")
        self.comment_tags_label_2.pack(side="top", fill="x", expand=True)

        self.doctype_declaration_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.doctype_declaration_tags_frame.grid(row=0, column=5, sticky="nsew")
        self.doctype_declaration_tags_label_1 = tkinter.Label(self.doctype_declaration_tags_frame, bd=3, text="Doctype declaration tags")
        self.doctype_declaration_tags_label_1.pack(side="top", fill="x", expand=True)
        self.doctype_declaration_tags_label_2 = tkinter.Label(self.doctype_declaration_tags_frame, bd=3, text="")
        self.doctype_declaration_tags_label_2.pack(side="top", fill="x", expand=True)

        self.unknown_declaration_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.unknown_declaration_tags_frame.grid(row=0, column=6, sticky="nsew")
        self.unknown_declaration_tags_label_1 = tkinter.Label(self.unknown_declaration_tags_frame, bd=3, text="Unknown declaration tags")
        self.unknown_declaration_tags_label_1.pack(side="top", fill="x", expand=True)
        self.unknown_declaration_tags_label_2 = tkinter.Label(self.unknown_declaration_tags_frame, bd=3, text="")
        self.unknown_declaration_tags_label_2.pack(side="top", fill="x", expand=True)

        self.process_tags_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.process_tags_frame.grid(row=0, column=7, sticky="nsew")
        self.process_tags_label_1 = tkinter.Label(self.process_tags_frame, bd=3, text="Process tags")
        self.process_tags_label_1.pack(side="top", fill="x", expand=True)
        self.process_tags_label_2 = tkinter.Label(self.process_tags_frame, bd=3, text="")
        self.process_tags_label_2.pack(side="top", fill="x", expand=True)

        self.html_data_count_frame = tkinter.Frame(self.stats_frame, highlightthickness=1, highlightbackground="gray")
        self.html_data_count_frame.grid(row=0, column=8, sticky="nsew")
        self.html_data_count_label_1 = tkinter.Label(self.html_data_count_frame, bd=3, bg="light gray", text="Tags with content")
        self.html_data_count_label_1.pack(side="top", fill="x", expand=True)
        self.html_data_count_label_2 = tkinter.Label(self.html_data_count_frame, bd=3, text="")
        self.html_data_count_label_2.pack(side="top", fill="x", expand=True)

        #self.stats_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(2, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(3, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(4, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(5, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(6, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(7, weight=1, uniform="group1")
        #self.stats_frame.grid_columnconfigure(8, weight=1, uniform="group1")
        #self.stats_frame.grid_rowconfigure(0, weight=1)







        self.f4 = tkinter.Frame(self)
        self.f4.pack(side="bottom", fill="x")

        self.l4_1 = tkinter.Label(self.f4, text="Status: ")
        self.l4_1.pack(side="left", anchor="n")

        self.l4_2 = tkinter.Label(self.f4)
        self.l4_2.pack(side="left", fill="x", expand=True, anchor="w")



    def __audit_site(self, event=None):
        self.url = self.site_entry.get()

        if self.url.strip():

            try:
                if alias_manager.get_alias(self.url) is not None:
                    self.url = alias_manager.get_alias(self.url)

                if not self.url.startswith("http"):
                    self.url = "http://{}".format(self.url)
                    self.site_entry.delete(0, "end")
                    self.site_entry.insert(0, self.url)

                self.site_entry.delete(0, "end")
                self.site_entry.insert(0, self.url)

                audit_date = strftime("%Y-%m-%d %H:%M:%S %z", localtime())
                site_name = None
                db_manager = None

                try:
                    db_manager = SQLiteManager()
                except Exception as e:
                    logger.exception("Something went wrong while creating connection to the database.\n{}".format(str(e)))

                site_auditor = SiteAuditor(self.url)

                self.__print_tag_stats(audit_date, site_auditor.get_tag_statistics())

                begin_index = self.url.find("://")
                if begin_index == -1:
                    begin_index = 0
                else:
                    begin_index += 3

                end_index = self.url.find("/", begin_index)
                if end_index == -1:
                    end_index = self.url.find("?", begin_index)

                if end_index == -1:
                    site_name = self.url[begin_index:]
                else:
                    site_name = self.url[begin_index:end_index]


                if db_manager is not None:
                    db_manager.save_audit_statistics(self.url, site_name, audit_date, site_auditor.get_tag_statistics())
                    logger.info("{}, check web site - success.".format(self.url))
                    self.l4_1["bg"] = "green"
                    self.l4_2["bg"] = "green"
                    self.l4_2["text"] = "Success. Site statistics were saved to the database."
                else:
                    logger.info("{}, check web site - success.".format(self.url))
                    self.l4_1["bg"] = "yellow"
                    self.l4_2["bg"] = "yellow"
                    self.l4_2["text"] = "Site statistics were reached successfully, but were not saved to the database." \
                                        " Problem with creating a connection to the database." \
                                        " See logs for details."

            except Exception as e:
                self.l4_1["bg"] = "red"
                self.l4_2["bg"] = "red"
                self.l4_2["text"] = "Fail. {}".format(str(e))
                logger.exception("{}, check web site - fail.\n{}".format(self.url, str(e)))

        else:
            showwarning(title='Tag Counter', message='Empty web site url. Enter some url into "Web site" field.')




    def __show_audit_from_db(self, event=None):
        self.url = self.site_entry.get()

        if self.url.strip():

            try:
                if alias_manager.get_alias(self.url) is not None:
                    self.url = alias_manager.get_alias(self.url)

                if not self.url.startswith("http"):
                    self.url = "http://{}".format(self.url)
                    self.site_entry.delete(0, "end")
                    self.site_entry.insert(0, self.url)

                db_manager = None

                try:
                    db_manager = SQLiteManager()
                except Exception as e:
                    logger.exception("Something went wrong while creating connection to the database.\n{}".format(str(e)))

                audit_info = db_manager.get_audit_statistics(self.url)

                if audit_info is not None:
                    self.__print_tag_stats(audit_info["audit_date"], audit_info["audit_stats"])
                    logger.info("{}, check database - success.".format(self.url))
                    self.l4_1["bg"] = "green"
                    self.l4_2["bg"] = "green"
                    self.l4_2["text"] = "Success. Data successfully retrieved from the database."
                else:
                    self.l4_1["bg"] = "yellow"
                    self.l4_2["bg"] = "yellow"
                    self.l4_2["text"] = "There are no information in the database. Use \"DOWNLOAD\" button to check the real web site"

            except Exception as e:
                self.l4_1["bg"] = "red"
                self.l4_2["bg"] = "red"
                self.l4_2["text"] = "Fail. {}".format(str(e))
                logger.exception("{}, get info from database - fail.\n{}".format(self.url, str(e)))

        else:
            showwarning(title='Tag Counter', message='Empty web site url. Enter some url into "Web site" field.')


    def __print_tag_stats(self, audit_date, tag_stats):
        self.audit_date_label["text"] = "Audit date:   {}".format(audit_date)

        self.total_tags_label_2["text"] = str(tag_stats["start_tags"] + tag_stats["end_tags"] + tag_stats["empty_tags"]
                                  + tag_stats["comment_tags"] + tag_stats["doctype_declaration_tags"]
                                  + tag_stats["unknown_declaration_tags"] + tag_stats["process_tags"])
        self.start_tags_label_2["text"] = str(tag_stats["start_tags"])
        self.end_tags_label_2["text"] = str(tag_stats["end_tags"])
        self.empty_tags_label_2["text"] = str(tag_stats["empty_tags"])
        self.comment_tags_label_2["text"] = str(tag_stats["comment_tags"])
        self.doctype_declaration_tags_label_2["text"] = str(tag_stats["doctype_declaration_tags"])
        self.unknown_declaration_tags_label_2["text"] = str(tag_stats["unknown_declaration_tags"])
        self.process_tags_label_2["text"] = str(tag_stats["process_tags"])
        self.html_data_count_label_2["text"] = str(tag_stats["html_data_count"])
