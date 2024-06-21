import json
from Helper import ___PATH___, ___FILE___LINE, log, level0,level1,level2,level3, getMonth, getShortMonth, getnumMonth

from Helper import OPTION1, OPTION2, OPTION3, OPTION4
from DisplayTable import *
class ConfigTable():
    def __init__(self, option) -> None:
        self.srcPath = ___PATH___()
        self.srcPath = self.srcPath.replace('src', '')
        self.Configfile = self.srcPath + 'configurations\\config.json'
        self.ReportingPath = self.srcPath + 'Reports\\'
        self.TemplatePath = self.srcPath + 'Template\\'
        self.option = option
        #self.construct()
        self.h = []
        self.data = []
        self.title = ''

    def getCategoryData(self):
        log("Getting Expense Categories Data" + ___FILE___LINE(), level3)
        heading = ['Category', 'Category definition']
        catdata = []
        with open(self.Configfile, 'r') as f:
            data = json.load(f)
            CategoriesList = data['ExpenseCategories'].keys()
            catdef = data['ExpenseCategories'].copy()
            for cat in CategoriesList:
                lst = [cat, catdef[cat]]
                catdata.append(lst)
        return heading, catdata
    
    def getBillsData(self):
        log("Getting Bills Data" + ___FILE___LINE(), level3)
        heading = ['Bills', 'Bills definition']
        billdata = []
        with open(self.Configfile, 'r') as f:
            data = json.load(f)
            BillsList = data['Bills'].keys()
            billdef = data['Bills'].copy()
            for bill in BillsList:
                lst = [bill, billdef[bill]]
                billdata.append(lst)
        return heading, billdata
    
    def getGroceryData(self):
        log("Getting Grocery Data" + ___FILE___LINE(), level3)
        heading = ['Grocery', 'Grocery definition']
        Grocerydata = []
        with open(self.Configfile, 'r') as f:
            data = json.load(f)
            GroceryList = data['Grocery Distribution'].keys()
            Grocerydef = data['Grocery Distribution'].copy()
            for Grocery in GroceryList:
                lst = [Grocery, Grocerydef[Grocery]]
                Grocerydata.append(lst)
        return heading, Grocerydata
    
    def getUtilityData(self):
        log("Getting Utilities Data" + ___FILE___LINE(), level3)
        heading = ['Utility', 'Utility definition']
        Utilitydata = []
        with open(self.Configfile, 'r') as f:
            data = json.load(f)
            UtilityList = data['Utility Distribution'].keys()
            Utilitydef = data['Utility Distribution'].copy()
            for Utility in UtilityList:
                lst = [Utility, Utilitydef[Utility]]
                Utilitydata.append(lst)
        return heading, Utilitydata
    
    def Configure(self):
        log("Entering Configuration" + ___FILE___LINE(), level3)
        if self.option == OPTION1:
            self.h, self.data = self.getCategoryData()
        elif self.option == OPTION2:
            self.h, self.data = self.getBillsData()
        elif self.option == OPTION3:
            self.h, self.data = self.getUtilityData()
        elif self.option == OPTION4:
            self.h, self.data = self.getGroceryData()
            self.title = f'{self.option} Configuration'

        #root = window.TKroot
        root = tk.Tk()
        app = DisplayTable(parent = root, title=self.title, data=self.data)
        app.pack(fill='both')
        root.mainloop()
   

if __name__ == '__main__' :
    app = ConfigTable(OPTION1)
    app.Configure()
    
    