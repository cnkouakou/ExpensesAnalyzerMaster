from pandastable import Table
import pandas as pd
import tkinter as tk
import customtkinter

class Tabulation(tk.Frame):
    def __init__(self, parent, data, col, title = None) -> None:
        tk.Frame.__init__(self, parent, relief = "sunken")

        self.data = data
        self.columns = col
        self.title = title

        self.df = pd.DataFrame(self.data, columns=self.columns)
        top = tk.Toplevel(self)
        top.title(self.title)
        self.table_FRAME = tk.Frame(top)
        
        self.table = Table(self.table_FRAME, 
                    dataframe=self.df, 
                    showstatusbar=True, 
                    showtoolbar=True, 
                    editable=True,
                    rows=20,
                    width=1000,
                    enable_menus=True
                    )
        
        #self.table.autoResizeColumns()
        #self.frame.grid(row=0, column=0, padx=10, pady=10, columnspan=4)
        #self.frame.grid(row=1, column=1, padx=30, pady=10, columnspan=4, rowspan=10)

        self.table.show()

       # root.mainloop()