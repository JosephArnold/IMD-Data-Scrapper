from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import csv

def fill_form():
    #regno = 5304740
    
    dict = {}
    
    with open('TNRainfallJanuary.csv', 'r') as file:
    # Create a CSV reader object
        csv_reader = csv.reader(file)
    
    
        # Iterate over each row in the CSV file
        for row in csv_reader:
        # Assuming the first column is the key and the second and third columns are the values
            if(len(row) > 0):
                if row[0] in dict.keys():
                    dict[row[0]]['Rainfall'] += float(row[2])
                else:
                    dict.update({row[0]: {'District': row[1], 'Rainfall': float(row[2])}})
        
    with open('TNRainfallFebruary.csv', 'r') as file:
    # Create a CSV reader object
        csv_reader = csv.reader(file)
    
    
        # Iterate over each row in the CSV file
        for row in csv_reader:
        # Assuming the first column is the key and the second and third columns are the values
            if(len(row) > 0):
                if row[0] in dict.keys():
                    dict[row[0]]['Rainfall'] += float(row[2])
                else:
                    dict.update({row[0]: {'District': row[1], 'Rainfall': float(row[2])}})

    with open('TNRainfallMarch.csv', 'r') as file:
    # Create a CSV reader object
        csv_reader = csv.reader(file)
    
    
        # Iterate over each row in the CSV file
        for row in csv_reader:
        # Assuming the first column is the key and the second and third columns are the values
            if(len(row) > 0):
                if row[0] in dict.keys():
                    dict[row[0]]['Rainfall'] += float(row[2])
                else:
                    dict.update({row[0]: {'District': row[1], 'Rainfall': float(row[2])}})

    with open('TNRainfallApril.csv', 'r') as file:
    # Create a CSV reader object
        csv_reader = csv.reader(file)
    
    
        # Iterate over each row in the CSV file
        for row in csv_reader:
        # Assuming the first column is the key and the second and third columns are the values
            if(len(row) > 0):
                if row[0] in dict.keys():
                    dict[row[0]]['Rainfall'] += float(row[2])
                else:
                    dict.update({row[0]: {'District': row[1], 'Rainfall': float(row[2])}})
        
    with open('TNRainfall.csv', 'r') as file:
    # Create a CSV reader object
        csv_reader = csv.reader(file)
     
        # Iterate over each row in the CSV file
        for row in csv_reader:
        # Assuming the first column is the key and the second and third columns are the values
            if(len(row) > 0):
                if row[0] in dict.keys():
                    dict[row[0]]['Rainfall'] += float(row[2])
                else:
                    dict.update({row[0]: {'District': row[1], 'Rainfall': float(row[2])}})
   
    
    with open('C:\\Users\\xjose\\OneDrive\\Desktop\\python\\TNRainfall26thMay.csv','w') as f:
        writer = csv.writer(f)
        
        for key in dict.keys():
            writer.writerow([key, dict[key]['District'], dict[key]['Rainfall']])
# Call the function to fill the form
#with open("regn:os528.txt", "a") as file:
#    file.write("Writing to file \n")
fill_form()
