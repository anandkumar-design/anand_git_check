from .settings import DATABASES
import psycopg2

def connection_data_student(request):
    conn = psycopg2.connect(
    database=DATABASES['student']['NAME'], 
    user=DATABASES['student']['USER'], 
    password=DATABASES['student']['PASSWORD'], 
    host=DATABASES['student']['HOST'], 
    port= DATABASES['student']['PORT']
    )
    return conn


def connection_data_defualt(request):
    conn = psycopg2.connect(
    database=DATABASES['default']['NAME'], 
    user=DATABASES['default']['USER'], 
    password=DATABASES['default']['PASSWORD'], 
    host=DATABASES['default']['HOST'], 
    port= DATABASES['default']['PORT']
    )
    return conn

def cursor_data(conn,query):
    cursor = conn.cursor()
    cursor.execute(query)
    col_name_data=col_name(cursor)
    data=cursor.fetchall()
    dict_data=dict_change_data(col_name_data,data)
    conn.close()
    return dict_data


def col_name(cursor):
    column_names = [desc[0] for desc in cursor.description]
    return column_names

def dict_change_data(col_name_data,data):
    new_data=[]
    for i in data:
        c={}
        for j in range(len(i)):
            c[col_name_data[j]]=i[j]
        new_data.append(c)
    return new_data
