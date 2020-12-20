#curl -d '%7B%22resource_id%22%3A%228a21d39d-91e3-40db-aca1-f73f7ab1df69%22%2C%22q%22%3A%22%22%2C%22filters%22%3A%7B%7D%2C%22include_total%22%3Atrue%2C%22limit%22%3A78120%2C%22offset%22%3A0%7D' https://data.gov.il/api/3/action/datastore_search -o israel_data_today.json

import json
import csv
# Opening JSON file and loading the data 
# into the variable data 
with open('israel_data_today.json') as json_file: 
    data = json.load(json_file) 
  
employee_data = data["result"]["records"]
print(len(employee_data))
  
# now we will open a file for writing 
data_file = open('israel_file.csv', 'w') 
  
# create the csv writer object 
csv_writer = csv.writer(data_file) 
  
# Counter variable used for writing  
# headers to the CSV file 
count = 0
  
for emp in employee_data: 
    if count == 0: 
  
        # Writing headers of CSV file 
        header = emp.keys() 
        csv_writer.writerow(header) 
        count += 1
  
    # Writing data of CSV file 
    csv_writer.writerow(emp.values()) 
  
data_file.close() 



