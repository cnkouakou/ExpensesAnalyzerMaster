import PySimpleGUI as sg
import random, string
import os
import errno
import json
from Helper import ___PATH___, ___FILE___LINE, log, level0,level1,level2,level3, getMonth, getShortMonth, getnumMonth
edit = False
class Configurator():
    Configfile = ''
    def __init__(self, currentmonth, currentyear ) -> None:
        self.pptxcurrentmonth = currentmonth
        self.pptxcurrentyear = currentyear
        self.srcPath = ___PATH___()
        self.srcPath = self.srcPath.replace('src', '')
        self.Configfile = self.srcPath + 'configurations\\config.json'
        self.ReportingPath = self.srcPath + 'Reports\\'
        self.TemplatePath = self.srcPath + 'Templates\\'


    def getCategoryData(self):
        heading = ['Category', ['Category definition']]
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
        heading = ['Bills', ['Bills definition']]
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
        heading = ['Grocery', ['Grocery definition']]
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
        heading = ['Utility', ['Utility definition']]
        Utilitydata = []
        with open(self.Configfile, 'r') as f:
            data = json.load(f)
            UtilityList = data['Utility Distribution'].keys()
            Utilitydef = data['Utility Distribution'].copy()
            for Utility in UtilityList:
                lst = [Utility, Utilitydef[Utility]]
                Utilitydata.append(lst)
        return heading, Utilitydata


    def CreateConfigGui(self):
        catheading, catdata = self.getCategoryData()
        billheading, billdata = self.getBillsData()
        utilheading, utildata = self.getUtilityData()
        grocheading, grocdata = self.getGroceryData()

        sg.set_options(dpi_awareness=True)
        cat_layout = [
            [
                sg.Table(
                    values = catdata, 
                    headings= catheading, 
                    max_col_width=100,
                    font= ('Arial', 11),
                    auto_size_columns=True,
                    justification='left',
                    num_rows= 20, 
                    alternating_row_color=sg.theme_button_color()[1],
                    selected_row_colors='red on yellow',
                    size = (150, 20),
                    key='-CatConfigTable-',
                    expand_x= True,
                    expand_y=True,
                    enable_click_events= True,
                    vertical_scroll_only=False

                )
            ]
        ]

        button_layout  = [
                [
                sg.Text('cell clicked:'), sg.T(size=(20,1) ,key = '-CLICKED-CELL-'), sg.Button('Add New Categry', size=(20,1)),
                sg.Button('Delete Categry', size=(20,1)),
                sg.Button('Save', size=(20,1)),
                sg.T(size=(10,1)),
                sg.Button('Exit', size=(20,1))
             ]
        ]
        grocery_layout = [
            [
                sg.Table(
                    values = grocdata, 
                    headings= grocheading, 
                    max_col_width=100,
                    font= ('Arial', 11),
                    auto_size_columns=True,
                    justification='left',
                    num_rows= 20, 
                    alternating_row_color=sg.theme_button_color()[1],
                    selected_row_colors='red on yellow',
                    size = (150, 20),
                    key='-GrocConfigTable-',
                    expand_x= True,
                    expand_y=True,
                    enable_click_events= True,
                    vertical_scroll_only=False

                )
            ]


        ]
        bills_layout = [
            [
                sg.Table(
                    values = billdata, 
                    headings= billheading, 
                    max_col_width=100,
                    font= ('Arial', 11),
                    auto_size_columns=True,
                    justification='left',
                    num_rows= 20, 
                    alternating_row_color=sg.theme_button_color()[1],
                    selected_row_colors='red on yellow',
                    size = (150, 20),
                    key='-BillConfigTable-',
                    expand_x= True,
                    expand_y=True,
                    enable_click_events= True,
                    vertical_scroll_only=False

                )
            ]

        ]
        utility_layout = [
            [
                sg.Table(
                    values = utildata, 
                    headings= utilheading, 
                    max_col_width=100,
                    font= ('Arial', 11),
                    auto_size_columns=True,
                    justification='left',
                    num_rows= 20, 
                    alternating_row_color=sg.theme_button_color()[1],
                    selected_row_colors='red on yellow',
                    size = (150, 20),
                    key='-UtilConfigTable-',
                    expand_x= True,
                    expand_y=True,
                    enable_click_events= True,
                    vertical_scroll_only=False

                )
            ]
        ]

        Tabgroup_layout = [[
            sg.TabGroup(
                [[
                    sg.Tab("Category", cat_layout), 
                    sg.Tab("Grocery", grocery_layout),
                    sg.Tab("Bills", bills_layout),
                    sg.Tab("Utilities", utility_layout)
                ]])
            
            ]]
        final_layout = [
            Tabgroup_layout,
            [sg.Frame( 'Click Action Button', button_layout, size = (1060, 50), element_justification = 'left', title_color = 'yellow', border_width = 1)]
        ]

        window = sg.Window('Configuration Wndow', final_layout, resizable=True, finalize=True)
        return window
    
    def update_cell(self, window, key, row, col, justify = 'right' ):
        global textvariable, edit
        if edit or row <= 0:
            return None
        #define the call back funtion when we go out of focus
        def callback(event,row,col,text,key):
            global edit
            try:
                widget = event.widget
                if key == 'Focus_Out':
                    text = widget.get()
                # we need to distrot the widget
                widget.destroy()
                widget.master.destroy()
                values = list(table.item(row, 'values'))
                values[col] = text
                table.item(row, values=values)
                edit = False
            except Exception as Ex:
                edit = False
                print (f'{Ex}')

        edit = True
        y_offset = 32
        x_ofset = 15
        root = window.TKroot
        table = window[key].Widget
        text = table.item(row,'values')[col]
        x, y, width, height = table.bbox(row, col)
        # create a frame 
        frame = sg.tk.Frame(root)
        # set the position of the frame to thw box
        frame.place(x=x + x_ofset, y=y + y_offset, anchor='nw', width=width, height=height)
        #get the conten of the cell
        textwidth = len(str(text))
        textvariable = sg.tk.StringVar(value = str(text))
        #textvariable.set(value = str(text))
        entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify, width=textwidth, font=('Arial', 11))
        entry.pack()
        #make sure the entry cover all the way to the end of the frame 
        entry.select_range(0, sg.tk.END)
        # and the cursor is at the end of the entry
        entry.icursor(sg.tk.END)
        entry.focus_force()

        entry.bind('<FocusOut>', lambda e, r=row, c=col, t=text, k='Focus_Out': callback(e,r,c,t,k))

    

    def start(self): 
        window = self.CreateConfigGui()
        while True:
            event, values = window.read()
            print("Event: (0), Values: {1}".format(event, values))
            if event in (sg.WIN_CLOSED, 'Cancel', 'Exit'):
                break
            elif isinstance(event, tuple):
                if isinstance(event[2][0], int) and event[2][1] != -1:
                    tablekey = event[0]
                    cell = event[2]
                    row, col = event[2]
                    #col_num_clicked = event[2][1]
                    window['-CLICKED-CELL-'].update(cell)
                    self.update_cell(window, tablekey,row + 1, col , justify = 'left' )
        window.close()

if __name__ == '__main__' :
    print("Entering in main")
    config = Configurator('May', 2024)
    config.start()
