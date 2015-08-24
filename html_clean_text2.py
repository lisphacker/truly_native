#!/usr/bin/env python

import zipfile
import re
import sys
from bs4 import BeautifulSoup

blocked_tags = ['script', 'style', 'link']
strip_ns = re.compile('(?:\{[a-zA-Z0-9\.:/]+\})?([a-z]+)')

blocked_words = ['cookie', 'menu', 'footer', 'widget']

textre = re.compile('[a-zA-Z]+')

def clean_link(link):
    ts = textre.findall(link)[1:]
    ts = filter(lambda s: len(s) > 1, ts)
    return ' '.join(ts)
    
def clean(name, s):
    soup = BeautifulSoup(s)

    text_list = []
    
    ps = soup.find_all('p')
    for p in ps:
        #text_list.append(p.text)
        pass

    imgs = soup.find_all('img')
    for img in imgs:
        try:
            text_list.append(clean_link(img.attrs['src']))
            print img.attrs['src']
            print clean_link(img.attrs['src'])
            print ''
        except:
            pass
    

    text_list = map(str, text_list)
    
    return ' '.join(map(str.strip, ' '.join(text_list).split())).lower()
    
def main():
    html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'
    cleaned_html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html_cleaned2.zip'

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
    main2()
