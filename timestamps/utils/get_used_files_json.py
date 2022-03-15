import json

#processed_data item i.e.: {"D_981B_02": {"title": "Título" "times": [{"start": 300.48, "end": 301.29}] } }
processed_data = dict()
search_db = dict()
json_word = "nosotros"
json_search = "search_audio.json"
json_total_words = "total_words.json"
json_output = json_word + ".json"


with open(json_search, "r") as search:
    search_db = json.load(search)

with open(json_total_words, "r") as total_words:
    data = json.load(total_words)

    for item in data[json_word]:
        
        for element in search_db:
            if item['filename'] in element['assets'][0]['path']:
                id = element['fondo']['id_externo']
                title = element['assets'][0]['title']    
        
        new_format = {
            'titulo': title,
            'tiempos': [{
                'inicio': item['start'], 
                'fin': item['end']
                }]
            }     
        if id in processed_data.keys():
           processed_data[id]['tiempos'].append(new_format['tiempos'][0])
        else:
            processed_data[id] = new_format

with open(json_output, "w") as json_file:
    json.dump(processed_data, json_file)
 