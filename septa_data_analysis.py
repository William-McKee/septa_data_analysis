"""
SEPTA Data Set from transitfeeds.com
William McKee
December 2017
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
    print("CONTENTS OF ZIP FILE " + zipfilename + ":")
    print()
    with zipfile.ZipFile(zipfilename, 'r') as z:
        file_name_list = sorted(z.namelist())
        for file in file_name_list:
            with z.open(file, 'r') as input_file:
                for line_number, line in enumerate(input_file):
                    if line_number > limit:
                        break
                    print(line)
            print()
    print()

# Loop through zip files
NUM_LINES = 5
ZIP_FILE_NAMES = ['septa_bus_gfts.zip', 'septa_rail_gfts.zip']
for file in ZIP_FILE_NAMES:
    # Read the zip files and display some file contents
    read_and_print_first_lines_from_zipped_file(file, NUM_LINES)

    # Extract zip file contents
    directory_name = os.path.splitext(file)[0]
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(directory_name)

    # Convert txt files to csv files
    os.chdir(directory_name)
    for input_file in os.listdir('.'):
        with open(input_file, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            output_file = os.path.splitext(input_file)[0] + ".csv"
            print("Convert " + input_file + " contents to " + output_file)
            with open(output_file, 'w', ) as out_file:
                writer = csv.writer(out_file, lineterminator = '\n')
                writer.writerows(lines)
            
    # Remove original text files
    for item in os.listdir('.'):
        if item.endswith(".txt"):
            os.remove(item)

    os.chdir('..')