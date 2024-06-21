import PySimpleGUI as sg
from inspect import currentframe, getframeinfo
import os
import datetime
from datetime import date
from datetime import datetime

python_only = False
level0 = None
level1 = 1
level2 = 2
level3 = 3
OPTION1 = 'CATEGORY'
OPTION2 = 'BILLS'
OPTION3 = 'UTILITY'
OPTION4 = 'GROCERY'

stmtlogfile = "stmt.log"

Months  =  ['', 'January', 'February', 'March', 'April', 'May', 'June','July', 'August', 'September', 'October', 'November', 'December' ]
shortMonths  =  ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec' ]
NumMonths = [0,1,2,3,4,5,6,7,8,9,10,11,12]

def getMonth(n : int):
    return Months[n]

def getShortMonth(n : int):
    return shortMonths[n]

def getnumMonth(m: str):
    for i in range(0, len(Months)):
        if Months[i] == m:
            return i


def ___PATH___ (do_print=False):
    frameinfo = getframeinfo(currentframe().f_back)
    filename =  frameinfo.filename.split('/')[-1]
    path = os.path.dirname(os.path.abspath(filename))
    if do_print:
        log(path + ___FILE___LINE(), level3)
    return path
   
def ___FILE___LINE(do_print=False):
    frameinfo = getframeinfo(currentframe().f_back)
    filename = frameinfo.filename.split('/')[-1]
    linenumber =  frameinfo.lineno
    loc_str = '--->File: %s, line: %d ' % (filename, linenumber)
    if do_print: 
        print('HERE AT' % (loc_str)) 
    else:
        return loc_str
    
def fileandline():
    frameinfo = getframeinfo(currentframe().f_back)
    filename = frameinfo.filename.split('/')[-1]
    linenumber =  frameinfo.lineno
    loc_str = '--->File: %s, line: %d ' % (filename, linenumber)

    return loc_str
def log(str, level = None):
    if level == None:
        print(str)
    elif level == level1:
        print(str)
    elif level == level2:
        print(str + ___FILE___LINE())
    elif level == level3:
        path = ___PATH___()
        path = path.replace('src', '')
        dtt = f'[{datetime.now()}]  '
        with open(path + "Logs\\" + stmtlogfile, 'at') as log:
            logstr = dtt + str + "\n"
            #print(logstr)
            log.write(logstr)
            log.close() 

def get_file_list_dict():
    datapath = get_data_path()
    data_files_dict = {}
    for dirname,  dirnames, filenames in os.walk(datapath):
        for filename in filenames:
            if python_only is not True or filename.endswith('.py') or filename.endswith('.pyw'):
                fname_full = os.join(dirname, filename)
                if filename not in data_files_dict.keys():
                    data_files_dict[filename] = fname_full
                else:
                    for i in range(1,100):
                        new_filename = f'{filename}_{i}'
                        if new_filename not in data_files_dict:
                            data_files_dict[new_filename] = fname_full
                            break

    return data_files_dict                

def get_data_path():
    data_path = sg.user_settings_get_entry('-data folder', os.path.dirname(__file__))
    return data_path + '\datapath'

def get_log_file():
    data_path = sg.user_settings_get_entry('-log file', os.path.dirname(__file__))
    return data_path + '\log'

def get_data_file():
    data_path = sg.user_settings_get_entry('-data folder-', os.path.dirname(__file__))
 
def get_file_list():
    return sorted(list(get_file_list_dict().keys()))