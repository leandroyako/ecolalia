import os
import json

d = dict()
directory = "timestamps"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):   
        split_tup = os.path.splitext(f)
        if split_tup[1] == '.json':
            with open(f, "r") as read_file:
                data = json.load(read_file)
                for item in data:     
                    aux_item = item.copy()
                    del aux_item['word']
                    if item['word'] in d:
                        d[item['word']].append(aux_item)
                    else:
                        d[item['word']] = [aux_item]
                                
with open(directory+'total_words.json', "w") as json_file:
    json.dump(d, json_file)

print("Done")