import os

"""
class Singleton(object):
    _instance = None

    def __new__(cls, path, var2):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, path, var2)
        return cls._instance
"""


class AliasManager:
    def __init__(self):
        self.path = os.getcwd()


