#!/usr/bin/python3
# Short program that concatenates text files in directories and subdirectories into one file.
# Usage: python3 dass.py [command] [options] [output]
# Try python3 dass.py --help for more information.
# ./inst.sh will install the program to /usr/local/bin/dass
# The output file will be created if it does not exist. If it does exist, it will be overwritten.

import os
import re
import shlex
import argparse
import markdown
import yaml
#import argcomplete

def create(args):
    if args.chapter:
        print("Adding new chapter with number " + str(f"{args.number:03d} and title {args.title}"))
        new_dir = os.path.join(str(f"{args.number:03d}{args.title}"))
        if not os.path.exists(os.path.normpath(new_dir)): 
            os.mkdir(new_dir)
        else:
            print("Directory already exists.")
            exit(1)
        exit()
    else:
        print("Adding new document with number " + str(f"{args.number:03d} and title {args.title}"))
        if not os.path.exists(os.path.join(str(f"{args.number:03d}{args.title}.txt"))):
            # Create new file:
            new_file = open(os.path.join(str(f"{args.number:03d}{args.title}.txt")), 'w')
        else:
            print("File already exists!")
            exit(1)
        print(new_file)
        """ if not os.path.exists(os.path.normpath(new_file.name)):
            new_file.write('')
        else:
            print("File already exists. 2")
            exit(1) """
        new_file.close()
        exit()

def rename(args):
    # Look for document or directory beginning with number:
    print("Looking for document with number " + str(f"{args.in_number:03d}"))
    for dirpath, dirnames, filenames in os.walk(args.directory, topdown=True):
        for file in filenames:
            if file.startswith(str(f"{args.in_number:03d}")):
                print("Found file " + file)
                if args.title:
                    if not os.path.exists(os.path.normpath(os.path.join(args.directory, str(f"{args.out_number:03d}{args.title}.txt")))):
                        os.rename(os.path.join(args.directory, file), os.path.join(args.directory, str(f"{args.out_number:03d}{args.title}.txt")))
                        print("Renamed file " + file + " to " + str(f"{args.out_number:03d}{args.title}.txt"))
                    else:
                        print("File already exists.")
                        exit(1)
                else:
                    # If no title is given, use the old title:
                    title = re.search(r'(\d+)(.*)', file).group(2)
                    if not os.path.exists(os.path.normpath(os.path.join(args.directory, str(f"{args.out_number:03d}{title}")))):
                        os.rename(os.path.join(args.directory, file), os.path.join(args.directory, str(f"{args.out_number:03d}{title}")))
                        print("Renamed file " + file + " to " + str(f"{args.out_number:03d}{title}"))
                    else:
                        print("File already exists.")
                        exit(1)
                exit()
        for dir in dirnames:
            if dir.startswith(str(f"{args.in_number:03d}")):
                print("Found directory " + dir)
                if args.title:
                    if not os.path.exists(os.path.normpath(os.path.join(args.directory, str(f"{args.out_number:03d}{args.title}")))):
                        os.rename(os.path.join(args.directory, dir), os.path.join(args.directory, str(f"{args.out_number:03d}{args.title}")))
                        print("Renamed directory " + dir + " to " + str(f"{args.out_number:03d}{args.title}"))
                    else:
                        print("Directory already exists.")
                        exit(1)
                else:
                    # If no title is given, use the old title:
                    title = re.search(r'(\d+)(.*)', dir).group(2)
                    if not os.path.exists(os.path.normpath(os.path.join(args.directory, str(f"{args.out_number:03d}{title}")))):
                        os.rename(os.path.join(args.directory, dir), os.path.join(args.directory, str(f"{args.out_number:03d}{title}")))
                        print("Renamed directory " + dir + " to " + str(f"{args.out_number:03d}{title}"))
                    else:
                        print("Directory already exists.")
                        exit(1)
                exit()
    
