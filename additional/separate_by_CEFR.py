import json

def separate(CEFR):
    words = [key for (key,value) in full_dict.items() if value==CEFR]
    with open(f"{lvl}_words.json","w") as file:
        words = json.dumps(words, indent=4)
        file.write(words)

with open("words_with_CEFR.json", "r") as full_json:
    global full_dict 
    full_dict = json.load(full_json)

for lvl in ["a1","a2","b1","b2","c1"]:
    separate(lvl)