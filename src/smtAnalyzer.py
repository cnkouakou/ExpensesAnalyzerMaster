import PySimpleGUI as sg
import pandas as pd
import os
import errno
from Helper import ___PATH___, ___FILE___LINE, log, level0,level1,level2,level3, getMonth, getShortMonth, getnumMonth
import datetime
from Configurator import *
from ConfiguratorX import *
from datetime import date
from datetime import datetime
import time
import json
from pathlib import Path
from screeninfo import get_monitors
import csv
import sys
import shutil
import re
import openpyxl
from openpyxl import Workbook
import openpyxl.chart
from openpyxl.chart import BarChart3D, Reference
import statistics as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.patches import ConnectionPatch
import matplotlib.cm
import calendar
from fpdf import FPDF
from annualReporting import *
import operator
import subprocess
from DisplayTable import *

powerpoint = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.exe"
acrobateReader = "C:\\Program Files\\Adobe\Acrobat DC\\Acrobat\\Acrobat.exe"
excelreader = "C:\\Program Files\\Microsoft Office\\root\Office16\\EXCEL.exe"
configfile = ''
srcPath = ''
reportPath = ''
templatepath = ''
iconfile = ''
headings = []
ExpenseCategoriesList = [] # list of all categries of expenses
ExpenseCategoriesdataDict = {} #contains all the csv file as rows 
categoriesData = []         #
allcatogory_dict = {} #contains all the categories as keys and data for each category
tabledata = [] # a list of lists containing all row for a given table
sumOfExpensesCategoryAmounts = {} # as a key value pair for each category 
percentofsalary = {}
sumofsalary = {}
NAME_SIZE = 20
WIDTH = 210
HEIGHT = 297
use_custom_titlebar = False
statementfile = ''
currentMonth = ''
global_theme= ''
monthlySaving = 0.0
titlefont = {'family':'serif','color':'blue','size':20}
months = list(calendar.month_name)
p_Monitorwidth = 1000
progressbar = None
an = Annual()
an.prep()
currentMonth = an.currentMonth
modifiedMonths = an.modifiedMonths
for m in get_monitors():
    if m.is_primary:
        p_Monitorwidth  =  m.width
left_width= int (0.40*p_Monitorwidth)
right_width = int(0.60*p_Monitorwidth)
bottom_width = int(0.95*p_Monitorwidth)
l_input_width = int (0.1*left_width)
progess_width  = 105
reportfile = ''

AboutMe = """
Version: 1.1.2 (Beta Verion)
Date: 2024-06-19T23:20:00
Evnvironment:
anaconda-client    1.2.2        PySimpleGUI        4.60.5
appJar             0.94.0       python-dateutil    2.8.2
backport           0.3.1        python-pptx        0.6.23            
beautifulsoup4     4.11.1       pytz               2022.1
certifi            2022.5.18.1  PyVISA             1.12.0
charset-normalizer 2.0.12       PyYAML             6.0
clyent             1.2.1        requests           2.28.0
customtkinter      5.2.2        rsa                4.9
cycler             0.11.0       sciparse           0.1.22
darkdetect         0.8.0        scippy             0.1.31
dearpygui          1.6.2        scippy             0.1.31
et-xmlfile         1.1.0        scipy              1.8.1
fonttools          4.33.3       screeninfo         0.8
fpdf               1.7.2        Send2Trash         1.8.0
future             1.0.0        setuptools         56.0.0
idna               3.3          six                1.16.0
kaleido            0.2.1        soupsieve          2.3.2.post1
kiwisolver         1.4.2        tenacity           8.3.0
lxml               5.2.2        typing_extensions  4.2.0
matplotlib         3.5.2        tzdata             2024.1
numexpr            2.10.0       urllib3            1.26.9           
numpy              1.22.4       wcwidth            0.2.5
openpyxl           3.0.9        webencodings       0.5.1
packaging          21.3         xlrd               2.0.1
pandas             2.2.2        XlsxWriter         3.2.0
pandastable        0.13.1       xlutils            2.0.0
Pillow             9.1.1        xlwt               1.3.0
Pint               0.19.2       xmltodict          0.13.0
pip                24.0
plotly             5.22.0
pyasn1             0.6.0
pyodbc             4.0.32
pyparsing          3.0.9
pyserial           3.5
"""
'''
srcPath = ___PATH___()
srcPath = srcPath.replace('src', '')
configfile = srcPath + 'configurations\\config.json'
reportPath = srcPath + 'Reports\\'
'''
monthToNumber = dict((month, index) for index, month in enumerate(calendar.month_abbr) if month)

