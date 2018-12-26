import sqlite3
import pickle
from tag_counter.services.Singleton import Singleton


class SQLiteManager(Singleton):
    __database_name = "tag_counter.db"

    # I planed to extend usage of the database at the beginning. Now tables tag_types, tag_list and tag_attributes are useless
    # A half of columns in site_audits are also useless
    # no time to delete all useless code
    __site_audits_ddl = "create table site_audits ("\
                                "audit_id integer primary key"\
                                ",site_name text not null"\
                                ",site_url text not null"\
                                ",audit_date text not null"\
                                ",start_tags integer"\
                                ",end_tags integer"\
                                ",empty_tags integer"\
                                ",comment_tags integer"\
                                ",doctype_declaration_tags integer"\
                                ",unknown_declaration_tags integer"\
                                ",process_tags integer"\
                                ",html_data_count integer"\
                                ",pickled_stats blob);"



    __tag_types_ddl = "create table tag_types ("\
                              "tag_type_id integer primary key"\
                              ",tag_type_name text not null unique"\
                              ",tag_type_desctiption text);"

    # [(<tag type name>, <tag type description>),...]
    __tag_types_list = [("Start Tag", None), ("End Tag", None), ("Html Data", None), ("Empty Tag", None)
                        , ("Comment Tag", None), ("Doctype Declaration Tag", None), ("Unknown Declaration Tag", None)
                        , ("Process Tag", None)]

    __tag_list_ddl = "create table tag_list ("\
                              "tag_id integer primary key"\
                              ",audit_id integer not null"\
                              ",order_number integer not null"\
                              ",tag_type text not null"\
                              ",tag_name text not null"\
                              ",unique(audit_id, order_number)"\
                              ",foreign key(audit_id) references site_audits(audit_id));"

    __tag_attributes_ddl = "create table tag_attributes ("\
                              "attribute_id integer primary key"\
                              ",tag_id integer not null"\
                              ",key text not null"\
                              ",value text null"\
                              ",foreign key(tag_id) references tag_list(tag_id));"



    def __init__(self):
        with sqlite3.connect(self.__database_name) as connection:
            cursor = connection.cursor()

            cursor.execute("select 1 from sqlite_master where type='table' AND name='site_audits';")
            if cursor.fetchone() is None:
                cursor.execute(self.__site_audits_ddl)
            connection.commit()

            cursor.execute("select 1 from sqlite_master where type='table' AND name='tag_types';")
            if cursor.fetchone() is None:
                cursor.execute(self.__tag_types_ddl)
                cursor.executemany("insert into tag_types (tag_type_name, tag_type_desctiption) values(?, ?);", self.__tag_types_list)
            else:
                cursor.execute("delete from tag_types;")
                cursor.executemany("insert into tag_types (tag_type_name, tag_type_desctiption) values(?, ?);", self.__tag_types_list)
            connection.commit()


            cursor.execute("select 1 from sqlite_master where type='table' AND name='tag_list';")
            if cursor.fetchone() is None:
                cursor.execute(self.__tag_list_ddl)
            connection.commit()

            cursor.execute("select 1 from sqlite_master where type='table' AND name='tag_attributes';")
            if cursor.fetchone() is None:
                cursor.execute(self.__tag_attributes_ddl)
            connection.commit()


    def get_tag_types_dict(self):
        tag_types_dict = {}
        with sqlite3.connect(self.__database_name) as connection:
            cursor = connection.cursor()

            for row in cursor.execute("select tag_type_name, tag_type_id from tag_types order by tag_type_id;"):
                tag_types_dict[row[0]] = row[1]

        return tag_types_dict


    def save_audit_statistics(self, site_url, site_neme, audit_date, stats):
        audit_id = None
        pickled_stats = pickle.dumps(stats)

        if type(stats) is not dict:
            raise TypeError("unsupported type for parameter [stats]: '{}'. Only 'dict' allowed.".format(type(stats)))

        row = tuple([site_neme, site_url, audit_date, stats["start_tags"], stats["end_tags"], stats["empty_tags"]
                      , stats["comment_tags"], stats["doctype_declaration_tags"], stats["unknown_declaration_tags"]
                      , stats["process_tags"], stats["html_data_count"], pickled_stats])


        with sqlite3.connect(self.__database_name) as connection:
            cursor = connection.cursor()

            cursor.execute("insert into site_audits (site_name, site_url, audit_date, start_tags, end_tags"
                           ", empty_tags, comment_tags, doctype_declaration_tags, unknown_declaration_tags"
                           ", process_tags, html_data_count, pickled_stats) "
                           "values (?,?,?,?,?,?,?,?,?,?,?,?);", row)

            cursor.execute("SELECT last_insert_rowid();")
            audit_id = cursor.fetchone()[0]

            if audit_id is None or audit_id < 1:
                connection.rollback()
                raise Exception("something went wrong while getting audit_id from the database: audit_id = {}.\nTransaction was rolled back.".format(audit_id))
            else:
                connection.commit()

        return audit_id


    def get_audit_statistics(self, url):
        if type(url) is not str:
            raise TypeError("unsupported type for parameter [url]: '{}'. Only 'str' allowed.".format(type(url)))

        url = url.strip()
        if url == "":
            raise Exception("unsupported value for parameter [url]: \"{}\". Only not empty strings allowed.".format(url))

        with sqlite3.connect(self.__database_name) as connection:
            cursor = connection.cursor()

            cursor.execute("select audit_date, pickled_stats "
                           "from site_audits "
                           "where site_url = ? "
                           "order by audit_id desc "
                           "limit 1;", (url,))

            audit_stats = cursor.fetchone()
            connection.commit()  # just to close the transaction

            if audit_stats is None:
                return None
            else:
                return {"audit_date": audit_stats[0], "audit_stats": pickle.loads(audit_stats[1])}




