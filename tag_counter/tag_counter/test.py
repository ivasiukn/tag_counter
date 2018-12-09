#from tag_counter.tags.Tags import Tag
from tag_counter.HtmlCounter import HTMLCounter


html = "<a e=2><b r=3>fff</b></a>"
html_counter = HTMLCounter()
html_counter.feed(html)
tag_list = html_counter.tag_list
for tag in tag_list:
    print(tag)



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