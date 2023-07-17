import json
import spacy
import string
import argparse
import pathlib

# FIX LATER: 
# fix analysis %
# read texts with wrong content smarter
# добавить мб транскрипции (опционально)

def load_text(path: str = "raw.txt") -> str:
    with open(path,"r", errors="ignore") as text:
        return text.read()


def load_json(cefr: str) -> set:
    with open(f"{cefr}_words.json", "r") as json_file:
        data = json.load(json_file)
        return set(data)


def analysis_into_str(analysis, levels) -> str:
    categories = levels+["misc"]
    output = ""
    output += "\n".join([key + " --- " + str(analysis["stats"][key]) for key in categories])
    output += "\n------------------------\n"
    output += "\n------------------------\n".join([key.upper() +"\n------------------------\n" + "\n".join(sorted([word for word in analysis["words"][key]])) for key in categories])
    output += "\n"
    return output


def save_cheatsheet(data, path: str) -> None:
    with open(path, "w") as file:
        return file.write(data)


def lemmatize_text(text: str) -> str:
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

def text_into_lemmatized_list(text: str) -> list[str]:
    return lemmatize_text(text).split(' ')

def remove_punctuation_and_unknown(text: str) -> str:
    printable = string.printable
    text = ''.join(filter(lambda x: x in printable, text))
    return text.translate(str.maketrans('', '', string.punctuation))


def analyze_CEFR(text: str, levels: list[str]) -> dict:
    lemma_list = text_into_lemmatized_list(text)
    list_len = len(lemma_list)
    stats = {}
    words = {}
    checked = set()
    for lvl in levels:
        cefr_list = load_json(lvl)
        difference = [word for word in lemma_list if word in cefr_list]
        words[lvl] = set(difference)
        stats[lvl] = "{:.1%}".format(len(difference)/list_len)
        checked.update(difference)
    words["misc"] = [word for word in set(lemma_list) if word not in checked]
    stats["misc"] = "{:.1%}".format((list_len - len(checked))/list_len)
    return {"stats": stats, 
            "words": words}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", 
                        type=str, 
                        required=False, 
                        default="raw.txt")
    parser.add_argument("-l", "--levels", 
                        help="CEFR-levels to check (default = \"a1,a2,b1,b2,c1\")", 
                        type=str, 
                        required=False, 
                        default="a1,a2,b1,b2,c1")
    return parser.parse_args()



def main():
    args = parse_args()

    filename = pathlib.Path(args.filename)
    text = remove_punctuation_and_unknown(load_text(filename))

    levels = args.levels.split(",")
    print(filename.stem, levels)
    analysis = analyze_CEFR(text, levels)

    output_filename = str(filename.parent) + '/' + filename.stem+"_cheatsheet.txt"
    save_cheatsheet(analysis_into_str(analysis, levels), path=output_filename)


if __name__ == "__main__":
	main()

