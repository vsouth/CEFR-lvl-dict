import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import string

# FIX LATER: pronoun "us" turns into "u"

def load_text(path = "raw.txt"):
    with open(path,"r", errors="ignore") as text:
        return text.read()


def load_json(cefr):
    with open(f"{cefr}_words.json", "r") as json_file:
        data = json.load(json_file)
        return set(data)


def analysis_into_str(analysis):
    output = ""
    output += "\n".join([key + " --- " + str(analysis["stats"][key]) for key in ["a1","a2","b1","b2","c1","misc"]])
    output += "\n------------------------\n"
    output += "\n------------------------\n".join([key.upper() +"\n------------------------\n" + "\n".join(sorted([word for word in analysis["words"][key]])) for key in ["a1","a2","b1","b2","c1", "misc"]])
    output += "\n"
    return output


def save_cheatsheet(data, path = "cheatsheet.txt"):
    with open(path, "w") as file:
        return file.write(data)


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def text_into_lemmatized_list(text):
    lemmatizer = WordNetLemmatizer()
    list_from_text = [lemmatizer.lemmatize(w, get_wordnet_pos(w)).lower() for w in nltk.word_tokenize(text)]
    return list_from_text
    

def remove_punctuation_and_unknown(text):
    printable = string.printable
    text = ''.join(filter(lambda x: x in printable, text))
    return text.translate(str.maketrans('', '', string.punctuation))


def analyze_CEFR(text):
    lemma_list = text_into_lemmatized_list(text)
    list_len = len(lemma_list)
    stats = {}
    words = {}
    checked = set()
    for lvl in ["a1","a2","b1","b2","c1"]:
        cefr_list = load_json(lvl)
        difference = [word for word in lemma_list if word in cefr_list]
        words[lvl] = set(difference)
        stats[lvl] = "{:.1%}".format(len(difference)/list_len)
        checked.update(difference)
    words["misc"] = [word for word in set(lemma_list) if word not in checked]
    stats["misc"] = "{:.1%}".format((list_len - len(checked))/list_len)
    return {"stats": stats, 
            "words": words}

text = remove_punctuation_and_unknown(load_text())
analysis = analyze_CEFR(text)
save_cheatsheet(analysis_into_str(analysis))


