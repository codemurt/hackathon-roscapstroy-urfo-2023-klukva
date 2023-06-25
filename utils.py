import re

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('russian')


p1 = ['требования', 'треб', 'рабо']
p2 = ['условия', 'усло', 'пред']

def post_class_changer(sentences, classes, paterns = {1:p1, 2:p2}):
    res = classes.copy()
    for i in range(len(sentences)):
        for k in paterns:
            for p in paterns[k]:
                if p in sentences[i].lower():
                    res[i]=k
                    break
    return res


def clean_text(text):
 
    text = text.lower()
 
    text = re.sub(r"[^a-zA-Zа-яёА-ЯЁ?.!,?:]+", " ", text)
    text = re.sub(r"http\S+", "",text) #Removing URLs
    #text = re.sub(r"http", "",text)
 
    html = re.compile(r'<.*?>')
 
    text = html.sub(r'',text) #Removing html tags
 
    punctuations = '@#!?+&*[]-%.:/();$=><|{}^' + "'`" + '_'
    for p in punctuations:
        text = text.replace(p,'') #Removing punctuations

    sw = stopwords.words('russian')
 
    text = [word.lower() for word in text.split() if word.lower() not in sw]
 
    text = " ".join(text) #removing stopwords
 
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text) #Removing emojis
 
    return text


def post(classes):
    used=[]

    helper = [0]
    not_check = [0]
    for c in classes:
        if c not in helper:
            helper.append(c)
            not_check.append(helper[-2])

        if c in used and c not in not_check:
            i = used[::-1].index(c)
            i = len(used)-i
            for j in range(i, len(used)):
                used[j]=c

        if c in not_check:
            used.append(0)
        else:
            used.append(c)

    return used

def concate(res, text):
    f = res[0]
    t = text[0]
 
    tuxha = []
    results = [res[0]]
    for idx, elem in enumerate(res[1:], start=1):
        if f == elem:
            t += text[idx]
        else:
            f = elem
            tuxha.append(t)
            t = text[idx]
            results.append(f)
    tuxha.append(t)
    return results, tuxha