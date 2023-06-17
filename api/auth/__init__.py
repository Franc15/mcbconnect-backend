from api.utils import connect_to_db
from flask import jsonify
import hashlib
import jwt

# Dummy data
rightEnterpriseId = 'mcb9876'
wrongEnterpriseId = 'absa9876'

rightEmployeeId = 'jus1234'
wrongEmployeeId = 'fran1234'

rightEmployeePassword = 'wamswa4321'
wrongEmployeePassword = 'wamswa9876'


# Method to login the user
def login_user(id, password):

    # check if id is null
    if id is None:
        print({'error': 'Invalid login'})
        return jsonify({
            'success' : False,
            'message' : 'Id field cannot be empty.'
        })
    
    # check if password is null
    if password is None:
        print({'error': 'Password is null'})
        return jsonify({
            'success' : False,
            'message' : 'Password field cannot be empty.'
        })
    
    # check if id exists in database
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (id,))
    row = cur.fetchone()

    if row is None:
        print({'error': 'User does not exist'})
        return jsonify({
            'success' : False,
            'message' : 'User does not exist in the database'
        })
    
    password_from_db = row[1]
    
    # Hash the input password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    if hashed_password != password_from_db:
        print({'error': 'Invalid password'})
        jsonify({'success': False, 'message': 'Password do not match!' })
        return
    
    jwt_token = jwt.encode(payload={
            'user_id': row[0],
            'user_role': row[2]
        }, key=password, algorithm="HS256")
    
    print({'success': False, 'message': 'úser loggen in success', 'token': jwt_token})
    return jsonify({
        'success': True,
        'token': jwt_token
    })


# Method call
# loginUser(rightEnterpriseId, rightEmployeeId, rightEmployeePassword)
# loginUser(wrongEnterpriseId, wrongEmployeeId, wrongEmployeePassword)