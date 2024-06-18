import json
from collections import OrderedDict

cc_json_file = "cc_list.json"
questions_json_file = "updated_links_dict.json"
output_json_file = "combined_json.json"

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# JSON으로 불러오기
cc_json = read_json_file(cc_json_file)
questions_json = read_json_file(questions_json_file)

# JSON 합치기, question_json에 cc_json을 추가하되, 두 파일에서 첫번째 키가 일치하는 경우 cc_json의 value를 question_json의 key 아래 "CC"라는 키를 생성하고 value로 넣기
combined_json = {}

for symptom in questions_json.keys():
    if symptom in cc_json.keys():
        combined_json[symptom] = questions_json[symptom]
        combined_json[symptom]["CC"] = cc_json[symptom]
    else:
        combined_json[symptom] = questions_json[symptom]

# 키 순서 변경
ordered_combined_json = OrderedDict()
for symptom, details in combined_json.items():
    ordered_combined_json[symptom] = OrderedDict()
    if "link" in details:
        ordered_combined_json[symptom]["link"] = details["link"]
    if "CC" in details:
        ordered_combined_json[symptom]["CC"] = details["CC"]
    if "response" in details:
        ordered_combined_json[symptom]["response"] = details["response"]

# 합쳐진 JSON 파일 저장
write_json_file(ordered_combined_json, output_json_file)