import os
import requests
import json

base_url_database_prod = f"http://{os.getenv("BASE_URL")}:5000/"
base_url_pricer = f"http://{os.getenv("BASE_URL")}:5001/"
base_url_arm = f"http://{os.getenv("BASE_URL")}:5002/"
base_url_imm = f"http://{os.getenv("BASE_URL")}:5003/"
base_url_datafaker = f"http://{os.getenv("BASE_URL")}:5004/"

headers = {
    'Content-Type': 'application/json'
}

def get_service_method_list(base_url):
    response = requests.get(f'{base_url}/methods')
    if response.status_code == 200:
        method_list = response.json()
    else:
        print("Failed to get items:", response.status_code)
        method_list = []
    return method_list

def call_pricer(method_name, direction, data):
    if method_name not in ['calculateGreeks', 'calculatePrice']:
        return "Error", "Wrong method name for pricer"
    URL = base_url_pricer + method_name
    if direction == 'GET':
        response = requests.get(URL, headers=headers, params=data)
    elif direction == 'PUT':
        response = requests.put(URL, headers=headers, data=data)
    elif direction == 'POST':
        response = requests.post(URL, headers=headers, data=data)
    return URL, response.status_code, json.loads(response.content.decode('utf-8'))

def call_arm(method_name, direction, data):
    URL = base_url_arm + method_name
    response = requests.get(URL, headers=headers, data=data)
    return URL, response.status_code, json.loads(response.content.decode('utf-8'))

def call_imm(method_name, direction, data):
    if method_name not in ['displayAdjustedPrice']:
        return "Error", "Wrong method name for imm"
    URL = base_url_imm + method_name
    if direction == 'GET':
        response = requests.get(URL, headers=headers)
    elif direction == 'PUT':
        response = requests.put(URL, headers=headers, data=data)
    elif direction == 'POST':
        response = requests.post(URL, headers=headers, data=data)
    return URL, response.status_code, json.loads(response.content.decode('utf-8'))

def call_data_faker(method_name, direction, data):
    if method_name not in ['getNumbers', 'setValues']:
        return "Error", "Wrong method name for recommender FinData"
    URL = base_url_imm + method_name
    if direction == 'GET':
        response = requests.get(URL, headers=headers)
    elif direction == 'PUT':
        response = requests.put(URL, headers=headers, data=data)
    elif direction == 'POST':
        response = requests.post(URL, headers=headers, data=data)
    return URL, response.status_code, json.loads(response.content.decode('utf-8'))



def call_api(method_name, direction, data):
    URL = base_url_database_prod + method_name
    response = requests.get(URL, headers=headers, data=data)
    return URL, response.status_code, json.loads(response.content.decode('utf-8'))
