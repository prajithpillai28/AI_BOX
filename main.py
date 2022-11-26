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
    print("4. Save list to csv")
    print("5. Save list to xml")
    print("6. Exit")
    choice = int(input("Please enter your choice: "))
    return choice


  def sorting(pb,r,c):
    # Adding a contact 
    print(len(pb))
    print(pb)        
    p1=pb[:,0]
    r1=pb[:,1]
    # And once you modify the list, you return it to the calling function wiz main, here.
    return p1, r1

  def display_all(pb):
    if not pb:
    # if display function is called after deleting all contacts then the len will be 0
    # And then without this condition it will throw an error
      print("List is empty: []")
    else:
      for i in range(len(pb)):
        print(pb[i])
  def search_existing(pb):
    # This function searches for an existing contact and displays the result
    choice = int(input("Enter search criteria\n\n\
    1. Name\n2. Address\n3. Number\n"))
    # We're doing so just to ensure that the user experiences a customized search result
      
    temp = []
    check = -1
      
    if choice == 1:
    # This will execute for searches based on contact name
      query = str(
      input("Please enter the name of the contact you wish to search: "))
      for i in range(len(pb)):
        if query == pb[i][0]:
          check = i
          temp.append(pb[i])
                  
    elif choice == 2:
    # This will execute for searches based on address
      query = str(
      input("Please enter the address of the contact you wish to search: "))
      for i in range(len(pb)):
        if query == pb[i][1]:
          check = i
          temp.append(pb[i])
                  
    elif choice == 3:
    # This will execute for searches based on contact's e-mail address
      query = int(input("Please enter the number of the contact you wish to search: "))
      for i in range(len(pb)):
        if query == pb[i][2]:
          check = i
          temp.append(pb[i])
    else:
      # If the user enters any other choice then the search will be unsuccessful
      print("Invalid search criteria")
      return -1
      # returning -1 indicates that the search was unsuccessful
      
      # all the searches are stored in temp and all the results will be displayed with
      # the help of display function
      
    if check == -1:
      return -1
          # returning -1 indicates that the query did not exist in the directory
    else:
      display_all(temp)
      return check
      # we're just returning a index value wiz not -1 to calling function just to notify
      # that the search worked successfully

  def createxml(pb):
  
        # we make root element
    usrconfig = ET.Element("phonebook")
        # create sub element
    usrconfig = ET.SubElement(usrconfig, "phonebook")
        # insert list element into sub elements
    for user in range(len( pb)):
      usr = ET.SubElement(usrconfig, "phone")
      usr.text = str(pb[user])
      tree = ET.ElementTree(usrconfig)
      # write the tree into an XML file
      tree.write("Output.xml", encoding ='utf-8', xml_declaration = True)

  def createcsv(pb):
    file = open('Phonebook.csv', 'w+', newline ='') 
    with file:     
      write = csv.writer(file) 
      write.writerows(pb) 

if __name__ == "__main__":      
  ch=1
  r,c=Data.data()
  dd = pd.read_csv('C:/Users/praji/OneDrive/Desktop/colour changing method/data_299.csv') 
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
      Directory.search_existing(pb)
    elif choice==4:
      Directory.createcsv(pb)
    elif choice==5:
      Directory.createxml(pb)
    else:  
      pref="yes"

    


 

