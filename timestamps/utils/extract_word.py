import json

d = dict()
word = 'nosotros'
json_input = "total_words.json"
json_output = word + ".json"

with open(json_input, "r") as read_file:
    data = json.load(read_file)
    d = data[word]
    
with open(json_output, "w") as json_file:
    json.dump(d, json_file)    