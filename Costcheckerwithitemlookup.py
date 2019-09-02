import os
import sys
import yaml
import json
import requests
import numpy as np


itemId = 32772
yaml_data=open(os.path.join(sys.path[0], "blueprints.txt"), "r")
data = yaml.load(yaml_data)

   
try:
    read_bpItemTable = np.load('BPItemtable.npy').item()
except:  
    modIdbpiddata = {}
    
    for x in data:
        try:
            b = data[x]['activities']['manufacturing']['products'][0]['typeID']
            c = data[x]['blueprintTypeID']
            modIdbpiddata.update({b : c})
        except KeyError:
            continue
    np.save('BPItemtable.npy', modIdbpiddata)
    read_bpItemTable = np.load('BPItemtable.npy').item() 

        
bpid = read_bpItemTable.get(itemId)

componentList = data[str(bpid)]['activities']['manufacturing']['materials']
productId = []
productId.append(str(data[str(bpid)]['activities']['manufacturing']['products'][0]['typeID']))

compsIdsOnly = []
compsIdsAndQuants = {}
for x in componentList:
    compsIdsOnly.append(str(x['typeID']))
    lol = str(x['typeID'])
    numberation = x['quantity']
    compsIdsAndQuants[lol] = numberation

url = ("https://market.fuzzwork.co.uk/aggregates/?station=60003760&types=" + ",".join(compsIdsOnly)+ "," + str((productId[0])))

response = requests.get(url)
rPython = json.loads(response.text)

costList = []

print "itemID    " + "Each Price    " + "Total Price"
for z in compsIdsOnly:
    price = float(rPython[z]['buy']['max'])
    quantity = float(int(compsIdsAndQuants[z]))
    total = str(price * quantity)
    costList.append(float(total))
    print z + "      " + str(price)+ "     " + total
marketCost = rPython[productId[0]]['sell']['min']

print "Build Cost   " + str(sum(costList))
print "Market Cost  " + str(marketCost)