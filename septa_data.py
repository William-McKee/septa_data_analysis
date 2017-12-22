# -*- coding: utf-8 -*-
"""
SEPTA Data Project

Main Program
"""

from zip_file_processing import process_zip_files

# Convert zip file contents to CSV
num_lines = 5
zip_file_names = ['septa_bus_gfts.zip', 'septa_rail_gfts.zip']
directory_names = process_zip_files(zip_file_names, num_lines)

if __debug__:
    print("Directory List:")
    print(directory_names)

# TODO: Add GUI