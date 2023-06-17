from flask import Flask, request, jsonify
from urllib.request import urlopen
import psycopg2
from dotenv import load_dotenv
import os
import requests
from api.service import get_customer_info, get_customer_transactions, get_customer_account

load_dotenv()

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
    
    resp = get_customer_info(mcb_customer_id)

    # retreieve customer id from the response
    user_dict = dict()
    user_dict['Customer'] = resp['Customer']

    # Get user account
    user_dict['Account'] = get_customer_account(mcb_customer_id)

    # Get user transactions
    user_dict['Transaction'] = get_customer_transactions(user_dict['Account']['AccountNumber'])

    # resp2 = requests.get(os.environ.get('MCB_API_URL') + 'customers/' + user_dict['Customer']['CustomerId'] + '/accounts', headers=headers)
    # user_dict['Account'] = resp2.json()[0]

    # resp3 = requests.get(os.environ.get('MCB_API_URL') + 'accounts/' + user_dict['Account']['AccountNumber'] + '/transactions', headers=headers)
    # user_dict['Transaction'] = resp3.json()

    return jsonify(user_dict)

# post endpoint
@app.route('/api/v1', methods=['POST'])
def post_api():
    req_data = request.get_json()
    return jsonify(req_data)


app.run()