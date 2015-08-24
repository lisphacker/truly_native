#!/usr/bin/env python

import zipfile
import re
import xml.etree.ElementTree as et

blocked_tags = ['script', 'style', 'link']
strip_ns = re.compile('(?:\{[a-zA-Z0-9\.:/]+\})?([a-z]+)')

blocked_words = ['cookie', 'menu', 'footer', 'widget']


def clean_node(node):
    s = ''

    print node.tag, type(node.tag), type(node)
    print node.tag.lower()
    
    tag = strip_ns.match(node.tag.lower()).group(1)
    if tag in blocked_tags:
        return s

    if tag == 'div':
        for word in blocked_words:
            if node.attrib.get('id', '').lower().find(word) != -1:
                return s
            if node.attrib.get('class', '').lower().find(word) != -1:
                return s
            if node.attrib.get('name', '').lower().find(word) != -1:
                return s

    if node.text is not None:
        s += node.text.lower()

    for child in node:
        s += clean_node(child)

    return s
        
def clean(name, s):
    try:
        root = et.XML(s)
    except Exception as e:
        print 'Exception processing', name
        raise e

    cleaned = clean_node(root)

    words = re.split('[^a-z]+', cleaned)
    words = filter(lambda s: len(s) > 1, words)
    
    return ' '.join(words)
    
def main():
    html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'
    cleaned_html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html_cleaned.zip'

    zin = zipfile.ZipFile(html_zip_file, 'r')
    zout = zipfile.ZipFile(cleaned_html_zip_file, 'w', zipfile.ZIP_DEFLATED, True)

    zfis = zin.infolist()
    n = len(zfis)

    lastpc = -100
    for i, zfi in enumerate(zfis):
        zout.writestr(zfi, clean(zfi.filename, zin.read(zfi)))
        pc = ((i + 1) * 100) / n
        if pc != lastpc:
            print '\b\b\b\b\b\b', pc, '%',
            lastpc = pc
    print


if __name__ == '__main__':
    main()
    pass
    
