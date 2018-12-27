import os
import yaml
from tag_counter.services.Singleton import Singleton


class AliasManager(Singleton):
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
        if alias is None:
            raise AttributeError("parameter [alias] can not be 'None'. It must be not empty 'str'.")
        else:
            if type(alias) is not str:
                raise TypeError("unsupported type for parameter [alias]: '{}'. Only 'str' allowed.".format(type(alias)))
            else:
                if alias.strip() == "":
                    raise AttributeError("parameter [alias] can not be empty or consist only of whitespaces. It must be not empty 'str'.")


        if url is None:
            raise AttributeError("parameter [url] can not be 'None'. It must be not empty 'str'.")
        else:
            if type(url) is not str:
                raise TypeError("unsupported type for parameter [url]: '{}'. Only 'str' allowed.".format(type(url)))
            else:
                if url.strip() == "":
                    raise AttributeError("parameter [url] can not be empty or consist only of whitespaces. It must be not empty 'str'.")


        if alias not in self.__aliases_dict.keys():
            with open(self.__file_name, "a") as aliases_file:
                aliases_file.write("\r\n{}: {}\r\n".format(alias, url))
                self.__aliases_dict[alias] = url
        else:
            self.__update_alias(alias, url)


    def __update_alias(self, alias, new_url):
        with open(self.__file_name, "w") as aliases_file:
            self.__aliases_dict[alias] = new_url
            yaml.dump(self.__aliases_dict, aliases_file, default_flow_style=False)


    def read_aliases(self):
        if os.stat(self.__file_name).st_size != 0:
            with open(self.__file_name, "r") as aliases_file:
                self.__aliases_dict = yaml.load(aliases_file)


    def reload_aliases(self):
        self.read_aliases()
