#%%
import sqlite3
import csv
import pandas as pd
import re
import spacy

#%%
conn= sqlite3.connect('greviewdb.sqlite')
cur=conn.cursor()

#%%
db_df = pd.read_sql_query("SELECT * FROM Reviews;", conn)
db_df.to_csv('database.csv', index=False)
train=pd.read_csv('database.csv')
if(train.empty):
    print("There's no data to be analysed.")
#%%
print(train['review'])
#%%
print(train['rating'])
#%%
train['rating'].value_counts()
#%%
lst=[]
for item in train['rating']:
    x=int(re.search('[0-5]',item).group(0))
    lst.append(x)
train['rating']=pd.Series(lst)
print(train['rating'])
#%%
train.drop(['id','placeid','name'],inplace=True,axis=1)
#%%
nlp=spacy.load("en_core_web_sm")
#%% replace
test=nlp("Crazy experience that will leave you mind blown!")
nlp.pipe_names
#%% checking
for item in test:
    print(item.text,'->',item.pos_)
#%% testing if i remember
test2='this is a repititive la di da sentece ha ha di da da !'
dict={}
for item in test2.split():
    dict[item]=dict.get(item,0)+1
print(dict)
#%% WHat we need is words (from the reviews) which could hep in distinguishing postive from negative [i.e. w/o prep, conjunctions,etc.], format them [ same form- remove capitalization] for each review.
# Then, maybe catch their frequency of occurence in that sentence and hence keep on making new columns for new words (all word sof all reviews will be columns)
#%%

#%%
