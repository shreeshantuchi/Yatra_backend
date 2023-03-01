import requests
from bs4 import BeautifulSoup
import csv

# Send a GET request to the URL
url = 'https://www.countryfaq.com/list-of-countries-and-their-flags/'
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the country names and flags
table = soup.find('table')



# Extract the data from the table and write to a CSV file
with open('country_flags.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Country', 'Flag'])
    # Write data rows
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        try:
            flag_url = columns[0].find('img')['src']
        except:
            flag_url="not found"
        try:
            country_name = columns[1].text.strip()
        except:
            country_name="not found"
        if country_name!="not found" and flag_url!="not found":
            writer.writerow([country_name, flag_url])
