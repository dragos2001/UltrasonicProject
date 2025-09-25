# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 10:23:33 2025

@author: BRD5CLJ
"""
import sys
import tkinter as tk
from tkinter import filedialog as fd

class FileHandler:
    
    def __init__(self):
        pass
   
    def select_file(self):
        root=tk.Tk()
        root.withdraw()
        
        file=fd.askopenfilename(title="Open file")
        if file:
            root.destroy()
            return file
        else:
            root.destroy()
            print("No template selected")
        
    def select_directory(self,title):
        root=tk.Tk()
        root.withdraw()
        directory = fd.askdirectory(title=title)
        
        if directory:
            root.destroy()
            return directory
        else:
            root.destroy()
            print("No directory selected")
    
    def select_files(self):
        root=tk.Tk()
        root.withdraw()
        files=fd.askopenfilenames(title="Select Directory")
        
        if files:
            root.destroy()
            return files
        else:
            root.destroy()
            print("No files selected")