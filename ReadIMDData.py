import io
from urllib.request import Request, urlopen

from PyPDF2 import PdfFileReader
import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import pandas as pd
import datetime

url = "https://mausam.imd.gov.in/bengaluru/mcdata/daily_report.pdf"
#url = "http://bedi.co.in/~pcws/imd_reports/15_10_2022.pdf"
remote_file = urlopen(Request(url)).read()
memory_file = io.BytesIO(remote_file)
pdf_file = PdfFileReader(memory_file)
 
# printing number of pages in pdf file
#print(pdf_file.numPages)
  
# creating a page object
pageObj = pdf_file.getPage(2)
  
# extracting text from page
data = pageObj.extractText()
#print(data)

re.sub('[^A-Za-z0-9 ]+', '', data)
data_list = data.strip().split(" ")
current_date = None
current_date_in_sheetformat = None
HAL_max = None
HAL_min = None
HAL_rain = None
City_max = None
City_min = None
City_rain = None
KIAL_max = None
KIAL_min = None
KIAL_rain = None



for i in range(len(data_list)):
  #  print(data_list[i])
    if(data_list[i].strip() == "OBSERVATIONS"):
        print(re.sub(r'/', '',data_list[i+10].strip()), data_list[i+8].strip(), re.sub(r'[a-zA-Z]', '', data_list[i+7].strip()))
        date_str = data_list[i+8].strip()+ "-" +re.sub(r'[a-zA-Z]', '', data_list[i+7].strip())+"-"+re.sub(r'/', '',data_list[i+10].strip())
        print("date after parsing ",date_str)
        try:
            current_date = datetime.datetime.strptime(date_str, '%B-%d-%Y').date()
            current_date_in_sheetformat = datetime.datetime.strptime(date_str, '%B-%d-%Y').strftime('%d/%m/%Y')
            
        except:
            print('Oops report in a different format')
            current_date = re.sub(r'[th]','',data_list[i+8].strip()) + "-" + data_list[i+9].strip() + "-" + re.sub(r'/', '', data_list[i+12].strip())
            print("date after parsing ",current_date)
            current_date_in_sheetformat = datetime.datetime.strptime(current_date, '%d-%B-%Y').strftime('%d/%m/%Y')           
            
        print('Date of report is ', current_date, 'date in the sheet format ', current_date_in_sheetformat )
        
    if(data_list[i].strip() == "HAL"):
        print("HAL max is "+data_list[i+2]+" Min is "+data_list[i+4]+" Rainfall: "+data_list[i+11])
        try:
            HAL_max = float(data_list[i+2])
            HAL_min = float(data_list[i+4])
            HAL_rain = float(data_list[i+11])
        except:
            print('Oops temperature in a different format')
        
    if(data_list[i].strip() == "City"):
        print("City max is "+data_list[i+1]+" Min is "+data_list[i+3]+" Rainfall: "+data_list[i+10])
        City_max = float(data_list[i+1])
        City_min = float(data_list[i+3])
        City_rain = float(data_list[i+10])
        
    if(data_list[i].strip() == "KIAL" and data_list[i+1].strip() == "AP" ):
        print("KIAL max is "+data_list[i+2]+" Min is "+data_list[i+4]+" Rainfall: "+data_list[i+11])
        KIAL_max = float(data_list[i+2])
        KIAL_min = float(data_list[i+4])
        KIAL_rain = float(data_list[i+11])
       
  
# closing the pdf file object
memory_file.close()

#sys.exit()
# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("bengaluruweathersheet-ecb00166c1e1.json", scope)
client = gspread.authorize(credentials)

# Open the spreadsheet
sheet = client.open('BengaluruWeather').worksheet('IMD-2022') 
# read csv with pandas
current_row = sheet.find(current_date_in_sheetformat)
print('Record found in ',current_row.row)
insertRow = [current_date_in_sheetformat, City_max, City_min, City_rain,  KIAL_max, KIAL_min, KIAL_rain, HAL_max, HAL_min, HAL_rain]
#sheet.insert_row(insertRow, current_row.row)
#sheet.update('A'+ str(current_row.row),current_date_in_sheetformat)
sheet.update('B'+ str(current_row.row),float(City_max.strip()))
sheet.update('C'+ str(current_row.row),float(City_min.strip()))
sheet.update('D'+ str(current_row.row),float(City_rain.strip()))
sheet.update('E'+ str(current_row.row), float(KIAL_max.strip()))
sheet.update('F'+ str(current_row.row), float(KIAL_min))
sheet.update('G'+ str(current_row.row), float(KIAL_rain))
sheet.update('H'+ str(current_row.row), float(HAL_max))
sheet.update('I'+ str(current_row.row), float(HAL_min))
sheet.update('J'+ str(current_row.row), float(HAL_rain))
print("sheet updated")
#for r in range(3, len(current_year_data)):
#    row = current_year_data(r)
    #pp = pprint.PrettyPrinter()
    #pp.pprint(row)
#    current_row_date = datetime.datetime.strptime(row[0].strip(), '%d/%m/%Y').date()
#   if((current_row_date == current_date) and row[1] == '' ):
#        insertRow = [City_max, City_min, City_rain,  KIAL_max, KIAL_min, KIAL_rain, HAL_max, HAL_min, HAL_rain]
#        sheet.add_rows(insertRow,r)# Insert the list as a row at index 1
#        break

#pp = pprint.PrettyPrinter()
#pp.pprint(row)

