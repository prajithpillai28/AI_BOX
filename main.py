
import sys
import pickle
import pandas as pd
import json
import csv
import xml.etree.ElementTree as ET  
from base.ml.machine import ML
from base.data.datapreprocessing import Datapreprocessing as DP

import numpy as np
from sklearn.model_selection import train_test_split


class Data:
  def data():
    r  = int(input("Please enter initial predictors: "))
    c = int(input("Please enter initial responsess: "))

    return r,c

  def menu():
    print("1. Dataset Sorting")
    print("2. Linear Regression")
    print("3. Multiple Linear Regression")
    print("4. Polynomial Linear Regression")
    print("5. Logistic regression")
    print("6. Exit")
    choice = int(input("Please enter your choice: "))
    return choice


  def sorting(pb,r,c):
    # Adding a contact 
    print(len(pb))
    print(pb)        
    p1=pb[:,2]
    r1=pb[:,5]
    print(" \n The inputs are : \n")
    print(p1)
    print(" \n The outputs are : \n")
    print(r1)
    # And once you modify the list, you return it to the calling function wiz main, here.
    return p1, r1

  def sortinglr(pb,r,c):
    # Adding a contact 
    print(len(pb))
    print(pb)        
    p1=pb[:,0]
    r1=pb[:,1]
    print(" \n The inputs are : \n")
    print(p1)
    print(" \n The outputs are : \n")
    print(r1)
    # And once you modify the list, you return it to the calling function wiz main, here.
    return p1, r1

  def sortingplr(pb,r,c):
    # Adding a contact 
    print(len(pb))
    print(pb)        
    p1=pb[:,0]
    r1=pb[:,1]
    print(" \n The inputs are : \n")
    print(p1)
    print(" \n The outputs are : \n")
    print(r1)
    # And once you modify the list, you return it to the calling function wiz main, here.
    return p1, r1

  def sortingmlr(pb,r,c):
    # Adding a contact 
    print(len(pb))
    print(pb)        
    p1=pb[:,0:r]
    r1=pb[:,r:r+c]
    # And once you modify the list, you return it to the calling function wiz main, here.
    print(" \n The inputs are : \n")
    print(p1)
    print(" \n The outputs are : \n")
    print(r1)
    return p1, r1
  def sortinglogr(pb,r,c):
    print(len(pb))
    print(pb)        
    p1=pb[:,0:r]
    r1=pb[:,r:r+c]
    # And once you modify the list, you return it to the calling function wiz main, here.
    print(" \n The inputs are : \n")
    print(p1)
    print(" \n The outputs are : \n")
    print(r1)

    return p1,r1

if __name__ == "__main__":      
  ch=1
  r,c=Data.data()
  dd = pd.read_csv('C:/Users/praji/OneDrive/Desktop/colour changing method/data1.csv') 
  dd1=np.array(dd)
  print(dd1)
  dd.head(r+c)
  pref="no"
  while(pref=="no"):
    choice=Data.menu()
    if choice==1:
      x,y=Data.sorting(dd1,r,c)
      print (str("\nPredictors send as input:\n "))
      print(x)
      print (str("\nResponses send as output:\n ")) 
      print(y)
    elif choice==2:
      x,y=Data.sorting(dd1,r,c)
      print(x)
      print(y)
      x1,x2,y1,y2=DP.train_test_splitlr(x,y)
      ML.lr(x1,y1,x2,y2)
    elif choice==3:
      x,y = Data.sortingmlr(dd1,r,c)
      x1,x2,y1,y2 = DP.train_test_splitmlr(x,y)
      ML.mlr(x1,y1,x2,y2,r)
    elif choice==4:
      x,y = Data.sortingplr(dd1,r,c)   
      x1,x2,y1,y2 = DP.train_test_splitlr(x,y)
      ML.plr(x1,y1,x2,y2)
    elif choice==5:
      x,y = Data.sortinglogr(dd1,r,c)   
      x1,x2,y1,y2 = DP.train_test_splitlogr(x,y)
      ML.logr(x1,y1,x2,y2)

    else:  
      pref="yes"

    


 

