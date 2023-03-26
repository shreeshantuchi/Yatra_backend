import numpy as np
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack
import math,os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatra.settings')

import django
django.setup()

from Activites.models import Activity

cv=TfidfVectorizer()
vectorizer = TfidfVectorizer()

def stem(text):
    y=[]
    for i in text.split(','):
#        print(i)
        if i != None:
            y.append(ps.stem(i))
        else:
            y.append(i)
#     print(y)
#     print(type(''.join(x for x in y)))
    return ','.join(x for x in y)

def stemd(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return y


def sortkey(text):
    y=[]
    y=sorted(text.split(","))
    return ','.join(x for x in y)

def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', '(', ')','[', ']', '{', '}'])
    text = text.replace(',', ' ').replace('\n', ' ')  # replace commas and newlines with spaces
    text = ' '.join(text.split()) 
    tokens = nltk.word_tokenize(text)
    filtered_text = [word for word in tokens if word.lower() not in stop_words and not re.match(r'^\d+(\.\d+)?$', word)]
    return " ".join(filtered_text)

def buildDataFrame():
    destinations=(Activity.objects.all())

    name=[]
    address=[]
    average_price=[]
    keywords=[]
    index=[]
    description=[]

    for destination in destinations:
        name.append(destination.name)
        address.append(destination.location)
        average_price.append(destination.average_price)
        keywords.append(destination.related_keywords)
        description.append(destination.description)
        index.append(destination.id)
    
        print(destination.location)
    # for i in range(1,len(name)):
    #     print(name[i], address[i],average_price[i],keywords[i])

    new_dict={'Name':name,'Location':address,'AvgPrice':average_price,'Description':description,'Keywords':keywords,'Index':index}

    data_destination=pd.DataFrame(new_dict)
    
    #removing space aplying stem converting to lower case and sorting values for keywords
    data_destination['Keywords']=data_destination['Keywords'].apply(lambda x :x.replace(' ',''))
    data_destination['Keywords']=data_destination['Keywords'].apply(stem)
    data_destination['Keywords']=data_destination['Keywords'].apply(lambda x:x.lower())
    data_destination['Keywords']=data_destination['Keywords'].apply(sortkey)
    data_destination['Description']=data_destination['Description'].apply(lambda x:x.lower())
    data_destination['Description']=data_destination['Description'].apply(remove_stop_words)
    data_destination['tags']=data_destination['Description'].apply(stemd)
    data_destination['Location']=data_destination['Location'].apply(lambda x:x.lower())
    

    print('data frame ready')
    print(data_destination.head(50))
    return data_destination

def vectorize(data_destination):
    keywords_matrix = vectorizer.fit_transform(data_destination['Keywords']+data_destination['Description'])
    return keywords_matrix
    # keywords_matrix=np.asarray(keywords_matrix)
    # cv.get_feature_names()

def get_recommendations(user_location, user_interest,data_destination):
    keywords_matrix=vectorize(data_destination)
    # Clean and stem user input
    user_interest = stem(user_interest)
    
    # Split user interest into individual keywords
    user_interest_list = user_interest.split(",")
    
    # Initialize empty list for keyword vectors
    keyword_vecs = []
    
    # Loop through each keyword, vectorize it, and append to keyword_vecs list
    for keyword in user_interest_list:
        keyword_vec = vectorizer.transform([stem(keyword)])
        keyword_vecs.append(keyword_vec)
    
    # Sum the keyword vectors to get a single vector for the user's input
    query_interest_vec = vstack(keyword_vecs).sum(axis=0)
    
    # Compute cosine similarity between user interests and keywords in the dataset
    cosine_sim_interest = cosine_similarity(np.asarray(query_interest_vec), keywords_matrix)
    print(cosine_sim_interest)
    # Normalize cosine similarity scores
    cosine_sim_interest_norm = cosine_sim_interest / cosine_sim_interest.max()
    print(cosine_sim_interest_norm)
    
    
    if 'kathmandu' in user_location.lower():
        user_location='Kathmandu'
    if 'lalitpur' in user_location.lower():
        user_location='Lalitpur'
    if 'bhaktapur' in user_location.lower():
        user_location='Bhaktapur'

    # Compute location similarity between user location and locations in the dataset
    location_similarities = data_destination['Location'].apply(lambda x: 1 if user_location.lower() in x else 0)
    
    # Normalize location similarity scores
    location_similarities_norm = location_similarities * 1.0 / location_similarities.max()
    location_similarities_norm = location_similarities_norm.values.reshape(1, -1)

    print(location_similarities)
    # Combine the two similarity scores using a weighted sum
    # You can adjust the weights to give more importance to one score over the other
    
    combined_similarities = 0.5 * cosine_sim_interest_norm + 0.5 * location_similarities_norm
    
    # Get the indices of the top N recommendations
    top_n_indices = np.argsort(-combined_similarities[0])    

    # Get the similarity scores for the top N recommendations
    similarity_scores = combined_similarities[0][top_n_indices]
    print("Similarity Scores:", similarity_scores)    
    
    # Get the top N recommendations and add the similarity scores
    results = data_destination.iloc[top_n_indices]    
    results = results.copy()
    results['score'] = similarity_scores
    results['id']= top_n_indices
    
    return results.index



def activityrecomendation(location,interest):
    data=buildDataFrame()
    indexs=get_recommendations(location,interest,data)
    print(data.iloc[indexs])
    return indexs
