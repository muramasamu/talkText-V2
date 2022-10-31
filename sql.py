import os

import mysql.connector as MySQLdb

def _con_open():
    # connection create
    connection = MySQLdb.connect(
        host=os.environ['railwayDBHost'],
        port=int(os.environ['railwayDBPort']),
        user=os.environ['railwayDBUser'],
        passwd=os.environ['railwayDBPasswd'],
        db=os.environ['railwayDB'])
    return connection

def _con_close(connection):
    # close
    connection.close()

def selectAll(sql):
    connection = _con_open()
    cursor = connection.cursor()

    # execute
    cursor.execute(sql)
    rows = cursor.fetchall()

    # close
    _con_close(connection)

    return rows

def selectOne(sql):
    connection = _con_open()
    #cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = connection.cursor(dictionary=True)

    # execute
    cursor.execute(sql)
    row = cursor.fetchone()

    # close
    _con_close(connection)

    return row

def update(sql):
    connection = _con_open()
    cursor = connection.cursor()

    # execute
    cursor.execute(sql)
    connection.commit()

    # close
    _con_close(connection)