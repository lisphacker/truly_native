#!/usr/bin/env python

import zipfile
import re
import sys
from bs4 import BeautifulSoup
from collections import namedtuple
from multiprocessing import Process, Queue

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
        'p':NodeProp('p', ['class'], False),
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
    return HTMLCleaner(s).clean()

def clean_files(html_zip_file, files, queue):
    zin = zipfile.ZipFile(html_zip_file, 'r')

    for file_ in files:
        with zin.open(file_, 'r') as f:
            queue.put((file_, clean(file_, f.read())))

    zin.close()

def split_list(l, num_parts):
    part_len = int(len(l) / num_parts)

    r = []
    
    for i in range(num_parts):
        s = i * part_len
        e = (i + 1) * part_len
        if i == num_parts - 1:
            e = len(l)
        r.append(l[s:e])

    return r

def main():
    html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'
    cleaned_html_zip_file = '/home/gautham/work/kaggle/truly_native/data/html_cleaned3.zip'

    num_processes = 6

    zin = zipfile.ZipFile(html_zip_file, 'r')
    html_files = zin.namelist()
    
    n = len(html_files)
    zin.close()

    html_file_partitions = split_list(html_files, num_processes)

    processes = []
    queues = []
    for i in range(num_processes):
        queue = Queue()
        process = Process(target=clean_files, args=(html_zip_file, html_file_partitions[i], queue))
        process.start()
        
        queues.append(queue)
        processes.append(process)

    zout = zipfile.ZipFile(cleaned_html_zip_file, 'w', zipfile.ZIP_DEFLATED, True)

    child_processes_running = True
    i = 0
    last_i = 0
    while child_processes_running:
        
        queues_empty = False
        while not queues_empty:
            queues_empty = True
            for queue in queues:
                if not queue.empty():
                    queues_empty = False
                    fn, text = queue.get()
                    zout.writestr(fn, text)
                    i += 1

        if last_i != i:
            print i, '/', n
            last_i = i
        
        child_processes_running = False
        for process in processes:
            if process.is_alive():
                child_processes_running = True


        
if __name__ == '__main__':
    main()
