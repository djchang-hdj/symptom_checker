#  json_in_korean.json 파일을 읽어서 각 항목으로 JSON 파일을 생성
# 파일 이름은 기존 파일 이름 + _review_01 .. 02 로 생성
# 최상위 key 하나당 파일 하나 생성
# 생성된 파일은 claude 3로 번역 예정

import json
import os

json_in_korean_file = "json_in_korean.json"

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
        
original_json = read_json_file(json_in_korean_file)

for key, value in original_json.items():
    write_json_file(value, f"./json_review/{key}_review.json")
    
    
# ./json_review 폴더의 모든 파일 목록 만들기 
file_list = os.listdir("./json_review")

# 각 파일의 뒤에 텍스트 추가하기 
text = """ 


###############
이 JSON을 한글로 번역해야 한다. JSON의 구조는 그대로 두고 한글로 번역하자. 
이미 한글인 경우는 변역하지 않아도 된다. 
단, Ohter는 영어로 남기고 번역하지 않는다. 
############### """

for file_name in file_list:
    with open(f"./json_review/{file_name}", 'a', encoding='utf-8') as file:
        file.write(text)
        
        
# # ./json_review 폴더의 모든 파일 확장자를 json에서 txt로 변경하기
# for file_name in file_list:
#     os.rename(f"./json_review/{file_name}", f"./json_review/{file_name.replace('.json', '.txt')}")