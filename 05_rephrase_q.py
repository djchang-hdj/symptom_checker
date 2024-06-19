# "combined_json.json"을 불러와서 기본적 질문을 구성하는 코드.

# 모든 selection 뒤에 other 추가
# {
#     "Abdominal pain in adults": {
#         "symptom": "Abdominal pain in adults",
#         "link": "https://www.mayoclinic.org/symptom-checker/abdominal-pain-in-adults-adult/related-factors/itt-20009075",
#         "response": {
#             "consultation": [
#                 {
#                     "question": "Pain is",
#                     "selections": [
#                         "Burning",
#                         "Crampy",
#                         "Dull",
#                         "Gnawing",
#                         "Intense",
#                         "Intermittent or episodic",
#                         "Ongoing (chronic)",
#                         "Sharp",
#                         "Steady",
#                         "Sudden (acute)",
#                         "Worsening or progressing"
#                     ]
#                 },
#         }
#     }
# }

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from tqdm import tqdm

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

json_file = "combined_json.json"
output_json_file = "combined_json_with_other.json"

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_other_to_selections(data):
    for key, value in data.items():
        if 'response' in value and 'consultation' in value['response']:
            for consultation in value['response']['consultation']:
                if 'selections' in consultation:
                    consultation['selections'].append("Other")


def change_question_with_openai(symptom, question):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""You are a doctor researching a diagnosis. 
                You are requested to ask detailed questions about a given chief complaint.
                The user will request in a format of "cc: symptom, item to ask: question". 
                You should rephrase the question as you would ask a patient. 
                For example, if the user presents cc:"Abdominal pain in adults", item to ask: "Pain is", 
                you might result: "What is your abdominal pain like?"
                Just pose a question..
                """
            },
            {
                "role": "user",
                "content": f"cc: {symptom}, item to ask: {question}"
            }
        ],
        temperature=0.8,
        top_p=1
    )   
    return response.choices[0].message.content

#질문을 변경하는 함수 : tqdm 적용  
def change_question(data):
    for key, value in tqdm(data.items()):
        symptom = key
        if 'response' in value and 'consultation' in value['response']:
            for consultation in value['response']['consultation']:
                if 'question' in consultation:
                    consultation['question'] = change_question_with_openai(symptom, consultation['question'])

json_data = read_json_file(json_file)
add_other_to_selections(json_data)
change_question(json_data)
write_json_file(json_data, output_json_file)
