import os
import psycopg2


def create_connection(database_url):
    def return_connection():
        try:
            if os.environ.get('MODE') == 'DEVELOPMENT':
                print('Development Database In Use - Dev db connection created - DB, line 9')
                return psycopg2.connect(dbname=database_url['database'], user=database_url['user'], password=database_url['password'], host=database_url['host'])
            else:
                print('Production database in use - Production connection created - DB, line 12')
                return psycopg2.connect(database_url, sslmode='require')
        except:
            print('Problem creating database connection')

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


def create_table(database_url, table, page_url=None):
    connection = create_connection(database_url)

    connection['cur'].execute(f"CREATE TABLE IF NOT EXISTS {table} (id SERIAL PRIMARY KEY, page_url TEXT UNIQUE, data TEXT)")
    connection['conn'].commit()

    close_connection(connection)

    if page_url is None:
        return

    write_to_db(database_url, 'web_pages', page_url)

    return
