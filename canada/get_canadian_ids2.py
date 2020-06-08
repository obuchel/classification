import json
import csv

kkeys={}
with open('canadian_data_first.csv', 'r', newline='') as csvfile:
        spamwriter = csv.reader(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for el in spamwriter:
                if el[2]!="":
                        print(el[0],el[2])
                        kkeys[el[0]]=el[2]
with open('canadian_keys.json', 'w') as outfile:
    json.dump(kkeys, outfile)                        
