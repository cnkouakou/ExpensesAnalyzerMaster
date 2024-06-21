import customtkinter as ctk
import pandas as pd
from tkinter import END
import tkinter as tk
from pandastable import Table, Menu

class MyTable(Table):
    def __init__(self, parent=None, **kwargs):
        Table.__init__(self, parent, **kwargs)
        self.app = parent
        return

def popupmenu(self, event, rows=None, cols=None, ouside=None):
    popupmenu = Table.popupMenu(self, tearoff=0)
    def popupFocusOut(event):
        popupmenu.unpost()
    
    popupmenu.add_command(label= 'Close', command=self.app.close)
    popupmenu.bind("<FocusOut>", popupFocusOut)
    popupmenu.focus_set()
    popupmenu.post(event.x_root, event.y_root)
    return popupmenu


class DisplayTable(tk.Frame):
    
    col = ['A', 'B', 'C', 'D']

    def __init__(self, parent, title, data, heading):
        tk.Frame.__init__(self, parent, relief='sunken')
        self.data = data
        self.title = title
        self.heading = ['Name'] + heading

        df = pd.DataFrame(self.data, columns=self.heading)
        top = tk.Toplevel(self)
        self.table_FRAME = tk.Frame(top)
        top.title = self.title

        self.table = MyTable(self.table_FRAME,
                             dataframe = df,
                             showtoolbar = True,
                             showstatusbar = True,
                             rows = 30,
                             columns = self.heading, 
                             width=800

                             )
        self.table.grid(row=0, column=0, padx=10, pady=10, columnspan=4)
        self.table_FRAME.grid(row=1, column=1, padx=30, pady=10, columnspan=4, rowspan=10)
        self.table.rowheader = self.heading
        self.table.show()

if __name__ == '__main__':
        
    testdata = {
        "A":[12, 55, 33, 45],
        "B":[32, 15, 62, 41],
        "C":[95, 45, 21, 80],
        "B":[78, 12, 91, 77]
    }
    root = tk.Tk()
    app = DisplayTable(parent = root, title="My test of DisplayTable", data=testdata)
    app.pack(fill='both')
    root.mainloop()