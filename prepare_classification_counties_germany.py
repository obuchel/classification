
import urllib.request as urllib2
import bz2
import pandas as pd
import json
from os import listdir
from os.path import isfile, join
import json
onlyfiles = [f for f in listdir('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/') if isfile(join('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/', f))]
'''
with bz2.open('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+onlyfiles[-3], "r") as bzinput:
    print(bzinput)
    lines = []
    for i, line in enumerate(bzinput):
        if i == 10: break
        tweets = json.loads(line)
        lines.append(tweets)
'''
'''
filename0 = "/Users/olgabuchel/Downloads/2020-rki-archive-master/data/2_parsed/data_2020-06-08-02-30.json"
with open(filename0, 'r') as file:
    print(json.load(file)[0])
'''
print(onlyfiles)




filename = "/Users/olgabuchel/Downloads/2020-03-27-12-00_dump.csv.bz2"
import bz2
import csv
from functools import partial

class BZ2_CSV_LineReader(object):
    def __init__(self, filename, buffer_size=4*1024):
        self.filename = filename
        self.buffer_size = buffer_size

    def readlines(self):
        with open(self.filename, 'rb') as file:
            for row in csv.reader(self._line_reader(file)):
                yield row

    def _line_reader(self, file):
        buffer = ''
        decompressor = bz2.BZ2Decompressor()
        reader = partial(file.read, self.buffer_size)

        for bindata in iter(reader, b''):
            block = decompressor.decompress(bindata).decode('utf-8')
            buffer += block
            if '\n' in buffer:
                lines = buffer.splitlines(True)
                if lines:
                    buffer = '' if lines[-1].endswith('\n') else lines.pop()
                    for line in lines:
                        yield line

main_df=pd.DataFrame()
main_df2=pd.DataFrame()
if __name__ == '__main__':
    for el in onlyfiles:
        if ".csv" in el:
            #print(el)
            bz2_csv_filename = '/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+el
            all_rows=[]
            kkeys=[]
            ind=0
            for row in BZ2_CSV_LineReader(bz2_csv_filename).readlines():
                if ind>0:
                    #print(kkeys)
                    #Bundesland         Landkreis Altersgruppe Geschlecht  ...            Meldedatum IdLandkreis
                    try:
                        row[0]=row[kkeys.index("Bundesland")]+", "+row[kkeys.index("Landkreis")]
                        #row[kkeys.index("Datenstand")]=row[kkeys.index("Datenstand")].split(" ")[0].replace(",","")
                        row[kkeys.index("Datenstand")]=el.split("-")[2]+"-"+el.split("-")[1]+"-"+el.split("-")[0]
                        all_rows.append(row)
                    except:
                        #print(kkeys,row)
                        continue
                else:
                    kkeys=row
                ind+=1
            kkeys[0]="Combined_Key"    
            df = pd.DataFrame(all_rows, columns=kkeys)
            df['AnzahlFall']=pd.to_numeric(df["AnzahlFall"])
            #df.loc[:,'Datenstand'] = el.split("-")[0]+"-"+el.split("-")[1]+"-"+el.split("-")[2]
            #print(df)
            df0=df.groupby(['Combined_Key','Datenstand'])['AnzahlFall'].sum().reset_index()
            main_df=pd.concat([main_df,df0])
        elif ".json" in el:
            bz2_csv_filename = '/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+el
            all_rows=[]
            kkeys1=[]
            ind=0
            with open(bz2_csv_filename) as file1:
                data=json.load(file1)
                for row in data[0]["features"]:
                    if ind==0:
                        kkeys1=list(data[0]["features"][0]["attributes"].keys())
                        kkeys1[0]="Combined_Key"
                    ind+=1    
                    arr=list(row["attributes"].values())
                    try:
                        arr[0]=arr[kkeys1.index("Bundesland")]+", "+arr[kkeys1.index("Landkreis")]
                        arr[kkeys1.index("Datenstand")]=el.split("-")[2]+"-"+el.split("-")[1]+"-"+el.split("-")[0]
                        all_rows.append(arr)
                    except:
                        print(kkeys1,arr)
                        continue
            df = pd.DataFrame(all_rows, columns=kkeys1)
            df['AnzahlFall']=pd.to_numeric(df["AnzahlFall"])
            df0=df.groupby(['Combined_Key','Datenstand'])['AnzahlFall'].sum().reset_index()
            main_df2=pd.concat([main_df2,df0])

main_df3=pd.concat([main_df,main_df2])
df4=main_df3.groupby(['Combined_Key','Datenstand'])['AnzahlFall'].sum().reset_index()
print(df4.columns)
df4.set_index('Datenstand')
pivoted_table=df4.pivot(index='Combined_Key', columns='Datenstand', values='AnzahlFall')
print(pivoted_table)
print(pivoted_table.columns)

'''
DatetimeIndex(['2020-01-04', '2020-02-04', '2020-03-04', '2020-03-27',
               '2020-03-28', '2020-03-30', '2020-03-31', '2020-04-04',
               '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16',
               '2020-04-17', '2020-04-18', '2020-04-19', '2020-04-20',
               '2020-04-21', '2020-04-22', '2020-04-23', '2020-04-24',
               '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28',
               '2020-05-04', '2020-06-04', '2020-07-04', '2020-08-04',
               '2020-09-04', '2020-10-04', '2020-11-04', '2020-12-04'],
              dtype='datetime64[ns]', name='Datenstand', freq=None)

'''
