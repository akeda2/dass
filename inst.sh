#!/bin/bash
# This is deprecated. Use build.sh instead.

[ -f dass.py ] && sudo cp --remove-destination dass.py /usr/local/bin/dass
#[ ! -e ~/boinc-hosts.json ] && ln -s $(realpath boinc-hosts.json) ~/
