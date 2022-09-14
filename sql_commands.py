import psycopg2
from psycopg2 import OperationalError
from hash_and_encrypt import encrypt_string, decrypt_string, change_password


create_users_table = '''
CREATE TABLE IF NOT EXISTS accounts (
    password BYTEA,
    cipher_iv BYTEA,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    url VARCHAR(255),
    app_name VARCHAR(255)
    )
    '''


'''Funct to create SQL Connection for sql queries. 
    - Requires PSQL Database, user, password, host and port data: '''
def create_connection():
    try:
        connection = psycopg2.connect(database='password_manager', user='chaynewhite', password='Abcd1234', host='localhost', port='5432')
        print("Connection to PostgreSQL DB successful\n")

    except OperationalError as e:
        print(f"The error '{e}' occurred.")
    return connection


'''Funct to create tables, insert records, modify records, and delete records in postgreSQL:'''
def execute_query(query):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully\n")

    except OperationalError as e:
        print(f'The error "{e}" occurred')


'''Creates table in PSQL if tables doesn't exist.'''
def create_table():
    execute_query(create_users_table)


'''Funct to show all records.'''
def show_all_records():
    print('tapping into show records:')
    
    connection = create_connection()
    cursor = connection.cursor()
    post_query_all = 'SELECT * from accounts'
    cursor.execute(post_query_all)
    records = cursor.fetchall()

    print('Order is as listed:\nPassword | Email | Username | URL | App_name :\n')

    for item in records:

        item_ci = item[0]
        item_pass = item[1]

        #DATA CHECK:
        # print(f'In showing records()\nitem_pass: {type(item_pass)}, item_ci: {type(item_ci)}')
        # print(f'converted bytes: {bytes(item_pass)}, {bytes(item_ci)}')

        conv = decrypt_string(item_pass, item_ci)

        print(f"{conv} | {item[2]} | {item[3]} | {item[4]} | {item[5]}\n")


'''Funct to insert entries:
    - Requires password, email, username, url, app_name data.
    - Takes data, call encryption, then sql query to save data to database.'''
def insert_entry(password, email, username, url, app_name):

    print(f'tapping into insert_entry:\n')

    connection = create_connection()
    password, email, username, url, app_name = password, email, username, url, app_name
    print(f'password: {password}, email: {email}, username:{username}, url:{url},app_name: {app_name}')

    # encryption: PASSWORD: STR ->
    password_t = encrypt_string(password)
    print(password_t)

    password_c = password_t[0]
    cipher_iv = password_t[1]

    # #DATA CHECK
    # print(f"Here's the crypted strings and iv:\npassword_c:{password_c},\npassword_iv:{cipher_iv}")

    connection.autocommit = True
    cursor = connection.cursor()

    insert_passwords_entry = '''INSERT INTO accounts (password, cipher_iv, email, username, url, app_name) VALUES (%s, %s, %s, %s, %s, %s)'''
    print(insert_passwords_entry)

    print('''INSERT INTO accounts (password, cipher_iv, email, username, url, app_name) VALUES ({}, {}, {}, {}, {}, {})'''.format(password_c, cipher_iv, email, username, url, app_name))


    #real sql command:
    record_to_insert = (password_c, cipher_iv, email, username, url, app_name)#('test3test123', 'stest@gmail.com', 'stest_acct', 'www.snapchat.com', 'snapchat')
    cursor.execute(insert_passwords_entry, record_to_insert)

    connection.commit()
    print('entry added.\n')

    # SHOWS ALL RECORDS 
    # show_all_records()
    

'''Funct that taps into sql database: 
    - Takes string data as sql queries, search database, retrieve's data into a tuple, loops through data, decrypts password then shows in console. '''
