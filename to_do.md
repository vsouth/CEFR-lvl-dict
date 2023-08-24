# To do
- [ ] юнит тесты, чтобы проверять, не сломалось ли что-то!!
- [ ] починить стату, поместить стату в отд функцию
- [ ] regex чтобы работать с непонятными символами
    - [ ] символы других языков
    - [ ] пунктуация
    - [ ] служебные символы
- [ ] выбор формата ввода (файл, текст) и вывода (файл (txt, json), текст)
- [ ] реализовать возможность юзать как модуль
	- [x] > py make_cheatsheet.py -f "D:\\User\\Downloads\\pride_and_prejudice.txt" -l "a1,a2" 
	- [ ] 
```
from CEFR-lvl-dict import analyze_text
# ...
response = custom_formatting(analyze_text(message))
# or
response = analyze_text(message, format="text")
```
- [ ] рефакторинг на классы по возможности (filemanager)
- [ ] прикрутить транскрипции (words-to-ipa или какой то такой модуль видела)
- [ ] оптимизировать как нить
	- [ ] прикрутить бд вместо жсонов и проверить что лучше
	- [ ] set or dict (with counter) instead of list
# Links
https://stackoverflow.com/questions/40633006/why-is-testing-for-inclusion-faster-with-a-dict-than-a-set