#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# yandex-talks.py

"""
This script reads all available Yandex talks.
The range of searching talks is hardcoded 0-1000, you may change it 
by changing talks_min and talks_max.
The output is yandex-talks.csv file with number, name and link for each talk 
split by tab.
"""

__author__    = 'Bulat Zamilov <bulat.zamilov@gmail.com>'
__version__   = '0.1.3'
__date__      = '2013 April 5th'
__copyright__ = 'Copyright (c) 2013 Bulat Zamilov' 
__license__   = 'GPLv3'

import urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser
import codecs

class YandexHTMLParser(HTMLParser):
    gotcha = False
    
    def handle_starttag(self, tag, attrs):
        #print tag + '' + attrs
        attr = ('class', 'b-talk__title')
        if attr in attrs and tag == 'div':
            self.gotcha = True
            #print "Found Title"

    def handle_data(self, data):
        if self.gotcha:
            self.title = data.encode()
            self.gotcha = False

talks_min = 0
talks_max = 1001

for i in range(talks_min, talks_max):
    url = "http://events.yandex.ru/talks/" + str(i)
    try:
        page = urllib.request.urlopen(url)
        parser = YandexHTMLParser()
        parser.feed(codecs.decode(page.read(), 'utf8'))
        log = open('yandex-talks.csv', 'a')
        title = codecs.decode(parser.title, 'utf8')
        final_url = page.url
        print ("Processing link #%d - %s (%s)" % (i, final_url, title))
        log_string = str(i) + '\t' + title + '\t' + final_url + '\n'
        log.write(log_string)
        log.close()
        parser.close()
    except urllib.error.URLError:
        pass
