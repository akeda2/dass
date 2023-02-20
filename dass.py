#!/usr/bin/python3
# SHort program that concatenates text files in directories and subdirectories into one file.
# Usage: python dass.py [directory] [output file]
# The output file will be created if it does not exist. If it does exist, it will be overwritten.

import os
#import sys
import re
#import io
import shlex
import argparse
import markdown

argparse = argparse.ArgumentParser(description='Concatenate text files in directories and subdirectories into one file.')
argparse.add_argument('directory', help='The directory to concatenate.')
argparse.add_argument('output_file', help='The output file to create.')
argparse.add_argument('-m', '--markdown', action='store_true', help='Use Markdown syntax for headers.')
argparse.add_argument('-w', '--html', action='store_true', help='Convert output into HTML. Useful for markdown output.')
argparse.add_argument('-t', '--title', help='Custom title for the output file.')
argparse.add_argument('-b', '--disable_bom', action='store_true', help='Disable the Byte Order Mark (BOM) in the output file.')
args = argparse.parse_args()


def main():
    #if len(sys.argv) != 3:
    #    print("Usage: python dass.py [directory] [output file]")
    #    return
    #directory = sys.argv[1]
    directory = os.path.normpath(args.directory)
    print(directory)
    #output_file = sys.argv[2]
    output_file = os.path.normpath(args.output_file)
    print(output_file)
    if os.path.exists(output_file):
        print("Output file exists. It will be overwritten.")
    output = open(output_file, 'w', encoding='utf-8-sig')

    directories = []
    files = []
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        directories.append(dirpath)
        files.extend(os.path.join(dirpath, f) for f in filenames)

    directories = sorted(directories)
    files = sorted(files)
    #directories = []
    #files = []
    #for root, dirs, filenames in os.walk(directory, topdown=False):
        # The os.walk should sort the files and the directories in the order they are listed in the directory.
    #    directories.append(root)
    #    files.extend(os.path.join(dirs, f) for f in filenames)
    #    files = sorted(files)
    #    dirs = sorted(dirs)
    if args.title:
        if args.markdown:
            output.write("# " + args.title + "\n\n")
        else:
            output.write(args.title + "\n\n")
    print(directories)
    print(files)
    last_chapter = ''
    for file in files:
        #print(file)
        #output.write(file)
        #print(dirpath + '...' + file)
        if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            out_buff = ''
            for line in input_file.readlines():
                lex = shlex.shlex(line)
                lex.whitespace = ''
                line = ''.join(list(lex))
                if not line:
                    continue
                out_buff += line

        chapter = re.sub("^\d+", "", os.path.dirname(os.path.normpath(file)))
        if chapter != last_chapter:
            #writeonce = True
            if args.markdown:
                output.write("\n\n" + "## " + chapter + "\n\n")
            else:
                output.write("\n\n" + chapter + "\n\n")
            last_chapter = chapter
        if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            print(input_file.name)
            # Write the name of the file without extension to the output file.
            if args.markdown:
                output.write("\n\n" + "### " + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n")
            else:
                output.write("\n\n" + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n")
            output.write(out_buff)
            """ for line in input_file.readlines():
                lex = shlex.shlex(line)
                lex.whitespace = '' # if you want to strip newlines, use '\n'
                line = ''.join(list(lex))
                if not line:
                    continue
                # process decommented line
                # fields = shlex.split(line, comments=True)
                #if not fields:
                #    continue
                
                output.write(line)

                #output.write(input_file.read()) """
            # print the filename of the file that is being concatenated to the output file.
            input_file.close()
    if args.html:
        # Read the output file into a string.
        output.close()
        output = open(output_file, 'r', encoding='utf-8-sig')
        output_string = output.read()
        output.close()
        output = open(output_file, 'w', encoding='utf-8-sig')
        output.write(markdown.markdown(output_string, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite']))
    output.close()

if __name__ == "__main__":
    main() 
