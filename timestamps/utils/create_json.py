import json

#d = {"de": [{"conf" : 1, "start":0, "end": 1, "filename": "myFile"}]}
d = dict()
json_filename = "timestamps/demo.json"

with open(json_filename, "r") as read_file:
    data = json.load(read_file)
  
    for item in data:
 
        aux_item = item.copy()
        del aux_item['word']
        if item['word'] in d:
            d[item['word']] = [d[item['word']], aux_item]
        else:
            d[item['word']] = [aux_item]          

with open(json_filename+'.new.json', "w") as json_file:
    json.dump(d, json_file)
  