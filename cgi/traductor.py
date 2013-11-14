#!/usr/bin/python
#-*-  coding: utf-8 -*-
import cgitb; cgitb.enable(format = 'text')
import sys
import os
from time import gmtime, strftime
from xml.dom.minidom import parseString, parse
from xml.parsers import expat
import xml.etree.cElementTree as ET
import urllib2
import urllib
import json


class Line(object):

    def __init__(self, name, text, translatable, context, section, supersection):
        self.name = name
        self.text = text
        self.translatable = translatable
        self.context = context
        self.section = section
        self.supersection = supersection
    
    def serialize(self):
        return {'name': self.name, 'text': self.text, 'translatable': self.translatable, 'context': self.context, 'section': self.section, 'supersection': self.supersection}


class User(object):

    def __init__(self, name, languages):
        self.name = name
        self.languages = languages

    def serialize(self):
        langs = []
        for lang in self.languages:
            langs.append(lang.serialize())
        return {'name': self.name, 'languages': langs}


class Language(object):
    
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def serialize(self):
        return {'name': self.name, 'code': self.code}


# Configuration
SOURCE_URL = "https://raw.github.com/jjhaggar/ninja-trials/master/res/values/strings.xml"
WORKINGPATH = "/home/bruno/temp/"
LANGUAGES = {'zh': Language('Chinese','zh'), 'fr': Language('French','fr'), 
            'de': Language('German','de'), 'jp': Language('Japanese', 'jp'), 
            'pt': Language('Portuguese', 'pt'), 'ru': Language('Russian', 'ru'),
            'es': Language('Spanish', 'es')}
users = []
users.append(User("Bruno", (LANGUAGES['pt'], LANGUAGES['es'])))
users.append(User("superusuario", LANGUAGES.values()))
source_data = None
source_lines = None

def encapsulate_answer(error, data):
    if error:
        print json.dumps({'error': 'true', 'data': data})
    else:
        print json.dumps({'error': 'false', 'data': data})


def debugger(message):
    encapsulate_answer(True, message)
    sys.exit(0)


def download_source():
    global source_data
    response = urllib2.urlopen(SOURCE_URL)
    source_data = response.read()


def process_source():
    global source_lines
    source_lines = []
    dom = parseString(source_data)
    nodes = dom.documentElement.childNodes
    lastsection = None
    lastsupersection = None
    lastcontext = None
    sectionheader = 'Group-Start: '
    sectiontail = 'Group-End: '
    supersectionheader = 'MegaGroup-Start: '
    supersectiontail = 'MegaGroup-End: '
    for node in nodes:
        if node.nodeType is node.COMMENT_NODE:
            notacontextcomment = False
            try:
                sectionStartPosition = node.data.index(sectionheader)
                lastsection = node.data[sectionStartPosition+len(sectionheader):len(node.data)]
                notacontextcomment = True
            except ValueError:
                pass
            try:
                sectionStartPosition = node.data.index(sectiontail)
                lastsection = None
                notacontextcomment = True
            except ValueError:
                pass
            try:
                supersectionStartPosition = node.data.index(supersectionheader)
                lastsupersection = node.data[supersectionStartPosition+len(supersectionheader):len(node.data)]
                notacontextcomment = True
            except ValueError:
                pass
            try:
                supersectionStartPosition = node.data.index(supersectiontail)
                lastsupersection = None
                notacontextcomment = True
            except ValueError:
                pass
            if not notacontextcomment:
                lastcontext = node.data
        if node.nodeType is node.ELEMENT_NODE:
            name = node.getAttributeNode('name').nodeValue
            try:
                text = node.firstChild.data
            except AttributeError:
                text = ""
            try:
                translatable = node.getAttributeNode('translatable').nodeValue
            except AttributeError:
                translatable = "true"
            source_lines.append(Line(name, text, translatable, lastcontext, lastsection, lastsupersection))


def write_xml(filename, source_lines):
    resources = ET.Element("resources")
    for line in source_lines:
        string = ET.SubElement(resources, "string")
        string.set("name", line.name)
        #string.set("translatable", line.translatable)
        string.text = line.text
    xml_content = ET.tostring(resources, encoding='utf-8', method='xml')
    file = open(WORKINGPATH+filename, 'w')
    file.truncate()
    file.write(xml_content)
    file.close()


