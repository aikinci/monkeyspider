#!/bin/sh
#$Id$

# Installation script for monkey-spider version 0.2
chmod +x bin/*
cp -r bin/* /usr/bin/

cp -r etc/* /etc/

mkdir /usr/share/doc/monkeyspider/
cp -r INSTALL README* COPYING CHANGELOG examples/ /usr/share/doc/monkeyspider/