def compile(args):
    # Load config from yaml file if given, otherwise load the first yaml file found in the current directory.
    if args.load:
        # Check if args.load is the default value or if a file was given.
        if args.load == 'def':
            for file in os.listdir(os.getcwd()):
                if file.endswith(".yaml"):
                    # Load configuration from the first yaSml file found in the current directory.
                    settingsfile = file
        # Load configuration from the given yaml file.
        # Check if the file exists.
        elif os.path.isfile(args.load):
            print("Settings file to load: " + args.load)
            settingsfile = args.load
        else:
            print("File not found: " + args.load)
            exit()
            
        with open(settingsfile, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                compile_parser.set_defaults(**config)
                print("Loaded configuration from file: " + settingsfile)
            except yaml.YAMLError as exc:
                print(exc)
                exit()
                #break
    if args.save:
        # Save the given settings to a file:
        settings = {
            "directory": args.directory if args.directory else os.getcwd(),
            "output_name": args.output_name if args.output_name else input("Output name: "),
            "markdown": args.markdown if args.markdown else False,
            "html": args.html if args.html else False,
            "title": args.title if args.title else input("Title: "),
        }
        new_settings = settings['output_name'] + '.yaml'
        with open(new_settings, 'w') as file:
            documents = yaml.dump(settings, file)
    # Compile the document:
    if args.html:
        args.markdown = True
    directory = os.path.normpath(args.directory)
    print(directory)
    outname = os.path.normpath(args.output_name) if args.output_name else config['output_name'] or os.path.normpath(input("Output name: "))
    output_text = os.path.normpath(outname + ".text") if args.output_name else os.path.normpath(config['output_name'] + ".text") or os.path.normpath(input("Output name: ") + ".text")
    output_markdown = os.path.normpath(outname + ".md") if args.output_name else os.path.normpath(config['output_name'] + ".md") or os.path.normpath(input("Output name: ") + ".md")
    output_html = os.path.normpath(outname + ".html") if args.output_name else os.path.normpath(config['output_name'] + ".html") or os.path.normpath(input("Output name: ") + ".html")
    print(outname)
    if os.path.exists(output_text) or os.path.exists(output_markdown) or os.path.exists(output_html):
        if args.no_overwrite:
            print("File exists! --no_overwrite is set. Exiting.")
            exit()
        else:
            print("At least one file exists. It will be overwritten.")
    out_text = open(output_text, 'w', encoding='utf-8-sig')
    if args.markdown:
        out_md = open(output_markdown, 'w', encoding='utf-8-sig')
    if args.html:
        out_html = open(output_html, 'w', encoding='utf-8-sig')


    directories = []
    files = []
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        directories.append(dirpath)
        files.extend(os.path.join(dirpath, f) for f in filenames)

    directories = sorted(directories)
    files = sorted(files)
    out_buf_md = ''
    out_buf_text = ''
    if args.title:
        if args.markdown:
            out_buf_md += "# " + args.title + "\n\n"
        out_buf_text += args.title + "\n\n"
    print(directories)
    print(files)
    last_chapter = ''
    for file in files:
        if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            print(input_file.name)
            temp_buf = ''
            for line in input_file.readlines():
                """ lex = shlex.shlex(line)
                lex.whitespace = ''
                line = ''.join(list(lex))
                if not line:
                    print("Found comment line: " + line + " Skipping.")
                    continue """
                temp_buf += line

            chapter = re.sub("^\d+", "", os.path.dirname(os.path.normpath(input_file.name)))
            print("Current filename: " + input_file.name)
            print("Chapter: " + chapter + " Last chapter: " + last_chapter)
            if chapter != last_chapter:
                print("+Chapter: " + chapter)
                if args.markdown:
                    out_buf_md += "\n\n" + "## " + chapter + "\n\n"
                out_buf_text += "\n\n" + chapter + "\n\n"
                last_chapter = chapter

        #if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            print("Input file for rubrik: " + input_file.name)
            # Write the name of the file without extension to the output file.
            if args.markdown:
                out_buf_md += "\n\n" + "### " + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n"
                out_buf_md += temp_buf
            out_buf_text += "\n\n" + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n"
            out_buf_text += temp_buf
            # print the filename of the file that is being concatenated to the output file.
            input_file.close()
    out_text.write(out_buf_text)
    out_text.close()
    if args.markdown:
        out_md.write(out_buf_md)
        out_md.close()
    if args.html:
        out_html.write(markdown.markdown(out_buf_md, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite']))
        out_html.close()

argparse = argparse.ArgumentParser(description='Concatenate text files in directories and subdirectories into one file.', allow_abbrev=True)
subparsers = argparse.add_subparsers(title='subcommands',help='sub-command help', dest='subcommand')

# A parser for the "compile" command
compile_parser = subparsers.add_parser('compile', aliases=['c','co','com','comp'], help='Sort and Compile a directory of numbered text files into output file.')
compile_parser.add_argument('-d', '--directory', nargs='?', default=".", help='The base directory to concatenate.')
compile_parser.add_argument('output_name', nargs='?', help='Filename without extension use for output files. If any file exists, it will be overwritten.')
compile_parser.add_argument('-m', '--markdown', action='store_true', help='Use Markdown syntax for headers. Outputs a .md file.')
compile_parser.add_argument('-w', '--html', action='store_true', help='Convert output into HTML. Outputs a .html file.')
compile_parser.add_argument('-b', '--disable_bom', action='store_true', help='Disable the Byte Order Mark (BOM) in the output file(s).')
compile_parser.add_argument('-n', '--no_overwrite', action='store_true', help='Do not overwrite existing files.')
compile_parser.add_argument('-t', '--title', help='Custom title for the output file.')
compile_parser.add_argument('-s', '--save', action='store_true', help='Save the given configuration to a file.')
# Load configuration from the first yaml file found in the current directory. Just load any existing yaml file:
compile_parser.add_argument('-l', '--load', const='def', nargs='?', help='Load a configuration from a file.')
compile_parser.set_defaults(func=compile)

# A parser for the "add" command
add_parser = subparsers.add_parser('add', aliases=['a','ad'], help='Add a new document')
add_parser.add_argument('number', type=int, help='The sorting number of the new document.')
add_parser.add_argument('title', help='The title of the new document.')
add_parser.add_argument('-c', '--chapter', action="store_true", help='Add new chapter/directory iso document.')

# Rename command
ren_parser = subparsers.add_parser('rename', aliases=['r','re','ren'], help='Rename a document')
ren_parser.add_argument('in_number', type=int, help='The current sorting number of document to rename.')
ren_parser.add_argument('out_number', type=int, help='The new sorting number of the document to rename.')
ren_parser.add_argument('title', nargs='?', help='The new title of the document. If left empty, the old title will be used.')
ren_parser.add_argument('-d', '--directory', nargs='?', default=".", help='The base directory.')


add_parser.set_defaults(func=create)
ren_parser.set_defaults(func=rename)
args = argparse.parse_args()
#argcomplete.autocomplete(argparse)




def main(args):
    args.func(args)
if __name__ == "__main__":
    main(args) 
