from tag_counter.Tags import StartTag
from tag_counter.HtmlCounter import HTMLCounter
from tag_counter.services.AliasManager import AliasManager
from tag_counter.services.SQLiteManager import SQLiteManager
import sqlite3
import sys

#print(socket.getdefaulttimeout())

#c = open("test_file.yaml", "w+")

#a = SQLiteManager()
#print(a.get_tag_types_dict())

a = {"a": 1, "b": 2}
print(a["b"])
print(a["a"])

"""
conn = sqlite3.connect("tag_counter.db")
cursor = conn.cursor()
cursor.execute("select 1 from sqlite_master where type='table' AND name='site_audit'")
if cursor.fetchone() is None:
    print("True, "
          "True")
else:
    print('False')
"""

"""
a = AliasManager()
b = AliasManager()
c = SQLiteManager()
d = SQLiteManager()

print(a)
print(b)
print(c)
print(d)
"""
#a.update_alias("ydx", "yandex.comt")
#print(a.get_aliases_dict())







"""
a = StartTag("a", [("id", "55")])

if type(a) is StartTag:
    print("True")
else:
    print("False")
"""

"""
html = "<a e=2><b r=3>fff</b></a>"
html_counter = HTMLCounter()
html_counter.feed(html)
tag_list = html_counter.tag_list
for tag in tag_list:
    print(tag)
"""


"""
url = 'https://www.google.com/'

response = urllib.urlopen(url)
webContent = response.read()

print(type(webContent))
print(webContent.decode("ascii"))

#parser = HTMLParser()
"""

#print(type("ds"))

#print(str(None))

#tag = Tag("a", [("id", 45), ("rrr", "eee")], None, False)
#print(str(tag))

#b = [("id", 45), ("rrr", "eee")]

#c = all(isinstance(item, tuple) for item in b)


#print(type(b[0]))

"""
a = "sss"

if type(a) is not str:
    print("Yes")
else:
    print("No")
print(type(a))
"""