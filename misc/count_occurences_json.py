import json
import csv

words = "/home/yako/premio_agn/sc/total_words.json"
csv_path = '/home/yako/premio_agn/misc/cuenta.csv'

data_file = open(csv_path, 'w', newline='')
csv_writer = csv.writer(data_file)

d = dict()

with open(words, "r") as json_file:
    data = json.load(json_file)

    for word in data:
        d[word] = len(data[word])

d = sorted(d.items(),key= lambda x:x[1])

for item in d:
    csv_writer.writerow(item)
