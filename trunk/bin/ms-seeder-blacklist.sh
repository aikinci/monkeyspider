#! /bin/sh
#$Id$

# ms-seeder-blacklist.sh - load hosts files from several places of the internet and 
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
echo This script downloads and concatenates hosts from various hosts file providers
# Check if required programs are installed
echo Checking installed programs first
for CMD in awk sed wget unzip grep p7zip; do
   type $CMD &> /dev/null
   if [ $? != "0" ]; then
      echo "The command '$CMD' is required and is not in your path."
      exit 1
   fi
done

CURDIR=$(pwd)
#echo $CURDIR
cd /tmp

# Delete any hosts file and temporary directory which might exist previously
rm -rf hosts*

touch hosts 

#### http://hostsfile.mine.nu
wget http://hostsfile.mine.nu/Hosts.zip -O hosts.tmp.zip
unzip hosts.tmp.zip
cat Hosts >> hosts
rm Hosts hosts.tmp.zip

#### http://www.mvps.org/winhelp2002/hosts.htm
wget http://www.mvps.org/winhelp2002/hosts.zip -O hosts.tmp.zip
unzip hosts.tmp.zip -d hoststmp
cat hoststmp/HOSTS >> hosts
rm -rf hoststmp hosts.tmp.zip

#### http://www.hostsfile.org/hosts.html
wget http://www.hostsfile.org/Downloads/BadHosts.unx.7z -O hosts.tmp.7z
p7zip -d hosts.tmp.7z
find BadHosts.unx -iname "add.*" -exec cat {} >> hosts \;
rm -rf hosts.tmp.7z BadHosts.unx

#### http://hosts-file.net/
wget http://hosts-file.net/download/hphosts.zip -O hosts.tmp.zip
unzip hosts.tmp.zip -d hoststmp
cat hoststmp/HOSTS.txt >> hosts
rm -rf hoststmp hosts.tmp.zip

#### http://someonewhocares.org/hosts/
wget http://someonewhocares.org/hosts/hosts -O hosts.tmp
cat hosts.tmp >> hosts
rm hosts.tmp

#### filter and format the file
grep -v '#' hosts |sed '/^$/d' | awk '{print $2}'|sed 's/^[ \t]*//;s/[ \t]*$//' | sed 's/\x0D$//'| sort -u   > hosts.tmp
rm hosts

cd $CURDIR
mv /tmp/hosts.tmp hosts

echo Gathered $(wc -l hosts |awk '{print $1}') unique hosts and wrote it to the file hosts


