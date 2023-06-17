import requests
from dotenv import load_dotenv
import os

headers = {
    'Authorization': 'Bearer ' + os.environ.get('MCB_API_TOKEN'),
}

def get_customer_info(customer_id):
    url = os.environ.get('MCB_API_URL') + 'customers/' + customer_id 
    resp = requests.get(url, headers=headers)
    return resp.json()
