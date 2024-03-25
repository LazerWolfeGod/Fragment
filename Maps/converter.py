import json,os

for file in os.listdir():
    if '.json' in file:
        print(file)
        with open(file,'r') as f:
            dat = json.load(f)
        new_dat = {'map':{'tilemap':dat['map'],'pos':[0,0]},
                   'entities':dat['entities']}
        with open(file,'w') as f:
            json.dump(new_dat,f)
