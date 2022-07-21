import os
import psycopg2


def create_connection(database_url):
    def return_connection():
        try:
            if os.environ.get('MODE') == 'DEVELOPMENT':
                return psycopg2.connect(dbname=database_url['database'], user=database_url['user'], password=database_url['password'], host=database_url['host'])
            else:
                return psycopg2.connect(database_url, sslmode='require')
        except:
            print('This has gotten a bit hacky!')

    conn = return_connection()
    cur = conn.cursor()
    
    return {'conn': conn, 'cur':cur}

def close_connection(connection):
    connection['cur'].close()
    connection['conn'].close()

    return


def write_to_db(database_url, table, page_url, data=""):
    connection = create_connection(database_url)

    connection['cur'].execute(f"insert into {table} (page_url, data) values (%s, %s) on conflict do nothing", (page_url, data))
    connection['conn'].commit()

    close_connection(connection)

    return

def update_table(database_url, table, column, row, data):
    connection = create_connection(database_url)

    connection['cur'].execute(f"update {table} set {column}=%s where page_url = %s", (data, row))
    connection['conn'].commit()

    close_connection(connection)

    return

def read_from_db(database_url, table, column, row):
    connection = create_connection(database_url)

    connection['cur'].execute(f"select {column} from {table} where page_url = %s ", (row,))
    result = connection['cur'].fetchone()

    close_connection(connection)

    return result


def create_table(database_url, table, page_url):
    connection = create_connection(database_url)

    connection['cur'].execute(f"CREATE TABLE IF NOT EXISTS {table} (id SERIAL PRIMARY KEY, page_url TEXT UNIQUE, data TEXT)")
    connection['conn'].commit()

    write_to_db(database_url, 'web_pages', page_url)

    close_connection(connection)

    return
