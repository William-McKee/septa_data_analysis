# -*- coding: utf-8 -*-
"""
SEPTA Data Project

Build and handle GUI functionality
"""

import tkinter as tk

class Septa_Gui_Frame(tk.Frame):
    '''Septa Gui'''
    
    def __init__(self,parent=None):
        '''Initialize Septa Gui'''
        # Save initial grame
        self.root = tk.Frame.__init__(self,parent)
        self.parent = parent
        
        # Initialize Radio Buttons
        self.transport_choices = ["Bus", "Rail"]
        self.transport_selection = tk.IntVar()
        self.transport_selection.set(0)
        
        # Build widgets
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        '''Build Septa Gui'''
        # Initial window settings
        self.winfo_toplevel().title("SEPTA Data Exploration")
        self.winfo_toplevel().geometry('300x80')
        
        # Label for transportation choices
        tk.Label(self.root, 
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
            
    def ShowChoice(self):
        '''Dummy function'''
        print(self.transport_selection.get())