def GetExpCategories():
    global ExpenseCategoriesList
    global ExpenseCategoriesdataDict

    log("Getting Expense Categories" + ___FILE___LINE(), level3)
    try:
        with open(configfile, 'r') as f:
            ExpenseCategoriesList.clear()
            ExpenseCategoriesdataDict.clear()
            data = json.load(f)
            ExpenseCategoriesList = data['ExpenseCategories'].keys()
            ExpenseCategoriesdataDict = data['ExpenseCategories'].copy()
            f.close()
    except Exception as ex:
        log(f'Error - Exception occured: {ex}' + ___FILE___LINE(), level3 )
        return None


def GetHeader():
    global headings
    log("Getting Header" + ___FILE___LINE(), level3)
    path = ___PATH___()
    try:
        with open(configfile, 'r') as f:
            headings.clear()
            data = json.load(f)
            headings = data["header"]
            return headings
    except Exception as ex:
        log(f"Error - Exception Occured: {ex}" + ___FILE___LINE(), + level3)
        return None
    
def name(name):
    dots = NAME_SIZE-len(name)-2
    return sg.Text(name + ' ' + ' '*dots, size=(NAME_SIZE,1), justification = 'l', pad = (0,0), font = 'Georgis 12')



def loadcsvfile():
    loadallCategoryDataDict()    
    log("File loaded successfully"+ ___FILE___LINE(), level3)


def calculatetotal(data):
    total = 0.00
    for row in data: 
        stramt = str(row[2]).replace(',', '')
        if stramt == '':
            stramt = '0.0'
        amt = float(stramt)
        total = total + amt
    return "%.2f" % abs(total)

def updatetabledata(window, selectedtab):
    global allcatogory_dict
    data = []
    category = selectedtab.replace("Tab_", "")
    if category == 'Salaries':
        data = an.UpdatedSalariesDict[currentMonth][currentMonth]
    else:
        data = allcatogory_dict[category][category]
   
    ttlamt = calculatetotal(data)
    lastrow = [' ', 'Total:' ,ttlamt]
    tmpdata = list(data).copy()
    tmpdata.append(['----------------------',
                    '----------------------',
                    '----------------------',
                    '----------------------'])
    tmpdata.append(lastrow)
    if category == "Salaries":
        sumofsalary[category] = ttlamt
    elif category == "Transfers":
        pass
    else:
        sumOfExpensesCategoryAmounts[category] = ttlamt
    table = f'Table_{category}'
    window[table].update(values =  tmpdata)

def calculatepercentofsalary():
    totalIncome = float(sumofsalary["Salaries"])
    if totalIncome != 0.0:
        for category in sumOfExpensesCategoryAmounts.keys():
            expense = float(sumOfExpensesCategoryAmounts[category])
            percentofsalary[category] = 100*(expense/totalIncome)

def calculateMonthlySaving():
    global monthlySaving
    totalexpenses = 0.0
    monthlySaving = 0.0
    for category in sumOfExpensesCategoryAmounts.keys():
        totalexpenses = totalexpenses + float(sumOfExpensesCategoryAmounts[category])
    monthlySaving = "%.2f" % (float(sumofsalary["Salaries"]) - totalexpenses)
    print(f'Saving per month: {monthlySaving}')

    
def updatealltabledata(window):
    for category in ExpenseCategoriesList:
        updatetabledata(window, category)
    calculatepercentofsalary()
        


defaultdata =  [
["Date", "Description", "Summary", "Running Balance"],
["1", "1", "1", "1"],
["2", "2", "2", "2"],
["3", "3", "3", "3"],
["1", "1", "1", "1"],
["2", "2", "2", "2"],
["3", "3", "3", "3"],
["1", "1", "1", "1"],
["2", "2","2", "2"],
["3", "3", "3", "3"]
]

