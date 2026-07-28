# dass.py Makefile
# This is deprecated. Use build.sh directly when possible.

SHELL := /usr/bin/env bash
.DEFAULT_GOAL := all

APPNAME := dass
INSTALL_DIR ?= $(HOME)/.local/bin
DEBUG ?= 0

.PHONY: all build dass install test clean distclean

all: install

build dass:
	@echo "Makefile is deprecated. Delegating to ./build.sh"
	@DEBUG=$(DEBUG) SKIP_INSTALL=1 ./build.sh

install:
	@echo "Makefile is deprecated. Delegating to ./build.sh"
	@DEBUG=$(DEBUG) SKIP_INSTALL=0 INSTALL_DIR="$(INSTALL_DIR)" ./build.sh

test:
	python3 -m pytest -q

clean:
	rm -rf ./dist ./build ./*.spec ./*.pyc ./*.log

distclean: clean
	rm -rf ./venv