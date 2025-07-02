import requests
from bs4 import BeautifulSoup
import json

result = {}
urls = ['https://www.usaswimming.org/times/popular-resources/national-age-group-records/scy/10-under', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/scy/11-12', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/scy/13-14', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/scy/15-16', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/scy/17-18', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/lcm/10-under', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/lcm/11-12', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/lcm/13-14', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/lcm/15-16', 'https://www.usaswimming.org/times/popular-resources/national-age-group-records/lcm/17-18']
index = 0
for age_group in ['SCY10', 'SCY12', 'SCY14', 'SCY16', 'SCY18', 'LCM10', 'LCM12', 'LCM14', 'LCM16', 'LCM18']:
    url = urls[index]
    index+=1

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    table = soup.find("table", class_="usas-times-nationalagegrouprecords-table")

    rows = []
    if table:
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            rows.append(cells)

    keywords = {'Time', 'Event', 'WOMEN', 'MEN'}

    rows = [
        row for row in rows if row and row[0] in keywords
    ]


    rows = rows[1:]

    for i in range(0, len(rows), 3):
        group = rows[i:i+3]
        if len(group) < 3:
            continue 

        gender_row = group[0][0]
        gender_prefix = 'W' if 'WOMEN' in gender_row.upper() else 'M'

        event = None
        time = None


        for row in group[1:]:
            if row[0] == 'Event':
                event = row[1]
            elif row[0] == 'Time':
                time = row[1]

        if event and time:
            key = age_group + gender_prefix + event
            result[key] = time


with open("nagtimes.json", "w") as f:
    json.dump(result, f, indent=2)