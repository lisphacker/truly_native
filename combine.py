#!/usr/bin/env python

import glob
import zipfile
import os.path as pth
import sys

src_dir = '/home/gautham/downloads/kaggle/truly_native'

src_files = glob.glob(src_dir + '/?.zip')
src_files.sort()

out_file = '/home/gautham/work/kaggle/truly_native/data/html.zip'

zout = zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED, True)

for src_file in src_files:
    print 'Processing', src_file
    zin = zipfile.ZipFile(src_file)

    zfis = zin.infolist()

    n = len(zfis)
    for i, zfi in enumerate(zfis):
        if not zfi.filename.endswith('.txt'):
            continue

        zout.writestr(pth.basename(zfi.filename), zin.read(zfi))

        print '\b\b\b\b\b\b\b', (i + 1) * 100 / n, '%',

    print ''
        

