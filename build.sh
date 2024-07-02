#!/bin/bash -x
#
# Build and install:
APPNAME="dass"
#
# Check for the existence of the python3-venv package
echo "Checking for python3-venv:"
dpkg -l | grep -q python3-venv || echo "python3-venv package not installed'"


# Check for the existence of the venv module
echo "Checking for venv module"
python3 -m venv --help &> /dev/null || { echo "Python venv is not installed!'"; exit 1; }
#    echo "Python venv is installed."
#else
#    echo "Python venv is not installed!"
#    echo "If you are using Debian/Ubuntu/etc, install via:"
#    echo "sudo apt update; sudo apt install python3-venv"
#fi

# Create a virtual environment if it doesn't exist
echo "Creating or reusing a virtual environment"
[[ ! -d venv ]] && { python3 -m venv venv || { echo "venv creation failed" ; exit 1; } ; }

# Activate the virtual environment
echo "Activating the virtual environment"
source venv/bin/activate || { echo "venv activation failed" ; exit 1; }
echo "Installing dependenies"
pip install -r requirements.txt || { echo "pip install failed" ; exit 1; }

# Run PyInstaller to create the executable
echo "Running PyInstaller"
pyinstaller --onefile "$APPNAME".py --clean -F --noupx || { echo "pyinstaller failed" ; exit 1; }

# Copy/install the executable to /usr/local/bin
echo "Installing to /usr/local/bin"
sudo install -v -m 755 dist/"$APPNAME" /usr/local/bin/"$APPNAME" || { echo "install failed" ; exit 1; }

# Deactivate the virtual environment
deactivate || { echo "venv deactivation failed" ; exit 1; }
#deactivate

# Remove the build files:
rm -rfv ./dist/ ./build/ ./*.spec ./*.pyc ./*.log "$APPNAME".spec dist/ "$APPNAME"

echo "Build complete. Installed to /usr/local/bin/$APPNAME"