def find_entry(param):
    #param = str: COLUMNS: Password | Email | Username | URL | App_name : ->
    try:
        print(f'tapping into finder:\n')
        
        detail = input("What's the name of social you want to search by?(If using simple SQL, just press 'enter' to skip.) ").lower()
        
        if len(detail) > 0: 
            '''Specific Search:'''
            insert_search = '''SELECT * from accounts WHERE {} LIKE '%{}%' '''.format(param, detail)

        else:
            '''General Search:'''
            insert_search = '''SELECT {}, password, cipher_iv, app_name from accounts'''.format(param)

        connection = create_connection()
        cursor = connection.cursor()

        post_query_all = 'SELECT * from accounts'
        cursor.execute(post_query_all)

        print(f'insert_search -> {insert_search}:\n')
    
        cursor.execute(insert_search)

        result = cursor.fetchall()

        try:
            for item in result:
                '''using this to check TUPLE for both positions to then assign, or will skip..'''
                if memoryview in list(map(type, item)):

                    ''' sorting funct() to put memoryview in positions to be retrieved...'''                    
                    res = sorted(item, key = lambda ele: isinstance(ele, memoryview))

                    # MEMORYVIEW Items:
                    item_p = res[-1]
                    item_c = res[-2]

                    # DECRYPT HERE:
                    pass_d = decrypt_string(item_p, item_c)

                    print(f"Here's your account data: {res[0]} | {res[1]} | {pass_d}\n")

                else:
                    print('not reading memoryview')
                    pass
            
        except TypeError as error:
            print(error)

    except psycopg2.Error as error:
        print(error)


'''Funct that takes strings as SQL queries:
    - Uses sql queries to select database data,saves any new data.
    - PASSWORDS: taps into selected data passwords, calls encryption() to re-encrypt new password.
    - Supports sql custom queries for multiple data changes. '''
def update_entry(param):
    print('tapping into updater:\n')

    sql_custom = input(f"If a sql custom query for {param}, write here, *** Dont forget (''). NO PASSWORDS\n(else type 'n'...) -> ")
    print(sql_custom)

    if sql_custom != 'n':
        try:
            # take multiple columns, except password:
            record_to_change = '''UPDATE accounts SET {} WHERE app_name='{}';'''.format(sql_custom, param)
        
        except psycopg2.Error as error:
            print(error)

    else:
        # Individual record:
        record_column = input(f'which column to change? COLUMNS: Password | Email | Username | URL | App_name : -> ')
        record_detail = input(f'what data would you like to insert into {record_column}? -> ')
        
        #password encryption process:
        if 'password' in record_column:
            print(record_column)
            pass_change = change_password(record_detail)

            # check to make sure values are in right slot:
            pass_change_en = pass_change[0]
            pass_change_ci = pass_change[1]
            
            print(f"password enc: {type(pass_change_en), pass_change_en}\npass_cipher: {type(pass_change_ci), pass_change_ci}\n")

            #PASSWORD/Cipher_IV ONLY:
            record_to_change = '''UPDATE accounts SET password='{}',cipher_iv='{}' WHERE app_name='{}';'''.format(pass_change_en, pass_change_ci, param)
            print(record_to_change)

        else:
            record_to_change = '''UPDATE accounts SET {}='{}' WHERE app_name='{}';'''.format(record_column, record_detail, param)

    print(f"Here's your record to change: {record_to_change}")

    try:
        execute_query(record_to_change)

    except psycopg2.Error as error:
        print(error)

    # SHOW RECORDS!
    show_all_records()


'''Funct that takes string data as sql queries:
    - Uses sql command to delete specific data. 
    - Supports customized sql queries.'''
def delete_entry(param):
    print('tapping into deleter:\n')

    if param == '1':
        select_column = input("Which 'column' to select from: -> ").lower()
        select_detail = input("Which data to search from: -> ").lower()
        custom_sql_delete = '''DELETE FROM accounts WHERE {} like '{}%';'''.format(select_column, select_detail)
        
        print(custom_sql_delete)

    elif param == '2':
        select_app = input("Which 'app_name' to select from: -> ").lower()
        custom_sql_delete = '''DELETE FROM accounts WHERE app_name='{}';'''.format(select_app)
        
        print(custom_sql_delete)

    execute_query(custom_sql_delete)

    show_all_records()