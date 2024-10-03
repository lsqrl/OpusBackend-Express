import requests

base_url_database_prod = 'http://127.0.0.1:5000/'
base_url_pricer = 'http://127.0.0.1:5001/'
base_url_arm = 'http://127.0.0.1:5002/'
base_url_imm = 'http://127.0.0.1:5003/'

def get_pricer_method_list(base_url):
    response = requests.get(f'{base_url}/methods')
    if response.status_code == 200:
        method_list = response.json()
    else:
        print("Failed to get items:", response.status_code)
        method_list = []
    return method_list