tabledata = defaultdata

def new_tabletab(category):
    global global_theme
    log(f"Creating tab for {category} category table" + ___FILE___LINE(), level3)
    try:
        global_theme = sg.theme_global()
    except Exception as ex:
        global_theme = sg.theme()

    table = sg.Table(values = tabledata, headings = headings, max_col_width = 400,
                auto_size_columns = True,
                justification = 'center',
                text_color ='white',
                num_rows = 20,
                alternating_row_color = sg.theme_button_color()[1],
                key = f'Table_{category}',
                selected_row_colors='red on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                size = (right_width -10, 20),
                enable_click_events=True, # Comment out to not enable header and other clicks
                right_click_selects = True
                        )

    tab = sg.Tab( f'{category}', 
                [[table]], 
            key = f'Tab_{category}' )
    return tab
        
def get_theme():
    try:
        global_theme = sg.theme_global
    except Exception as ex:
        global_theme = sg.theme()  

    user_theme = sg.user_settings_get_entry('-theme', '')
    if user_theme == '':
        user_theme = global_theme
    return user_theme


def createGui():
    global iconfile 
    srcPath = ___PATH___()
    srcPath = srcPath.replace('src', '')
    configfile = srcPath + 'configurations\\config.json'
    reportPath = srcPath + 'Reports\\'
    templatepath = srcPath + 'Templates\\'
    iconfile = f'{templatepath}statement.ico'
    theme = get_theme()
    #theme = None  # just in case the theme crashes uncomment to restore then comment back
    if not theme:
        theme = sg.OFFICIAL_PYSIMPLEGUI_THEME
    sg.theme()
    log("Creating Gui." + ___FILE___LINE(), level3)
    headings = GetHeader()
    menu_layout = [
        ['File', ['Current tab to Excel', 'All tabs to Excel', '---', 'Exit']],
        ['&Edit', ['!Copy', '!Paste', '!Delete']],
        ['&Reports', 
            ['Plots',
                ['Expenses Chart Plot', 'Expenses Pie Plot', 'Expense Ratio', "Annual Bills Bars", "Annual Bills" , "Annual Grocery" ,"Annual Grocery Bars"], 
            ["Tables", ["Bills", "Annual Salary", "Groceries"]],
            'Monthly Report', 'Annual Report']],
        ['Statistics', ['Bills Stats', 'Grocery Stats', 'Utility Stats', 'Category Stats']],

        ['Tabulation', ['Bills Tabulation', 'Grocery Tabulation', 'Utility Tabulation', 'Category Tabulation']],
        
        ['Configurations', ['!Font', 'Settings']],
        ['Help', ['!View Help', '!Version', 'About Me']]
    ]
    statement_layout = [
        [name('Select the statement file'), sg.In("", size = (l_input_width, 1), enable_events = True, k = '-STATEMENTFILE-'),
        sg.FileBrowse('   Browse...', file_types= [('csv File', '*.csv')], enable_events = True)]
   ]
    listoftabs = []
    for category in ExpenseCategoriesList:
        tab = new_tabletab(category)
        listoftabs.append(tab)

    tabgroup = sg.TabGroup([listoftabs], key = 'Tabgroup', enable_events = True)

    '''
    tabgroup = sg.TabGroup(
        [[new_tabletab(category) for category in ExpenseCategoriesList]],
        key = 'Tabgroup', enable_events = True)'''
    
    tablayout = [
    [sg.Column(
        [[tabgroup]],
        scrollable=True,                # Scrollable Column
        vertical_scroll_only=False,     # With both of vrtical and horizontal scroll bar
        size_subsample_height=1,        # height same as height of tabgroup
        size_subsample_width=2,         # 1/2 width as width of tabgroup
        key='Column', size = (right_width -10, 500))]
    ]

    result_layout = [
        [
            name('Current Month:'), sg.T(currentMonth, font='Georgia 12', text_color = 'yellow', k='-currentmonth-'), 
            name('      Monthly Saving:'), sg.T(monthlySaving, font='Georgia 12', text_color = 'yellow', k='-Saving-'),
            name('      Select a month', ), sg.Combo (modifiedMonths, readonly=True, k='-MONTHS-', size= (20, 1), default_value= currentMonth, enable_events = True) 
        ]
    ]
    # the buttons layout
    buttons_layout = [
        sg.Button('Current tab to Excel', size=(20,2)),
        sg.Button('All tabs to Excel', size=(20,2)),
        sg.Button('Monthly Report', size=(20,2)),
        sg.Button('Annual Report', size=(20,2)),
        sg.Button('Archive', size=(20,2)),
        sg.Button('Exit', size=(20,2)),
    ]


    final_layout = [
        [sg.Menu(menu_layout, tearoff=True)],
        [sg.T("Dr. Kouakou's Statement Analyzer", font="Any 20", justification = 'c', expand_x = True)],
        [name('Default Theme:'), sg.T(global_theme, size = (20, 1), font='Georgia 12'), [sg.ProgressBar(28, size= (progess_width,2), bar_color= ('green3', 'yellow'),visible=False, key='-PROGRESS_BAR-')]],
        [name('Theme'), sg.Combo (['']+sg. theme_list(), sg.user_settings_get_entry('-theme-', ''), readonly=True, k='-THEME-'), sg.Button('Set Theme')],
        statement_layout, result_layout, tablayout,
        #Button frame
        [sg.Frame( 'Click Action Button', [buttons_layout], size = (right_width-10, 50), element_justification = 'left', title_color = 'yellow', border_width = 1)]
    ]

    window = sg.Window("Dr. Kouakou's Statement Analyzer", final_layout, resizable = True, finalize=True, keep_on_top=False, use_custom_titlebar=use_custom_titlebar, icon=iconfile)
    #window.maximize()
    return window
