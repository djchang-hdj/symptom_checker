# https://www.mayoclinic.org/symptom-checker/select-symptom/itt-20009075 에 들어가서  <div class="check"> </div>에 있는 링크의 제목과 링크를 dictionary로 저장하기

import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage
url = "https://www.mayoclinic.org/symptom-checker/select-symptom/itt-20009075"

base_url = "https://www.mayoclinic.org"
# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.content, 'html.parser')

# Find the <div> with class "check"
check_div = soup.find('div', class_='check')

# Initialize an empty dictionary to store the links
links_dict = {}

# Find all <a> tags within the <div class="check">
# add base_url to the link
if check_div:
    for a_tag in check_div.find_all('a'):
        title = a_tag.get_text(strip=True)
        link = a_tag.get('href')
        if title and link:
            full_link = base_url + link
            links_dict[title] = full_link
            
# save the dictionary to a json file
with open('links_dict.json', 'w') as f:
    json.dump(links_dict, f)

# Print the dictionary
print(links_dict)

