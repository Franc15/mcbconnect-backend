from flask import Flask, request, jsonify
from urllib.request import urlopen
import psycopg2
from dotenv import load_dotenv
import os
import requests

load_dotenv()

headers = {
    'Authorization': 'Bearer ' + os.environ.get('MCB_API_TOKEN'),
}

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(host="localhost", database="mcbconnect-db", user="postgres", password="franc123")
    return conn

@app.route('/api/v1')
def get_root():
    return jsonify({'message': 'Hello world from MCB Connect!'})

@app.route('/api/v1/customers')
def get_customers():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/api/v1/<test>')
def get_test(test):
    test = request.view_args['test']
    request = requests.get('http://localhost:5000/api/v1/customers', )
    print(request.json())
    return jsonify({'message': 'Hello world from MCB Connect! ' + test})



# search customer by nic
@app.route('/api/v1/customers/<string:nic>')
def get_api(nic):
    nic = request.view_args['nic']
    mcb_customer_id = None
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id = %s", (nic,))
    row = cur.fetchone()
    if row is None:
        return jsonify({'message': 'Customer not found!'})
    else:
        mcb_customer_id = row[1]
    
    url = os.environ.get('MCB_API_URL') + 'customers/' + mcb_customer_id 
    resp = requests.get(url, headers=headers)

    # retreieve customer id from the response
    user_dict = dict()
    user_dict['CustomerId'] = resp.json()['Customer']['CustomerId']
    user_dict['CustomerStatus'] = resp.json()['Customer']['CustomerStatus']
    user_dict['Title'] = resp.json()['Customer']['Title']
    user_dict['FirstName'] = resp.json()['Customer']['FirstName']
    user_dict['LastName'] = resp.json()['Customer']['LastName']
    user_dict['DateOfBirth'] = resp.json()['Customer']['DateOfBirth']
    user_dict['preferredLanguage'] = resp.json()['Customer']['preferredLanguage']
    user_dict['Gender'] = resp.json['Customer']['Gender']
    user_dict['PhoneNumber'] = resp.json()['Customer']['PhoneNumber']
    user_dict['StreetName'] = resp.json()['Customer']['StreetName']
    user_dict['City'] = resp.json()['Customer']['City']
    user_dict['Country'] = resp.json()['Customer']['Country']
    user_dict['PostalCode'] = resp.json()['Customer']['PostalCode']
    user_dict['JobTitle'] = resp.json()['Customer']['JobTitle']
    user_dict['Salary'] = resp.json()['Customer']['Salary']
    user_dict['EmployerName'] = resp.json()['Customer']['EmployerName']

    resp2 = requests.get(os.environ.get('MCB_API_URL') + 'customers/' + user_dict['CustomerId'] + '/accounts', headers=headers)
    user_dict['Accounts'] = resp2.json()
    return jsonify(user_dict)

# post endpoint
@app.route('/api/v1', methods=['POST'])
def post_api():
    req_data = request.get_json()
    return jsonify(req_data)


app.run()