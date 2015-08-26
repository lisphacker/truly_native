#!/usr/bin/env python

import zipfile
import re
import sys
from bs4 import BeautifulSoup
from collections import namedtuple

textre = re.compile('[a-z]+')
hexre = re.compile('%[0-9a-f]{2}')

def clean_text(s):
    s = str(s).lower()

    # Remove hex codes.
    s = '#'.join(hexre.split(s))

    # Find all text entries.
    ts = textre.findall(s)
    if ts[0] in ['http', 'https', 'ftp']:
        ts = ts[1:]
        
    ts = filter(lambda s: len(s) > 1, ts)

    return ' '.join(ts)


NodeProp = namedtuple('NodeProp', ['tag', 'attributes', 'skip_text'])

class HTMLCleaner:
    nodeprops = {
        'p':NodeProp('p', ['class'], True),
        'img':NodeProp('img', ['class', 'src', 'data-img'], False),
        'link':NodeProp('link', ['href'], False),
        'a':NodeProp('a', ['title', 'href', 'class'], False),
        'div':NodeProp('div', ['class'], False),
        'script':NodeProp('script', ['src'], True),
        'meta':NodeProp('meta', ['content'], True)
    }
    
    
    def __init__(self, html_text, skip_text_for_unknown_nodes=False):
        self.skip_text_for_unknown_nodes = skip_text_for_unknown_nodes
        self.__soup = BeautifulSoup(html_text)

    def clean(self):
        text_list = []
        
        nodes = self.__soup.find_all(True)
        for node in nodes:
            txt = ''
            if node.name in self.nodeprops:
                nodeprop = self.nodeprops[node.name]
                
                if not nodeprop.skip_text:
                    try:
                        txt += ' ' + clean_text(node.text)
                    except:
                        pass

                for attr_name in nodeprop.attributes:
                    try:
                        txt += ' ' + clean_text(node.attrs[attr_name])
                    except:
                        pass

            else:
                if not self.skip_text_for_unknown_nodes:
                    try:
                        txt += ' ' + clean_text(node.text)
                    except:
                        pass
                    
            text_list.append(txt)

        return ' '.join(map(str.strip, ' '.join(text_list).split())).lower()

def clean(name, s):
    return HTMLCleaner(s, True).clean()
    
def main():
    html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'
    cleaned_html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html_cleaned2_no_text.zip'

    zin = zipfile.ZipFile(html_zip_file, 'r')
    zout = zipfile.ZipFile(cleaned_html_zip_file, 'w', zipfile.ZIP_DEFLATED, True)

    zfis = zin.infolist()
    n = len(zfis)

    lastpc = -100
    for i, zfi in enumerate(zfis):
        zout.writestr(zfi, clean(zfi.filename, zin.read(zfi)))
        print (i + 1), '/', n

def main2():
    with open('2940496.html', 'r') as f:
        print clean('a', f.read())
        
if __name__ == '__main__':
    main()
