#!/usr/bin/env python
#$Id$

# ms-seeder-websearch-yahoo - Retrieves Urls from the Yahoo! Search Web Service
#                             for a particular Web search

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

# Depends on pYsearch from http://pysearch.sourceforge.net/

# A valid Yahoo Application ID is necessary to use this Web Service. It can be
# obtained from http://developer.yahoo.com/wsregapp/ 

import sys


try:
    from yahoo.search.web import WebSearch
except:
    print 'Error importing the pYsearch modules. Check your installation'
    sys.exit(2)

def usage():
    print "Usage: ms-seeder-websearch-yahoo '<yahoo-app-id>' '<search-term>' <number of results (max 100)>"

def main():

    if (len(sys.argv) != 4):
    	usage()
    	sys.exit(2)
    	
    srch = WebSearch(app_id=sys.argv[1])
    srch.query = sys.argv[2]
    # only the first 100 results are queryable
    srch.results = sys.argv[3]
    # Disable content filter to get all available results
    srch.adult_ok = 1
    LinkIdx = 0
	
    for res in srch.parse_results():
        LinkIdx = LinkIdx + 1
        print res.Url


if __name__ == "__main__":
    main()