def Archive():
    an.Archive()
    sg.popup_notify(title="Archiving done", display_duration_in_ms= 2000)

def CreateEmptyCatData():
    log("Creating Empty Category Data. "+ ___FILE___LINE(), level3)
    global allcatogory_dict
    for cat in ExpenseCategoriesList: 
    #create an empty list for each
        catdata = []
        catdatadict = {cat: catdata}
        allcatogory_dict.__setitem__(cat, catdatadict)
    print (allcatogory_dict)

def loadallCategoryDataDict():
    global allcatogory_dict
    global currentMonth
    allcatogory_dict.clear()
    CreateEmptyCatData()
    log("Loading all Category Data dictionary. "+ ___FILE___LINE(), level3)
    with open(statementfile, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        log(f'Header is: {header}' + ___FILE___LINE(), level3)
        description = ''
        for entry in csvreader:
            try:
                endbalance  = entry [0]
                patern = '(Ending balance as of )(.*)'
                result = re.search(patern, endbalance)
                if result:
                    t = result.groups ()[1]
                    m, d, y=t.split('/')                    
                    currentMonth = months[int(m)]
            except Exception as ex:
                log (f'Error: - {ex}:' + ___FILE___LINE(), level3)
                continue
            try:
                description =  entry [1] # the description is in the seco
            except Exception as e:
                continue
            if description == '':
                continue
            if description == 'Description':
                continue
            for cat in ExpenseCategoriesList:
                found = False
                catdefinition = ExpenseCategoriesdataDict[cat]
                for val in catdefinition:
                    val = val.lower()
                    description = description.lower()
                    if val in description:
                        catdata = allcatogory_dict[cat]
                        catdata[cat].append(entry)
                        found = True
                        break
                if found == True:
                    break
                elif cat == 'Others':
                    catdata = allcatogory_dict[cat]
                    catdata[cat].append(entry)
                    break

def sort_table(data, col_num_clicked):
    try:
        table_data = sorted(data, key=operator.itemgetter(col_num_clicked))
    except Exception as e:
        sg.popup_error(f'Error sorting table {e}')
    return table_data




# ==================================================================================
#    getting data from Annual
#==================================================================================

def getMonthData(window, month):
    log('Enetring getMonthData...')
    global allcatogory_dict
    global currentMonth
    allcatogory_dict.clear()
    CreateEmptyCatData()
    monthDict = an.MontlyDistribution[month]
    for entry in monthDict[month]:
        try:
            description =  entry [1] # the description is in the seco
        except Exception as e:
            continue
        if description == '':
            continue
        if description == 'Description':
            continue
        for cat in ExpenseCategoriesList:
            found = False
            catdefinition = ExpenseCategoriesdataDict[cat]
            for val in catdefinition:
                val = val.lower()
                description = description.lower()
                if val in description:
                    catdata = allcatogory_dict[cat]
                    catdata[cat].append(entry)
                    found = True
                    break
            if found == True:
                break
            elif cat == 'Others':
                catdata = allcatogory_dict[cat]
                catdata[cat].append(entry)
                break
    updatealltabledata(window)
    calculateMonthlySaving()
    window['-currentmonth-'].update(value = currentMonth)
    window['-Saving-'].update(value = monthlySaving)
    window['-MONTHS-'].update(value = currentMonth)
    return monthDict

def ExportCatToExcel (window, slectedtab):
    category = slectedtab.replace("Tab_", "")
    log(f"Exporting {category} category to Excel " + ___FILE___LINE(), level3)
    data = allcatogory_dict[category] [category]
    #create the excel file name with current date and time
    dtt = f'{datetime.now()}'
    for ele in [':', '-', '.', ' ']:
        dtt = dtt.replace(ele, '')
    excelfile = f'{reportPath}{dtt}.xlsx'
    df1 = pd.DataFrame(data=data, columns=headings)
    df1.to_excel(excelfile, sheet_name=category)
    openreportfile(excelfile)

    #print(data)

def ExportAllToExcel():
    #create the excel file name with current date and time
    log("Exporting all tabs to Excel. "+ ___FILE___LINE(), level3)
    dtt = f'{datetime.now()}'
    for ele in [':', '-', '.', ' ']:
        dtt = dtt.replace(ele, '')
    excelfile = f'{reportPath}{dtt}.xlsx'

    with pd.ExcelWriter (excelfile) as writer:
        for cat in ExpenseCategoriesList:
            data = allcatogory_dict[cat][cat]
            df = pd.DataFrame(data=data, columns=headings)
            df.to_excel(writer, sheet_name=cat)
    openreportfile(excelfile)

def ExpenseBarPlot(window, save = False):
    x = []
    y = []
    x = sumOfExpensesCategoryAmounts.keys()
    for cat in x:
        val = float(sumOfExpensesCategoryAmounts[cat])
        y.append(val)
    # plot
    path = ___PATH___()
    ExpenseBarPlotpngFile = f"{reportPath}EExpenseBarPlotpng.png"
    bar_labels = x
    fig, ax = plt.subplots(figsize=(10, 5))
    bars =  ax.bar(x, y, label=bar_labels, width=1, edgecolor="white", linewidth=0.5)
    ax.set_ylabel('Expenses per month.')
    ax.set_title(f'Comparison of how much we spend per category for {currentMonth}', fontdict = titlefont, pad=32, loc = 'left')
    plt.xticks(range(len(x)), x, rotation=45)
    for index,data in enumerate(y):
        plt.text(x= index - 0.5 , y =data+1 , s=f"${data}" , fontdict=dict(fontsize=10))
    fig.tight_layout() # adjust the layout to fit the chart, or fig.subplots_adjust(bottom=0.2)
    if save == True:
        plt.savefig(ExpenseBarPlotpngFile)
        plt.close()
        return ExpenseBarPlotpngFile
    else:
        plt.show()
        return None
        
def ExpensePiePlot(window, save = False):
    # make figure and assign axis objects
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.subplots_adjust(wspace=0)
    ExpensePiePlotpngFile = f"{reportPath}ExpensePiePlotpng.png"
    # pie chart parameters
    labels = sumOfExpensesCategoryAmounts.keys()
    overall_ratios = []
    for cat in labels:
        val = float(sumOfExpensesCategoryAmounts[cat])
        overall_ratios.append(val)
    
    explode = []
    count = labels.__len__()
    
    for i in range(0, count, 1):
        if i == 0:
            explode.append(0.1)
        else:
            explode.append(0)

    # rotate so that first wedge is split by the x-axis
    angle = -180 * overall_ratios[0]
    wedges, *_ = ax.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                        labels=labels, explode=explode)
    ax.set_title(f'Comparison of proprtions of spending per category  for {currentMonth}', fontdict = titlefont, pad=32, loc = 'left')
    fig.tight_layout() # adjust the layout to fit the chart,
    if save == True:
        plt.savefig(ExpensePiePlotpngFile)
        plt.close()
        return ExpensePiePlotpngFile
    else:
        plt.show()
        return None
    

