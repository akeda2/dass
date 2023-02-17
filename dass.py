#!/usr/bin/python3
# SHort program that concatenates text files in directories and subdirectories into one file.
# Usage: python dass.py [directory] [output file]
# The output file will be created if it does not exist. If it does exist, it will be overwritten.

import os
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python dass.py [directory] [output file]")
        return
    directory = sys.argv[1]
    output_file = sys.argv[2]
    output = open(output_file, 'w')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                input_file = open(os.path.join(root, file), 'r')
                output.write(input_file.read())
                output.write("...")
                input_file.close()
    output.close()
    