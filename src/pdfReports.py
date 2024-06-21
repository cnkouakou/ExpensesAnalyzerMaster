
from fpdf import FPDF
import datetime
import os
from datetime import date
from datetime import datetime
from Helper import ___PATH___, ___FILE___LINE, log, level0,level1,level2,level3
WIDTH = 210
HEIGHT = 297
class pdfReports():
    #the below are sessons of the pdf report 
    
    reportfilename = ""
    pdfIntroduction = ""
    pdfIncome = ""
    pdfExpenses = ""
    pdfBillsDetails = ""
    pdfClothing = ""
    pdfCreditCardpayment = ""
    pdfcurrentmonth = ""
    pdfcurrentyear = ""
    pdftitle = ""
    pdfSpendingSuggestion = "Spending Suggestions:"
    pdfReportingPath = ""
    pdfTemplatePath = ''
    pdfConfigfile = ""
    currentGrocery           = 0.0
    grocerymin                = 0.0
    currentBill              = 0.0
    billmin                  = 0.0
    currentClothing          = 0.0
    clothingmin              = 0.0
    incomecurrent             = 0.0
    twentypercentincome      = 0.0
    thirtyperscentofsaving   = 0.0
    tenperscentofsaving      = 0.0
    totalExpensemin          = 0.0
    maxsaving                = 0.0
    freelanceincome          = 0.0
    mortgage                 = 0.0
    utility                  = 0.0
    carpayment               = 0.0
    Gas                      = 0.0
    insurrance               = 0.0
    telephone                = 0.0
    subscriptions            = 0.0
    totalOthers              = 0.0
    restaurant               = 0.0
    pharmacy                 = 0.0
    CreditCard               = 0.0
    studentloan              = 0.0
    totaMonthlyExp           = 0.0

    def __init__(self, currentmonth, currentyear ) -> None:
        self.pdfcurrentmonth = currentmonth
        self.pdfcurrentyear = currentyear
        srcPath = ___PATH___()
        srcPath = srcPath.replace('src', '')
        pdfConfigfile = srcPath + 'configurations\\config.json'
        self.pdfReportingPath = srcPath + 'Reports\\'
        self.pdfTemplatePath = srcPath + 'Templates\\'
        self.pdftitle = f"Household Financial Report: {self.pdfcurrentmonth} {self.pdfcurrentyear}"
    
    def getIncome(self):
        incomecurrent = float("%.2f" % self.incomecurrent )
        freelanceincome =float("%.2f" % self.freelanceincome)
        totaMonthlyExp = float("%.2f" % self.totaMonthlyExp)
        totalincome = incomecurrent + freelanceincome
        netincome = float("%.2f" %(totalincome - totaMonthlyExp))

        pdtIncome = str(f'''Income:
            Salary (after tax): ${self.incomecurrent}
            Freelance/Side Income: ${self.freelanceincome}
            Total Income: ${float("%.2f" % self.incomecurrent) + float("%.2f" % self.freelanceincome) }
             Net Income (Income - Expenses): ${netincome}
            =======================================================================
                    ''')
        return pdtIncome
    
    def getPdfExpenses (self): 
        mortgage = "%.2f" % self.mortgage
        utilities = "%.2f" % self.utility
        totalhousing = float("%.2f" %(float(mortgage) + float(utilities)))

        pdfExpenses = str(f'''Expenses:
        Housing:Rent/Mortgage: ${self.mortgage}
        Utilities (electricity, water, gas, Internet & Cable, Telephone...: ${self.utility}
        Total Housing: ${totalhousing}
        Groceries: Monthly Grocery Spend: ${self.currentGrocery}
        Transportation: Car Payment: ${self.carpayment}; Gas: ${self.Gas}; Insurance: ${self.insurrance}
        Bills:Phone: ${self.telephone}; Miscellaneous/Others: ${self.totalOthers}
        Total Bills: ${self.currentBill}.
        Clothing: Clothing: ${self.currentClothing}     
        Entertainment: Dining Out: ${self.restaurant}    
        Healthcare: Total Healthcare/pharmacy: ${self.pharmacy}
        Debt Payments:Credit Card Payments: ${self.CreditCard}
        Student Loans: ${self.studentloan}
        Total Debt Payments: ${float(self.CreditCard) + float(self.studentloan)}
        Total Monthly Expenses: ${self.totaMonthlyExp}          
        
            ''')
        return pdfExpenses

    def getpdfsuggestion(self):
        pdfsuggestion = (f'''
        Spending Suggestions:
        Groceries:Current Spend: ${self.currentGrocery}
        Suggestion: Try meal planning and bulk buying to reduce the grocery bill by 10-15%. Target: ${self.grocerymin}.
        Bills: Current Spend: ${self.currentBill}
        Suggestion: Review phone and subscription plans to ensure they are necessary and cost-effective. 
        Consider downgrading or eliminating some services. Target: ${self.billmin}.
        Clothing:Current Spend: ${self.currentClothing} 
        Suggestion: Set a quarterly clothing budget instead of monthly, and look for sales and discounts. 
        your target is ${self.clothingmin}.
        Savings: Suggestion: Aim to save at least 20% of net income. With ${self.incomecurrent} net income, 
        save at least ${self.twentypercentincome} monthly. Use automatic transfers to a savings account to ensure consistency.
        Long-Term Savings: ${self.thirtyperscentofsaving} (Emergency Fund, Retirement, Investments)
        Short-Term Savings: ${self.tenperscentofsaving}  (Vacations, Large Purchases)
        
        ''')
        return pdfsuggestion

    pdfFinancialOutlook = "Adjusted Financial Outlook:"

    def getpdfRevisedMonthly(self):
        pdfRevisedMonthly = str(f'''
        "Adjusted Financial Outlook:"                    
        Revised Monthly Expenses:

        Groceries: ${self.grocerymin}
        Bills: ${self.billmin}
        Clothing: ${self.clothingmin}
        Total Revised Expenses: ${self.totalExpensemin}
        Revised Net Saving (Income - Revised Expenses): ${self.maxsaving}

        Revised Savings:

        Savings (20% of Revised Net Income): ${self.twentypercentincome}
        Long-Term Savings: ${self.thirtyperscentofsaving}
        Short-Term Savings: ${self.tenperscentofsaving}
        This approach ensures a balanced budget, where discretionary spending is minimized, 
        and savings are maximized, ensuring financial stability and growth.
        ============================================================================
        ''')
        return pdfRevisedMonthly


    def setTheNumbers(self, numbers, currentmonth):
        global currentGrocery         
        global grocerymin                
        global currentBill              
        global billmin                  
        global currentClothing          
        global clothingmin              
        global incomecurrent             
        global twentypercentincome      
        global thirtyperscentofsaving   
        global tenperscentofsaving      
        global totalExpensemin          
        global maxsaving                
        global freelanceincome         
        global mortgage                 
        global utility                 
        global carpayment               
        global Gas                     
        global insurrance               
        global telephone                
        global subscriptions            
        global totalOthers              
        global restaurant               
        global pharmacy                
        global CreditCard               
        global studentloan              
        global totaMonthlyExp  
        self.pdfcurrentmonth          = currentmonth          
        self.currentGrocery           = float(numbers['currentGrocery'])
        self.grocerymin                = float(numbers['grocerymin'])
        self.currentBill              = float(numbers['currentBill'])
        self.billmin                  = float(numbers['billmin'])
        self.currentClothing          = float(numbers['currentClothing'])
        self.clothingmin              = float(numbers['clothingmin'])
        self.incomecurrent            = float(numbers['incomecurrent'])
        self.twentypercentincome      = float(numbers['twentypercentincome'])
        self.thirtyperscentofsaving   = float(numbers['thirtyperscentofsaving'])
        self.tenperscentofsaving      = float(numbers['tenperscentofsaving'])
        self.totalExpensemin          = float(numbers['totalExpensemin'])
        self.maxsaving                = float(numbers['maxsaving'])
        self.freelanceincome          = float(numbers['freelanceincome'])
        self.mortgage                 = float(numbers['mortgage'])
        self.utility                  = float(numbers['utility'])
        self.carpayment               = float(numbers['carpayment'])
        self.Gas                      = float(numbers['Gas'])
        self.insurrance               = float(numbers['insurrance'])
        self.telephone                = float(numbers['telephone'])
        self.subscriptions            = float(numbers['subscriptions'])
        self.totalOthers              = float(numbers['totalOthers'])
        self.restaurant               = float(numbers['restaurant'])
        self.pharmacy                 = float(numbers['pharmacy'])
        self.CreditCard               = float(numbers['CreditCard'])
        self.studentloan              = float(numbers['studentloan'])
        self.totaMonthlyExp           = float(numbers['totaMonthlyExp'])

    def getReportFilename(self):
        dtt = f'{datetime.now()}'
        for ele in [':', '-', '.', ' ']:
            dtt = dtt.replace(ele, '')
        self.reportfilename = self.pdfReportingPath + dtt + 'MonthlyReport.pdf'

    def header(self, pdf):
        # Arial bold 15
        pdf.image(f'{self.pdfTemplatePath}header.png', 0,0, WIDTH)
        pdf.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = pdf.get_string_width(self.pdftitle) + 6
        pdf.set_x((210 - w) / 2)
        # Colors of frame, background and text
        pdf.set_draw_color(0, 80, 180)
        pdf.set_fill_color(230, 230, 0)
        pdf.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        pdf.set_line_width(1)
        # Title
        pdf.cell(w, 9, self.pdftitle, 1, 1, 'C', 1)
        # Line break
        pdf.ln(10)
    
    

    def add_footer(self, pdf):
        # Position at 1.5 cm from bottom
        pdf.set_y(-15)
        # Arial italic 8
        pdf.set_font('Arial', 'I', 8)
        # Text color in gray
        pdf.set_text_color(128)
        # Page number
        pdf.cell(0, 10, 'Page ' + str(pdf.page_no()), 0, 0, 'C')

    def add_page_title(self, num, label, pdf):
        # Arial 12
        pdf.set_font('Arial', '', 12)
        # Background color
        pdf.set_fill_color(200, 220, 255)
        # Title
        pdf.cell(0, 6, 'Page %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        pdf.ln(4)

    def add_page_body(self, name, pdf): 
        pdf.set_text_color(0, 0, 0)       
        # Times 12
        pdf.set_font('Times', '', 12)
        # Output justified text
        pdf.set_xy(10, 10)
        pdf.image(f'{self.pdfReportingPath}Salaries-table.png', 40, 40, 0.65*WIDTH)
        pdf.set_xy(10, 100)
        pdf.multi_cell(0, 5, self.getIncome(), border = 0)

        pdf.set_xy(10, 200)
        pdf.image(f'{self.pdfReportingPath}Expenses-table.png', 40, 140, 0.65*WIDTH)

        pdf.set_xy(10, 240)
        pdf.image(f'{self.pdfReportingPath}ExpensePiePlotpng.png', 40, 240, 0.65*WIDTH)

        pdf.set_xy(10, 340)
        pdf.multi_cell(0, 5, self.getPdfExpenses(), border = 0)
        pdf.multi_cell(0, 5, self.getpdfsuggestion(), border = 0)
        
        # Line break
        pdf.ln()

    def add_page_body (self, content, pngfile, pdf, ypos):
        pdf.set_text_color(0, 0, 0)     
        pdf.set_font('Times', '', 12)  # Times 12  
        pdf.set_xy(10, ypos)
        pngfileexist =  os.path.isfile(pngfile)
        if pngfileexist:
            pdf.image(pngfile, 40, 40, 0.65*WIDTH)
            pdf.set_xy(10, 100)
        pdf.multi_cell(0, 5, content, border = 0)
       
    def add_an_image(slf, pdf, imagefile, x, y, w):
        pngfileexist =  os.path.isfile(imagefile)
        if pngfileexist:
            pdf.image(imagefile, x, y, w)
        else:
            print(f'Invalid File {imagefile}')

    def add_text(self, texttoadd, pdf, xpos, ypos):
        pdf.set_text_color(0, 0, 0)     
        pdf.set_font('Times', '', 12)  # Times 12 
        pdf.set_xy(xpos, ypos) 
        pdf.multi_cell(0, 5,  texttoadd, border = 0)


    def add_a_page(self, num, title, pdf):
        pdf.add_page()
        self.header(pdf)
        self.add_page_title(num, title, pdf)


    def generatePdfReport(self):
        self.pdftitle = f"Household Financial Report: {self.pdfcurrentmonth} {self.pdfcurrentyear}"
        self.getReportFilename()
        pdf = FPDF()
        pdf.set_title(self.pdftitle)
        pdf.set_author('Claude Kouakou')

        self.add_a_page(1, "Income",  pdf)
        salarypngfile = f'{self.pdfReportingPath}Salaries-table.png'
        incomecontent = self.getIncome()
        self.add_an_image(pdf, salarypngfile, 40, 40, 0.7*WIDTH)
        self.add_text(incomecontent, pdf, 10, 85)

        Expbarpngfile = f'{self.pdfReportingPath}ExpenseRatiopng.png'
        self.add_an_image(pdf, Expbarpngfile, 40, 120, 0.7*WIDTH)

        Exppiepngfile = f'{self.pdfReportingPath}ExpensePiePlotpng.png'
        self.add_an_image(pdf, Exppiepngfile, 40, 195, 0.7*WIDTH)

        self.add_a_page(2, "Expenses",  pdf)
        Expensespng = f'{self.pdfReportingPath}Expenses-table.png'
        self.add_an_image(pdf, Expensespng, 40, 40, 0.7*WIDTH)
        expcontent = self.getPdfExpenses()
        self.add_text(expcontent, pdf, 10, 150)


        self.add_a_page(3, "Suggestion",  pdf)
        Suggestionpng = f'{self.pdfReportingPath}CategoryStats-table.png'
        self.add_an_image(pdf, Suggestionpng, 40, 40, 0.7*WIDTH)
        suggestions = self.getpdfsuggestion()
        self.add_text(suggestions, pdf, 10, 180)

        self.add_a_page(4, "Stastics",  pdf)
        Stat1png = f'{self.pdfReportingPath}BillsStats-table.png'
        self.add_an_image(pdf, Stat1png, 40, 40, 0.7*WIDTH)
        Stat2png = f'{self.pdfReportingPath}GroceryStats-table.png'
        self.add_an_image(pdf, Stat2png, 40, 150, 0.7*WIDTH)
        
        self.add_a_page(5, "Stastics - continue",  pdf)
        Stat3png = f'{self.pdfReportingPath}UtilitiesStats-table.png'
        self.add_an_image(pdf, Stat3png, 40, 40, 0.7*WIDTH)
        Stat4png = f'{self.pdfReportingPath}billLineChartFile.png'
        self.add_an_image(pdf, Stat4png, 40, 110, 0.7*WIDTH)
        Stat5png = f'{self.pdfReportingPath}GroceryLineChartFile.png'
        self.add_an_image(pdf, Stat5png, 40, 185, 0.7*WIDTH)
 
        pdf.output(self.reportfilename, 'F')
        
        return self.reportfilename

    def generateAnualReport(self):
        pass
       

