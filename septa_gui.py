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
    
    def __init__(self, directory_list, parent=None):
        '''
        Build Septa Gui
        parent = parent control
        directory_list = directory list containing bus then rail directory
        '''
        # Save initial grame
        self.root = tk.Frame.__init__(self,parent)
        self.directory_list = directory_list
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
                           command=self.LoadRoutesListbox,
                           value=val).pack(anchor=tk.W)
                       
        # Create Frame for Routes Listbox            
        self.septa_routes_frame = tk.Frame(self.root)
        self.septa_routes_frame.pack()
        
        # Create Label for Routes Listbox
        self.septa_routes_frame_label = tk.Label(self.septa_routes_frame, 
                                                 text="Route Names:",
                                                 justify = tk.LEFT).pack()

        # Create and link Routes Listbox and Scrollbar
        self.septa_routes_listbox = tk.Listbox(self.septa_routes_frame, width=20, height=10)
        self.septa_routes_listbox.pack(side="left", fill="y")
        self.septa_routes_scrollbar = tk.Scrollbar(self.septa_routes_frame, orient="vertical")
        self.septa_routes_scrollbar.config(command=self.septa_routes_listbox.yview)
        self.septa_routes_scrollbar.pack(side="right", fill="y")
        self.septa_routes_listbox.config(yscrollcommand=self.septa_routes_scrollbar.set, 
                                         height=20, width=40)
        
    def LoadRoutesListbox(self):
        '''
        Load Listbox with bus or rail lines based on radio button choice
        '''
        # Clear previous contets
        self.septa_routes_listbox.delete(0, "end")
        
        # CSV file to read
        csv_file_name = 'routes.csv'
                
        # Check for Bus or Rail
        if (self.transport_selection.get() == 0):                     # === Bus
            # Specify index
            FIELD_WANTED_INDEX = 2   # 'route_long_name'
            
            # Change directory
            os.chdir(self.directory_list[0])
                
        else:                                                        # === Rail
            # Specify index
            FIELD_WANTED_INDEX = 1  # 'route_short_name'
            
            # Change directory
            os.chdir(self.directory_list[1])
            
        # Load bus or train routes
        self.LoadListboxItemsFromCsvFile(self.septa_routes_listbox, csv_file_name, FIELD_WANTED_INDEX)
        
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