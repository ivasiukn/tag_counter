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
tag = Tag("a", [("id",45), ("rrr", "eee")], "VALUE", 1)

print(tag.name)

