import streamlit as st
from annotated_text import annotated_text
import pickle
from razdel import sentenize
import joblib
from utils import post, clean_text, post_class_changer
 
loaded_rf = joblib.load("rf_classifier.joblib")
 
with open('tfidf-vec.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
 
#st.sidebar.success("Выберете вид использования")
 
text =  st.text_area(label='Введите текст для анализа')
button = st.button("Обработать")
text = list(sentenize(text))
sents = [clean_text(_.text) for _ in text]
text = [sentence.text for sentence in text]
vecs = vectorizer.transform(sents)
results = loaded_rf.predict(vecs)
 
print(results, "pre pre")
results = post_class_changer(sents, results)
print(results, "pre post")
results = post(results)
print(results, "post post")
 
classes = ['не принадлежит ни одному классу', 'requirements', 'terms', 'notes']
 
res_text = []
for idx, elem in enumerate(text):
    if not results[idx]:
        res_text.append(elem)
    else:
        res_text.append((elem, classes[results[idx]]))
if res_text or button:
    annotated_text(res_text)