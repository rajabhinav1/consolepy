import pandas as pd
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog



class TableCollection(object):
    def __init__(self, tables):
        self.tables = tables
        pd_tables = []
        for table in self.tables:
            pd_tables.append(table.pd_table)

        self.groupTable = pd.concat(pd_tables)
        self.__Setup()


    def __Setup(self):
        self.modules   = self.groupTable["Module"].unique()
        self.lecturers = self.groupTable["Allocated Staff Name"].unique()
        self.locations = self.groupTable["Zone Name"].unique()

    def ToExcel(self):
        writer = pd.ExcelWriter('table.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter excel
        self.filteredTable.to_excel(writer, sheet_name='Sheet1')

        # Close the excel writer and output the excel file
        writer.save()

    def ToPDF(self):
        # Convert the dataframe to an html string
        html = self.filteredTable.to_html()

        # Initialize PDF document
        doc = QTextDocument()
        doc.setHtml(html)

        # Initialize PDF writer
        printer = QPrinter()
        printer.setOutputFileName("table.pdf")
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageSize(QPrinter.A4)

        # Print HTML to PDF file
        doc.print_(printer)
    
    def FilterModule(self):
        # Print available modules 
        for i in range(len(self.modules)):
            print("Module: {0} ({1}): ".format(self.modules[i], i))

        # Prompt user
        prompt = input().lower()
        try:
            prompt = int(prompt)
            if(prompt < len(self.modules) and prompt >= 0):
                # Apply filter
                self.__Filter("Module", self.modules[prompt])
        except ValueError:
            print("Invalid value ({0})".format(prompt))

    def FilterLecturer(self):
        # Print available lectureres 
        for i in range(len(self.lecturers)):
            print("Lecturer: {0} ({1}): ".format(self.lecturers[i], i))

        # Prompt user
        prompt = input().lower()
        try:
            prompt = int(prompt)
            if(prompt < len(self.lecturers) and prompt >= 0):
                # Apply filter
                self.__Filter("Allocated Staff Name", self.lecturers[prompt])
        except ValueError:
            print("Invalid value ({0})".format(prompt))

    def FilterLocation(self):
        # Print available locations 
        for i in range(len(self.locations)):
            print("Location: {0} ({1}): ".format(self.locations[i], i))
        
        # Prompt user
        prompt = input().lower()
        try:
            prompt = int(prompt)
            if(prompt < len(self.locations) and prompt >= 0):
                # Apply filter
                self.__Filter("Zone Name", self.locations[prompt])
        except ValueError:
            print("Invalid value ({0})".format(prompt))


    


    def __Filter(self, field, value):
        # Get filter condition
        _filter = self.groupTable[field] == value

        # Filter table
        self.filteredTable = self.groupTable[_filter]

        # Prompt user for input
        while True:
            # Print the table
            print(self.filteredTable)
            prompt = input("Save (s) - Sort (r) - Go back (g): ").lower()

            # Save
            if(prompt == "s"):
                # Save as excel and pdf
                self.ToExcel()
                self.ToPDF()
                print("Table has been saved as a PDF and XLSX")
                break
            # Sort
            elif(prompt == "r"):
                # Seperator
                print("-"*10)

                # Print columns
                for i in range(len(self.filteredTable.columns)):
                    print("{0} {1}: ".format(self.filteredTable.columns[i], i))
                
                # Seperator
                print("-"*10)
                innerPrompt = input("""
Type the id of field(s) to sort by seperated by a hyphen '-'\n
Example: 0 - 3 - 6: 
Input: """)

                # Get fields id
                fields = [x.strip() for x in innerPrompt.split("-")]

                sortCol = []
                try:
                    # Get fields
                    [sortCol.append(self.filteredTable.columns[int(x)]) for x in fields]

                    # Prompt user for sort order
                    sortOrder = int(input("Ascending (0) - Descending (1): ").lower()) == 0
                    self.filteredTable = self.filteredTable.sort_values(sortCol, axis=0, ascending=sortOrder)
                except:
                    print("Invalid Id or formation")
            elif(prompt == "g"):
                break
            else:
                pass
