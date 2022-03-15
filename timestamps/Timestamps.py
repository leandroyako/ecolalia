import os
import sys
import wave
import json

from vosk import Model, KaldiRecognizer

class Timestamps:
    
    def __init__(self, file_path, model_path, output_folder):
    # path to vosk model downloaded from
    # https://alphacephei.com/vosk/models

        if not os.path.exists(model_path):
            print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
            sys.exit()

        print(f"Reading your vosk model '{model_path}'...")
        self.model = Model(model_path)
        print(f"'{model_path}' model was successfully read")

        self.filename = os.path.splitext(os.path.split(file_path)[1])[0]
        print(self.filename)
        
        # name of the audio file to recognize
        self.audio_filename = file_path
        # name of the text file to write recognized text
        self.text_filename = output_folder + self.filename + ".txt"
        self.json_filename = output_folder + self.filename + ".json"
        
        if not os.path.exists(self.audio_filename):
            print(f"File '{self.audio_filename}' doesn't exist")
            sys.exit()

        print(f"Reading your file '{self.audio_filename}'...")
        self.wf = wave.open(self.audio_filename, "rb")
        print(f"'{self.audio_filename}' file was successfully read")

        # check if audio is mono wav
        if self.wf.getnchannels() != 1 or self.wf.getsampwidth() != 2 or self.wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit()

    def transcribe(self):
        rec = KaldiRecognizer(self.model, self.wf.getframerate())
        rec.SetWords(True)
        results = []
        # recognize speech using vosk model
        while True:
            data = self.wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result)

        part_result = json.loads(rec.FinalResult())
        results.append(part_result)

        # convert list of JSON dictionaries to list of objects
        list_of_words = []
        for sentence in results:
            if len(sentence) == 1:
                # sometimes there are bugs in recognition 
                # and it returns an empty dictionary
                # {'text': ''}
                continue
            for obj in sentence['result']:
                obj['filename'] = self.filename
                list_of_words.append(obj)  # and add it to list
        
        print(f"Saving results to '{self.json_filename}'...")
        with open(self.json_filename, "w") as self.json_filename:
            self.json_filename.write(str(list_of_words).replace("'", '"'))
        print(f"Results successfully saved")
        
        # forming a final string from the words
        text = ''
        for r in results:
            text += r['text'] + ' '

        print(f"Saving text to '{self.text_filename}'...")
        with open(self.text_filename, "w") as text_file:
            text_file.write(text)
        print(f"Text successfully saved")