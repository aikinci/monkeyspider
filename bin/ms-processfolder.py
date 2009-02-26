#!/usr/bin/env python
#$Id$

# ms-processfolder - Examines a given directory with ARC files utilizing the  
# 		             available scanner modules

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

import os.path
import sys

import os
import popen2
import re

def usage():
    print 'ms-processfolder.py [folder/with/ARC/files/]'

def main():
    if (len(sys.argv) != 2):
        usage()
        exit(2)

    if not os.path.exists(sys.argv[1]):
        print "Error: Folder does not exist or you don't have the needed permissions"
        usage()
        exit(2)

    if not os.path.isdir(sys.argv[1]):
        usage()
        exit(2)

    arcsdir = os.path.abspath(sys.argv[1])

    os.chdir(arcsdir)

    fl = os.listdir('.')
    filelist = []

    for x in fl:
        if re.compile(".arc.gz$").search(x, 1):
            filelist.append(x)  
    
    
    st = open('status.log', 'w')

    st.write('Processing ARC files in Folder: %s \n' % os.getcwd())
    
    for x in filelist:
        arcfile = os.path.abspath(x)
        st.write('ms-extract-arc:\t\t' + popen2.popen4("ms-extract-arc.py " + arcfile)[0].read())
        st.write('ms-scanner-clamav:\t' + popen2.popen4("ms-scanner-clamav.py " + arcfile[:-7])[0].read())
        st.write(popen2.popen3("rm -rf %s" % arcfile[:-7])[2].read())

    st.write('Done!\n')
    st.close()


if __name__ == "__main__":
    main()
