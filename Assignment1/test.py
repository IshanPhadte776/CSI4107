from bs4 import BeautifulSoup
import collections

from lxml import etree

file = open("coll/AP880212", 'r').read().replace("\n", "")

document = BeautifulSoup(file, 'lxml')

for doc in document('doc'):

    print(doc.find('head'))
    tags = []
    for tag in doc.find_all():
        tags.append(tag.name)
    print(tags)
    print(doc.contents)
    break