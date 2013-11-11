from xml.dom.minidom import parseString
import xml.etree.cElementTree as ET


class Line():

    def __init__(self, name, text, context, section, translatable):
        self.name = name
        self.text = text
        self.context = context
        self.section = section


class User():

    def __init__(self, name, languages):
        self.name = name
        self.languages = languages

# Configuration
STRINGSOURCE = "https://raw.github.com/jjhaggar/ninja-trials/master/res/values/strings.xml"
WORKINGPATH = "C:\\borrame\learnpythonthehardway\\"
LANGUAGES = ("zh", "fr", "de", "jp", "pt", "ru", "es")
users = []
users.append(User("Bruno", (LANGUAGES[6], LANGUAGES[4])))
users.append(User("superusuario", LANGUAGES)




# Reading source xml
# http://stackoverflow.com/questions/8732165/python-xml-processing-after-a-specific-comment
source_lines = []
file = open('strings.xml', 'r')
source_data = file.read()
file.close()
dom = parseString(source_data)
elements = dom.getElementsByTagName('string')
for element in elements:
    text = element.firstChild.data.encode('utf-8')
    atr = element.getAttributeNode('name')
    name = atr.nodeValue.encode('utf-8')
    atr = element.getAttributeNode('context')
    if atr is not None:
        context = atr.nodeValue.encode('utf-8')
        source_lines.append(Line(name, text, context, None, None))
    else:
        source_lines.append(Line(name, text, None, None, None))




# Writing new xml
resources = ET.Element("resources")
for line in source_lines:
    string = ET.SubElement(resources, "string")
    string.set("name", line.name)
    if not line.context is None:
        string.set("context", line.context)
    string.text = line.text.decode('utf-8')
escribeesto = ET.tostring(resources, encoding='utf8', method='xml')
file = open('strings2.xml', 'w')
file.truncate()
file.write(escribeesto)
file.close()


"""
TODO

CGI
"""
