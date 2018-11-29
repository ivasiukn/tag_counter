import urllib.request as urllib
from html.parser import HTMLParser
from Tag import Tag
from bs4 import BeautifulSoup

"""
url = 'https://www.google.com/'

response = urllib.urlopen(url)
webContent = response.read()

print(type(webContent))
print(webContent.decode("ascii"))

#parser = HTMLParser()
"""
tag = Tag("a", [("id", 45), ("rrr", "eee")], "VALUE", 0)
print(tag.has_end_tag)

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