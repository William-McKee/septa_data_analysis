# -*- coding: utf-8 -*-
"""
SEPTA Data Project

Build and handle GUI functionality
"""

import tkinter as tk

class Septa_Gui_Frame(tk.Frame):
    '''Septa Gui'''
    
    def __init__(self,parent=None):
        '''Build Septa Gui'''
        # Save initial grame
        self.root = tk.Frame.__init__(self,parent)
        self.parent = parent
        
        # Initial window settings
        self.winfo_toplevel().title("SEPTA Data Exploration")
        self.winfo_toplevel().geometry('300x300')
        
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
                           command=self.ShowChoice,
                           value=val).pack(anchor=tk.W)
            
        # Create Frame for Listbox            
        self.septa_listbox_frame = tk.Frame(self.root)
        self.septa_listbox_frame.pack()

        # Create and link listbox and scrollbar
        self.septa_listbox = tk.Listbox(self.septa_listbox_frame, width=20, height=10)
        self.septa_listbox.pack(side="left", fill="y")
        self.septa_scrollbar = tk.Scrollbar(self.septa_listbox_frame, orient="vertical")
        self.septa_scrollbar.config(command=self.septa_listbox.yview)
        self.septa_scrollbar.pack(side="right", fill="y")
        self.septa_listbox.config(yscrollcommand=self.septa_scrollbar.set)

        
    def ShowChoice(self):
        '''
        Dummy function - how to populate list box
        TODO: Add pandas dataframe contents to listbox in lieu of this dummy data
        TODO: Pass directories into this class
        '''
        self.septa_listbox.delete(0, "end")
        if (self.transport_selection.get() == 0):
            lbitems = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
            for item in lbitems:
                self.septa_listbox.insert("end", item)
        else:
            lbitems = ["Sunday", "Monday", "Tuesday", "Wednesday",  
                       "Thursday", "Friday", "Saturday"]
            for item in lbitems:
                self.septa_listbox.insert("end", item)