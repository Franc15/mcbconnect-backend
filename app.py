from flask import Flask, request, jsonify
from urllib.request import urlopen
from dotenv import load_dotenv
import os
import requests
from api.service import get_customer_info, get_customer_transactions, get_customer_account
from flask_cors import CORS
from api.utils import connect_to_db
from api.auth import login_user
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/v1')
def get_root():
    return jsonify({'message': 'Hello world from MCB Connect!'})

@app.route('/api/v1/customers')
def get_customers():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    return jsonify(rows)


# authentication route
@app.route('/api/v1/login', methods=['POST'])
def auth():
    # get id and password from user 
    data = json.loads(request.data)
    id = data.get('id',None)
    enterprise_id = data.get('enterprise_id')
    password = data.get('password')

    # check if user exists in selected enterprise
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE employee_id = '%s' AND enterprise_id= '%s'" % (id, enterprise_id))
    rows = cur.fetchone()

    if rows is None:
        return jsonify({
            'success': False, 
            'message': 'User does not exist in selected enterprise.'
            })
    
    # login_user(id, password)
    return jsonify({
        'success': True, 
        'message': 'User logged in success.'
        })

@app.route('/api/v1/customers/<string:nic>/check', methods=['GET'])
def get_customer(nic):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id = '%s'" % nic)
    rows = cur.fetchone()
    if rows is None:
        return jsonify({
            'success': False, 
            'message': 'Customer does not have an MCB Account.'
        })
    return jsonify({'success': True, 'data': rows})


@app.route('/api/v1/requests/<string:employee_id>', methods=['GET'])
def get_requests(employee_id): 

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests WHERE employee_id = '%s'" % employee_id)
    rows = cur.fetchall()

    if rows == [] or rows is None:
        return jsonify({
            'success': False, 
            'message': 'No requests found.'
        })
    
    results = []

    for item in rows:
        result = dict()
        cur.execute("SELECT * FROM customers WHERE customer_id = '%s'" % item[1])
        customer_row = cur.fetchone()
        if customer_row is None:
            return
        user_info = get_customer_info(customer_row[1])
        print(user_info)
        result['Nic'] = item[1]
        result['Name'] = user_info['Customer']['FirstName'] + " " + user_info['Customer']['LastName']
        result['dateRequested'] = item[2]
        result['status'] = item[3]
        results.append(result)
    
    return jsonify({'success': True, 'data': results})
    

# search customer by nic
@app.route('/api/v1/customers/<string:nic>')
def get_api(nic):
    nic = request.view_args['nic']
    mcb_customer_id = None
    conn = connect_to_db()
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
    return jsonify(user_dict)

# post endpoint
@app.route('/api/v1', methods=['POST'])
def post_api():
    req_data = request.get_json()
    return jsonify(req_data)

app.run()