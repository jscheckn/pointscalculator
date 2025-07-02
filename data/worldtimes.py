import requests
from bs4 import BeautifulSoup
import json

result={}
index = 0
urls = ["https://swimswam.com/records/mens-us-open-records-scy/", "https://swimswam.com/records/womens-us-open-records-scy/", "https://swimswam.com/records/mens-world-records-lcm/", "https://swimswam.com/records/womens-world-records-lcm/"]
for filters in ["SCYOpenM", "SCYOpenW", "LCMOpenM", "LCMOpenW"]:
    response = requests.get(urls[index])
    index+=1

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', id='ranking')
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        rows.append(cells)

    rows = rows[1:] 

    for row in rows:
        key = filters + row[0]
        result[key] = row[3]

# Replacements to make
replacements = {
    " Free": " Freestyle",
    " Back": " Backstroke",
    " Breast": " Breaststroke",
    " Fly": " Butterfly",
    " IM": " Individual Medley"
}

# Create a new dictionary with updated keys
updated_data = {}
for key, value in result.items():
    new_key = key
    for old, new in replacements.items():
        new_key = new_key.replace(old, new)
    updated_data[new_key] = value

with open("worldTimes.json", "w") as f:
    json.dump(updated_data, f, indent=2)
