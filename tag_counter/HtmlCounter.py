import urllib.request as urllib
from html.parser import HTMLParser
from bs4 import BeautifulSoup

url = 'https://www.google.com/'

response = urllib.urlopen(url)
webContent = response.read()

print(type(webContent))
print(webContent.decode("ascii"))

parser = HTMLParser()

parser.