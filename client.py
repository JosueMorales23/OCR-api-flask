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

if 'cleaned_text' or 'splitted_text' in response_data:
    cleaned_text = response_data['cleaned_text']
    splitted_text = response_data['splitted_text']

    matches = pattern_utils.search_patterns(cleaned_text)

    not_found = "\33[31m" + "Not found" + "\33[0m"
    found = "\33[32m" + "Found" + "\33[0m"

    document_type = matches[0].group(0) if matches[0] else not_found
    id_number = matches[1].group(2) if matches[1] else not_found
    name = matches[2].group(4) if matches[2] else not_found
    issue_date = matches[3].group(2) if matches[3] else not_found

    document_type2 = matches[4].group(0) if matches[4] else not_found
    member_id = matches[5].group(1) if matches[5] else not_found
    name2 = matches[6].group(1) if matches[6] else not_found
    effective_date = matches[7].group(1) if matches[7] else not_found

    # specifics patterns
    specific_member_id = matches[8].group(0) if matches[8] else not_found

    document_type3 = matches[9].group(0) if matches[9] else not_found
    document_type4 = matches[10].group(0) if matches[10] else not_found
    document_type5 = matches[11].group(0) if matches[11] else not_found
    name3 = matches[12].group(0) if matches[12] else not_found
    document_type6 = matches[13].group(0) if matches[13] else not_found
    document_type7 = matches[14].group(0) if matches[14] else not_found
    document_type8 = matches[15].group(0) if matches[15] else not_found

    print("---------------------------------")
    if specific_member_id:
        print(f"Member: {found}")
    else:
        print(f"Member: {not_found}")

    if document_type == 'BENEFITS IDENTIFICATION CARD':
        print(f"Document Type: {document_type}")
        print(f"ID Number: {id_number}")
        print(f"Name: {name}")
        print(f"Issue Date (mm/dd/yy): {issue_date}")

    if document_type2 == "MediCal Program":
        print(f"Document Type: {document_type2}")
        print(f"Member ID: {member_id}")
        print(f"Name: {name2}")
        print(f"Effective Date (m/d/yyyy): {effective_date}")

    if (document_type3 == 'Benefits' or document_type4 == 'Identification'
            or document_type5 == 'Card'):
        print(f"Document Type: {document_type3}" + " " + f"{document_type4}"
              + " " + f"{document_type5}")
        print(f"ID Number: {id_number}")
        print(f"Name: {name3}")
        print(f"Issue Date (mm/dd/yy): {issue_date}")

    if document_type6 == 'Anthem' or document_type7 == 'LA Care' or document_type8 == 'BlueCross':
        print(f"Document Type: {document_type6} " f"{document_type7} " + f"{document_type8}")

    print("---------------------------------")
    print(f"All: ", response_data)
    print("---------------------------------")
