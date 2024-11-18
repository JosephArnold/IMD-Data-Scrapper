from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


def fill_form():
    
    dict = {}
    file_to_append = 'TNNovemberRainfall_till08_2024.csv'
    file_to_save = 'TNNovemberRainfall_till18_2024.csv'
    start_date = "09/11/2024"
    end_date = "18/11/2024"
    parse_link = 'https://beta-tnsmart.rimes.int/index.php/Rainfall/daily_data'
    
  
    #uncomment only if you need to append the data to a previous excel file
    startdate = datetime.strptime(start_date, "%d/%m/%Y")
    enddate = datetime.strptime(end_date, "%d/%m/%Y")
    
    with open(file_to_append, 'r') as file:
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
     
    
    while startdate <= enddate:
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()),options=options)
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(parse_link)
       
        element = driver.find_element(By.ID, 'date')  # Add date
        element.send_keys(startdate.strftime("%d/%m/%Y")) 
        drop_down_element = driver.find_element(By.ID, 'type')  # Add date
        dropdown = Select(drop_down_element)
        dropdown.select_by_visible_text("Rainfall wise")

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
                if(len(cells) > 4):
                    if cells[3].get_text() in dict.keys(): #fourth column on web page containing station name
                        dict[cells[3].get_text()]['Rainfall'] += float(cells[4].get_text()) #insert rainfall information for new station
                    else:
                        dict.update({cells[3].get_text(): {'District': cells[2].get_text(), 'Rainfall': float(cells[4].get_text())}}) #add to existing tally
                    print(cells[0].get_text() + " "+ cells[1].get_text() + " "+ cells[2].get_text()+" "+cells[3].get_text()+" "+cells[4].get_text())
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
    
    with open(file_to_save,'w') as f:
        writer = csv.writer(f)
        
        for key in dict.keys():
            writer.writerow([key, dict[key]['District'], dict[key]['Rainfall']])
# Call the function to fill the form
#with open("regn:os528.txt", "a") as file:
#    file.write("Writing to file \n")
fill_form()
