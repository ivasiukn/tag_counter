
class StartTag:
    def __init__(self, name, attributes, **kwargs):
        self.name = name
        self.attributes = attributes
        if kwargs.get("content") is not None:
            self.content = kwargs.get("content")
        else:
            self.content = None


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is str:
            if name.strip():
                self.__name = name
            else:
                raise Exception("parameter [name] is empty or consists of whitespaces.")
        else:
            raise TypeError("unsupported type for parameter [name]: '{}'. Only 'str' allowed.".format(type(name)))


    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes):
        if type(attributes) is list:
            if all(isinstance(item, tuple) for item in attributes):
                self.__attributes = attributes
            else:
                raise TypeError("unsupported type for item(s) in [attributes]. All items can be only: 'tuple'.")
        else:
            raise TypeError("unsupported type for parameter [attributes]. Only 'list' allowed.")


    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        try:
            if content is not None:
                str_content = str(content)
                self.__content = str_content
            else:
                self.__content = None
        except Exception:
            raise TypeError("parameter 'value' should be convertible to type 'str'.")


    def __str__(self):
        str_attributes = " ".join("{attr}=\"{val}\"".format(attr=tup[0], val=tup[1]) for tup in self.attributes)
        str_content = ""
        if self.__content is not None: str_content = self.__content
        return "<{name} {attributes}>{content}".format(name=self.name, attributes=str_attributes, content=str_content)





class EndTag:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is str:
            if name.strip():
                self.__name = name
            else:
                raise Exception("parameter [name] is empty or consists of whitespaces.")
        else:
            raise TypeError("unsupported type for parameter [name]: '{}'. Only 'str' allowed.".format(type(name)))

    def __str__(self):
        return "</{name}>".format(name=self.name)





class EmptyTag:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is str:
            if name.strip():
                self.__name = name
            else:
                raise Exception("parameter [name] is empty or consists of whitespaces.")
        else:
            raise TypeError("unsupported type for parameter [name]: '{}'. Only 'str' allowed.".format(type(name)))


    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes):
        if type(attributes) is list:
            if all(isinstance(item, tuple) for item in attributes):
                self.__attributes = attributes
            else:
                raise TypeError("unsupported type for item(s) in attributes. All items can be only: 'tuple'.")
        else:
            raise TypeError("unsupported type for parameter [attributes]. Only 'list' allowed.")


    def __str__(self):
        str_attributes = " ".join("{attr}=\"{val}\"".format(attr=tup[0], val=tup[1]) for tup in self.attributes)
        return "<{name} {attributes}/>".format(name=self.name, attributes=str_attributes)





class CommentTag:
    def __init__(self, comment):
        self.comment = comment

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, comment):
        if type(comment) is str:
            self.__comment = comment
        else:
            raise TypeError("unsupported type for parameter [comment]: '{}'. Only 'str' allowed.".format(type(comment)))

    def __str__(self):
        return "<!--{comment}-->".format(comment=self.comment)





class DoctypeDeclarationTag:
    def __init__(self, declaration):
        self.declaration = declaration

    @property
    def declaration(self):
        return self.__declaration

    @declaration.setter
    def declaration(self, declaration):
        if type(declaration) is str:
            self.__declaration = declaration
        else:
            raise TypeError("unsupported type for parameter [declaration]: '{}'. Only 'str' allowed.".format(type(declaration)))

    def __str__(self):
        return "<!{declaration}>".format(declaration=self.declaration)





class UnknownDeclarationTag:
    def __init__(self, declaration):
        self.declaration = declaration

    @property
    def declaration(self):
        return self.__declaration

    @declaration.setter
    def declaration(self, declaration):
        if type(declaration) is str:
            self.__declaration = declaration
        else:
            raise TypeError("unsupported type for parameter [declaration]: '{}'. Only 'str' allowed.".format(type(declaration)))

    def __str__(self):
        return "<!{declaration}>".format(declaration=self.declaration)





class ProcessTag:
    def __init__(self, process):
        self.process = process

    @property
    def process(self):
        return self.__process

    @process.setter
    def process(self, process):
        if type(process) is str:
            self.__process = process
        else:
            raise TypeError("unsupported type for parameter [process]: '{}'. Only 'str' allowed.".format(type(process)))

    def __str__(self):
        return "<?{process}>".format(process=self.process)
