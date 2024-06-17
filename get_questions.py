import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from pydantic import BaseModel
from typing import List

class ConsultationQuestion(BaseModel):
    question: str
    selections: List[str]

class ConsultationResponse(BaseModel):
    consultation: List[ConsultationQuestion]

# Step 1: Load the JSON file containing the links
with open('links_dict.json', 'r') as file:
    data = json.load(file)

# Step 2: Function to fetch HTML content and extract the desired sections
def fetch_html_and_extract(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        frm_items = soup.find_all('div', class_='frm_item')
        if frm_items:
            result = []
            for item in frm_items:
                legend = item.find('legend')
                if legend:
                    question = legend.text.strip()
                    labels = item.find_all('label')
                    selections = [label.text.strip() for label in labels]
                    result.append({"question": question, "selections": selections})
            return result
        else:
            return [{"question": "No content found", "selections": []}]
    except requests.exceptions.RequestException as e:
        return [{"question": "Error fetching the content", "selections": [str(e)]}]

# Step 3: Iterate over each item in the JSON and fetch the HTML content with a progress bar
for symptom in tqdm(data, desc="Processing symptoms"):
    link = data[symptom]
    html_content_list = fetch_html_and_extract(link)
    time.sleep(2)  # Wait for 2 seconds before processing the next link
    
    # Transform the extracted content into ConsultationResponse format
    consultation_questions = [
        ConsultationQuestion(question=item["question"], selections=item["selections"])
        for item in html_content_list
    ]
    consultation_response = ConsultationResponse(consultation=consultation_questions)
    
    # Update the JSON structure
    data[symptom] = {
        "link": link,
        "questions": consultation_response.dict()
    }

# Step 4: Save the updated JSON back to a file
with open('updated_links_dict.json', 'w') as file:
    json.dump(data, file, indent=4)
