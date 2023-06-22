from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cur.fetchone()
    cur.close()

    if user:
        response = {'message': 'Пользователь найден', 'status': 'success'}
    else:
        response = {'message': 'Пользователь не найден', 'status': 'error'}

    return jsonify(response)

@app.route('/api/getAllLogs', methods=['GET'])
def getAllLogs():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM access_logs')
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cur.close()
    
    return jsonify(result)

@app.route('/api/getLogsFilterIP', methods=['GET'])
def getLogsFilterIP():
    data = request.get_json()
    ip = data['ip']

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM access_logs WHERE ip_address = '{ip}'")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cur.close()
    
    return jsonify(result)

@app.route('/api/getLogsFilterDate', methods=['GET'])
def getLogsFilterDate():
    data = request.get_json()
    start_date = data['start_date']
    end_date = data['end_date']

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM access_logs WHERE access_date BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59'")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cur.close()
    
    return jsonify(result)

@app.route('/api/getLogsFilterAll', methods=['GET'])
def getLogsFilterAll():
    data = request.get_json()
    ip = data['ip']

    start_date = data['start_date']
    end_date = data['end_date']
    
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM access_logs WHERE (access_date BETWEEN '{start_date} 00:00:00' AND '{end_date} 23:59:59') AND (ip_address = '{ip}')")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    result = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        result.append(row_dict)

    cur.close()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
