#!/usr/bin/env python
#$Id$

# ms-seeder-websearch-livesearch - Retrieves Urls from the Windows Live Search
#                                  Web Service for a particular Web search

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

# depends on SOAPpy from http://pywebsvcs.sourceforge.net/

# A valid Live ID is necessary to use this Web Service. It can be obtained from 
# http://dev.live.com/liveid/

import sys

try:
    from SOAPpy import WSDL
except:
    print 'Error importing the SOAPpy module. Check your installation'
    sys.exit(2)
    

def usage():
    print "Usage: ms-seeder-websearch-livesearch '<live-id>' '<search-term>' <number of results (max 250)>"
    
def main():  

    if (len(sys.argv) != 4):
    	usage()
    	sys.exit(2)  

    wsdl_url = 'http://soap.search.msn.com/webservices.asmx?wsdl'
    server = WSDL.Proxy(wsdl_url)

    # search results are restricted to 250

    AppID = sys.argv[1]
    query = sys.argv[2]
    
    # number of results, currently not functional
    num_results = sys.argv[3]

    # always delivery 250 results
    # TODO use the num_results variable to deliver a certain amount of results
    for offset in (0, 50, 100, 150, 200):
        params = {
            'AppID': AppID,
            'Query': query,
            'CultureInfo': 'en-US',
            'SafeSearch': 'Off',
            'Requests': {
            'SourceRequest':{
            'Source': 'Web',
            'Offset': offset,
            # Count is restricted to 50 results at once
            'Count': 50,
            'ResultFields': 'All',
            }}
            }
    
        server_results = server.Search(Request=params)
        results = server_results.Responses[0].Results[0]
    
        for a in range(len(results)):
            print results[a].Url
            
if __name__ == "__main__":
    main()

