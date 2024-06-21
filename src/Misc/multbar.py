import numpy as np  
import matplotlib.pyplot as plt  
  
X = ['Group A','Group B','Group C','Group D'] 
Ygirls = [10,20,20,40] 
Zboys = [20,30,25,30] 
ZTeen = [30,20,20,24] 
  
X_axis = np.arange(len(X)) 
X =  X_axis - 0.2 
plt.bar(X, Ygirls, 0.2, label = 'Girls') 
X= X + 0.2
plt.bar(X, Zboys, 0.2, label = 'Boys') 
X= X + 0.2
plt.bar(X, ZTeen, 0.2, label = 'ZTeen') 
  
plt.xticks(X_axis, X) 
plt.xlabel("Groups") 
plt.ylabel("Number of Students") 
plt.title("Number of Students in each group") 
plt.legend() 
plt.show() 