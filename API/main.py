import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
import json


@app.route('/user/add', methods=['POST'])
def create_user():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _json = request.json
        _username = _json['username']
        _email = _json['email']
        _password = _json['password']
        _city = _json['city']
        # validate the received values
        if _username and _email and _password and request.method == 'POST':
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "INSERT INTO users(username, email, password, city) VALUES(%s, %s, %s, %s)"
            data = (_username, _email, _hashed_password, _city)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify({'status': 200, 'message': 'User added successfully!'})
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/list')
def list_users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT username, email, city FROM users")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/<string:username>', methods=['POST'])
def get_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT username, email, city FROM users WHERE username=%s", username)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/update', methods=['PUT'])
def update_user():
    try:
        _json = request.json
        _username = _json['username']
        _email = _json['email']
        _city = _json['city']
        # validate the received values
        if _username and _email and request.method == 'PUT':
            sql = "UPDATE users SET email=%s, city=%s WHERE username=%s"
            data = (_email, _city, _username)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify({'status': 200, 'message': 'User updated successfully!'})
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/delete/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=%s", (username,))
        conn.commit()
        resp = jsonify({'status': 200, 'message': 'User deleted successfully!'})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/login', methods=['POST'])
def user_login():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        if _username and _password and request.method == 'POST':
            _hashed_password = generate_password_hash(_password)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM users WHERE username=%s, password=%s"
            data = (_username, _hashed_password)
            cursor.execute(sql, data)
            row = cursor.fetchone()
            resp = jsonify(row)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()
