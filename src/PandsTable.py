from pandastable import Table
import pandas as pd
import tkinter as tk
df = pd.DataFrame({'Name' : ['John', 'Alice', 'Bob' ],
                   'Age': [20,30,40],
                   'Gender': ['Male', 'Female', 'Male']
                   })
class PandasApp():
    def __init__(self) -> None:
        self.construct()

    def construct(self):
        root = tk.Tk()
        root.title('TK table')
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        self.table = Table(self.frame, dataframe=df, showstatusbar=True, showtoolbar=True)
        self.bttn1 = tk.Button(self.frame, text='Add New', width=20, state='active')

        self.table.show()
       
        root.mainloop()


        #self.add_row()

    def add_row(self):
        new_row = {'Name': 'Smith', 'Age': '18', 'Gender': 'Male'}
        self.table.model.df = self.table.model.df._append(new_row, ignore_index= True)
        self.table.redraw()


app = PandasApp()


