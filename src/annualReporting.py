import os
import PySimpleGUI as sg
from Helper import ___PATH___, fileandline, log, level0,level1,level2,level3, getMonth, getShortMonth, getnumMonth
import Helper as hp
from Helper import OPTION1, OPTION2, OPTION3, OPTION4
#from Tabulation import *

from pdfReports import *
from pptxReports import *
import datetime
import re
from time import sleep
from datetime import date
from datetime import datetime, timedelta
from pathlib import Path
import csv
import sys
import shutil
import statistics as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm
import numpy as np
from matplotlib.patches import ConnectionPatch
import calendar
from fpdf import FPDF
import json
titlefont = {'family':'serif','color':'blue','size':20}
class Annual(): 
    progressbar = None  
    statementfolder = ''
    reportPath = ''
    reportArchivePath = ''
    annualStatementFolder = ''
    annualStatement = ''
    annualstament = 'annual_stmt.csv'
    annualstatmentFileList = [] # contains the list of all statement file
    currentyear = 2024
    currentMonth = 'January'
    months = []
    MontlyDistribution = {}
    MonthlyTotalExpenses = {} # amount spent per month
    MonthlyTotalExPerCat = {} # amount spent per month per category
    CategoriesList = [] # list of all categries of expenses
    configfile = ''
    ExpenseCategoriesdataDict = {} #categories data definition
    BillsList = []          #contains a list of bills
    BillDefinitionDict = {} # contain bill definitions
    BillDataDict = {}       # contains the bills values
    GroceryList = []          #contains a list of Groceres Store
    UtilitiesList = []
    UtilitiesDataDict = {}
    GroceryDefinitionDict = {} # contain Grocery Store definitions
    UtilitiesDefinitionDict = {}
    GroceryDataDict = {}       # contains the Grocery values
    MonthlyBillsDict = {}
    MonthlyGroceryDict = {}
    MonthlyUtilityDict = {}
    UpdatedSalariesDict = {}
    lastMonthofdata = 0
    BillMeans = {}  # contains all the bill means for all months
    totalbillsPermonth = []
    modifiedMonths = []
    theReport = None
    thepptxReport = None
    currentMonthNumber = 1
    monthsToNumber = {}
 # Mean values for the bills
    __Billsmean         = 0.0
    __Grocerymean       = 0.0
    __Gasmean           = 0.0
    __CCPaymentmean     = 0.0
    __Clothingmean      = 0.0
    __Utilitiesmean     = 0.0
    __Restaurantmean    = 0.0
    __TotalExpensemean  = 0.0
    __TatalSavingsmean  = 0.0

    def __init__(self) -> None:
        self.months = list(calendar.month_name)
        self.currentMonth,  self.currentyear = self.getCurrentMonthandYear()
        self.monthsToNumber = dict((month, index) for index, month in enumerate(calendar.month_name) if month)
        self.currentMonthNumber = self.monthsToNumber[self.currentMonth]
        self.theReport  = pdfReports(self.currentMonth, self.currentyear)
        self.thepptxReport = PPTXReport(self.currentMonth, self.currentyear)

        srcPath = ___PATH___()
        srcPath = srcPath.replace('src', '')
        self.configfile = srcPath + 'configurations\\config.json'
        self.reportPath = srcPath + 'Reports\\'
        self.reportArchivePath = srcPath + 'Reports\\Archives\\'
        with open(self.configfile, 'r') as f:
            self.CategoriesList.clear()
            self.BillsList.clear()
            self.GroceryList.clear()
            self.UtilitiesList.clear()
            self.BillDefinitionDict.clear()
            self.GroceryDefinitionDict.clear()
            data = json.load(f)
            self.CategoriesList = data['ExpenseCategories'].keys()
            self.ExpenseCategoriesdataDict = data['ExpenseCategories'].copy()
            self.BillsList = data['Bills'].keys()
            self.GroceryList = data['Grocery Distribution'].keys()
            self.UtilitiesList = data['Utility Distribution']
            self.BillDefinitionDict = data['Bills'].copy()
            self.GroceryDefinitionDict = data['Grocery Distribution'].copy()
            self.UtilitiesDefinitionDict = data['Utility Distribution'].copy()

    def setParent(self, parent: sg.Window):
        self.parent = sg.Window(parent)
        
    def Archive(self):
        log("Archiving old files" + fileandline(), level3)
        # create the new arche file name
        dtt = f'{datetime.now()}'
        for ele in [':', '-', '.', ' ']:
            dtt = dtt.replace(ele, '')
        zipfilename = self.reportArchivePath + dtt + '_Archive.zip'
        # get date time object for exactly x days - x is the number of days to keep files
        last_week = datetime.now() - timedelta(days = 1)
        #convert datetime object to timestamp
        timestamp = datetime.timestamp(last_week)

        #get list of file in the report directory
        files = [f for f in os.listdir(self.reportPath) if os.path.isfile(f) ]
        #iterate over the fils and get their created dates and times
        #for file in files:
            #created = os.stat(file).st_ctime

        #add file to a list if ceated more that a week ago
        old = []
        for file in files:
            created = os.stat(file).st_ctime
            if created < timestamp:
                old.append(file)
        #add the old files to a zip archive 
        from zipfile import ZipFile
        with ZipFile(zipfilename, 'w') as zipfile:
            for file in old:
                zipfile.write(file)
                if os.path.exists(f'{self.reportPath}{file}'): os.remove(f'{self.reportPath}{file}')

        #BONUS convert the loop to generate a staement
        #old =(f for f in files if os.stat(f).st_ctime < timestamp ) 
        #with ZipFile("old.zip", 'w') as zipfile:
            #for file in old:
                #zipfile.write(file)

    def getCurrentMonthandYear(self):
        dt = datetime.now()
        year = dt.year
        Month = dt.month
        day = dt.day
        if day  < 26: # statement are avalable only after the 26
            Month = Month - 1
        strMonth = getMonth(Month)
        return strMonth, year
            


    def getFolders(self):
        path = ___PATH___()
        path = path.replace('src', '')
        self.statementfolder = path + 'statements\\'
        self.annualStatementFolder = self.statementfolder + 'annualStatements\\'
        return self.statementfolder, self.annualStatementFolder

    def generateAnnualStatement(self): #internal \
        self.annualstatmentFileList.clear()
        log("generating Annual Statement" + fileandline(), level3)
        # get the list of all statement files
        for file in os.listdir(self.statementfolder):   
            # check the extension of files
            if file.endswith('.csv'):
                self.annualstatmentFileList.append(file)
        #now build a statement file with all the statements
        filename = self.annualStatementFolder + self.annualstament
        try:
            os.remove(filename) #delete it and create 
        except OSError as e: # this would be "except OSError, e:" before Python 2.6
            print (e)

        with open(self.annualStatementFolder + self.annualstament, 'at', newline="") as of:
            csvwriter = csv.writer(of)
            for file in self.annualstatmentFileList:
                with open(self.statementfolder + file, 'r') as f:
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    for entry in csvreader:
                        csvwriter.writerow(entry)

                    f.close()
        of.close()


    def cleanup(self):
        log("Cleaning up" + fileandline(), level3)
        #self.CategoriesList
        #self.BillsList.clear()
        self.BillDefinitionDict.clear()
        self.MonthlyTotalExPerCat.clear()
        self.MontlyDistribution.clear()


    def CreateEmptyMonthlyData(self): # just creates the data structure
        self.MontlyDistribution.clear()
        for mth in self.months:
            if mth == '':
                continue 
            mthdata = []
            mthdatadict = {mth: mthdata}
            self.MontlyDistribution.__setitem__(mth, mthdatadict)
        return self.MontlyDistribution
     

     # UpdatedSalariesDict
    def CreateEmptyMonthlySalaryData(self):
        global UpdatedSalariesDict
        self.UpdatedSalariesDict.clear()
        for mth in self.months:
            if mth == '':
                continue 
            mthdata = []
            mthdatadict = {mth: mthdata}
            self.UpdatedSalariesDict.__setitem__(mth, mthdatadict)

    def CreateEmptyMonthlyTotalExPerCat(self): # just creates the data structure
        self.MonthlyTotalExPerCat.clear()
        for mth in self.months:
            if mth == '':
                continue 
            mthDict = {}
            for cat in self.CategoriesList:
                catVal = {str(cat): 0.0}
                mthDict.__setitem__(str(cat) , catVal)
            self.MonthlyTotalExPerCat.__setitem__(mth, mthDict)
        return self.MonthlyTotalExPerCat

    def createMontlyDistribution(self): # distributes the data for each month
        log("creating Montly Distribution - distributes the data for each month" + fileandline(), level3)
        global modifiedMonths
        self.CreateEmptyMonthlyData()
        annualfile = self.annualStatementFolder + self.annualstament
        with open(annualfile, 'r') as of:
            csvreader = csv.reader(of)
            header = next(csvreader)
            for entry in csvreader:
                m = 0 
                d = 0
                y = 0
                try:
                    if entry[1] == '':
                        continue
                    thedate = entry[0]          
                    m,d,y = thedate.split('/')
                except Exception as e:
                    continue  # the entry has no date format
                if y.isnumeric() == False:
                    continue
                if int(y) < self.currentyear:
                    continue
                else:
                    if int(m) > self.lastMonthofdata:
                        self.lastMonthofdata = int(m)
                    month = self.months[int(m)] 
                    datadict = self.MontlyDistribution[month]
                    datadict[month].append(entry)
        self.modifiedMonths = self.months.copy()
        self.modifiedMonths.pop(0) # remove the empty month
        for i in range(11, 1, -1):   # get the last month with data
            if i >= self.lastMonthofdata:
                self.modifiedMonths.pop(i)       
        return self.MontlyDistribution
    
    def calculatetotalbillsPermonth(self):
        log("Calculating total bills per month" + fileandline(), level3)
        for mth in self.modifiedMonths:
            mthtotal = 0.0
            for bill in self.BillsList:
               val =  self.BillDataDict[bill]
               index = getnumMonth(mth) - 1# 0 based indexing 
               mthtotal = mthtotal + float(val[index])
            self.totalbillsPermonth.append(mthtotal)
        print("totalbillsPermonth:")
        print(self.totalbillsPermonth)


    def calculateMonthlyTotalExpenses(self):
        log("Calculating monthly total expenses"+ fileandline(), level3)
        for month in self.months:
            if month == '':
                continue
            mthexpval = 0.0
            for category in self.CategoriesList:
                if category == "Salaries":
                    continue
                if category == "Transfers":
                    continue
                exp = self.MonthlyTotalExPerCat[month][category]
                val = exp[category]
                mthexpval = mthexpval + float(val)
            self.MonthlyTotalExpenses.__setitem__(month,"%.2f" %  mthexpval)  
        #print("MonthlyTotalExpenses:")  
        #print(self.MonthlyTotalExpenses)
        

    def updateMonthlyTotalperCat(self):
        log("updating monthly total per category" + fileandline(), level3)
        for month in self.months:
            if month == '':
                continue
            mthdata =  self.MontlyDistribution[month][month] # give access to data (a list) in the month
            for entry in mthdata:
                try:
                    description = entry[1]
                    if description == '':
                        break
                    amt = entry[2]
                    amt = str(amt).replace(',', '')
                    if amt == '':
                        continue
                    for cat in self.CategoriesList:
                        found = False
                        catdefinition = self.ExpenseCategoriesdataDict[cat]
                        for val in catdefinition:
                            if val in description:
                                catVal = self.MonthlyTotalExPerCat[month][cat]
                                totalval = float(catVal[cat]) + float(amt)
                                catVal.__setitem__(cat, totalval)
                                found = True
                                break
                        if found == True:
                            break
                        elif cat == 'Others':
                            catVal = self.MonthlyTotalExPerCat[month][cat]
                            totalval = float(catVal[cat]) + float(amt)
                            catVal.__setitem__(cat, totalval)
                            break
                except Exception as Ex:
                    continue
        #print("MonthlyTotalExPerCat: \n")
        #print(self.MonthlyTotalExPerCat)
        return self.MonthlyTotalExPerCat 
    
    def updateMonthlySalaries(self):
        log("updating monthly salaries" + fileandline(), level3)
        global UpdatedSalariesDict
        salarydefinition = self.ExpenseCategoriesdataDict['Salaries']
        self.CreateEmptyMonthlySalaryData()
        for file in os.listdir(self.statementfolder): 
            # check the extension of files
            if file.endswith('.csv'):
                with open(self.statementfolder + file, 'r') as f:
                    csvreader = csv.reader(f)
                    header = next(csvreader)
                    TotalSalary = 0.0
                    month = ''
                    for entry in csvreader:
                        try:
                            endbalance  = entry [0]
                            patern = '(Ending balance as of )(.*)'
                            result = re.search(patern, endbalance)
                            if result:
                                t = result.groups ()[1]
                                m, d, y=t.split('/')                    
                                month = self.months[int(m)]
                        except Exception as ex:
                            continue
                        description = entry [1]
                        if description == '':
                            continue
                        elif any (salarydef in description for salarydef in salarydefinition):
                            strVal = entry[2]
                            strVal = str(strVal).replace(',', '')
                            TotalSalary = TotalSalary + float(strVal)
                            self.UpdatedSalariesDict[month][month].append(entry)

                    sal = self.MonthlyTotalExPerCat[month]["Salaries"] 
                    sal["Salaries"] = "%.2f" % TotalSalary    
                    f.close()


    def CreateEmptyMonthlyBills(self): # just creates the data structure
            self.MonthlyBillsDict.clear()
            for mth in self.months:
                if mth == '':
                    continue 
                mthDict = {}
                for bill in self.BillsList:
                    billVal = {str(bill): 0.0}
                    mthDict.__setitem__(str(bill) , billVal)
                self.MonthlyBillsDict.__setitem__(mth, mthDict)
            return self.MonthlyBillsDict
    

    def updateMonthlyBills(self):
        log("updating monthly bills" + fileandline(), level3)
        for month in self.months:
            if month == '':
                continue
            mthdata =  self.MontlyDistribution[month][month] # give access to data (a list) in the month
            for entry in mthdata:   
                try:
                    description = entry[1]
                    if description == '':
                        break
                    amt = entry[2]
                    amt = str(amt).replace(',', '')
                    if amt == '':
                        continue
                    for bill in self.BillsList:
                        found = False
                        billdefinition = self.BillDefinitionDict[bill]
                        for val in billdefinition:
                            if val in description:
                                billVal = self.MonthlyBillsDict[month][bill]
                                totalval = float(billVal[bill]) + float(amt)
                                billVal.__setitem__(bill, totalval)
                                found = True
                                break
                            if found == True:
                                break
                            elif bill == 'Others':
                                billVal = self.MonthlyBillsDict[month][bill]
                                totalval = float(billVal[bill]) + float(amt)
                                billVal.__setitem__(bill, totalval)
                                break
                except Exception as Ex:
                    continue
        print("MonthlyBillsDict:")
        print(self.MonthlyBillsDict)
        return self.MonthlyBillsDict 

    def GetBillValues(self):
        log("getting bill values" + fileandline(), level3)
        global BillDataDict
        for b in self.BillsList:
            bValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                bill = self.MonthlyBillsDict[mth][b]
                amt = "%.2f" % abs(bill[b])
                bValList.append(float(amt))
                self.BillDataDict.__setitem__(b ,  bValList)
        print("BillDataDict:")
        print(self.BillDataDict)


    def GetGroceryValues(self):
        log("Getting grocery values" + fileandline(), level3)
        global GroceryDataDict
        for g in self.GroceryList:
            gValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                grocey = self.MonthlyGroceryDict[mth][g]
                amt = "%.2f" % abs(grocey[g])
                gValList.append(float(amt))
                self.GroceryDataDict.__setitem__(g ,  gValList)
        #print("GroceryDataDict:")
        #print(self.GroceryDataDict)

    def GetUtilityValues(self):
        global UtilitiesDataDict
        for u in self.UtilitiesList:
            uValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                utility = self.MonthlyUtilityDict[mth][u]
                amt = "%.2f" % abs(utility[u])
                uValList.append(float(amt))
                self.UtilitiesDataDict.__setitem__(u ,  uValList)
        #print("UtilitiesDataDict:")
        #print(self.UtilitiesDataDict)

    def CreateEmptyMonthlyUtility(self): # just creates the data structure
        self.MonthlyUtilityDict.clear()
        for mth in self.months:
            if mth == '':
                continue 
            mthDict = {}
            for utility in self.UtilitiesList:
                utilVal = {str(utility): 0.0}
                mthDict.__setitem__(str(utility) , utilVal)
            self.MonthlyUtilityDict.__setitem__(mth, mthDict)
        return self.MonthlyUtilityDict


    def CreateEmptyMonthlyGrocery(self): # just creates the data structure
        self.MonthlyGroceryDict.clear()
        for mth in self.months:
            if mth == '':
                continue 
            mthDict = {}
            for grocery in self.GroceryList:
                groceryVal = {str(grocery): 0.0}
                mthDict.__setitem__(str(grocery) , groceryVal)
            self.MonthlyGroceryDict.__setitem__(mth, mthDict)
        return self.MonthlyGroceryDict


    def updateMonthlyUtilities(self):
        log("updating monthly utilities" + fileandline(), level3)
        global MonthlyUtilityDict
        for month in self.months:
            if month == '':
                continue
            mthdata =  self.MontlyDistribution[month][month] # give access to data (a list) in the month
            for entry in mthdata:   
                try:
                    description = entry[1]
                    if description == '':
                        break
                    amt = entry[2]
                    amt = str(amt).replace(',', '')
                    if amt == '':
                        continue
                    for u in self.UtilitiesList:
                        found = False
                        utilitydefinition = self.UtilitiesDefinitionDict[u]
                        for val in utilitydefinition:
                            if val in description:
                                utilVal = self.MonthlyUtilityDict[month][u]
                                totalval = float(utilVal[u]) + float(amt)
                                utilVal.__setitem__(u, totalval)
                                found = True
                                break
                            if found == True:
                                break
                            elif u == 'Others':
                                utilVal = self.MonthlyUtilityDict[month][u]
                                totalval = float(utilVal[u]) + float(amt)
                                utilVal.__setitem__(u, totalval)
                                break
                except Exception as Ex:
                    continue
        #print("MonthlyUtilityDict:")
        #print(self.MonthlyUtilityDict)
        return self.MonthlyUtilityDict




    def updateMonthlyGroceries(self):
        log("updating monthly groceries" + fileandline(), level3)
        global MonthlyGroceryDict
        for month in self.months:
            if month == '':
                continue
            mthdata =  self.MontlyDistribution[month][month] # give access to data (a list) in the month
            for entry in mthdata:   
                try:
                    description = entry[1]
                    if description == '':
                        break
                    amt = entry[2]
                    amt = str(amt).replace(',', '')
                    if amt == '':
                        continue
                    for grocery in self.GroceryList:
                        found = False
                        grocerydefinition = self.GroceryDefinitionDict[grocery]
                        for val in grocerydefinition:
                            if val in description:
                                groceryVal = self.MonthlyGroceryDict[month][grocery]
                                totalval = float(groceryVal[grocery]) + float(amt)
                                groceryVal.__setitem__(grocery, totalval)
                                found = True
                                break
                            if found == True:
                                break
                            elif grocery == 'Others':
                                groceryVal = self.MonthlyGroceryDict[month][grocery]
                                totalval = float(groceryVal[grocery]) + float(amt)
                                groceryVal.__setitem__(grocery, totalval)
                                break
                except Exception as Ex:
                    continue
        #print("MonthlyGroceryDict:")
        #print(self.MonthlyGroceryDict)
        return self.MonthlyGroceryDict




    def setReportdata(self, currentMonth: str):
        log("Entering setReportdata..." + fileandline(), level3)
        reportData = {}

        NumMonth = getnumMonth(currentMonth)
        groc = self.MonthlyTotalExPerCat[currentMonth]['Grocery']
        reportData.__setitem__('currentGrocery', abs(groc['Grocery']))
 
        mm1,mm2, mm3 = self.getCatmmm("Grocery")
        reportData.__setitem__('grocerymin', mm1)

        gas = self.MonthlyTotalExPerCat[currentMonth]['Gas']
        reportData.__setitem__('Gas', abs(gas['Gas']))

        clo = self.MonthlyTotalExPerCat[currentMonth]['Clothing']
        reportData.__setitem__('currentClothing', abs(clo['Clothing']))

        mc1,mc2, mc3 = self.getCatmmm("Clothing")
        reportData.__setitem__('clothingmin', mc1)

        sal = self.MonthlyTotalExPerCat[currentMonth]['Salaries']
        val = sal['Salaries']
        reportData.__setitem__('incomecurrent', abs(float(val)))

        tenpctin =  20*float(sal['Salaries'])/100
        reportData.__setitem__('twentypercentincome', abs(tenpctin))

        reportData.__setitem__('freelanceincome', 0.0)

        mor = self.MonthlyTotalExPerCat[currentMonth]['Mortgage']
        reportData.__setitem__('mortgage', abs(mor['Mortgage']))

        util = self.MonthlyTotalExPerCat[currentMonth]['Utilities']
        reportData.__setitem__('utility', abs(util['Utilities']))

        car = self.MonthlyTotalExPerCat[currentMonth]['Car Repair']
        reportData.__setitem__('carpayment', abs(car['Car Repair']))

        ins = self.MonthlyTotalExPerCat[currentMonth]['Insurance']
        reportData.__setitem__('insurrance', abs(ins['Insurance']))

        reportData.__setitem__('subscriptions', 0.0)

        oth = self.MonthlyTotalExPerCat[currentMonth]['Others']
        reportData.__setitem__('totalOthers', abs(oth['Others']))

        rest = self.MonthlyTotalExPerCat[currentMonth]['Restaurant']
        reportData.__setitem__('restaurant', abs(rest['Restaurant']))

        phar = self.MonthlyTotalExPerCat[currentMonth]['Pharmacy']
        reportData.__setitem__('pharmacy', abs(phar['Pharmacy']))

        cc = self.MonthlyTotalExPerCat[currentMonth]['CC Payment']
        reportData.__setitem__('CreditCard', abs(cc['CC Payment']))

        reportData.__setitem__('studentloan', 0.0)

        totalbill = 0.0
        for bill in self.BillsList: 
            billval = self.BillDataDict[bill][NumMonth -1]
            totalbill = float(totalbill) + float(billval)

        totalbill = "%.2f" % totalbill
        reportData.__setitem__('currentBill', abs(float(totalbill)))

        tel = self.BillDataDict['Telephone'][NumMonth -1]
        reportData.__setitem__('telephone', abs(tel))

        ttb = self.totalbillsPermonth.copy()
        self.removezeros(ttb)
        billmin =   min(ttb)
        reportData.__setitem__('billmin', billmin)

        monthExp = self.MonthlyTotalExpenses[currentMonth]
        reportData.__setitem__('totaMonthlyExp', abs(float(monthExp)))

        saving = abs(float(sal['Salaries'])) - float(monthExp)
        thirtypercentofsaving = 30*float(saving)/100
        thirtypercentofsaving = "%.2f" % thirtypercentofsaving
        reportData.__setitem__('thirtyperscentofsaving', float(thirtypercentofsaving))

        tenpercentofsaving = 10*float(saving)/100
        reportData.__setitem__('tenperscentofsaving', tenpercentofsaving)
        montlyexpList = []
        for mth in self.months:
            if mth == '':
                continue
            val = float(self.MonthlyTotalExpenses[mth])
            montlyexpList.append(abs(val))
        montlyexpListCopy = montlyexpList.copy()
        montlyexp = self.removezeros(montlyexpListCopy)
        minex = min(montlyexp)
        reportData.__setitem__('totalExpensemin', minex)

        maxsaving = float(sal['Salaries']) - float(minex)
        maxsaving = "%.2f" % maxsaving
        reportData.__setitem__('maxsaving', float(maxsaving))
        #================================================================

        self.theReport.setTheNumbers(reportData, currentMonth)

        
    def prep(self):
        log("Entering prep in annual reporting .." + fileandline(), level=level3)

        self.getFolders()                       # Initializes all the directories where we can find things
        self.generateAnnualStatement()          # merge all the statements together
        self.createMontlyDistribution()         # Distrubutes the raw data to each months 
        self.CreateEmptyMonthlyTotalExPerCat()  # Craetes an empty structure for MonthlyTotalExPerCat per category
        self.updateMonthlyTotalperCat()         # fills in the data for MonthlyTotalExPerCat
     
        self.CreateEmptyMonthlyBills()          # Craetes an empty structure for MonthlyBillsDict
        self.updateMonthlyBills()               # initializes all montly bills in MonthlyBillsDict
        self.GetBillValues()                    # Collect all bills amount in BillDataDict
        
        self.CreateEmptyMonthlyGrocery()        # Craetes an empty structure for MonthlyGroceryDict
        self.updateMonthlyGroceries()           # initializes all montly grocery in MonthlyGroceryDict 
        self.GetGroceryValues()                 # Collect all grocery amount in GroceryDataDict
        
        self.CreateEmptyMonthlyUtility()        # Craetes an empty structure for MonthlyUtilitiesDict
        self.updateMonthlyUtilities()           # initializes all montly utilities in MonthlyGroceryDict
        self.GetUtilityValues()                 # Collect all utilities amount in UtilitiesDataDict
       
        self.calculateBillsMeanValues()         # Calculate the means of the Bills
        self.calculatetotalbillsPermonth()      # Calculates a list of the bills for each month
        self.calculateMonthlyTotalExpenses()    # Calculates expenses for each month
        self.updateMonthlySalaries()            # adjust the monthly salaries - BOFA month is for the 25 to the 24 of the next month
    #===============================================================================================
    # Statistics
    # data = [n1,n2,....nx]
    # mean = statis.mean(data)
    # Mean values over the year -
    

    def getOneBillMean(self, name):
        return self.BillMeans[name]
    
    def getCatmmm(self, categorie): #returns min mean and max
        catAmtlist = []
        for mth in self.modifiedMonths:
            mthcat = self.MonthlyTotalExPerCat[mth][categorie]
            someval = float(mthcat[categorie])
            val = "%.2f" % someval
            catAmtlist.append(abs(float(val)))
        catAmtlistCopy = catAmtlist.copy()
        self.removezeros(catAmtlistCopy)
        if len(catAmtlistCopy) > 0.0:
            return  min(catAmtlistCopy),  stats.mean(catAmtlistCopy), max(catAmtlistCopy)
        else:
            return 0.0, 0.0, 0.0
    

    def getBillmmm(self, bill): #returns min mean and max
        arrBill = self.BillDataDict[bill]
        arrBillCopy = list(arrBill).copy()
        self.removezeros(arrBillCopy)
        l = len(arrBillCopy) 
        if l > 0:
            return  min(arrBillCopy),  stats.mean(arrBillCopy), max(arrBillCopy)
        else:
            return 0.0, 0.0, 0.0

    def getGrocerymmm(self, grocery): #returns min mean and max
        arrGroc = self.GroceryDataDict[grocery]
        arrGrocCopy = list(arrGroc).copy()
        self.removezeros(arrGrocCopy)
        l = len(arrGrocCopy) 
        if l > 0:
            return  min(arrGrocCopy),  stats.mean(arrGrocCopy), max(arrGrocCopy)
        else:
            return 0.0, 0.0, 0.0
        
    def getUtilitiesmmm(self, Util): #returns min mean and max
        arrUtil = self.UtilitiesDataDict[Util]
        arrUtilCopy = list(arrUtil).copy()
        self.removezeros(arrUtilCopy)
        l = len(arrUtil) 
        if l > 0:
            return  min(arrUtilCopy),  stats.mean(arrUtilCopy), max(arrUtilCopy)
        else:
            return 0.0, 0.0, 0.0

    #removes all bills with value of $0.0
    def removezeros(self, listofvalues, i = 0):
        l = len(listofvalues)
        while True:
            l = len(listofvalues)
            if i >= l:
                break
            if listofvalues[i] == 0.0:
                listofvalues.pop(i)
            else:
                i = i+1
                self.removezeros(listofvalues, i)
        return listofvalues


    def calculateBillsMeanValues(self):
        log("calculating bills mean values..." + fileandline(), level3)
        global BillMeans
        self.BillMeans.clear()
        for bill in self.BillDataDict:
            if bill == 'Others':
                continue
            billdata = list(self.BillDataDict[bill])
            #remove the month where the values are 0.0
            billdataCopy = list(billdata).copy()
            billdataCopy = self.removezeros(billdataCopy)
            bm = stats.mean(billdataCopy)
            mn = "%.2f" % abs(bm)
            self.BillMeans.__setitem__(bill, mn)
        #print("BillMeans:")
        print(self.BillMeans)

    def getBillsAmount(self):
        global __Billsmean
        for bm in self.BillsList:
            mval = self.BillMeans[bm]
            self.__Billsmean = self.__Billsmean + float(mval)
        return self.__Billsmean
    #===============================================================================================
    #             Statistics

    def BillsStats(self, save = False):
        log("Entering BillsStats..." + fileandline(), level3)
        stats = []
        for bill in self.BillsList:
            m1, m2, m3 = self.getBillmmm(bill)
            stats.append([float(m1), float(m2), float(m3)]) 

        title_text = ('Comparison of bills trends statistics in the year ')
        
        column_headers = ['Min', 'Mean', 'Max']
        row_headers = self.BillsList
        cell_text = []
        for e in stats:
            cell_text.append([f'{x:1.1f}' for x in e])

        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')
        # Scaling influences the top and bottom cell padding.
        the_table.scale(.7, 1.7)

        # Hiding axes
        ax = plt.gca()

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        ttl = plt.suptitle(title_text)
        ttl.set_position([0.5,0.9])

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        fig.set_size_inches(8, 5)
        if save:
            plt.savefig(f'{self.reportPath}BillsStats-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()

    def GroceryStats(self, save = False):
        log("Entering GroceryStats..." + fileandline(), level3)
        stats = []
        for grocery in self.GroceryList:
            m1, m2, m3 = self.getGrocerymmm(grocery)
            stats.append([float(m1), float(m2), float(m3)]) 

        title_text = ('Comparison of grocery trends statistics in the year ')
        
        column_headers = ['Min', 'Mean', 'Max']
        row_headers = self.GroceryList
        cell_text = []
        for e in stats:
            cell_text.append([f'{x:1.1f}' for x in e])

        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')
        # Scaling influences the top and bottom cell padding.
        the_table.scale(.7, 1.7)

        # Hiding axes
        ax = plt.gca()

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        ttl = plt.suptitle(title_text)
        ttl.set_position([0.5,0.9])

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        fig.set_size_inches(8, 5)
        if save:
            plt.savefig(f'{self.reportPath}GroceryStats-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()


    def UtilityStats(self, save = False):
        log("Entering UtilityStats..."+ fileandline(), level3)
        stats = []
        for utility in self.UtilitiesList:
            m1, m2, m3 = self.getUtilitiesmmm(utility)
            stats.append([float(m1), float(m2), float(m3)]) 

        title_text = ('Comparison of utilities trends statistics in the year ')
        
        column_headers = ['Min', 'Mean', 'Max']
        row_headers = self.UtilitiesList
        cell_text = []
        for e in stats:
            cell_text.append([f'{x:1.1f}' for x in e])

        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')
        # Scaling influences the top and bottom cell padding.
        the_table.scale(.7, 1.7)

        # Hiding axes
        ax = plt.gca()

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        ttl = plt.suptitle(title_text)
        ttl.set_position([0.5,0.9])

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        fig.set_size_inches(8, 5)
        if save:
            plt.savefig(f'{self.reportPath}UtilitiesStats-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()

    def CategoryStats(self, save = False):
        log("Entering CategoryStats..." + fileandline(), level3)
        stats = []
        for cat in self.CategoriesList:
            m1, m2, m3 = self.getCatmmm(cat)
            stats.append([float(m1), float(m2), float(m3)]) 

        title_text = ('Comparison of spending categories trends statistics in the year ')
        
        column_headers = ['Min', 'Mean', 'Max']
        row_headers = self.CategoriesList
        cell_text = []
        for e in stats:
            cell_text.append([f'{x:1.1f}' for x in e])

        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')
        # Scaling influences the top and bottom cell padding.
        the_table.scale(.6, 1.0)

        # Hiding axes
        ax = plt.gca()

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        ttl = plt.suptitle(title_text)
        ttl.set_position([0.5, 0.9])

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        fig.set_size_inches(6, 7)
        if save:
            plt.savefig(f'{self.reportPath}CategoryStats-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()


    #===============================================================================================
    #    Ploting functionalities start here

    def lineChartOfBills(self, save = False): # all bills in one chart per month
        log("line chart of bills..." + fileandline(), level3)
        billLineChartFile = f"{self.reportPath}billLineChartFile.png"
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_ylabel('Bills per month. ($)')
        ax.set_title(f'Comparison of bills trends in the year ', fontdict = titlefont, pad=32, loc = 'left')
        for b in self.BillsList:
            bValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                bill = self.MonthlyBillsDict[mth][b]
                amt = "%.2f" % abs(bill[b])
                bValList.append(float(amt))
            ax.plot(self.modifiedMonths,bValList , label = b)
        plt.xticks(range(len(self.modifiedMonths)), self.modifiedMonths, rotation=45)
        plt.legend()
        fig.tight_layout() # adjust the layout to fit the chart, or fig.subplots_adjust(bottom=0.2)
        if save == True:
            plt.savefig(billLineChartFile)
            plt.close()
            #return billLineChartFile
        else:
            plt.show()
        #return None


    def barChartOfBills(self, save = False):
        log("Bar chart of bills..." + fileandline(), level3)
        billLineChartFile = f"{self.reportPath}billLineChartFile.png"
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_ylabel('Amount spent on bills per month. ($)')
        ax.set_title(f'Comparison of bills bar plot in the year ', fontdict = titlefont, pad=32, loc = 'left')
        bardict  = {}

        for b in self.BillsList:
            bValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                bill = self.MonthlyBillsDict[mth][b]
                amt = "%.2f" % abs(bill[b])
                bValList.append(float(amt))
                bardict.__setitem__(b ,  bValList)
        print (bardict)
        X_axis = np.arange(len(self.modifiedMonths))
        Width = 0.2 
        X = X_axis - Width 
        for bill  in self.BillsList:
            grbillVals = bardict[bill]
            print(grbillVals)
            plt.bar(X, grbillVals, width = Width, edgecolor = 'black', label = bill)
            X = X+ Width
            plt.xticks(range(len(self.modifiedMonths)), self.modifiedMonths, rotation=45)
            
        plt.legend()
        fig.tight_layout() # adjust the layout to fit the chart, or fig.subplots_adjust(bottom=0.2)
        if save == True:
            plt.savefig(billLineChartFile)
            plt.close()
            #return billLineChartFile
        else:
            plt.show()
        #return None
    


    def barChartOfGroceries(self, save = False):
        log("bar chart of groceries..."+ fileandline(), level3)
        GroceryLineChartFile = f"{self.reportPath}GroceryBarChartFile.png"
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_ylabel('Amount spent on grocery per store per month. ($)')
        ax.set_title(f'Comparison of Grocery per store bar plot in the year ', fontdict = titlefont, pad=32, loc = 'left')
        bardict  = {}

        for g in self.GroceryList:
            gValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                grocery = self.MonthlyGroceryDict[mth][g]
                amt = "%.2f" % abs(grocery[g])
                gValList.append(float(amt))
                bardict.__setitem__(g ,  gValList)
        #print (bardict)
        X_axis = np.arange(len(self.modifiedMonths))
        Width = 0.10 
        X = X_axis - Width 
        for grocery  in self.GroceryList:
            grGroceryVals = bardict[grocery]
            print(grGroceryVals)
            plt.bar(X, grGroceryVals, width = Width, edgecolor = 'black', label = grocery)
            X = X+ Width
            plt.xticks(range(len(self.modifiedMonths)), self.modifiedMonths, rotation=45)
            
        plt.legend()
        fig.tight_layout() # adjust the layout to fit the chart, or fig.subplots_adjust(bottom=0.2)
        if save == True:
            plt.savefig(GroceryLineChartFile)
            plt.close()
            return GroceryLineChartFile
        else:
            plt.show()
        return None


    def lineChartOfGrocery(self, save = False):
        log("line chart of groceries..." + fileandline(), level3)
        GroceryLineChartFile = f"{self.reportPath}GroceryLineChartFile.png"
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_ylabel('Grocery per store per month. ($)')
        ax.set_title(f'Comparison of grocery per store trends in the year ', fontdict = titlefont, pad=32, loc = 'left')
        for g in self.GroceryList:
            gValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                grocery = self.MonthlyGroceryDict[mth][g]
                amt = "%.2f" % abs(grocery[g])
                gValList.append(float(amt))
            ax.plot(self.modifiedMonths,gValList , label = g)
        plt.xticks(range(len(self.modifiedMonths)), self.modifiedMonths, rotation=45)
        plt.legend()
        fig.tight_layout() # adjust the layout to fit the chart, or fig.subplots_adjust(bottom=0.2)
        if save == True:
            plt.savefig(GroceryLineChartFile)
            plt.close()
            return GroceryLineChartFile
        else:
            plt.show()
        return None


    def pieChartOfBills(self, save = False):
        pass

    def tableOfSalaries(self, save = False):
        log("table of salaries..." + fileandline(), level3)
        title_text = 'Monthly Salaries'
        saldata = []
        for mth in self.modifiedMonths:
            if mth == '':
                continue
            sal = self.MonthlyTotalExPerCat[mth]['Salaries']
            saldata.append(float(sal['Salaries']))
        column_headers = self.modifiedMonths
        row_headers = ['Salaries']
        cell_text = []
        #for row in saldata:
        cell_text.append([f'{x:1.1f}' for x in saldata])

        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')
        # Scaling influences the top and bottom cell padding.
        the_table.scale(1, 1.5)

        # Hiding axes
        ax = plt.gca()

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        ttl = plt.suptitle(title_text)
        ttl.set_position([0.5,0.7])

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        fig.set_size_inches(8, 4.5)
        if save:
            plt.savefig(f'{self.reportPath}Salaries-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()

    def tableofExpenses(self, save = False):
        log("table of expenses..." + fileandline(), level3)
        title_text = 'Table of Expenses'
        #fig_background_color = 'yellow'
        fig_border = 'skyblue'
        row_labels = []
        categoryVal = []
        for cat in self.CategoriesList:
            if cat == "Salaries":
                continue
            if cat == "Transfers":
                continue
            MonthVal = [] 
            for mth in self.modifiedMonths:
                catVal = self.MonthlyTotalExPerCat[mth][cat]
                val = abs(float("%.2f" % catVal[cat]))
                MonthVal.append(val)
            categoryVal.append(MonthVal)
            row_labels.append(cat)
        toatls = []
        for m in self.modifiedMonths:
            val = self.MonthlyTotalExpenses[m]
            tot = abs(float(val))
            toatls.append(tot)
        categoryVal.append(toatls)
        row_labels.append("Total Expenses")

        column_headers = self.modifiedMonths
        row_headers = row_labels
        cell_text = []
        for row in categoryVal:
            cell_text.append([f'{x:1.1f}' for x in row])
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

        #Creating the figure. Setting a small pad on the tight layout

        plt.figure(linewidth=2,
                edgecolor = fig_border,
                #facecolor=fig_background_color,
                tight_layout={'pad':1})

        #Adding a table at the bottom of the axes

        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')

        # Scaling influences the top and bottom cell padding.
        the_table.scale(1, 1.5)

        # Hiding axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        plt.suptitle(title_text)

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        if save:
            plt.savefig(f'{self.reportPath}Expenses-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()

    
    def BillsTabulation(self):
        log("Tabulation of bills..." + fileandline(), level3)
        title_text = 'Bills cost per month'
        column_headers = ['Name'] + self.modifiedMonths
        bdata  = []
        for b in self.BillsList:
            bValList = [b]
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                bill = self.MonthlyBillsDict[mth][b]
                amt = "%.2f" % abs(bill[b])
                bValList.append(float(amt))
            bdata.append(bValList)
        return  bdata
          
    def GroceryTabulation(self):
        log("Tabulation of groceries..." + fileandline(), level3)
        title_text = 'Grocery cost per month'
        column_headers = ['Name'] + self.modifiedMonths
        gdata  = []
        for g in self.GroceryList:
            gValList = [g]
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                groc = self.MonthlyGroceryDict[mth][g]
                amt = "%.2f" % abs(groc[g])
                gValList.append(float(amt))
            gdata.append(gValList)
        return  gdata

    def UtilityTabulation(self):
        log("Tabulation of utilities..."+ fileandline(), level3)
        title_text = 'Utility cost per month'
        column_headers = ['Name'] + self.modifiedMonths
        udata  = []
        for u in self.UtilitiesList:
            uValList = [u]
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                util = self.MonthlyUtilityDict[mth][u]
                amt = "%.2f" % abs(util[u])
                uValList.append(float(amt))
            udata.append(uValList)
        return  udata   
          
    def CategoryTabulation(self):
        log("Tabulation of groceries..." + fileandline(), level3)
        title_text = 'Expenses per category per month'
        column_headers = ['Name'] + self.modifiedMonths
        cdata  = []
        for c in self.CategoriesList:
            cValList = [c]
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                cat = self.MonthlyTotalExPerCat[mth][c]
                amt = "%.2f" % abs(float(cat[c]))
                cValList.append(float(amt))
            cdata.append(cValList)
        return  cdata         

    def tableOfBills(self, save = False):
        log("Table of bills..." + fileandline(), level3)
        title_text = 'Bills cost per month'
        #fig_background_color = 'yellow'
        fig_border = 'skyblue'
        bardict  = {}
        for b in self.BillsList:
            bValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                bill = self.MonthlyBillsDict[mth][b]
                amt = "%.2f" % abs(bill[b])
                bValList.append(float(amt))
                bardict.__setitem__(b ,  bValList)

        column_headers = self.modifiedMonths
        row_headers = self.BillsList
        print(bardict)
        data = []
        for b in bardict:
            data.append(bardict[b])
        print(data)
        cell_text = []
        for row in data:
            cell_text.append([f'{x:1.1f}' for x in row])
              
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

        #Creating the figure. Setting a small pad on the tight layout

        plt.figure(linewidth=2,
                edgecolor = fig_border,
                #facecolor=fig_background_color,
                tight_layout={'pad':1})

        #Adding a table at the bottom of the axes

        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')

        # Scaling influences the top and bottom cell padding.
        the_table.scale(1, 1.5)

        # Hiding axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        plt.suptitle(title_text)

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        if save:
            plt.savefig(f'{self.reportPath}Bills-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()


    def tableOfGroceries(self, save = False):
        log("Table of groceries..." + fileandline(), level3)
        title_text = 'Cost distribution of grocery per month'
        #fig_background_color = 'yellow'
        fig_border = 'skyblue'
        bardict  = {}
        for g in self.GroceryList:
            gValList = []
            for mth in self.modifiedMonths:
                if mth == '':
                    continue
                bigrocery = self.MonthlyGroceryDict[mth][g]
                amt = "%.2f" % abs(bigrocery[g])
                gValList.append(float(amt))
                bardict.__setitem__(g ,  gValList)

        column_headers = self.modifiedMonths
        row_headers = self.GroceryList
        print(bardict)
        data = []
        for g in bardict:
            data.append(bardict[g])
        #print(data)
        cell_text = []
        for row in data:
            cell_text.append([f'{x:1.1f}' for x in row])
              
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
        ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

        #Creating the figure. Setting a small pad on the tight layout

        plt.figure(linewidth=2,
                edgecolor = fig_border,
                #facecolor=fig_background_color,
                tight_layout={'pad':1})

        #Adding a table at the bottom of the axes

        the_table = plt.table(cellText = cell_text,
                            rowLabels = list(row_headers),
                            rowColours = rcolors,
                            rowLoc = 'right',
                            colColours = ccolors,
                            colLabels = column_headers,
                            loc='center')

        # Scaling influences the top and bottom cell padding.
        the_table.scale(1, 1.5)

        # Hiding axes
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Hiding axes border
        plt.box(on=None)

        ttl = plt.suptitle(title_text)
        ttl.set_position([0.5, 0.855])

        # Without plt.draw() here, the title will center on the axes and not the figure.
        plt.draw()

        # Creating the image. plt.savefig ignores the edge and face colors, so we need to map them.
        fig = plt.gcf()
        if save:
            plt.savefig(f'{self.reportPath}grocery-table.png',
                        #bbox='tight',
                        edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150
                        )
            plt.close()
        else:
            plt.show()
            

    def generateMonhtlyPdfReport(self, month:str):
        log("Generating monhtly Pdf report..." + fileandline(), level3)
        self.setReportdata(month)
        return self.theReport.generatePdfReport()

    def generateAnnualReport(self, month:str):
        log("Generating annual PowerPoint report..." + fileandline(), level3)
        self.setReportdata(month)
        return self.thepptxReport.generateAllpptxReport()
       
