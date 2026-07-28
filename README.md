# dass - Document assembler
Assembles a file/directory structure into one output file.
### Installation:
Install in user mode with pipx:
```
pipx install dass
```

Install directly from this repository:
```
pipx install "git+https://github.com/akeda2/dass.git"
```

For local development from this checkout:
```
pipx install .
```

Upgrade later with:
```
pipx upgrade dass
```

Legacy binary build with venv + pyinstaller is still available:
```
./build.sh
```

### Makefile compatibility:
The Makefile is deprecated, but still supported as a wrapper around build.sh.

```
make              # equivalent to: SKIP_INSTALL=0 INSTALL_DIR=$HOME/.local/bin ./build.sh
make build        # equivalent to: SKIP_INSTALL=1 ./build.sh
make install      # equivalent to: SKIP_INSTALL=0 INSTALL_DIR=$HOME/.local/bin ./build.sh
make clean        # remove build artifacts
make distclean    # clean + remove venv
```

You can pass optional variables:

```
make install INSTALL_DIR=/tmp/dass-bin
make build DEBUG=1
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
dass compile -smw -t "Title of project" book
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