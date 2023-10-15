# dass - Document assembler
Assembles a file/directory structure into one output file.
### Installation:
```
To build with venv and pyinstaller:
./build.sh
```
### Usage:
```
options:
  -h, --help            show this help message and exit

subcommands:
  {compile,c,co,com,comp,add,a,ad,rename,r,re,ren,clean,cl,cle}
                        sub-command help
    compile (c, co, com, comp)
                        Sort and Compile a directory of numbered text files into output file.
    add (a, ad)         Add a new document
    rename (r, re, ren)
                        Rename a document
    clean (cl, cle)     Clean up the directory structure.
```
### Examples:
```
Create a new project:

mkdir mybook
cd mybook
dass add -c 010 "First chapter"
cd "010First chapter"
dass add 010 "First subsection"
dass add 020 "Second subsection"
(edit in editor of choice)

Compile into text/markdown/html and save settings for next build:
cd mybook
dass compile -smw -t "Title of project" .
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