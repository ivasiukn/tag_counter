
class Tag:

    def __init__(self, name, attributes, value, has_end_tag):
        self.name = name
        self.attributes = attributes
        self.value = value
        self.has_end_tag = has_end_tag

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is str:
            self.__name = name
        else:
            raise TypeError("unsupported parameter type for name: '{}'. Name can be only: 'str'.".format(type(name)))


    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes):
        if type(attributes) is list:
            if all(isinstance(item, tuple) for item in attributes):
                self.__attributes = attributes
            else:
                raise TypeError("unsupported parameter type for item(s) in attributes. All items can be only: 'tuple'.")
        else:
            raise TypeError("unsupported type for parameter 'attributes'. 'attributes' can be only: 'list'.")


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        # TODO: Tag.value validation
        self.__value = value


    @property
    def has_end_tag(self):
        return self.__has_end_tag

    @has_end_tag.setter
    def has_end_tag(self, has_end_tag):
        if type(has_end_tag) is bool:
            self.__has_end_tag = has_end_tag
        else:
            raise TypeError("unsupported type for parameter 'has_end_tag'. 'has_end_tag' can be only: 'bool'.")

