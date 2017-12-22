# Septa Data Analysis

This code analyzes the data set for Septa Bus and Rail lines downloaded from https://transitfeeds.com.  I downloaded the SEPTA Bus zip file and renamed gfts.zip to septa_bus_gfts.zip.  I downloaded the SEPTA Rail zip file and renamed gfts.zip to septa_rail_gfts.zip.

## File Contents

1. **septa_data.py**: Python code for main program which allows user to explore SEPTA data
2. **zip_file_processing.py**: Python code reads zip file and converts files to CSV files
3. **septa_gui.py**: Python code handling GUI setup and events
4. **Septa_Data.ipynb**: Python code sample analyzing the SEPTA data set
5. **septa_bus_gfts.zip**: Zip file containing text files relating to SEPTA Bus Routes
6. **septa_rail_gfts.zip**: Zip file containing text files relating to SEPTA Rail Routes

All files shall be downloaded in the same directory.  ZIP file contents do not have to be extracted.

## Running the code

Open **septa_data.py** in any directory and run the program.

## Jupyter Notebook

You can also load and run the Jupyter Notebook in order to explore the data set.  Jupyter Notebook can be installed from [here](http://jupyter.org/).  Alternatively, install [Anaconda](https://www.continuum.io/downloads) and then launch Notebook from Anaconda.  Install for Python 3.X series.

1. Open Jupyter Notebook and open **Septa_Data.ipynb**.
2. Starting with the first Markdown block, hit `Shift-Enter` for each block to run the code.