from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from tqdm import tqdm

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def make_cc_of_oneself(client, symptom):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""You are a doctor studying diagnostics. 
                You are simulating a patient with a certain symptom. 
                Patients with this symptom may present to the doctor in a variety of ways. 
                Create three chief complaints for the symptom in Korean.
                Keep it simple and concise. and give a list as a response.
                ["CC1", "CC2", "CC3"]
                """
            },
            {
                "role": "user",
                "content": f"{symptom}"
            }
        ],
        temperature=0.8,
        top_p=1
    )   
    return json.loads(response.choices[0].message.content)


def make_cc_for_ones_child(client, symptom):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""You are a doctor studying diagnostics. 
                You are simulating a parent who has a child with a certain symptom. 
                The child with this symptom may present to the doctor in a variety of ways. 
                Create three chief complaints for the symptom in Korean.
                Keep it simple and concise. and give a list as a response.
                ["아이가 __ ", "아이가 __", "아이가 __ "]
                """
            },
            {
                "role": "user",
                "content": f"{symptom}"
            }
        ],
        temperature=0.8,
        top_p=1
    )   
    return json.loads(response.choices[0].message.content)


def get_cc(client, symptom):
    if "adult" in symptom:
        return make_cc_of_oneself(client, symptom)
    elif "children" in symptom:
        return make_cc_for_ones_child(client, symptom)
    else:
        return None


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
symptoms = read_json_file("links_dict.json").keys()

output = {symptom: get_cc(client, symptom) for symptom in tqdm(symptoms)}

with open('cc_list.json', 'w', encoding='utf-8') as file:
    json.dump(output, file, ensure_ascii=False, indent=4)