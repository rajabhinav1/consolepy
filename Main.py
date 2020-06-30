import pandas as pd
import glob
import sys
from PyQt5.QtWidgets import QApplication 
from Table import *
from TableCollection import *

def Main():
    # Get tables
    directory = input("Raw file's directory: ")
    tables = []
    files = glob.glob(directory+"\\*.csv")
    if(len(files) == 0):
        print("No files were found.")
        exit(0)
    for file in files:
        table = Table()
        table.Populate(file)
        tables.append(table)

    # Make a collection of provided tables
    collection = TableCollection(tables)

    # Prompt user for input
    Prompt(collection)



def Prompt(collection):
    while True:
        prompt = input("List by module (1) - List by lecturer (2) - List by location (3) | Quit (q): ").lower()
        if(prompt == "1"):
            collection.FilterModule()
        elif (prompt == "2"):
            collection.FilterLecturer()
        elif(prompt == "3"):
            collection.FilterLocation()
        elif(prompt == "q"):
            quit()
        else:
            print("Invalid operation ({0})".format(prompt))


if __name__ == "__main__":
    app = QApplication([])
    Main()