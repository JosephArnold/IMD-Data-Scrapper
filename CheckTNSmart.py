from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import csv

def fill_form():
    
    dict = {}
    with open('TNRainfall28thMay.csv', 'r') as file:
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

    startdate = datetime.strptime("29/05/2023", "%d/%m/%Y")
    enddate = datetime.strptime("29/05/2023", "%d/%m/%Y")
    
    

    while startdate <= enddate:
        driver = webdriver.Chrome()  # Use Chrome as an example
        driver.get('https://beta-tnsmart.rimes.int/index.php/Rainfall/daily_data')
       
        element = driver.find_element(By.ID, 'date')  # Replace 'regno' with the actual ID of the registration number field
        element.send_keys(startdate.strftime("%d/%m/%Y")) 
    #for i in range(1000000, 10000000):
    # Create a dictionary with the form data
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')  #Replace with the appropriate CSS selector for the submit button
        submit_button.click()
        
        # Send the HTTP POST request
        time.sleep(5)
    #wait.until(EC.presence_of_element_located((By.ID, 'TOTAL')))

        result_element = driver.page_source  # Replace 'result' with the actual ID of the result element
        soup = BeautifulSoup(result_element, 'html.parser')

        # Find the <table> tag
        table = soup.find('table', id='data_table')
        
        if table:
        # Retrieve the contents of the <table> tag
            print("found table")
            rows = table.find_all('tr')
            for row in rows[1:]:
                # Find all the <td> tags in the row
                cells = row.find_all(['td', 'th'])
                if cells[2].get_text() in dict.keys():
                    dict[cells[2].get_text()]['Rainfall'] += float(cells[3].get_text())
                else:
                    dict.update({cells[2].get_text(): {'District': cells[1].get_text(), 'Rainfall': float(cells[3].get_text())}})
                #print(cells[1].get_text() + " "+ cells[2].get_text() + " "+ cells[3].get_text())
                # Iterate through the cells, starting from the second one
                #for cell in cells[1:]:
                # Print the cell contents
                #    print(cell.get_text())
        else:
            print("No <table> tag found in the HTML content")

        driver.quit()
        # Check the response status code
        #print(dict['Yercaud']['Rainfall'])
        
        time.sleep(2)
        startdate += timedelta(days=1)
    
    with open('C:\\Users\\xjose\\OneDrive\\Desktop\\python\\TNRainfall29thMay.csv','w') as f:
        writer = csv.writer(f)
        
        for key in dict.keys():
            writer.writerow([key, dict[key]['District'], dict[key]['Rainfall']])
# Call the function to fill the form
#with open("regn:os528.txt", "a") as file:
#    file.write("Writing to file \n")
fill_form()
