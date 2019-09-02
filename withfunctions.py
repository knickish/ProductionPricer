import os
import sys
import yaml
import json
import requests
import numpy as np
import wx


itemId = None

class WindowFrame(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(WindowFrame, self).__init__(*args, **kw)
        
        pnl = wx.Panel(self)
        
        inputBox = wx.TextEntryDialog(pnl, 'Enter Item ID', pos=(25,25))
        inputBox.SetValue("")
        if inputBox.ShowModal() == wx.ID_OK:
            global itemId
            itemId = inputBox.GetValue()
            
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = WindowFrame(None, title='Eve Cost Calculator')
    frm.Show()
    app.MainLoop()            

yaml_data=open(os.path.join(sys.path[0], "blueprints.txt"), "r")
data = yaml.load(yaml_data)

   
def tableCreator():
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
    return modIdbpiddata
    return read_bpItemTable
   
   
try:
    read_bpItemTable = np.load('BPItemtable.npy').item()
except:  
    tableCreator()

        
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


