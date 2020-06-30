import pandas as pd

class Table():
    # Populate pandas DataFrame
    def Populate(self, filename):
        self.pd_table = pd.read_csv(filename, index_col=0)
        try:
            self.pd_table.drop(columns="Description", inplace=True)
        except KeyError:
            pass
        self.__Setup()
    
    # Setup the DataFrame
    def __Setup(self):
        module  = []
        session = []
        for name in self.pd_table["Name"]:
            splitName = name.split("_")
            module.append(splitName[3])
            session.append(splitName[4])

        # Name isn't needed anymore
        self.pd_table.drop(columns="Name", inplace=True)
        self.pd_table.insert(0, "Module", module)
        self.pd_table.insert(1, "Session", session)