from annualReporting import *
from pdfReports import *
from pptxReports import *
from time import sleep
import subprocess




def run_command(command):
    p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    return p.communicate()
try:
    run_command('NOTEPAD++')
except Exception as ex:
    print(ex)
   
an = Annual()
ppt = PPTXReport('May', '2024')
rpt = pdfReports('May', '2024')
an.prep()

#an.updateMonthlySalaries()
ppt.generatepptxReport()
an.GroceryStats(True)
sleep(3)
an.UtilityStats(True)
sleep(3)
an.CategoryStats(True)
sleep(3)
an.BillsStats(True)
sleep(3)
#an.tableOfGroceries()
#an.tableofExpenses(False)
an.tableOfSalaries()
an.generatMonhtlyPdfReport('May')
#rpt.generatePdfReport()
an.GetBillValues()
#ar = [1.0, 2.0, 3.0, 0.0, 0.0, 4.0, 0.0, 0.0]
#an.removezeros(ar)
#an.tableOfBills(True)
#min1, mean1, max1 = an.getCatmmm("Grocery")
#min2, mean2, max2 = an.getCatmmm("Restaurant")
#min3, mean3, max3 = an.getCatmmm("Clothing")
#an.calculateBillsMeanValues()


#an.lineChartOfBills()
#an.barChartOfBills()
#print (dist2)