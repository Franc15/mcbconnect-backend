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

def get_customer_account(customer_id):
    accountUrl = os.environ.get('MCB_API_URL') + 'customers/' + customer_id + '/accounts'
    reponse  = requests.get(accountUrl, headers=headers)
    return reponse.json()[0]

def get_customer_transactions(customer_id):
    transactionUrl = os.environ.get('MCB_API_URL') + 'accounts/' + customer_id + '/transactions'
    response = requests.get(transactionUrl, headers=headers)
    return response.json()