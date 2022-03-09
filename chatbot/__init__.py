import flask
from flask import Flask
from chatbotconfig import *

app=Flask(__name__)
app.config.from_object(Config)

import tensorflow.keras
import nltk
import pickle
import json
from tensorflow.keras.models import load_model

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

model = load_model(r'C:\Users\ASUS\PycharmProjects\pythonProject3\chatbot_codes\chatbot_modell.h5')
intents = json.loads(open(r'C:\Users\ASUS\PycharmProjects\pythonProject3\chatbot_codes\intents.json').read())
words = pickle.load(open(r'C:\Users\ASUS\PycharmProjects\pythonProject3\chatbot_codes\words.pkl','rb'))
classes = pickle.load(open(r'C:\Users\ASUS\PycharmProjects\pythonProject3\chatbot_codes\classes.pkl','rb'))


from chatbot import routes