def donutPiePlot(save = False):
    # make figure and assign axis objects
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))
    ax.set_title(f"Expenses pie: A donut for {currentMonth}", fontdict = titlefont, pad=32, loc = 'left')
    categories = []
    categories = list(ExpenseCategoriesList)
    categories.pop(0) # remove the salaries
    categories.pop(0) # remove the salaries
    path = ___PATH___()
    ExpensePiePlotpngFile = f"{reportPath}ExpensePiePlotpng.png"
    # pie chart parameters
    labels = sumOfExpensesCategoryAmounts.keys()
    overall_ratios = []
    for cat in labels:
        val = float(sumOfExpensesCategoryAmounts[cat])
        overall_ratios.append(val)
    count = len(categories)
    for i in range(0, count):
        cat = f'{categories[i]} (${overall_ratios[i]})'
        categories[i] = cat

    wedges, texts = ax.pie(overall_ratios, wedgeprops=dict(width=0.5), shadow=True, startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
    for i, p in enumerate(wedges):# this is for the labaling
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(categories[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)  
    fig.tight_layout()
    if save == True:
        plt.savefig(ExpensePiePlotpngFile)
        plt.close()
        return ExpensePiePlotpngFile
    else:
        plt.show()
        return None

def ExpenseRatio(window, save = False):
    global percentofsalary
    x = []
    y = []
    x = percentofsalary.keys()
    for cat in x:
        val = float(percentofsalary[cat])
        y.append(val)
    # plot
    ExpenseRatiopnFile = f'{reportPath}ExpenseRatiopng.png'
    bar_labels = x
    fig, ax = plt.subplots(figsize=(10, 5))
    bars =  ax.bar(x, y, label=bar_labels, width=1,  edgecolor="white", linewidth=0.5)
    ax.set_ylabel('percent expenses per month.')
    ax.set_title(f'Spendings per category as a percentage of income  for {currentMonth}' , fontdict = titlefont, pad=32, loc = 'left')
    plt.xticks(range(len(x)), x, rotation=45)
    
    for index,data in enumerate(y):
        data = "%.2f" % data
        plt.text(x= index - 0.5 , y =float(data) + 0.5 , s=f"{data} %" , fontdict=dict(fontsize=10))
    
    fig.tight_layout() # adjust the layout to fit the chart,
    if save == True:
        plt.savefig(ExpenseRatiopnFile)
        plt.close()
        return ExpenseRatiopnFile
    else:
        plt.show()
        return None
    
def PlotBills(save = False):
    an.lineChartOfBills(save)

def AnnualBillsBars(save = False):
    an.barChartOfBills(save)

def  BillTable(save = False):
    an.tableOfBills(save)

def BillsTabulation(window):
    bdata = an.BillsTabulation()
    root = window.TKroot
    app = DisplayTable(parent = root, title="Bills tabulation", data=bdata, heading=an.modifiedMonths)
    app.pack(fill='both')
    root.mainloop()
   

def GroceryTable(save = False):
    an.tableOfGroceries(save)

def GroceryTabulation(window):
    bdata = an.GroceryTabulation()
    root = window.TKroot
    app = DisplayTable(parent = root, title="Grocery tabulation", data=bdata, heading=an.modifiedMonths)
    app.pack(fill='both')
    root.mainloop()

def CategoryTabulation(window):
    bdata = an.CategoryTabulation()
    root = window.TKroot
    app = DisplayTable(parent = root, title="Category tabulation", data=bdata, heading=an.modifiedMonths)
    app.pack(fill='both')
    root.mainloop()

def UtilityTabulation(window):
    bdata = an.UtilityTabulation()
    root = window.TKroot
    app = DisplayTable(parent = root, title="Utility tabulation", data=bdata, heading=an.modifiedMonths)
    app.pack(fill='both')
    root.mainloop()

def AnnualGroceryBars(save = False):
    an.barChartOfGroceries(save)

def openreportfile(reportfile):
    command = ''
    if reportfile.endswith('.pptx'):
        command = powerpoint
    elif reportfile.endswith('.pdf'): 
        command = acrobateReader
    elif reportfile.endswith('.xlsx'):
        command = excelreader  
    try:
        subprocess.run([command,reportfile]) # call the powerpoint\the file
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("So this app doesn't exist...") # handle file not found error.
        else:
            raise #Something else went wrong while trying to run the program\file
    

def MonthlyReport(window):
    #window['-PROGRESS_BAR-'].update(max_value = 28 )
    global reportfile
    count = 0
    window['-PROGRESS_BAR-'].update(visible= True)
    count += 2
    window['-PROGRESS_BAR-'].update(current_count=count)
    try:
        an.tableOfSalaries(save = True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        donutPiePlot(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        an.tableofExpenses(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        an.tableOfBills(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        ExpenseRatio(window, True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        ExpenseBarPlot(window, True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        BillsStats(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        GroceryStats(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        UtilityStats(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        CategoryStats(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        an.lineChartOfBills(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        an.lineChartOfGrocery(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        reportfile  = an.generateMonhtlyPdfReport(currentMonth)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
    except Exception as Ex:
        sg.popup_ok(f'Error Occurred: Monthly Report says: {Ex}')
    #sg.popup_ok('*** Monthly Report says.... "I am finished" ***')
    window['-PROGRESS_BAR-'].update(visible= False)
    openreportfile(reportfile)


def AnnualReport(window):
    global reportfile
    count = 0
    #window['-PROGRESS_BAR-'].update(max_value = 16 )
    window['-PROGRESS_BAR-'].update(visible= True)
    count += 2
    window['-PROGRESS_BAR-'].update(current_count=count)
    try:
        ExpenseBarPlot(window, True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count) 
        donutPiePlot(True) 
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        ExpenseRatio(window, True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        AnnualBillsBars(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        PlotBills(True) 
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        an.lineChartOfGrocery(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        AnnualGroceryBars(True)
        count += 2
        window['-PROGRESS_BAR-'].update(current_count=count)
        reportfile = an.generateAnnualReport(currentMonth)
    except Exception as Ex:
        sg.popup_ok(f'Error Occurred: Monthly Report says: {Ex}')
    #sg.popup_ok('*** Monthly Report says.... "I am finished" ***')
    window['-PROGRESS_BAR-'].update(visible= False)
    openreportfile(reportfile)

def UtilityStats(save = False):
    an.UtilityStats(save)

def BillsStats(save = False):
    an.BillsStats(save)

def GroceryStats(save = False):
    an.GroceryStats(save)

def CategoryStats(save = False):
    an.CategoryStats(save)
    
#def displaytimer():
#    global sg
#    sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', 
#                      transparent_color='white', time_between_frames=100)



def __main():
    global configfile
    global srcPath 
    global reportPath
    global currentMonth
    global an
    global progressbar
    log(' ', level3)
    log("=========================================Starting  Statement analyzer========================================", level3)

    #global redir
    srcPath = ___PATH___()
    srcPath = srcPath.replace('src', '')
    configfile = srcPath + 'configurations\\config.json'
    reportPath = srcPath + 'Reports\\'
    templatepath = srcPath + 'Templates\\'
    iconfile = f'{templatepath}statement.png'
    GetExpCategories()
    CreateEmptyCatData()
    
    window = createGui()
    an.setParent(window)
    monthDataDict = getMonthData(window, currentMonth)
    #redir = RedirectText(window, -TERMINAL_OUT-')
    #sys.stdout = redir
    selectedtab  = list(ExpenseCategoriesList)[0]
    updatetabledata(window, selectedtab)
    progressbar = window['-PROGRESS_BAR-']
    config = Configurator(currentMonth, 2024)
    while True:
        event, values = window.read()
        print("Event: (0), Values: {1}".format(event, values))
        if event in (sg.WIN_CLOSED, 'Cancel', 'Exit'):
            an.cleanup()
            break
        if isinstance(event, tuple):
            if 'Table_' in event[0]:
                #event[2][0] == -1 represent the raw
                #event[2][1] !=  -1 represent the collumn
                category = event[0]
                category = category.replace('Table_', '')
                if event[2][0] == -1 and event[2][1] != -1:
                    col_num_clicked = event[2][1]
                    category = selectedtab.replace("Tab_", "")
                    data = []
                    if category == "Salaries":
                        data = an.UpdatedSalariesDict[currentMonth][currentMonth]
                    else:
                        data = allcatogory_dict[category][category]
                    new_table_data = sort_table(data,col_num_clicked )
                    table = f'Table_{category}'
                    ttlamt = calculatetotal(data)
                    lastrow = [' ', 'Total:' ,ttlamt]
                    tmpdata = list(new_table_data).copy()
                    tmpdata.append(['----------------------',
                                    '----------------------',
                                    '----------------------',
                                    '----------------------'])
                    tmpdata.append(lastrow)
                    window[table].update(values =  tmpdata)

        elif event =='-STATEMENTFILE-': 
            global statementfile
            statementfile = values['-STATEMENTFILE-']
            loadcsvfile()
            updatealltabledata(window)
            calculateMonthlySaving()
            window['-currentmonth-'].update(value = currentMonth)
            window['-Saving-'].update(value = monthlySaving)
            window['-MONTHS-'].update(value = currentMonth)
        elif event == 'Tabgroup':
            print(f"Tab '{values[event]}' clicked")
            selectedtab = f'{values[event]}'
        elif event == 'Current tab to Excel':
            selectedtab = values['Tabgroup']
            ExportCatToExcel(window, selectedtab)
        elif event == 'All tabs to Excel':
            ExportAllToExcel()
        elif event == 'Set Theme':
            sg.user_settings_set_entry('-theme-', values['-THEME-'])
            theme = values['-THEME-']
            window.close()
            window ()
            sg.theme(theme)
            window = createGui()
            selectedtab = ''
            statementfile = values['-STATEMENTFILE-']
        elif event == 'Expenses Chart Plot':
            ExpenseBarPlot(window)   
        elif event == 'Expenses Pie Plot':
            #ExpensePiePlot(window)
            donutPiePlot(False)
        elif event == 'Expense Ratio':
            ExpenseRatio(window)
        elif event == 'Monthly Report':
            MonthlyReport(window)

        elif event == 'Annual Report':
            AnnualReport(window)
        elif event == 'Annual Bills':
            PlotBills(False)
        elif event == 'Annual Grocery':
            an.lineChartOfGrocery()
        elif event == 'Annual Bills Bars':
            AnnualBillsBars(False) 
        elif event == "Bills":
            BillTable(False)
        elif event == "Bills Tabulation":
            BillsTabulation(window)

        elif event == "Grocery Tabulation":
            GroceryTabulation(window)
        
        elif event == "Category Tabulation":
            CategoryTabulation(window)

        elif event == "Utility Tabulation":
            UtilityTabulation(window)

        elif event == "Groceries":
            GroceryTable(False)
        elif event == 'Annual Grocery Bars':
            AnnualGroceryBars(False) 
        elif event == "Annual Salary":
            an.tableOfSalaries()
        elif event == '-MONTHS-':
            currentMonth = values['-MONTHS-']
            window['-currentmonth-'].update(value = currentMonth)
            window['-Saving-'].update(value = monthlySaving)
            getMonthData(window, currentMonth)
        elif event == 'Bills Stats':
            BillsStats()
        elif event == 'Grocery Stats':
            GroceryStats()
        elif event == 'Utility Stats':
            UtilityStats()
        elif event == 'Category Stats':
            CategoryStats()
        elif event == 'Archive':
            Archive()
        elif event == 'Settings':
            config.start()
        elif event == 'About Me':
            sg.popup(AboutMe )
    window.close()


if __name__ == '__main__' :
    print("Entering in main")
    __main()