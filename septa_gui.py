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
        self.winfo_toplevel().geometry('925x450')
        
        # Radio Button Settings
        self.transport_choices = ["Bus", "Rail"]
        self.transport_selection = tk.IntVar()
        self.transport_selection.set(0)
        
        # Keep track of grid rows
        grid_row = 0
        
        # Create Label for transportation choices
        self.septa_transport_label = tk.Label(self.root, text="Select Transportation Type:")
        self.septa_transport_label.grid(row=grid_row, column=0, sticky="w", padx=10)
        
        # Add transportation choices radio buttons
        grid_row += 1
        for val, language in enumerate(self.transport_choices):
            thisRb = tk.Radiobutton(self.root, text=language, padx = 20, variable=self.transport_selection, 
                           command=self.LoadRoutesListbox, value=val)
            thisRb.grid(row=grid_row, column=0, sticky="w")
            grid_row += 1
                       
        # Create Frame for Routes Listbox            
        self.septa_routes_frame = tk.Frame(self.root)
        self.septa_routes_frame.grid(row=grid_row, column=0, padx=10)
        
        # Create Label for Routes Listbox
        self.septa_routes_frame_label = tk.Label(self.septa_routes_frame, 
                                                 text="Route Names:",
                                                 justify = "left").pack()

        # Create and link Routes Listbox and Scrollbar
        self.septa_routes_listbox = tk.Listbox(self.septa_routes_frame, width=20, height=10)
        self.septa_routes_listbox.pack(side="left", fill="y")
        self.septa_routes_scrollbar = tk.Scrollbar(self.septa_routes_frame, orient="vertical")
        self.septa_routes_scrollbar.config(command=self.septa_routes_listbox.yview)
        self.septa_routes_scrollbar.pack(side="right", fill="y")
        self.septa_routes_listbox.config(yscrollcommand=self.septa_routes_scrollbar.set,
                                         height=20, width=40)
        self.septa_routes_listbox.bind('<<ListboxSelect>>', self.LoadSchedules)
        
        # TODO: One function for Routes and Schedule Frames
        # Create Frame for Schedules ListBox
        self.septa_schedules_frame = tk.Frame(self.root)
        self.septa_schedules_frame.grid(row=grid_row, column=1, padx=10)
        
        # Create Label for Schedules Listbox
        self.septa_schedules_frame_label = tk.Label(self.septa_schedules_frame, 
                                                    text="Schedules:",
                                                    justify = "left").pack()
        
        # Create and link Schedule Listbox and Scrollbar
        self.septa_schedules_listbox = tk.Listbox(self.septa_schedules_frame, width=20, height=10)
        self.septa_schedules_listbox.pack(side="left", fill="y")
        self.septa_schedules_scrollbar = tk.Scrollbar(self.septa_schedules_frame, orient="vertical")
        self.septa_schedules_scrollbar.config(command=self.septa_schedules_listbox.yview)
        self.septa_schedules_scrollbar.pack(side="right", fill="y")
        self.septa_schedules_listbox.config(yscrollcommand=self.septa_schedules_scrollbar.set, 
                                           height=20, width=100)
        self.septa_schedules_listbox.bind('<<ListboxSelect>>', self.LoadMap)
        self.MAP_LOAD = 0
        
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
            FIELD_WANTED_INDEX = 2  # 'route_long_name'
            
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
            
    def LoadSchedules(self, event):
        '''
        Load Schedule for selected train or bus line
        event = event object provided by Tkinter
        '''
        
        # Clear previous contents
        self.septa_schedules_listbox.delete(0, "end")
            
        if (self.MAP_LOAD): # LoadMap invoked do not proceed here! TODO: Cleaner resolution of this issue?
            # Clear Loaded Map
            self.MAP_LOAD = 0
        else:  
            # Get selected item
            w = event.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            print('You selected item %d: "%s"' % (index, value))

            # TODO: Load Schedules
            # Load Dummy Contents for now
            items = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            for item in items:
                self.septa_schedules_listbox.insert("end", item)
            
    def LoadMap(self, event):
        '''
        Load Map for selected train or bus schedule
        event = event object provided by Tkinter
        '''
        # TODO: Load Map
        # Get selected item
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.MAP_LOAD = 1