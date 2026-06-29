# dass.py Makefile
# This is deprecated. Use build.sh directly when possible.

SHELL := /usr/bin/env bash
.DEFAULT_GOAL := all

APPNAME := dass
INSTALL_DIR ?= /usr/local/bin
DEBUG ?= 0

.PHONY: all build dass install clean distclean

all: build

build dass:
	@echo "Makefile is deprecated. Delegating to ./build.sh"
	@DEBUG=$(DEBUG) SKIP_INSTALL=1 ./build.sh

install:
	@echo "Makefile is deprecated. Delegating to ./build.sh"
	@DEBUG=$(DEBUG) SKIP_INSTALL=0 INSTALL_DIR="$(INSTALL_DIR)" ./build.sh

clean:
	rm -rf ./dist ./build ./*.spec ./*.pyc ./*.log

distclean: clean
	rm -rf ./venv