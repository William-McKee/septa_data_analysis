# -*- coding: utf-8 -*-
"""
SEPTA Data Project

Build and handle GUI functionality
"""

import tkinter as tk
from operator import itemgetter
import csv
import os

class Septa_Gui_Frame(tk.Frame):
    '''Septa Gui'''
    
    def __init__(self,parent=None):
        '''Build Septa Gui'''
        # Save initial grame
        self.root = tk.Frame.__init__(self,parent)
        self.parent = parent
        
        # Initial window settings
        self.winfo_toplevel().title("SEPTA Data Exploration")
        self.winfo_toplevel().geometry('300x450')
        
        # Radio Button Settings
        self.transport_choices = ["Bus", "Rail"]
        self.transport_selection = tk.IntVar()
        self.transport_selection.set(0)
        
        # Create Label for transportation choices
        self.septa_transport_label = tk.Label(self.root, 
                                              text="Select Transportation Type:",
                                              justify = tk.LEFT).pack()
        
        # Add transportation choices radio buttons
        for val, language in enumerate(self.transport_choices):
            tk.Radiobutton(self.root, 
                           text=language,
                           padx = 20, 
                           variable=self.transport_selection, 
                           command=self.LoadListbox,
                           value=val).pack(anchor=tk.W)
            
        # Create label for Listbox
        self.septa_listbox_label = tk.Label(self.root, 
                                            text="Route Names:",
                                            justify = tk.LEFT).pack()
            
        # Create Frame for Listbox            
        self.septa_listbox_frame = tk.Frame(self.root)
        self.septa_listbox_frame.pack()

        # Create and link listbox and scrollbar
        self.septa_listbox = tk.Listbox(self.septa_listbox_frame, width=20, height=10)
        self.septa_listbox.pack(side="left", fill="y")
        self.septa_scrollbar = tk.Scrollbar(self.septa_listbox_frame, orient="vertical")
        self.septa_scrollbar.config(command=self.septa_listbox.yview)
        self.septa_scrollbar.pack(side="right", fill="y")
        self.septa_listbox.config(yscrollcommand=self.septa_scrollbar.set, 
                                  selectmode=tk.EXTENDED, height=20, width=40)
        
    def LoadListbox(self):
        '''
        Load Listbox with bus or rail lines based on radio button choice
        TODO: Pass directories into this class
        '''
        # Clear previous contets
        self.septa_listbox.delete(0, "end")
        
        # CSV file to read
        csv_file_name = 'routes.csv'
                
        # Check for Bus or Rail
        if (self.transport_selection.get() == 0):                     # === Bus
            # Specify index
            FIELD_WANTED_INDEX = 2   # 'route_long_name'
            
            # Change directory
            os.chdir('septa_bus_gfts')
                
        else:                                                        # === Rail
            # Specify index
            FIELD_WANTED_INDEX = 1  # 'route_short_name'
            
            # Change directory
            os.chdir('septa_rail_gfts')
            
        # Load bus or train routes
        self.LoadListboxItemsFromCsvFile(self.septa_listbox, csv_file_name, FIELD_WANTED_INDEX)
        
        # Change back to original directory        
        os.chdir('..')
        
    def LoadListboxItemsFromCsvFile(self, listbox_control, csv_file_name, sort_index):
        '''
        Read CSV File and Load Listbox based on sorting index
        listbox_control = Listbox to be loaded with items
        csv_file_name   = CSV file containing rows to be loaded
        sort_index      = Index of CSV file column containing items
        '''
        routes_data_list = []
        with open(csv_file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            routes_data_list = sorted(list(reader), key=itemgetter(sort_index))
            
        # We only need one column for Listbox
        for item in routes_data_list:
            listbox_control.insert("end", item[sort_index])