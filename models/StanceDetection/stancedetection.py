# -*- coding: utf-8 -*-
"""StanceDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JalEkC-0i1VjHMfzTd_WQrlYs05kmk_d
"""

# Load libraries
import io
import pandas as pd
import numpy as np
import re
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle
import spacy

#Function to process/clean the tweets
pun = """!"$%&'()*+,-./:;<=>?[\]^`{|}~"""
stop_words = set(stopwords.words('english'))
lem = WordNetLemmatizer()


def clean_text(words):
    """The function to clean text"""
    words = re.sub("[^a-zA-Z]", " ", words)
    
    # Remove urls
    text = re.sub(r"http\S+|www\S+|https\S+", '', words, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    text = re.sub(r'\@\w+','', text)
    text = re.sub(r'\#\w+','', text)
    #remove numbers    
    #digits = '[0-9]'
    #text = re.sub(digits, '', text)
    #Remove emojis
    text = re.sub('(?::|;|=)(?:-)?(?:\)|\(|D|P)'," ",text)
    text = text.lower().split()
    return " ".join(text)

def remove_numbers(text):
    """The function to removing all numbers"""
    new_text = []
    for word in text.split():
        if not re.search('\d', word):
            new_text.append(word)
    return ' '.join(new_text)

def remove_stopwords(review):
    """The function to removing stopwords"""
    text = [word.lower() for word in review.split() if word.lower() not in stop_words]
    return " ".join(text)

def get_lemmatize(text):
    """The function to apply lemmatizing"""
    lem_text = [lem.lemmatize(word) for word in text.split()]
    return " ".join(lem_text)

# Load dataset
from google.colab import files
uploaded = files.upload()

dataset = pd.read_csv(io.BytesIO(uploaded['stanceDataset.csv']), header=0, index_col=0, sep=',',lineterminator='\r',encoding = 'unicode_escape')

print(dataset.shape)
print(dataset.head(5))

dataset['Tweet'] = dataset['Tweet'].astype(str)
dataset['Tweet'] = dataset['Tweet'].apply(clean_text)
print("done")
dataset['Tweet'] = dataset['Tweet'].apply(remove_stopwords)
dataset['Tweet'] = dataset['Tweet'].apply(remove_numbers)
dataset['Tweet'] = dataset['Tweet'].apply(get_lemmatize)
print(dataset[:5])

with open('stanceDataset_clean.csv', 'w') as f:
  dataset.to_csv(f)

dataset = pd.read_csv('stanceDataset_clean.csv', header=0, index_col=0)

# Shape
print(dataset.shape)

# Separate into input and output columns
X = dataset['Tweet'].values.astype('U')
y = dataset['Stance'].values.astype('U')

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 0)
model = Pipeline([('vect', CountVectorizer(min_df=5, ngram_range=(1, 2))),
                  ('tfidf', TfidfTransformer()),
                  ('model', LogisticRegression()), ])

# Create Logistic regression model
model.fit(X_train, y_train)

# Make predictions
ytest = np.array(y_test)
pred_y = model.predict(X_test)

# Evaluate predictions
print('accuracy %s' % accuracy_score(pred_y, y_test))
print(classification_report(ytest, pred_y))

# Save the model
with open("stance.pkl", "wb") as f:
    pickle.dump(model,f)

with open('stance.pkl', 'rb') as f:
        model = pickle.load(f)
s=["Trump is better than Hillary"]
a=model.predict(s)
print(a[0])

