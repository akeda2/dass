# dass.py Makefile
# This is deprecated. Use build.sh instead (uses venv)

all: dass del
# readme

# Create dass executable
dass:
	# Check for python3-venv:
	dpkg -l | grep -q python3-venv || echo "python3-venv package not installed'"
	python3 -m venv --help &> /dev/null || { echo "Python venv is not installed!'"; exit 1; }
	# Create venv if not exists
	[[ ! -d venv ]] && { python3 -m venv venv || { echo "venv creation failed" ; exit 1; } ; }
	source venv/bin/activate || { echo "venv activation failed" ; exit 1; }
	echo "Installing dependenies"
	pip install -r requirements.txt || { echo "pip install failed" ; exit 1; }

	pyinstaller --onefile "dass".py --clean -F --noupx && mv dist/dass . || { echo "pyinstaller failed" ; exit 1; }
	deactivate || { echo "venv deactivation failed" ; exit 1; }
# Remove files created by pyinstaller
del:
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log dass.spec dist/

# Clear pyinstall cache and delete file
clean:
	#pyinstaller --clean dass.py
	rm -rf ./dist/ ./build/ ./*.spec ./*.pyc ./*.log dass.spec dist/ dass

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install:
	mkdir -p $(DESTDIR)$(BINDIR)
	install -m755 dass $(DESTDIR)$(BINDIR)/dass