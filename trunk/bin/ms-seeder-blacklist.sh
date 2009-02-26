#! /bin/sh
#$Id$

# ms-seeder-blacklist - load hosts files from several places of the internet and 
#                    add them to one urllist

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

#### http://hostsfile.mine.nu
wget http://hostsfile.mine.nu.nyud.net:8080/Hosts.zip -O hosts.tmp.zip
unzip -f hosts.tmp.zip
cat Hosts >> hosts
rm Hosts hosts.tmp.zip
#### http://www.mvps.org/winhelp2002/hosts.htm
wget http://www.mvps.org/winhelp2002/hosts.txt -O hosts.tmp
cat hosts.tmp >> hosts
rm hosts.tmp
#### http://www.hostsfile.org/hosts.html (they have changed their file format to 7zip)
# wget http://www.hostsfile.org/BadHosts.tar.gz
# tar xfz BadHosts.tar.gz
# cat BadHosts/hosts.lnx >> hosts
# rm -rf BadHosts*
#### http://hphosts.mysteryfcm.co.uk/?s=Download
wget http://hphosts.mysteryfcm.co.uk/download/hosts.zip -O hosts.tmp.zip
unzip -f hosts.tmp.zip -d hoststmp
cat hoststmp/HOSTS.TXT >> hosts
rm -rf hoststmp hosts.tmp.zip
#### http://someonewhocares.org/hosts/
wget http://someonewhocares.org/hosts/hosts -O hosts.tmp
cat hosts.tmp >> hosts
#### http://www.everythingisnt.com/hosts.html
wget http://everythingisnt.com/hosts -O hosts.tmp
cat hosts.tmp >> hosts
#### filter and format the file
grep -v '#' hosts |sed '/^$/d' | awk '{print $2}'|sed 's/^[ \t]*//;s/[ \t]*$//' | sed 's/\x0D$//'| sort -u   > hosts.tmp
mv hosts.tmp hosts

