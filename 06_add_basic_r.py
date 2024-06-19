# combined_json_with_other.json"을 불러와서 기본적 질문을 구성하는 코드.

# {
#     "Abdominal pain in adults": {
#         "symptom": "Abdominal pain in adults",
#         "link": "https://www.mayoclinic.org/symptom-checker/abdominal-pain-in-adults-adult/related-factors/itt-20009075",
#         "response": {
#             "consultation": [
#                 {
#                     "question": "Can you describe the nature of your abdominal pain? What does it feel like?",
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
#                         "Worsening or progressing",
#                         "Other"
#                     ]
#                 },
#             ]
#         }
#     }
# }



import json
from tqdm import tqdm

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# "symptom"에 "adult"라는 문자열이 포함된 경우
# "consultation" 의 첫항목으로 
# "question" : "환자분의 나이가 어떻게 되시나요?",
# "selections" : [10대, 20대, 30대, 40대, 50대, 60대, 70대, 80대이상, other] 추가

# "symptom"에 "child"라는 문자열이 포함된 경우
# "consultation" 의 첫항목으로 
# "question" : "환자분의 나이가 어떻게 되시나요?",
# "selections" : [1세 미만, 1~3세, 3~7세, 7~10세, 10세 이상, other]추가

# 질문의 마지막에 # "question" : "증상과 관련하여 추가로 말씀하고 싶은 것이 있나요?
# "selections" : [아니오, 예]추가

def add_basic_questions(data):
    for key, value in data.items():
        symptom = value.get("symptom", "")
        consultation = value.get("response", {}).get("consultation", [])
        
        if "adult" in symptom:
            consultation.insert(0, {
                "question": "환자분의 나이가 어떻게 되시나요?",
                "selections": ["10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대이상", "other"]
            })
        elif "child" in symptom:
            consultation.insert(0, {
                "question": "환자분의 나이가 어떻게 되시나요?",
                "selections": ["1세 미만", "1~3세", "3~7세", "7~10세", "10세 이상", "other"]
            })
        
        consultation.append({
            "question": "증상과 관련하여 추가로 말씀하고 싶은 것이 있나요?",
            "selections": ["아니오", "예"]
        })
        
        value["response"]["consultation"] = consultation

    return data

json_file = "combined_json_with_other.json"
output_json_file = "json_with_basic_questions.json"

json_data = read_json_file(json_file)
updated_json_data = add_basic_questions(json_data)
write_json_file(updated_json_data, output_json_file)