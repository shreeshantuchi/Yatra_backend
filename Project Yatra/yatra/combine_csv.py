import pandas as pd

# read the CSV files into pandas dataframes
df_flags = pd.read_csv('D:\Study\Projects\Github\YATRA-backend\Yatra_backend\Project Yatra\yatra\countries.csv')
df_names = pd.read_csv('D:\Study\Projects\Github\YATRA-backend\Yatra_backend\Project Yatra\yatra\country_flags.csv')

# merge the two dataframes on the 'name' column, which contains the full name of the countries
df_combined = pd.merge(df_names, df_flags, on='Name')

# save the combined dataframe to a new CSV file
df_combined.to_csv('combined.csv', index=False)