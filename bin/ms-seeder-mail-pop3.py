#!/usr/bin/env python
#$Id$

# ms-seeder-mail-pop3 - Retrieves Urls out of emails from a pop3 mail account

# Copyright (C) 2006-2008 Ali Ikinci (ali at ikinci dot info)
#
# This file is part of the Monkey-Spider project.
# (http://monkeyspider.sourceforge.net)
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
# along with the Monkey-Spider project.  If not, see <http://www.gnu.org/licenses/>.

import sys

import poplib

def usage():
    print "Usage: ms-seeder-mail-pop3 '<hostname>' '<username>' '<password>'"

def main():

    if (len(sys.argv) != 4):
    	usage()
    	sys.exit(2)  
    
    host = sys.argv[1]
    user = sys.argv[2]
    passw = sys.argv[3]

    f = open("allmails.txt", "w")
    
    M = poplib.POP3(host)
    M.user(user)
    M.pass_(passw)
    numMessages = len(M.list()[1])
    for i in range(numMessages):
        for j in M.retr(i + 1)[1]:
            f.write(" ")
            f.write(j)
    f.close()

    # TODO: extract urls found in the mail
    
if __name__ == "__main__":
    main()
