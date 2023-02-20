from pandas.io.excel import read_excel
import pandas as pd
import numpy as np

df = read_excel("Data.xlsx")
from sklearn.neighbors import NearestNeighbors
location_user = ["Bhaktapur"]

# for location in ['Kathmandu', 'Bhaktapur', 'Lalitpur']:
for location in location_user:

    hotels_in_location = df[df['Location'] == location]
    X = hotels_in_location[['Review']]
    model = NearestNeighbors(n_neighbors=5)
    model.fit(X)
    X_test = np.array([[5], [5], [5], [5], [5]], dtype=np.int64)
    distances, indices = model.kneighbors(X_test)
    top_hotels = [hotels_in_location.iloc[index]['Hotels'] for index in indices[0]]
    print(f"Top 5 hotels in {location_user}:")
    print(top_hotels)
    print("\n")