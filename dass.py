#!/usr/bin/python3
# SHort program that concatenates text files in directories and subdirectories into one file.
# Usage: python dass.py [directory] [output file]
# The output file will be created if it does not exist. If it does exist, it will be overwritten.

import os
import sys
import re
import io

def main():
    if len(sys.argv) != 3:
        print("Usage: python dass.py [directory] [output file]")
        return
    directory = sys.argv[1]
    print(directory)
    output_file = sys.argv[2]
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
    print(directories)
    print(files)
    last_chapter = ""
    for file in files:
        #print(file)
        #output.write(file)
        #print(dirpath + '...' + file)
        chapter ="\n\n" + re.sub("^\d+", "", os.path.dirname(os.path.normpath(file))) + "\n\n"
        if chapter != last_chapter:
            #writeonce = True
            output.write(chapter)
            last_chapter = chapter
        if file.endswith(".txt"):
            input_file = open(os.path.join(file), 'r')
            print(input_file.name)
            # Write the name of the file without extension to the output file.
            output.write("\n\n" + re.sub("^\d+", "", os.path.splitext(os.path.basename(input_file.name))[0]) + "\n\n")
            output.write(input_file.read())
            # print the filename of the file that is being concatenated to the output file.
            input_file.close()
    output.close()

if __name__ == "__main__":
    main() 
