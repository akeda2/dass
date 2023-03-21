# dass - Document assembler
Assembles a file/directory structure into one output file.
### Installation:
```
To build with pyinstaller:
make
make install
To just install in /usr/local/bin/dass:
./setup.sh
```
### Usage:
```
dass [input directory] [output file]
Example:
dass . out
```
Subdirectories will be chapter-markers. All leading digits will be stripped.
Using a 3-digit numbering pattern to sort textblocks:
```
010Chapter\ 1
010Chapter\ 1\020Testfile\ 1.txt
010Chapter\ 1\030Testfile\ 2.txt
020Chapter\ 2
etc.
```