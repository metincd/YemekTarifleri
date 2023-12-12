import requests
from bs4 import BeautifulSoup
import json

url = "https://en.wikipedia.org/wiki/Table_of_food_nutrients"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all("table", {"class": "wikitable"})
data = []

for row in tables[0].find_all("tr"):
    columns = row.find_all("td")
    if columns:
        item = {
            "food": columns[0].text.strip(),
            "calories": columns[1].text.strip(),
        }
        data.append(item)

json_data = json.dumps(data, indent=4)
print(json_data)

with open('food_nutrients.json', 'w') as f:
    f.write(json_data)
