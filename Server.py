from flask import Flask, request
import pymysql
import lang_en as lang
import util
import time
from util import check_user_credentials, generate_hash, check_input_data


app = Flask(__name__)


@app.route('/sign_up', methods=['POST'])
def sign_up():
    """
    this is a decorator function which firstly checks if user's
    input structure is valid. then checks if user's data exists in
    database or not. then tries to insert entered data into database.

    :return: returns 400 status code and a message if data is invalid.
    otherwise a 200 status code and a different message will be returned
    :rtype: string, http status code
    """
    data = request.get_json()
    username = list(data)[0]
    if check_input_data(data, username) is True:
        password = generate_hash(data, username)
        if check_user_credentials(username, password, cursor) is False:
            cursor.execute('insert into information (username, password) values (%s, %s)', (username, password))
            conn.commit()
            return lang.Signup_success, 200
        else:
            return lang.Username_unavailable, 400
    return lang.User_Data_Input_Invalid, 400


@app.route('/login', methods=['POST'])
def login():
    """
    this is a decorator function which firstly checks if user's
    input structure is valid. then checks if user's data exists in
    database or not.

    :return: returns 400 status code and a message if data already exists
    in database. otherwise a 200 status code and a different message will
    be returned.
    :rtype: string, http status code
    """
    data = request.get_json()
    username = list(data)[0]
    password = generate_hash(data, username)
    if check_input_data(data, username) is True:
        if check_user_credentials(username, password, cursor) is True:
            return lang.Login_success, 200
        else:
            return lang.User_Data_Input_Invalid, 400
    return lang.User_Data_Input_Invalid, 400


@app.route('/forgotten_password', methods=['POST'])
def forgotten_password():
    """
    this is a decorator function which firstly checks if user's
    input structure is valid. then checks if user's data exists in
    database or not. then tries to update password in database.

    :return: returns 400 status code and a message if data is invalid
    otherwise a 200 status code and a different message will be returned
    :rtype: string, http status code
    """
    data = request.get_json()
    username = list(data)[0]
    if check_input_data(data, username) is True:
        password = generate_hash(data, username)
        if check_user_credentials(username, password, cursor) is True:
            cursor.execute('update information set password = %s where username = %s', (password, username))
            conn.commit()
            return lang.Update_password, 200
    return lang.User_Data_Input_Invalid, 400


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        password='root',
        database='users',
        port=3306,
        user='root'
    )
    cursor = conn.cursor()
    app.run()
