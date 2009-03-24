#!/usr/bin/env python
#$Id$

# ms-extract-arc - Dump all files contained in an Internet Archive ARC File together
#                  with a cdx index file

# Copyright (C) 2006-2008 Ali Ikinci (ali at ikinci dot info)
#
# This file is part of the Monkey-Spider project.
# http://monkeyspider.sourceforge.net
#
# The Monkey-Spider project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# the Monkey-Spider project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the Monkey-Spider project. If not, see http://www.gnu.org/licenses/

# depends on the acreader tool from the Heritrix package (http://crawler.archive.org)

import sys

import mimetypes
import os
import re
import string

def stripHeader(filename):
    # strip the protocol header from the file contents
    file = open(filename, 'r')

    idx = 0

    isFirstLine = True
    while True:
        result = re.compile(":").search(file.readline())
        idx = file.tell()
        if result == None and isFirstLine == False:
            break
        isFirstLine = False

    file.seek(idx)
    outfile = open(filename[:-4], "w")
    outfile.write(file.read())
    outfile.close()

    file.close()
    os.remove(filename)

def usage():
    print 'Usage: ms-extract-arc.py [filename].arc.gz'

def main():

    if (len(sys.argv) != 2):
        usage()
        sys.exit(2)

    if not os.path.exists(sys.argv[1]):
        usage()
        print "Error: File does not exist or you don't have the needed permissions"
        sys.exit(2)

    if not os.path.isfile(sys.argv[1]):
        usage()
        sys.exit(2)

    if sys.argv[1][-7:] != ".arc.gz":
        usage()
        print "Error: File is not in *.arc.gz Format"
        sys.exit(2)


    arcfile = os.path.basename(sys.argv[1])

    # change workingdir to where the arc file resides
    workdir = os.path.dirname(os.path.abspath(sys.argv[1]))
    os.chdir(workdir)

    print 'Extracting %s' % arcfile,

    # create a directory where the arcfile will be extracted, remove an older
    # one if there is
    arcdir = arcfile[:-7]
    if os.path.exists(arcdir):
        os.system("rm -rf " + arcdir)
    os.system("mkdir " + arcdir)
    os.system("gunzip " + arcfile)

    # generate cdx file with the arcreader tool from the Heritrix package
    cdxfile = arcfile[:-6] + "cdx"
    arcreaderinput = os.path.abspath(arcfile[:-3])
    os.system("arcreader -d true  " + arcreaderinput + " > " + cdxfile + ".tmp")
    os.system("mv " + cdxfile + ".tmp " + cdxfile)

    # open the cdxfile
    f = open(cdxfile, "r")
    cdx = f.readlines()
    f.close()

    g = open(arcfile[:-3], "r")

    for x in range(2, len(cdx)):
        archiveThisFile = False
        cdxstring = string.split(cdx[x])

        # generate file name
        fext = mimetypes.guess_extension(cdxstring[3])
        if (fext == None):
            fext = ".raw"

        findex = cdxstring[5]
        fname = findex + fext

        # Seek to the right position
        g.seek(int(cdxstring[6]))
        g.readline()
        h = open(arcdir + "/" + fname + ".tmp", "w")
        h.write(g.read(int(cdxstring[7])))
        h.close()

        stripHeader(arcdir + "/" + fname + ".tmp")

    g.close()

    os.system("gzip " + arcfile[:-3])
    print 'Done  extracting %s'%arcfile

if __name__ == "__main__":
    main()
