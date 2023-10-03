# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 17:49:00 2023

@author: prash
"""

import pandas as pd
import gzip
import json
import matplotlib.pyplot as plt
import seaborn as sns

path="C:\\Users\\prash\\Downloads\\reviews_Office_Products_5.json.gz"

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield json.loads(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')


df = getDF(path)



#getting review per item
reviews_per_item={b:len(df[df["asin"]==b])for b in df.asin.unique()}
reviews_per_item=pd.DataFrame(reviews_per_item, index=[0]).T

#reviews per user
reviews_per_user={b: len(df[df["reviewerName"]==b]) for b in df.reviewerName.unique()}
reviews_per_user=pd.DataFrame(reviews_per_user, index=[0]).T


#max and mean reviews per item and user
max_review_per_user=reviews_per_user[reviews_per_user[0]==reviews_per_user[0].max()]
max_review_per_item=reviews_per_item[reviews_per_item[0]==reviews_per_item[0].max()]
mean_review_per_item=reviews_per_item[0].mean()
mean_review_per_user=reviews_per_user[0].mean()

#average rating, word count per review, and average word count
average_rating=df["overall"].mean()
df["word_count"]=df["reviewText"].str.split().str.len()
average_word_count=df["word_count"].mean()

#applying labels positive, negative and neutral
df["label"]=df.apply(lambda x: "pos" if x["overall"]>=4 else "neutral" if x["overall"]==3 else"neg", axis=1)

df_select=df.sample(1000)




