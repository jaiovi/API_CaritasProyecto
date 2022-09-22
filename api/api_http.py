# Implementacion inicial de la API
from flask import Flask, jsonify, make_response, request
import mysql.connector
import json
import sys

mysql_params = {}
mysql_params['DB_HOST'] = '100.80.80.6'
mysql_params['DB_NAME'] = 'alumno04'
mysql_params['DB_USER'] = 'root'
mysql_params['DB_PASSWORD'] = 'user1234'

try:
    cnx = mysql.connector.connect(
        user=mysql_params['DB_USER'],
        password=mysql_params['DB_PASSWORD'],
        host=mysql_params['DB_HOST'],
        database=mysql_params['DB_NAME'], 
        auth_plugin='mysql_native_password'
        )
except Exception as e:
    print("Cannot connect to MySQL server!: {}".format(e))
    sys.exit()

def read_user_data(table_name, username):
    global cnx
    try:
        cnx.ping(reconnect=True, attempts=1, delay=3)
        cursor = cnx.cursor(dictionary=True)
        read = 'SELECT * FROM {} WHERE username = "{}"'.format(table_name, username)
        cursor.execute(read)
        a = cursor.fetchall()
        cnx.commit()
        cursor.close()
        return a
    except Exception as e:
        raise TypeError("read_user_data:%s" % e)


app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Shakira rocks!\n"

@app.route("/user")
def user():
    username = request.args.get('username', None)
    d_user = read_user_data('users', username)
    return make_response(jsonify(d_user))

if __name__ == '__main__':
    print ("Running API...")
    app.run(host='0.0.0.0', port=10210, debug=True) #el puerto se cambia por cada alumno
