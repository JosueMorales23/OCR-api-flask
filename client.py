import requests
import base64
import re

server_url = 'http://localhost:5000/process_image'

with open('ruta_a_tu_imagen.jpg', 'rb') as image_file:
    image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

json_data = {
    'imagen': image_base64
}

response = requests.post(server_url, json=json_data)

response_data = response.json()

if 'text' in response_data:
    text = response_data['text']

    id_pattern = r'(IDNo\.|No.)\s*(\w+)'
    name_pattern = r'(?<=[*~|])\s*([A-Z ]+)\n'  # ID0009, ID0015
    name_pattern_1 = r'(IDNo\.|No.)\s*(\w+)(\n\n~|\n~|\n|\n*)\s*([A-Z ]+)\n'  # ID0012, ID0017, ID0018, ID0020
    name_pattern_2 = r'(IDNo\.|No.)\s*(\w+)\s*([a-z ]+\s*,\n\n((\w+)\s*(\w+)\s*(\w+)))'  # ID0019
    issue_date_pattern = r'Issue\s*Date\s*(\d{2}\s*\d{2}\s*\d{2})'

    id_match = re.search(id_pattern, text, re.IGNORECASE)
    name_match = re.search(name_pattern, text, re.IGNORECASE)
    name_match1 = re.search(name_pattern_1, text, re.IGNORECASE)
    name_match2 = re.search(name_pattern_2, text, re.IGNORECASE)
    issue_date_match = re.search(issue_date_pattern, text, re.IGNORECASE)

    not_found = "\33[31m" + "Not found" + "\33[0m"

    id_number = id_match.group(2) if id_match else not_found
    name = name_match.group(1) if name_match else not_found
    issue_date = issue_date_match.group(1) if issue_date_match else not_found

    print("---------------------------------")
    print(f"ID Number: {id_number}")
    if name_match1:
        print(f"Name2: {name_match1.group(4)}")
    elif name_match:
        print(f"Name1: {name}")
    elif name_match2:
        print(f"Name3: {name_match2.group(4)}")
    else:
        print(f"Name: {not_found}")
    print(f"Issue Date: {issue_date}")
    print("---------------------------------")
    print(f"All: ", response_data)
    print("---------------------------------")
