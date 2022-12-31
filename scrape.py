from bs4 import BeautifulSoup
import requests
import json

URL = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
headers = {"User-Agent": "'User-agent': 'Mozilla/5.0'",}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
soup = soup.find("ul", {"class": "top-g"})
soup = soup.find_all("li")
print(soup[15]["data-hw"], soup[15]["data-ox5000"])
words = {}
for li in soup:
    try:
        words[li["data-hw"]]=li["data-ox5000"]
    except:
        print(li)

with open("words_with_CEFR.json", "w") as outfile:
    words = json.dumps(words, indent=4)
    outfile.write(words)
