import nltk as nlp
from nltk import pos_tag as tag
import webbrowser
import requests
from bs4 import BeautifulSoup
import lxml

def getSub(tags, t_w):
     rem = 0
     sub = []
     for det in range (0,len(tags)):
          if tags[det] == 'SUBJECT':
               sub.append(t_w[det-rem])
     return(sub)

def getSummary(soup):
        styleCorrect = soup.find_all("p")
        try:
            p = (styleCorrect[1]).getText()
            if p.count(".") < 2 and len(styleCorrect) >= 3:
                p = (styleCorrect[2]).getText()
            if p.count(".") < 2 and len(styleCorrect) >= 4:
                p = (styleCorrect[3]).getText()
            if p.count(".") < 2 and len(styleCorrect) >= 5:
                p = (styleCorrect[4]).getText()
        except:
            try:
                p = (styleCorrect[0]).getText()
            except:
                p = ""
        return p

def searchWiki(t_w):
     baseUrl = 'https://en.wikipedia.org/w/index.php?search='
     search = ''
     for i in range (0, len(t_w)):
          search = search + t_w[i]
          if i != len(t_w):
               search = search + '+'
     url = baseUrl + search

     source = requests.get(url).text
     soup = BeautifulSoup(source, 'lxml')
     
     styleCorrect = soup.find_all("b")
     found = True
     for i in styleCorrect:
          if "does not have an article" in str(i):
               found = False

     if found == True:   
          print(getSummary(soup))
     else:
          print('Sorry, I cant find the article you are looking for')

def main():

     run = True

     while run == True:
          print ()
          text = input('Input a question with a Proper pronoun, queston word and question detail')

          t = text.lower()
          t_w = t.split(' ')
          error = True
          tokens = tag(nlp.word_tokenize(t))
          print(tokens)
          tags = []
          for i in range (0,len(tokens)):
               temp = tokens[i]
               tagged = temp[1]
               if tagged == 'WRB' or tagged == 'WP':
                    tagged = 'Q_WORD'
               elif tagged == 'NNP' or tagged == 'NN' or tagged == 'NNS' or tagged == 'JJ':
                    tagged = 'SUBJECT'
               elif tagged == 'VB' or tagged == 'VBD' or tagged == 'VBG' or tagged == 'VBN' or tagged == 'VBP' or tagged == 'VBZ':
                    tagged = 'Q_DETAIL'
               else:
                    tagged = 'NONE'
               tags.append(tagged)
          sub = getSub(tags, t_w)
          print('Original question :',t_w)
          print('Question Subject :',sub)
          searchWiki(sub)
     

             

main()


'''
CC: conjunction, coordinating
CD: numeral, cardinal
DT: determiner
EX: existential there
IN: preposition or conjunction, subordinating
JJ: adjective or numeral, ordinal
JJR: adjective, comparative
JJS: adjective, superlative
LS: list item marker
MD: modal auxiliary
NN: noun, common, singular or mass
NNP: noun, proper, singular
NNS: noun, common, plural
PDT: pre-determiner
POS: genitive marker
PRP: pronoun, personal
PRP$: pronoun, possessive
RB: adverb
RBR: adverb, comparative
RBS: adverb, superlative
RP: particle
TO: "to" as preposition or infinitive marker
UH: interjection
VB: verb, base form
VBD: verb, past tense
VBG: verb, present participle or gerund
VBN: verb, past participle
VBP: verb, present tense, not 3rd person singular
VBZ: verb, present tense, 3rd person singular
WDT: WH-determiner
WP: WH-pronoun
WRB: Wh-adverb
'''

