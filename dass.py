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
argparse.add_argument('output_name', help='Output file with .text-extension to create. If it exists, it will be overwritten.')
argparse.add_argument('-m', '--markdown', action='store_true', help='Use Markdown syntax for headers. Outputs a .md file.')
argparse.add_argument('-w', '--html', action='store_true', help='Convert output into HTML. Outputs a .html file.')
argparse.add_argument('-t', '--title', help='Custom title for the output file.')
argparse.add_argument('-b', '--disable_bom', action='store_true', help='Disable the Byte Order Mark (BOM) in the output file.')
args = argparse.parse_args()


def main():
    #if len(sys.argv) != 3:
    #    print("Usage: python dass.py [directory] [output file]")
    #    return
    #directory = sys.argv[1]
    if args.html:
        args.markdown = True
    directory = os.path.normpath(args.directory)
    print(directory)
    #output_file = sys.argv[2]
    outname = os.path.normpath(args.output_name)
    output_text = os.path.normpath(outname + ".text")
    output_markdown = os.path.normpath(outname + ".md")
    output_html = os.path.normpath(outname + ".html")
    print(outname)
    if os.path.exists(output_text) or os.path.exists(output_markdown) or os.path.exists(output_html):
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
    #directories = []
    #files = []
    #for root, dirs, filenames in os.walk(directory, topdown=False):
        # The os.walk should sort the files and the directories in the order they are listed in the directory.
    #    directories.append(root)
    #    files.extend(os.path.join(dirs, f) for f in filenames)
    #    files = sorted(files)
    #    dirs = sorted(dirs)
    out_buf_md = ''
    out_buf_text = ''
    if args.title:
        if args.markdown:
            #output.write("# " + args.title + "\n\n")
            out_buf_md += "# " + args.title + "\n\n"
        
        #output.write(args.title + "\n\n")
        out_buf_text += args.title + "\n\n"
    print(directories)
    print(files)
    last_chapter = ''
    for file in files:
        #print(file)
        #output.write(file)
        #print(dirpath + '...' + file)
        if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            print(input_file.name)
            temp_buf = ''
            for line in input_file.readlines():
                lex = shlex.shlex(line)
                lex.whitespace = ''
                line = ''.join(list(lex))
                if not line:
                    print("Found comment line: " + line + " Skipping.")
                    continue
                #temp_out_buf_md += line
                #temp_out_buf_text += line
                temp_buf += line

            chapter = re.sub("^\d+", "", os.path.dirname(os.path.normpath(input_file.name)))
            print("Current filename: " + input_file.name)
            print("Chapter: " + chapter + " Last chapter: " + last_chapter)
            if chapter != last_chapter:
                print("+Chapter: " + chapter)
                if args.markdown:
                    #output.write("\n\n" + "## " + chapter + "\n\n")
                    out_buf_md += "\n\n" + "## " + chapter + "\n\n"
                
                #output.write("\n\n" + chapter + "\n\n")
                out_buf_text += "\n\n" + chapter + "\n\n"
                last_chapter = chapter

        #if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            print("Input file for rubrik: " + input_file.name)
            # Write the name of the file without extension to the output file.
            if args.markdown:
                #output.write("\n\n" + "### " + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n")
                out_buf_md += "\n\n" + "### " + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n"
                out_buf_md += temp_buf
            
            #output.write("\n\n" + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n")
            out_buf_text += "\n\n" + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n"
            out_buf_text += temp_buf
            #output.write(out_buff)
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
    out_text.write(out_buf_text)
    out_text.close()
    if args.markdown:
        out_md.write(out_buf_md)
        out_md.close()
    if args.html:
        out_html.write(markdown.markdown(out_buf_md, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite']))
        """ # Read the output file into a string.
        output.close()
        output = open(output_file, 'r', encoding='utf-8-sig')
        output_string = output.read()
        output.close()
        output_html = open(output_file, 'w', encoding='utf-8-sig')
        output.write(markdown.markdown(output_string, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])) """
        out_html.close()

if __name__ == "__main__":
    main() 
