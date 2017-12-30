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
            
        # Routes Listbox construction
        self.septa_routes_frame = tk.Frame()
        self.septa_routes_frame_label = tk.Label()
        self.septa_routes_listbox = tk.Listbox()
        self.septa_routes_scrollbar = tk.Scrollbar()
        self.septa_routes_frame, self.septa_routes_frame_label, self.septa_routes_listbox, self.septa_routes_scrollbar = \
            self.BuildListboxFrame(self.septa_routes_frame,
                               self.septa_routes_frame_label, 
                               self.septa_routes_listbox, 
                               self.septa_routes_scrollbar, 
                               self.LoadSchedules,
                               "Route Names:", grid_row, 0, 20, 40)
        
        # Schedules Listbox construction
        self.septa_schedules_frame = tk.Frame()
        self.septa_schedules_frame_label = tk.Label()
        self.septa_schedules_listbox = tk.Listbox()
        self.septa_schedules_scrollbar = tk.Scrollbar()
        self.septa_schedules_frame, self.septa_schedules_frame_label, self.septa_schedules_listbox, self.septa_schedules_scrollbar = \
            self.BuildListboxFrame(self.septa_schedules_frame,
                               self.septa_schedules_frame_label, 
                               self.septa_schedules_listbox, 
                               self.septa_schedules_scrollbar, 
                               self.LoadMap,
                               "Schedules:", grid_row, 1, 20, 100)
            
        # LoadSchedules/LoadMap flag
        self.MAP_LOAD = 0
        
    def BuildListboxFrame(self, our_frame, our_label, our_listbox, our_scrollbar, 
                          callback_function, our_labeltext, grid_row, grid_column,
                          our_listbox_height, our_listbox_width):
        '''
        Add Frame to GUI.  Frame contains label, listbox, and associated scrollbar.
        
        our_frame = Frame widget object
        our_label = Label widget object
        our_listbox = Listbox widget object
        our_scrollbar = Scrollbar widget object
        callback_function = Function called when user clicks listbox entry
        our_labeltext = Label Text
        grid_row = Frame's grid row location
        grid_column = Frame's grid column location
        our_listbox_height = Height of listbox widget
        our_listbox_width = Width of listbox widget
        
        Returns newly added Frame, Label, Listbox, and Scrollbar widgets
        '''
        # Create frame
        our_frame = tk.Frame(self.root)
        our_frame.grid(row=grid_row, column=grid_column, padx=10)
        
        # Create label for listbox
        our_label = tk.Label(our_frame, text=our_labeltext, justify = "left").pack()

        # Create and link listbox and scrollbar
        our_listbox = tk.Listbox(our_frame, width=20, height=10)
        our_listbox.pack(side="left", fill="y")
        our_scrollbar = tk.Scrollbar(our_frame, orient="vertical")
        our_scrollbar.config(command=our_listbox.yview)
        our_scrollbar.pack(side="right", fill="y")
        our_listbox.config(yscrollcommand=our_scrollbar.set,
                           height=our_listbox_height,
                           width=our_listbox_width)
        our_listbox.bind('<<ListboxSelect>>', callback_function)
        return our_frame, our_label, our_listbox, our_scrollbar
        
    def LoadRoutesListbox(self):
        '''
        Load Listbox with bus or rail lines based on radio button choice
        '''
        # Clear previous contets
        self.septa_routes_listbox.delete(0, "end")
        
        # CSV file to read
        csv_file_name = 'routes.csv'
        
        # Initialize
        sort_index = -1
        show_index_list = []
                
        # Check for Bus or Rail
        if (self.transport_selection.get() == 0):                     # === Bus
            # Specify index
            sort_index = 0                # 'route_id'
            show_index_list.append(0)     # 'route_id'
            show_index_list.append(2)     # 'route_long_name'
            
            # Change directory
            os.chdir(self.directory_list[0])
                
        else:                                                        # === Rail
            # Specify index
            sort_index = 1                # 'route_short_name'
            show_index_list.append(1)     # 'route_short_name'
            
            # Change directory
            os.chdir(self.directory_list[1])
            
        # Load bus or train routes
        self.LoadListboxItemsFromCsvFile(self.septa_routes_listbox, csv_file_name, 
                                         sort_index, show_index_list)
        
        # Change back to original directory        
        os.chdir('..')
        
    def LoadListboxItemsFromCsvFile(self, listbox_control, csv_file_name, 
                                    sort_index, show_index_list):
        '''
        Read CSV File and Load Listbox based on sorting index
        listbox_control = Listbox to be loaded with items
        csv_file_name   = CSV file containing rows to be loaded
        sort_index      = Sort items by this CSV column index
        show_index_list = List of CSV column indexes to show in Listbox
        '''
        routes_data_list = []
        with open(csv_file_name, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            routes_data_list = sorted(list(reader), key=itemgetter(sort_index))
            
        # Show only the specified items from index list
        for item in routes_data_list:
            item_to_insert = ""
            for index in show_index_list:
                item_to_insert += item[index] + "  "
            listbox_control.insert("end", item_to_insert.strip())
            
    def LoadSchedules(self, event):
        '''
        Load Schedule for selected train or bus line
        event = event object provided by Tkinter
        '''
        
        # Clear previous contents
        self.septa_schedules_listbox.delete(0, "end")
        
        # TODO: Cleaner resolution of this issue?
        if (self.MAP_LOAD): # LoadMap invoked do not proceed here!
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