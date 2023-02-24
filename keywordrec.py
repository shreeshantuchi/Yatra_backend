from pandas.io.excel import read_excel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the restaurant dataset
restaurants = read_excel("Data.xlsx")

# Split the keywords into individual words
restaurants['keywords'] = restaurants['keywords'].str.split(',')
restaurants['keywords'] = restaurants['keywords'].apply(lambda x: ' '.join(x))

# Vectorize the keywords
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(restaurants['keywords'])

# Compute similarity scores based on keywords and location
def get_recommendations(location, keywords):
    # Filter restaurants by location
    restaurants_location = restaurants[restaurants['Location'] == location]

    # Vectorize the keywords
    tfidf_location = TfidfVectorizer(stop_words='english')
    tfidf_location_matrix = tfidf_location.fit_transform(restaurants_location['keywords'])

    # Compute similarity scores based on keywords and location
    tfidf_matrix_combined = cosine_similarity(tfidf_matrix, tfidf_location_matrix)

    # Combine similarity scores based on keywords and location
    sim_scores_combined = tfidf_matrix_combined.mean(axis=1)

    # Get recommendations based on combined similarity scores
    keywords = keywords.split()
    keyword_vector = tfidf.transform([' '.join(keywords)])
    sim_scores = cosine_similarity(keyword_vector, tfidf_matrix)
    sim_scores = list(enumerate(sim_scores[0] * sim_scores_combined))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]
    restaurant_indices = [i[0] for i in sim_scores]
    recommendations = list(restaurants['Hotels'].iloc[restaurant_indices])
    return recommendations

# Get recommendations based on specific location and keywords
location = "Kathmandu"
keywords = "cozy,local"
recommendations = get_recommendations(location, keywords)
print(recommendations)
