import os
import yaml

"""
class Singleton(object):
    _instance = None

    def __new__(cls, path, var2):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, path, var2)
        return cls._instance
"""


class AliasManager:
    __file_name = "aliases.yaml"
    __aliases_dict = {}

    def __init__(self):
        try:
            self.read_aliases()
        except FileNotFoundError:
            aliases_file = open(self.__file_name, "w+")
            aliases_file.close()


    def get_alias(self, alias):
        if alias in self.__aliases_dict.keys():
            return self.__aliases_dict[alias]
        else:
            return None


    def get_aliases_dict(self):
        return self.__aliases_dict


    def add_alias(self, alias, url):
        if alias not in self.__aliases_dict.keys():
            with open(self.__file_name, "a") as aliases_file:
                aliases_file.write("{}: {}".format(alias, url))
                self.__aliases_dict[alias] = url
        else:
            self.update_alias(alias, url)


    def update_alias(self, alias, new_url):
        with open(self.__file_name, "w") as aliases_file:
            self.__aliases_dict[alias] = new_url
            yaml.dump(self.__aliases_dict, aliases_file, default_flow_style=False)


    def read_aliases(self):
        if os.stat(self.__file_name).st_size != 0:
            with open(self.__file_name, "r") as aliases_file:
                self.__aliases_dict = yaml.load(aliases_file)


    def reload_aliases(self):
        self.read_aliases()
