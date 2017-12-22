# -*- coding: utf-8 -*-
"""
SEPTA Data Project

Read zip files and convert contents to CSV files
"""

import zipfile
import csv
import os

def read_and_print_first_lines_from_zipped_file(zipfilename, limit):
    """
    Reads zip file and prints the first limit lines from each file contained in the zip file
    zipfilename = zip file name (such as 'example.zip')
    limit = number of lines to print in file
    """
    print()
    print("CONTENTS OF ZIP FILE " + zipfilename + ":")
    print()
    with zipfile.ZipFile(zipfilename, 'r') as z:
        file_name_list = sorted(z.namelist())
        for file in file_name_list:
            print(file)
            with z.open(file, 'r') as input_file:
                for line_number, line in enumerate(input_file):
                    if line_number > limit:
                        break
                    print(line)
            print()
    print()

def process_zip_files(zip_file_list, num_lines):  
    """
    Read zip files and convert each file to csv file
    zip_file_list = list of zip files containing data to be converted
    num_lines     = number of lines to display from each file
    Return list of directories containing the zip files
    """
    # Loop through zip files
    directory_name_list = []
    for file in zip_file_list:
        # Read the zip files and display some file contents
        if __debug__:
            read_and_print_first_lines_from_zipped_file(file, num_lines)

        # Extract zip file contents
        directory_name = os.path.splitext(file)[0]
        directory_name_list.append(directory_name)
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(directory_name)

        # Convert txt files to csv files
        os.chdir(directory_name)
        for input_file in os.listdir('.'):
            with open(input_file, 'r') as in_file:
                stripped = (line.strip() for line in in_file)
                lines = (line.split(",") for line in stripped if line)
                output_file = os.path.splitext(input_file)[0] + ".csv"
                if __debug__:
                    print("Convert " + input_file + " contents to " + output_file)
                with open(output_file, 'w', ) as out_file:
                    writer = csv.writer(out_file, lineterminator = '\n')
                    writer.writerows(lines)
            
        # Remove original text files
        for item in os.listdir('.'):
            if item.endswith(".txt"):
                os.remove(item)

        os.chdir('..')
        
    return directory_name_list