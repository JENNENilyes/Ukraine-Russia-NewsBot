from chatbot import app
from flask import render_template,flash, request
from chatbot.forms import chatbotform
from chatbot.__init__ import model,words,classes,intents

import nltk
import pickle
import json
import numpy as np
from tensorflow.keras.models import Sequential,load_model
import random
from datetime import datetime
import pytz
import requests
import os
# import billboard

import time
from pygame import mixer
# import COVID19Py

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()


#Scraping new news --------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
# from main import DataHouse

url='https://www.aljazeera.com/news/'


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
#driver = webdriver.Chrome(options=options, executable_path= r"C:\webdrivers\chromedriver.exe")
driver = webdriver.Chrome(options=options)




#Predict
def _clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def _bag_of_words(sentence, words):
    sentence_words = _clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


def _predict_class(sentence):
    p = _bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.15
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    return return_list


# def get_response(return_list,intents_json,text):
#
#     if len(return_list)==0:
#         tag='noanswer'
#     else:
#         tag=return_list[0]['intent']
#     if tag=='datetime':
#         x=''
#         tz = pytz.timezone('Asia/Kolkata')
#         dt=datetime.now(tz)
#         x+=str(dt.strftime("%A"))+' '
#         x+=str(dt.strftime("%d %B %Y"))+' '
#         x+=str(dt.strftime("%H:%M:%S"))
#         return x,'datetime'
#
#
#
#     if tag=='weather':
#         x=''
#         api_key='987f44e8c16780be8c85e25a409ed07b'
#         base_url = "http://api.openweathermap.org/data/2.5/weather?"
#         # city_name = input("Enter city name : ")
#         city_name = text.split(':')[1].strip()
#         complete_url = base_url + "appid=" + api_key + "&q=" + city_name
#         response = requests.get(complete_url)
#         response=response.json()
#         pres_temp=round(response['main']['temp']-273,2)
#         feels_temp=round(response['main']['feels_like']-273,2)
#         cond=response['weather'][0]['main']
#         x+='Present temp.:'+str(pres_temp)+'C. Feels like:'+str(feels_temp)+'C. '+str(cond)
#         print(x)
#         return x,'weather'
#
#     if tag=='news':
#         main_url = " http://newsapi.org/v2/top-headlines?country=in&apiKey=bc88c2e1ddd440d1be2cb0788d027ae2"
#         open_news_page = requests.get(main_url).json()
#         article = open_news_page["articles"]
#         results = []
#         x=''
#         for ar in article:
#             results.append([ar["title"],ar["url"]])
#
#         for i in range(10):
#             x+=(str(i + 1))
#             x+='. '+str(results[i][0])
#             x+=(str(results[i][1]))
#             if i!=9:
#                 x+='\n'
#
#         return x,'news'
#
#     if tag=='cricket':
#         c = Cricbuzz()
#         matches = c.matches()
#         for match in matches:
#             print(match['srs'],' ',match['mnum'],' ',match['status'])
#
#     if tag=='song':
#         chart=billboard.ChartData('hot-100')
#         x='The top 10 songs at the moment are: \n'
#         for i in range(10):
#             song=chart[i]
#             x+=str(i+1)+'. '+str(song.title)+'- '+str(song.artist)
#             if i!=9:
#                 x+='\n'
#         return x,'songs'
#
#     if tag=='timer':
#         #mixer.init()
#         x=text.split(':')[1].strip()
#         time.sleep(float(x)*60)
#         #mixer.music.load('Handbell-ringing-sound-effect.mp3')
#         #mixer.music.play()
#         x='Timer ringing...'
#         return x,'timer'
#
#
#     if tag=='covid19':
#
#         covid19=COVID19Py.COVID19(data_source='jhu')
#         country=text.split(':')[1].strip()
#         x=''
#         if country.lower()=='world':
#             latest_world=covid19.getLatest()
#             x+='Confirmed Cases:'+str(latest_world['confirmed'])+' Deaths:'+str(latest_world['deaths'])
#             return x,'covid19'
#         else:
#             latest=covid19.getLocations()
#             latest_conf=[]
#             latest_deaths=[]
#             for i in range(len(latest)):
#
#                 if latest[i]['country'].lower()== country.lower():
#                     latest_conf.append(latest[i]['latest']['confirmed'])
#                     latest_deaths.append(latest[i]['latest']['deaths'])
#             latest_conf=np.array(latest_conf)
#             latest_deaths=np.array(latest_deaths)
#             x+='Confirmed Cases:'+str(np.sum(latest_conf))+' Deaths:'+str(np.sum(latest_deaths))
#             return x,'covid19'
#
#
#
#     list_of_intents= intents_json['intents']
#     for i in list_of_intents:
#         if tag==i['tag'] :
#             result= random.choice(i['responses'])
#     return result,tag
#
# def response(text):
#     return_list=predict_class(text,model)
#     response,_=get_response(return_list,intents,text)
#     return response


def _get_response(ints, intents_json):
    try:

        tag = ints[0]['intent']
        if tag == 'update':
            driver.get(url)
            page_content = driver.page_source
            page1 = BeautifulSoup(page_content, 'lxml')
            # /html/body/div[1]/div/div[2]/div[2]/div/div/div/div[1]/a[1]
            # print("page1")
            link = page1.select('div.breaking-ticker__items a')[0]['href']
            LINK = "https://www.aljazeera.com" + link
            # print(LINK)

            driver.get(LINK)
            page_content2 = driver.page_source
            page2 = BeautifulSoup(page_content2, 'lxml')

            news = page2.select('div.wysiwyg.wysiwyg--all-content.css-1ck9wyi ul')[0].select('li')
            neww = ""
            for e in news:
                neww+=e.text + "\n "

            return neww






        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag']  == tag:
                result = random.choice(i['responses'])
                break
    except IndexError:
        result = "I don't understand!"

    return result



@app.route('/',methods=['GET','POST'])
#@app.route('/home',methods=['GET','POST'])
def yo():
    return render_template('main.html')

@app.route('/chat',methods=['GET','POST'])
#@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route("/get")
def chatbot():
    message = request.args.get('msg')
    ints = _predict_class(message)
    res = _get_response(ints, intents)


    return res
