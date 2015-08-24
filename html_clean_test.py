#!/usr/bin/env python

import zipfile
import re
import sys
from HTMLParser import HTMLParser

blocked_tags = ['script', 'style', 'link']
strip_ns = re.compile('(?:\{[a-zA-Z0-9\.:/]+\})?([a-z]+)')

blocked_words = ['cookie', 'menu', 'footer', 'widget']

count = 0
class DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.data_blocks = []
        
        self.level = 0
        self.blocked = False
        self.blocked_level = -1

    def block(self):
        if self.blocked:
            return

        self.blocked = True
        self.blocked_level = self.level

    def unblock(self):
        if not self.blocked:
            return
        
        self.blocked = False
        self.blocked_level = -1
        
    def handle_starttag(self, tag, attrs):
        self.level += 1

        #print '>>>', tag
        
        if tag in blocked_tags:
            self.block()

        for word in blocked_words:
            for k, v in attrs:
                if k in ['class', 'id', 'name']:
                    if v.lower().find(word) != -1:
                        self.block()
            
        
    def handle_endtag(self, tag):
        #print '<<<', tag
        
        if self.blocked:
            if self.blocked_level == self.level:
                self.unblock()
            
        self.level -= 1
        
    def handle_data(self, data):
        global count
        
        count += 1

        if count > 150000:
            sys.exit(0)
            
        if not self.blocked:
            self.data_blocks.append(data.lower())
            pass

    def get(self):
        return ' '.join(self.data_blocks)
        
def clean(name, s):
    parser = DeHTMLParser()
    parser.feed(s)

    words = re.split('[^a-z]+', parser.get())
    words = filter(lambda s: len(s) > 1, words)
    
    return ' '.join(words)
    
def main1():
    html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'
    cleaned_html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html_cleaned.zip'

    zin = zipfile.ZipFile(html_zip_file, 'r')
    zout = zipfile.ZipFile(cleaned_html_zip_file, 'w', zipfile.ZIP_DEFLATED, True)

    zfis = zin.infolist()
    n = len(zfis)

    lastpc = -100
    for i, zfi in enumerate(zfis):
        zout.writestr(zfi, clean(zfi.filename, zin.read(zfi)))
        print (i + 1), '/', n

def main2():
    html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'

    zin = zipfile.ZipFile(html_zip_file, 'r')

    zfis = zin.infolist()
    n = len(zfis)

    zfis = zfis[53258:]
    for i, zfi in enumerate(zfis):
        print i, zfi.filename
        print clean(zfi.filename, zin.read(zfi))
        #print (i + 1), '/', n
    pass

def main():
    with open('3878730_raw_html.txt', 'r') as f:
        print clean('a', f.read())
        
if __name__ == '__main__':
    main()
