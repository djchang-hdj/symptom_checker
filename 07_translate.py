# {
#     "Abdominal pain in adults": {
#         "symptom": "Abdominal pain in adults",
#         "link": "https://www.mayoclinic.org/symptom-checker/abdominal-pain-in-adults-adult/related-factors/itt-20009075",
#         "cc": [
#             "배가 아파요",
#             "복통이 있어요",
#             "속이 쓰려요"
#         ],
#         "response": {
#             "consultation": [
#                 {
#                     "question": "환자분의 나이가 어떻게 되시나요?",
#                     "selections": [
#                         "10대",
#                         "20대",
#                         "30대",
#                         "40대",
#                         "50대",
#                         "60대",
#                         "70대",
#                         "80대이상",
#                         "other"
#                     ]
#                 },
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
#                 {
#                     "question": "Can you tell me where exactly you're feeling the abdominal pain?",
#                     "selections": [
#                         "Abdomen but radiates to other parts of the body",
#                         "Lower abdomen",
#                         "Middle abdomen",
#                         "One or both sides",
#                         "Upper abdomen",
#                         "Other"
#                     ]
#                 },
#                 {
#                     "question": "Is there anything specific that seems to trigger or worsen your abdominal pain?",
#                     "selections": [
#                         "Coughing or other jarring movements",
#                         "Drinking alcohol",
#                         "Eating certain foods",
#                         "Menstrual cycle",
#                         "Stress",
#                         "Other"
#                     ]
#                 },
#                 {
#                     "question": "Does anything seem to relieve your abdominal pain, such as changing positions or taking medications?",
#                     "selections": [
#                         "Antacids",
#                         "Avoiding certain foods",
#                         "Changing position",
#                         "Drinking more water",
#                         "Eating certain foods",
#                         "Eating more fiber",
#                         "Other"
#                     ]
#                 },
#                 {
#                     "question": "Do you experience any other symptoms along with your abdominal pain?",
#                     "selections": [
#                         "Abdominal swelling",
#                         "Black or bloody stools",
#                         "Constipation",
#                         "Diarrhea",
#                         "Fever",
#                         "Inability to move bowels in spite of urge",
#                         "Loose, watery stools",
#                         "Nausea or vomiting",
#                         "Passing gas",
#                         "Pulsing sensation near the navel",
#                         "Rash",
#                         "Stomach growling or rumbling",
#                         "Unintended weight loss",
#                         "Urgent need to have a bowel movement",
#                         "Other"
#                     ]
#                 },
#                 {
#                     "question": "증상과 관련하여 추가로 말씀하고 싶은 것이 있나요?",
#                     "selections": [
#                         "아니오",
#                         "예"
#                     ]
#                 }
#             ]
#         }
#     },
# }

# 문항을 한국의 실정에 맞도록 문구를 수정하는 코드
# LLM을 사용하여 번역
# 한글로 번역하고 원문은 괄호 안에 병기한다. 원래 한글인 것은 그대로 둔다.

# 돈 많이 들고 성능 떨어짐

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from tqdm import tqdm

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

json_file = "json_with_basic_questions.json"
output_json_file = "json_in_korean.json"

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#텍스트에서 ```json과 ```를 제거하는 함수
def remove_backticks(text):
    return text.replace('```json', '').replace('```', '')

def translate_and_write_json(json_object):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a doctor, developer, and translator. 
                A user provides you with a JSON object. 
                The content is a set of medical questions.
                Translate to Korean leaving the original Korean as it is. Keep the Structure of the JSON as it is.
                the answer should start with '{' and end with '}'"""
            },
            {
                "role": "user",
                "content": json.dumps(json_object)
            }
        ],
        temperature=0.8,
        top_p=1
    )
    
    try:
        translated_content = response.choices[0].message.content
        print(translated_content)
        translated_content = remove_backticks(translated_content)
        return json.loads(translated_content)
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error in translation response: {e}")
        return None

json_object = read_json_file(json_file)

# json_object 에서 response를 translate_and_write_json에 적용한 뒤에 원래의 json_object의 response를 바꿔준다.
for key, value in json_object.items():
    translated_response = translate_and_write_json(value["response"])
    if translated_response:
        json_object[key]["response"] = translated_response

write_json_file(json_object, output_json_file)