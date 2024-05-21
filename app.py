from flask import Flask, request
import os
import socket
import json
import mysql.connector

app = Flask(__name__)


@app.route('/')
def hello():
    """Дополнить возврат в html значение счетчика (счетчик инициализируется в момент запуска приложения"""
    name = os.getenv("NAME", 'world')
    hostname = socket.gethostname()

    html = f"""
    <h1>Hello, {name}!</h1> 
    <b>Hostname:</b> {hostname} <br>
    """
    return html


@app.route('/stat')
def stat():
    """
    Прототип функции, возвращающей значение счетчика
    """

    import datetime

    headers = str(request.headers['User-Agent'])

    html = """
        <b>Datetime</b>: {d} <br>
        <b>Client User-Agent</b>: {req_headers}"""

    return html.format(d=datetime.datetime.now(), req_headers=headers)


@app.route('/backdoor')
def backdoor():
    """
    Название не придумал
    """

    html = """
        <p>Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. 
        Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        
        <img src="https://avatars.dzeninfra.ru/get-zen_doc/1705407/pub_5e00c4782fda8600b089c24a_5e00c48cfe289100b190f9c1/scale_1200">
        """
    
    return html



@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(host="mysqldb",
                                   user="root",
                                   password="pow@red1")
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(host="mysqldb",
                                   user="root",
                                   password="pow@red1",
                                   database="inventory")
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
   
    cursor.close()

    return 'init database'


@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(host="mysqldb",
                                   user="root",
                                   password="pow@red1",
                                   database="inventory")
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM widgets")

    row_headers = [x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route('/addlog')
def add_logs():
    """
    Позволяет вводить данные о посещении
    """

    mydb = mysql.connector.connect(host="mysqldb",
                                   user="root",
                                   password="pow@red1")
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(host="mysqldb",
                                   user="root",
                                   password="pow@red1",
                                   database="inventory")
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS addlog")
    cursor.execute("CREATE TABLE logs (datetime VARCHAR(255), client_info VARCHAR(255))")
    cursor.close()


    return 'add_log'


@app.route('/logs')
def get_logs():
    """
    Извлекает данные из таблицы logs
    
    """
    mydb = mysql.connector.connect(host="mysqldb",
                                   user="root",
                                   password="pow@red1",
                                   database="inventory")

    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM logs")

    row_headers = [x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
