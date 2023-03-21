# dass.py Makefile
# 

all: dass del
# readme

# Create dass executable
dass:
	pyinstaller dass.py -F
	mv dist/dass .

# Remove files created by pyinstaller
del:
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log dass.spec dist/

# Clear pyinstall cache and delete file
clean:
	pyinstaller --clean dass.py
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log dass.spec dist/

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install:
	mkdir -p $(DESTDIR)$(BINDIR)
	install -m755 dass $(DESTDIR)$(BINDIR)/dass