def read_xml(filename):
    source_lines = []
    try:
        file = open(WORKINGPATH+filename, 'r')
        file_data = file.read()
        file.close()
    except IOError:
        file = open(WORKINGPATH+filename, 'w')
        file.close()
        return source_lines
    try:
        dom = parseString(file_data)
    except:
        #debugger("Error parsing the xml of this language. Exception is\n%r" % sys.exc_info()[0])
        return source_lines
    elements = dom.getElementsByTagName('string')
    for e in elements:
        name = e.getAttributeNode('name').nodeValue
        try:
            text = e.firstChild.data
        except AttributeError:
            text = ""
        source_lines.append(Line(name, text, None, None, None, None))
    #debugger("There are %d elements with string tag on %s file\nand %d lines have been created." % (len(elements), filename, len(source_lines)))
    return source_lines


def get_user_by_name(username):
    for user in users:
        if user.name == username:
            return user
    return None


def user_has_language_code(username, lang_code):
    user = get_user_by_name(username)
    for l in user.languages:
        if l.code == lang_code:
            return True
    return False


def operation_login(r):
    # this is vulnerable to brute force attack, must implement
    # limited requests (10 requests/minute for example)
    if get_user_by_name(r['user']):
        encapsulate_answer(False, "User found.")
    else:
        encapsulate_answer(True, "User not found.")


def operation_getlanguages(r):
    user_found = False
    for user in users:
        if user.name == r['user']:
            encapsulate_answer(False, user.serialize()['languages'])
            user_found = True
            break
    if not user_found:
        encapsulate_answer(True, "User not found.")


def getLastVersion(langcode):
    onlyfiles = [ f for f in os.listdir(WORKINGPATH) if os.path.isfile(os.path.join(WORKINGPATH,f)) ]
    lastversion = 0
    for f in onlyfiles:
        version = 0
        try:
            prefix = 'strings-%s-' % langcode
            position = f.index(prefix)
            version = int(f[len(prefix) : len(f) - 4])
            if version > lastversion:
                lastversion = version
        except ValueError:
            pass
    if (lastversion is 0):
        lastversion = int(strftime("%Y%m%d%H%M%S", gmtime()))
    return lastversion


def operation_read(r):
    lang_code = r['data']
    if len(lang_code) is not 2:
        encapsulate_answer(True, "Invalid language code.")
    else:
        lastVersion = getLastVersion(lang_code)
        translation_lines = read_xml('strings-%s-%d.xml' % (lang_code, lastVersion))
        lines_original = []
        lines_translation = []
        for line in source_lines:
            lines_original.append(line.serialize())
        for line in translation_lines:
            lines_translation.append(line.serialize())
        encapsulate_answer(False, {'source': lines_original, lang_code: lines_translation})


def operation_write(r):
    lang_code = r['data']['language_code']
    username = r['user']
    if not user_has_language_code(username, lang_code):
        encapsulate_answer(True, "The user is not authorized to save translations in this language.")
    else:
        lines = []
        for l in r['data']['lines']:
            name = l['name']
            text = l['text']
            lines.append(Line(name, text, None, None, None, None))
        current_time = strftime("%Y%m%d%H%M%S", gmtime())
        write_xml('strings-%s-%s.xml' % (lang_code, current_time), lines)
        encapsulate_answer(False, "Translation saved.")


def answer(request):
    r = json.loads(request)
    if r['operation'] == 'login':
        operation_login(r)
    elif r['operation'] == 'read':
        download_source()
        process_source()
        operation_read(r)
    elif r['operation'] == 'write':
        download_source()
        process_source()
        operation_write(r)
    elif r['operation'] == 'getlanguages':
        operation_getlanguages(r)
    else:
        encapsulate_answer(True, "Requested operation is unrecognized.")


"""
EXAMPLES OF REQUESTS
request = json.dumps({'user': 'Bruno', 'operation': 'login'})
request = json.dumps({'user': 'Pepe', 'operation': 'getlanguages'})
request = json.dumps({'user': 'John', 'operation': 'read', 'data': 'es'})
"""
print "Content-type:application/json\r\n\r\n"
request = urllib.unquote(os.environ.get("QUERY_STRING", "No Query String in url"))
answer(request)

