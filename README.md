# dass - Document assembler
Assembles a file/directory structure into one output file.
### Usage:
```
dass [input directory] [output file]
Example:
dass . out
```
Subdirectories will be chapter-markers. All leading digits will be stripped.
Use a numbering pattern to sort textblocks:
```
010Chapter\ 1
020Chapter\ 2
etc.
```
