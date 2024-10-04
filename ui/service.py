import requests

base_url_database_prod = 'http://127.0.0.1:5000/'
base_url_pricer = 'http://127.0.0.1:5001/'
base_url_arm = 'http://127.0.0.1:5002/'
base_url_imm = 'http://127.0.0.1:5003/'

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
        response = requests.get(URL)
    elif direction == 'PUT':
        response = requests.put(URL, data=data)
    elif direction == 'POST':
        response = requests.post(URL, data=data)
    return URL, response

def call_arm(method_name, direction, data):
    URL = base_url_arm + method_name
    response = requests.get(URL, data=data)
    return URL, response

def call_imm(method_name, direction, data):
    if method_name not in ['displayAdjustedPrice']:
        return "Error", "Wrong method name for imm"
    URL = base_url_imm + method_name
    if direction == 'GET':
        response = requests.get(URL)
    elif direction == 'PUT':
        response = requests.put(URL, data=data)
    elif direction == 'POST':
        response = requests.post(URL, data=data)
    return URL, response


def call_api(method_name, direction, data):
    URL = base_url_database_prod + method_name
    response = requests.get(URL, data=data)
    return URL, response
