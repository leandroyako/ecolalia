import os
from Timestamps import Timestamps

model = "vosk-model-small-es-0.22/"
input_directory = "agn_bicentenario_wav/"
output_folder = "timestamps/"

for filename in os.listdir(input_directory):
    f = os.path.join(input_directory, filename)
    if os.path.isfile(f):   
        split_tup = os.path.splitext(f)      
        #text_filename = output_folder + split_tup[0].split("/")[-1] + ".txt"
        json_filename = output_folder + split_tup[0].split("/")[-1] + ".json"               
        if os.path.exists(json_filename):
            print(f"File '{json_filename}' exist")
        elif split_tup[1] == '.wav':
            audio = Timestamps(f, model, output_folder)
            audio.transcribe()
