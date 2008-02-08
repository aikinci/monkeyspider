#!/bin/sh
# Installation script for monkey-spider version 0.1
chmod +x bin/*
cp -r bin/* /usr/bin/

cp -r etc/* /etc/

mkdir /usr/share/doc/monkey-spider-0.1/
cp -r INSTALL README* COPYING examples/ /usr/share/doc/monkey-spider-0.1/
