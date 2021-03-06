#!/usr/bin/env python
#$Id$

# ms-scanner-clamav - Scans a given directory with clamav. Moves found malware 
#                     to a seperate attic directory and updates the malware database.

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

# depends on clamav from http://www.clamav.net and pygresql from 
# http://www.pygresql.org/

from os.path import basename
import sys

import ConfigParser
import os
import string

try:
    import pg
except:
    print 'Error importing the pg module. Check your pygresql installation'
    sys.exit(2)
    
def usage():
    print "Usage: ms-scanner-clamav.py [directory]"

def parseReportFile():
    
    config = ConfigParser.ConfigParser()
    config.read("/etc/monkey-spider.conf")
    try:
        dbName = config.get('ms-database', 'databasename')
        dbHost = config.get('ms-database', 'hostname')
        dbUser = config.get('ms-database', 'username')
        dbPass = config.get('ms-database', 'password')
        mwattic = config.get('ms-scanner', 'mwattic')
    except:
        print 'Unable to read configuration. Check the configuration file.'
        exit(2)

    #create attic for collected malware-binarys
    os.system("mkdir -p %s" % mwattic)

    #cdx file name
    cdxfile = basename(os.getcwd()) + ".cdx"

    f = open(cdxfile, "r")
    cdx = f.readlines()
    f.close()

    # checksum index of the files for the reassosiaction of found malware
    cix = {}
    for x in range(len(cdx)):
        cix[x] = string.split(cdx[x])[5]

    f = open("clamav.report", "r")
    clamav = f.readlines()
    f.close()
    
    clamav_engine_version = string.split(string.split(clamav[0])[1], "/")[0]
    clamav_signature_version = string.split(string.split(clamav[0])[1], "/")[1]
    clamav_last_update = string.split(clamav[0], "/")[2][:-1]

    for i in range(1, len(clamav)):
        mw_name = string.split(clamav[i])[1]
        mw_filename = string.split(string.split(clamav[i])[0], ":")[0]
        mw_checksum = string.split((string.split(string.split(string.split(clamav[i])[0], ":")[0], "/")[-1]), ".")[0]
        try:
            db = pg.connect(dbname=dbName, host=dbHost, user=dbUser, passwd=dbPass)
        except:
            print 'Unable to connect to database. Check your configuration.'
            exit(2)
    
        os.system("cp -u " + mw_filename + " %s" % mwattic)

        #Generate the next ids for databases malware and mw_scanner
        q = db.query("SELECT max(id) from malware")
        max_mw_id = q.getresult()[0][0]
        if max_mw_id == None:
            max_mw_id = 1
        else:
            max_mw_id = max_mw_id + 1

        q = db.query("SELECT max(id) from mw_scanner")
        max_mw_sc_id = q.getresult()[0][0]
        if max_mw_sc_id == None:
            max_mw_sc_id = 1
        else:
            max_mw_sc_id = max_mw_sc_id + 1

        id = max_mw_id
        filename = basename(mw_filename)
        checksum = string.split(basename(mw_filename), ".")[0]
        for x in range(len(cix)):
            if cix[x] == checksum:
                break
        url = string.split(cdx[x])[2].lower()
        size = 0
        date = string.split(cdx[x])[0]
        dateS = date[:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]
        q = "INSERT INTO malware VALUES (%s,'%s','%s','%s',%s,'%s','%s')" % (id, filename, url, checksum, size, dateS, mw_name)
        db.query(q)
        db.close()
        
def main():

    if (len(sys.argv) != 2):
        usage()
        sys.exit(2)

    if not os.path.exists(sys.argv[1]):
        print "Error: Path does not exist or you don't have the needed permissions"
        sys.exit(2)

    if not os.path.isdir(sys.argv[1]):
        usage()
        sys.exit(2)

    #chdir to where the arc file resides
    workdir = sys.argv[1]
    os.chdir(workdir)
    
    print 'Scanning folder %s for viruses with ClamAV' % workdir,

    #Scan directory with clamav and generate report file
    os.system("clamdscan -V > clamav.report")
    os.system("clamdscan -m --fdpass |grep FOUND >> clamav.report")
    
    parseReportFile()
    
    print '.'

        
if __name__ == "__main__":
    main()
