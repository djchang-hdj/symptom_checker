import os
import json

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Function to write JSON files
def write_json_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error writing file {file_path}: {e}")

# Remove _review_01 from filenames
json_dir = './json_revised'
file_list = os.listdir(json_dir)
for file in file_list:
    if "_review_01" in file:
        old_path = os.path.join(json_dir, file)
        new_path = os.path.join(json_dir, file.replace("_review_01", ""))
        os.rename(old_path, new_path)

# Update JSON files
file_list = os.listdir(json_dir)
for file in file_list:
    if file.endswith('.json'):  # Process only JSON files
        file_path = os.path.join(json_dir, file)
        data = read_json_file(file_path)
        if data is not None:
            symptom = os.path.splitext(file)[0]  # Get filename without extension
            data['symptom'] = symptom  # Add or update the 'symptom' key
            write_json_file(data, file_path)