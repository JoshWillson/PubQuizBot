import nltk as nlp
from nltk import pos_tag as tag
import webbrowser
import requests
from bs4 import BeautifulSoup
import lxml

def getSub(tags, t_w):
     sub = []
     for det in range (0,len(tags)):
          if tags[det] == 'SUBJECT':
               sub.append(t_w[det])
     return(sub)

def getSummary(soup):
        styleCorrect = soup.find_all("p")
        try:
            p = (styleCorrect[1]).getText()
            if p.count(".") < 2 and len(styleCorrect) >= 3:
                p = (styleCorrect[2]).getText()
            elif p.count(".") < 2 and len(styleCorrect) >= 4:
                p = (styleCorrect[3]).getText()
            elif p.count(".") < 2 and len(styleCorrect) >= 5:
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

     para =   getSummary(soup)
     return para

def validate_int(num):
    try:
        int(num)
        return True
    except:
        return False

def checkExists(para):
    para = para.strip()
    if para[:10] == 'The page "':
        return False
    if para[:15] == 'View (previous ':
        return False
    if para == 'There were no results matching the query.':
        return False
    if para[13:] == 'may refer to:':
        return False
    return True

def changeFormat(para, sub):
    count = 0
    for choicesub in sub:
        count += 1
        print (count,': ',choicesub)
    run_sub_menu = True
    while run_sub_menu == True:
        print('Is there a word here that you would best descirbe your search?')
        prompt = 'Please input a choice from 1 to '+str(count)+'\nIf there is no word here that would work, enter "none"'
        choice = input(prompt)
        if validate_int(choice) == True and int(choice) >= 1 and int(choice) <= count:
            run_sub_menu = False
            to_search = [(sub[int(choice)-1])]
            para2 = searchWiki(to_search)
            print(para2)
            if checkExists(para2) == False:
                print('This page still cannot be found')
            else:
                print ('\n\n',para2)
        elif choice.lower() == 'none':
            run_sub_menu = False
            sub2 = input('Enter the question subject')
            sub2 = sub2.split(' ')
            para2 = searchWiki(sub2)
            print(para2)
            if checkExists(para2) == False:
                print('This page still cannot be found')
            else:
                print ('\n\n',para2)
        else:
            print('That was not a valid choice')


def main():

     run = True

     while run == True:
          print ()
          text = input('Input a question with a Proper pronoun, queston word and question detail')
          length = len(text)
          if text.endswith('?'):
               text = text[0:-1]

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
               elif tagged == 'NNP' or tagged == 'NN' or tagged == 'NNS':  #This needs more work   i.e. countries dont work
                    tagged = 'SUBJECT'
               elif tagged == 'VB' or tagged == 'VBD' or tagged == 'VBG' or tagged == 'VBN' or tagged == 'VBP' or tagged == 'VBZ':
                    tagged = 'Q_DETAIL'
               else:
                    tagged = 'NONE'
               tags.append(tagged)
          sub = getSub(tags, t_w)
          print('\nOriginal question :',t_w)
          print('Question Subject :',sub, '\n')
          para = searchWiki(sub)
          if checkExists(para) == False:
              print('This page cannot be found')
              run_refine_menu = True
              while run_refine_menu == True:
                  choice = input('Do you want me to try and refine your search? (or try again?) [Enter "refine" or "again"]')
                  if choice.lower() == 'refine':
                      run_refine_menu = False
                      changeFormat(para, sub)
                  elif choice.lower() == 'again':
                      run_refine_menu = False

                  else:
                      print('That is not a valid choice')
          else:
              print (para)


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
