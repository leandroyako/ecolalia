import soundfile as sf
import pyloudnorm as pyln
from pathlib import Path
import json
json_path = "/home/yako/premio_agn/sc/loudness.json"
path = Path("/home/yako/premio_agn/sc/nosotros")
files = [{"file": file, "data": sf.read(file)} for file in path.glob("*wav")]

meter = pyln.Meter(rate=44100, block_size=0.1)

# print(files)
loudness = [
        (
            item["file"].name,
            meter.integrated_loudness(item["data"][0])
            )
        for item in files
        ]

print("Sorting by loudness")
loudness_sorted = sorted(loudness, key=lambda x: x[1])
dict = [{"order": i, "filename": item[0], "loudness": item[1]} for i, item in enumerate(loudness_sorted)]
with open(json_path, "w") as json_file:
    json.dump(dict, json_file)
