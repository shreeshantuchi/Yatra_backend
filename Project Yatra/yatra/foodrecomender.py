import pandas as pd
import numpy as np
import os
import string
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack

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
    # print(y)
#     print(type(''.join(x for x in y)))
    return ','.join(x for x in y)


def sortkey(text):
    y=[]
    y=sorted(text.split(","))
    return ','.join(x for x in y)

def lower(word):
    return word.lower()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatra.settings')

import django
django.setup()

from Food.models import Food

def buildDataFrame():
    foods=(Food.objects.all())

    name=[]
    address=[]
    average_price=[]
    keywords=[]
    index=[]
    ratings=[]

    for food in foods:
        if 'kathmandu' in food.location.lower():
            location='Kathmandu'
        if 'lalitpur' in food.location.lower():
            location='Lalitpur'
        if 'bhaktapur' in food.location.lower():
            location='Bhaktapur'
        name.append(food.name)
        address.append(location)
        average_price.append(food.average_price)
        keywords.append(food.related_keywords)
        index.append(food.id)
        ratings.append(food.ratings)
    
        # print(food.name,location,food.average_price,food.related_keywords)
    # for i in range(1,len(name)):
    #     print(name[i], address[i],average_price[i],keywords[i])

    new_dict={'Name':name,'Location':address,'AvgPrice':average_price,'Keywords':keywords,'Index':index,'Ratings':ratings}

    data_food=pd.DataFrame(new_dict)
    
    data_food['Keywords']=data_food['Keywords'].apply(stem)
    data_food['Keywords']=data_food['Keywords'].apply(lambda x:x.lower())
    data_food['Keywords']=data_food['Keywords'].apply(sortkey)
    data_food['Location']=data_food['Location'].apply(lower)
    data_food['Location'] = data_food['Location'].apply(lambda x: x.strip())
    

    print('data frame ready')
    return data_food


    



def vectorize(data_food):
    keywords_matrix = vectorizer.fit_transform(data_food['Keywords'])
    return keywords_matrix
    # keywords_matrix=np.asarray(keywords_matrix)
    # cv.get_feature_names()



def get_recommendations(user_location, user_interest,data_food):
    keywords_matrix=vectorize(data_food)
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
    # print('cosine sim interest',cosine_sim_interest)

    # Normalize cosine similarity scores
    cosine_sim_interest_norm = cosine_sim_interest / cosine_sim_interest.max()
    # print('cosine sim interest',cosine_sim_interest_norm)

    # Compute location similarity between user location and locations in the dataset
    
    #get the KBL
    if 'kathmandu' in user_location.lower():
        user_location='Kathmandu'
    if 'lalitpur' in user_location.lower():
        user_location='Lalitpur'
    if 'bhaktapur' in user_location.lower():
        user_location='Bhaktapur'

    location_similarities = data_food['Location'].apply(lambda x: 1 if x == user_location.lower() else 0)

    # Normalize location similarity scores
    location_similarities_norm = location_similarities * 1.0 / location_similarities.max()
    location_similarities_norm = location_similarities_norm.values.reshape(1, -1)
    # print('loation sim norm',location_similarities_norm)

    # Combine the two similarity scores using a weighted sum
    # You can adjust the weights to give more importance to one score over the other
    
    combined_similarities = 0.5 * cosine_sim_interest_norm + 0.5 * location_similarities_norm
    
    
    # Get the indices of the top N recommendations
    top_n_indices = np.argsort(-combined_similarities[0])  

    # Get the similarity scores for the top N recommendations
    similarity_scores = combined_similarities[0][top_n_indices]
    print("Similarity Scores:", similarity_scores)    
    
    # Get the top N recommendations and add the similarity scores
    results = data_food.iloc[top_n_indices]    
    results = results.copy()
    results['score'] = similarity_scores
    results['id']= top_n_indices
    
    return results.index


# recomendations=get_recommendations('Kathmandu','newari')

# recomendations.loc[recomendations['Name']=='SaSa: The Newa Restaurant'].head()
# rec_indx=recomendations.index+1
# print(rec_indx)

# print(recomendations)
# recomendations=recomendations+1
# print('printing recomendations')
# print(recomendations)

def get_popular_recommendations(user_location, user_interest,data_food):
    keywords_matrix=vectorize(data_food)
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
    # print('cosine sim interest',cosine_sim_interest)

    # Normalize cosine similarity scores
    cosine_sim_interest_norm = cosine_sim_interest / cosine_sim_interest.max()
    # print('cosine sim interest',cosine_sim_interest_norm)

    # Compute location similarity between user location and locations in the dataset
    
    #get the KBL
    if 'kathmandu' in user_location.lower():
        user_location='Kathmandu'
    if 'lalitpur' in user_location.lower():
        user_location='Lalitpur'
    if 'bhaktapur' in user_location.lower():
        user_location='Bhaktapur'

    location_similarities = data_food['Location'].apply(lambda x: 1 if x == user_location.lower() else 0)
    review_score=data_food['Ratings'].apply(lambda x: float(x))


    # Normalize location similarity scores
    location_similarities_norm = location_similarities * 1.0 / location_similarities.max()
    location_similarities_norm = location_similarities_norm.values.reshape(1, -1)
    # print('loation sim norm',location_similarities_norm)

    # Normalize location similarity scores
    review_norm = review_score * 1.0 / review_score.max()
    review_norm = review_norm.values.reshape(1, -1)
    # print('loation sim norm',location_similarities_norm)

    # Combine the two similarity scores using a weighted sum
    # You can adjust the weights to give more importance to one score over the other
    
    combined_similarities = 0.5 * review_norm + 0.4 * location_similarities_norm+ 0.1 * cosine_sim_interest_norm
    
    
    # Get the indices of the top N recommendations
    top_n_indices = np.argsort(-combined_similarities[0])  

    # Get the similarity scores for the top N recommendations
    similarity_scores = combined_similarities[0][top_n_indices]
    print("Similarity Scores:", similarity_scores)    
    
    # Get the top N recommendations and add the similarity scores
    results = data_food.iloc[top_n_indices]    
    results = results.copy()
    results['score'] = similarity_scores
    results['id']= top_n_indices
    
    return results.index

def foodrecomendation(location,interest):
    data_food=buildDataFrame()
    indexs=get_recommendations(location,interest,data_food)
    print(data_food.iloc[indexs])
    return indexs

def foodpopular(location,interest):
    data_food=buildDataFrame()
    indexs=get_popular_recommendations(location,interest,data_food)
    print(data_food.iloc[indexs])
    print("popular")
    return indexs




