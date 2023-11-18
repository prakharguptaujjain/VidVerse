import mysql.connector as mc

user = 'root'
password = '1234567890'
host = 'localhost'
database = 'users_db'

myConnection = mc.connect(host = host, user = user, password = password, database = database)
cur = myConnection.cursor()


# current tables: users, videos, click_through_search, click_through_ad

def insert(table, data):
    """
    Insert data into table
    """
    cur.execute(f"describe {table}")
    res = cur.fetchall()
    cols = [i[0] for i in res if i[0] in data]
    datatype = [i[1] for i in res if i[0] in data]
    query = f"INSERT INTO {table} ("
    for i in cols:
        query += f"{i},"
    query = query[:-1]
    query += ") VALUES ("

    for i in cols:
        if 'int' not in datatype[cols.index(i)]:
            query += f"'{data[i]}',"
        else:
            query += f"{data[i]},"
    
    query = query[:-1]
    query += ")"
    cur.execute(query)
    myConnection.commit()
    return

def search(table, data = None):
    """
    Search data from table
    current tables: users, videos, click_through_search, click_through_ad
    """
    if data == None:
        cur.execute(f"SELECT * FROM {table}")
        res = cur.fetchall()
        return res
    
    cur.execute(f"describe {table}")
    res = cur.fetchall()
    cols = [i[0] for i in res if i[0] in data]
    datatype = [i[1] for i in res if i[0] in data]
    query = f"SELECT * FROM {table} WHERE "
    for i in cols:
        if 'int' not in datatype[cols.index(i)]:
            query += f"{i} = '{data[i]}' AND "
        else:
            query += f"{i} = {data[i]} AND "
    query = query[:-4]
    cur.execute(query)
    res = cur.fetchall()
    return res

def run_query(query):
    cur.execute(query)
    res = cur.fetchall()
    if res != []:
        return res

def remove(table, data = None):
    """
    Remove data from table
    """
    if data == None:
        cur.execute(f"DELETE FROM {table}")
        myConnection.commit()
        return

    cur.execute(f"describe {table}")
    res = cur.fetchall()
    cols = [i[0] for i in res if i[0] in data]
    datatype = [i[1] for i in res if i[0] in data]
    query = f"DELETE FROM {table} WHERE "
    for i in cols:
        if 'int' not in datatype[cols.index(i)]:
            query += f"{i} = '{data[i]}' AND "
        else:
            query += f"{i} = {data[i]} AND "
    query = query[:-4]
    cur.execute(query)
    myConnection.commit()
    return