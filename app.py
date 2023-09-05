import os
import base64
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import pytesseract
import cv2
import numpy as np
import re
import pattern_utils

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
    cleaned_text = re.sub(r'[^\w\s]', '', extracted_text)
    cleaned_text = re.sub(r'\n\n', '\n', cleaned_text)
    splitted_text = cleaned_text.split("\n")

    matches = pattern_utils.search_patterns(cleaned_text)

    id_number = matches[1].group(2) if matches[0] else None
    name = matches[2].group(4) if matches[2] else None
    issue_date = matches[3].group(2) if matches[3] else None

    member_id = matches[5].group(1) if matches[4] else None
    name2 = matches[6].group(1) if matches[6] else None
    effective_date = matches[7].group(1) if matches[7] else None

    # specifics patterns
    specific_member_id = matches[8].group(0) if matches[8] else None

    document_type3 = matches[9].group(0) if matches[9] else None
    document_type4 = matches[10].group(0) if matches[9] else None
    document_type5 = matches[11].group(0) if matches[9] else None
    name3 = matches[12].group(3) if matches[12] else None
    document_type6 = matches[13].group(0) if matches[13] else None
    document_type7 = matches[14].group(0) if matches[14] else None
    document_type8 = matches[15].group(0) if matches[15] else None

    response_data = {
        "cleaned_text": cleaned_text,
        "text": extracted_text,
        "splitted_text": splitted_text,
    }

    if id_number and name and issue_date:
        response_data["id_number"] = id_number
        response_data["name"] = name
        response_data["issue_date"] = issue_date

    if member_id and name2 and effective_date:
        response_data["member_id"] = member_id
        response_data["name"] = name2
        response_data["effective_date"] = effective_date

    if specific_member_id:
        response_data["member_id"] = "true"
    else:
        response_data["member_id"] = "false"

    if document_type3 and document_type4 and document_type5:
        response_data["document_type"] = (document_type3 + " " + document_type4 + " " + document_type5)
        response_data["id_number"] = id_number
        response_data["name"] = name3
        response_data["issue_date"] = issue_date

    if document_type6 and document_type7 and document_type8:
        response_data["document_type"] = document_type6 + " " + document_type7 + " " + document_type8

    response_data = {key: value for key, value in response_data.items() if value is not None}

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
