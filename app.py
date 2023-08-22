import os
import base64
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pytesseract
import cv2
import numpy as np
import re

app = Flask(__name__)


def generate_random_key():
    return os.urandom(32)


def encrypt_image(image_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(image_data) + encryptor.finalize()
    return iv + encrypted_data


def decrypt_image(ciphertext, key, iv):
    extracted_iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(extracted_iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data


def preprocess_image(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray


@app.route('/process_image', methods=['POST'])
def process_image():
    if 'imagen' not in request.json:
        return jsonify({"error": "Missing image in request"}), 400

    imagen_base64 = request.json['imagen']

    try:
        image_data = base64.b64decode(imagen_base64)
    except base64.binascii.Error as e:
        print("Error decoding base64 image:", e)
        return jsonify({"error": "Invalid base64 format for image"}), 400

    iv = os.urandom(16)

    try:
        key = generate_random_key()
        encrypted_image = encrypt_image(image_data, key, iv)
    except Exception as e:
        print("Error encrypting image:", e)
        return jsonify({"error": "Error encrypting image"}), 500

    try:
        decrypted_image_data = decrypt_image(encrypted_image, key, iv)
    except Exception as e:
        print("Error decrypting image:", e)
        return jsonify({"error": "Error decrypting image"}), 500

    decrypted_image = preprocess_image(decrypted_image_data)
    extracted_text = pytesseract.image_to_string(decrypted_image, config='--psm 6')

    id_pattern = r'(IDNo\.|No.)\s*(\w+)'
    name_pattern = r'(IDNo\.|No.)\s*(\w+)(\n\n~|\n~|\n|\n*)\s*([A-Z ]+)\n'
    name_pattern_1 = r'(IDNo\.|No.)\s*(\w+)(\n\n~|\n~|\n|\n*)\s*([A-Z ]+)\n'
    name_pattern_2 = r'(IDNo\.|No.)\s*(\w+)\s*([a-z ]+\s*,\n\n((\w+)\s*(\w+)\s*(\w+)))'
    issue_date_pattern = r'Issue\s*Date\s*(\d{2}\s*\d{2}\s*\d{2})'

    member_id_pattern = r'Member\s*ID:\s*(\w+)'
    name_pattern2 = r'Name:\s*(.+)'
    effective_date_pattern = r'Effective\s*Date:\s*(\d{1}/\d{1}/\d{4})'

    id_match = re.search(id_pattern, extracted_text, re.IGNORECASE)
    name_match = re.search(name_pattern, extracted_text, re.IGNORECASE)
    name_match1 = re.search(name_pattern_1, extracted_text, re.IGNORECASE)
    name_match2 = re.search(name_pattern_2, extracted_text, re.IGNORECASE)
    issue_date_match = re.search(issue_date_pattern, extracted_text, re.IGNORECASE)

    id_number = id_match.group(2) if id_match else None
    name = name_match.group(4) if name_match else None
    name1 = name_match1.group(4) if name_match1 else None
    name4 = name_match2.group(4) if name_match2 else None
    issue_date = issue_date_match.group(1) if issue_date_match else None

    member_id_match = re.search(member_id_pattern, extracted_text, re.IGNORECASE)
    name_match2 = re.search(name_pattern2, extracted_text, re.IGNORECASE)
    effective_date_match = re.search(effective_date_pattern, extracted_text, re.IGNORECASE)

    member_id = member_id_match.group(1) if member_id_match else None
    name2 = name_match2.group(1) if name_match2 else None
    effective_date = effective_date_match.group(1) if effective_date_match else None

    response_data = {
        "message": "Image decrypted and text extracted",
        "text": extracted_text
    }

    if id_number or name or name1 or name2 or issue_date:
        response_data["id_number"] = id_number
        response_data["name"] = name
        response_data["name"] = name1
        response_data["name"] = name4
        response_data["issue_date"] = issue_date

    if member_id or name2 or effective_date:
        response_data["member_id"] = member_id
        response_data["name"] = name2
        response_data["effective_date"] = effective_date

    response_data = {key: value for key, value in response_data.items() if value is not None}

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
