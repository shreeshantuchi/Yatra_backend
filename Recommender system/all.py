from pandas.io.excel import read_excel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
data = read_excel("Data.xlsx")

# Preprocess data
vectorizer = TfidfVectorizer()
keywords_matrix = vectorizer.fit_transform(data['keywords'])

# Define similarity metric
def get_similarities(input_keywords, input_review, input_cost, input_location):
    # Calculate cosine similarities based on keywords
    input_matrix = vectorizer.transform([input_keywords])
    cosine_similarities = cosine_similarity(input_matrix, keywords_matrix).flatten()
    
    # Add review similarities
    review_similarities = data['Review'].apply(lambda x: 1 - abs(x - input_review) / 4)
    cosine_similarities += review_similarities
    
    # Add cost similarities
    cost_similarities = data['Average cost'].apply(lambda x: 1 - abs(x - input_cost) / 4900)
    cosine_similarities += cost_similarities
    
    # Add location similarities
    location_similarities = data['Location'].apply(lambda x: 1 if x == input_location else 0)
    cosine_similarities += location_similarities
    
    return cosine_similarities

# Recommend hotels based on user input
def recommend_hotels(input_keywords, input_review, input_cost, input_location, num_recommendations=5):
    similarities = get_similarities(input_keywords, input_review, input_cost, input_location)
    indices = similarities.argsort()[:-num_recommendations-1:-1]
    return list(data.iloc[indices]['Hotels'])

# Example usage
recommended_hotels = recommend_hotels('cozy,expensive', 4.5, 2500, 'Kathmandu')
print(recommended_hotels)
