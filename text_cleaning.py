import re
import nltk
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize

spell = SpellChecker()
spell.word_frequency.load_text_file('spellfinal1.txt')
punc = '''!()-[]{};"\,|-<>?@#$%^&*_~'''
alphabets= "([A-Za-z])"
numbers = "([0-9])"
dict = {}
t2 = []

def clean_string(text):
    text = text.replace("\r", "")
    text = text.replace("\n", " ")
    #text = re.sub("\n"," ",text)
    text = text.replace("\x0c","")
    text = re.sub(('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))'), '', text, flags=re.MULTILINE)
    text = "".join([char for char in text if char not in punc])
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","",text)
    text = re.sub( alphabets+"[.]"  ," ",text)
    #text = re.sub(" "+Alp+" "," ", text)
    text = re.sub(" "+numbers+"[.]"+" ","",text)
    text = " ".join(text.split())
    
    word_t1 = nltk.word_tokenize(text)
    tokens = [token.lower() for token in word_t1]

    misspelled = spell.unknown(tokens)

    for word in misspelled:
        corrected = spell.correction(word) 
        dict[word] = corrected

    text = text.lower()
    text = text.split()
    t2 = []
    for wrd in text:
        t2.append(dict.get(wrd, wrd))
      
    t2 = ' '.join(t2)

    return(t2)
