
###################################### export  data  to  csv  file  ##################################
import pandas as pd
import json
list = []
with open('db.json', 'r')as file:
    data = json.load(file)
    x = data['_default']
    for  each  in x :
    	list.append(x[each])
    df = pd.json_normalize(list)
    csvData = df.to_csv('data.csv' , index=False)
