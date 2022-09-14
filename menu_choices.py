from sql_commands import find_entry, insert_entry, update_entry, delete_entry, show_all_records

def menu_outline():
    print('Please choose from the following:')
    print("'1' to add accounts...")
    print("'2' to find accounts...")
    print("'3' to replace accounts...")
    print("'4' to delete accounts...")
    print("'0' to close program...\n")


def add_account_entry():
    param = input("Press 'q' to go back, else press 'c' to continue: ").lower()
    if param == 'q':
        pass

    elif param == 'c':
        app_name = input("What's the app name: -> ")
        email = input("What's email address: -> ")
        username = input("What's the username: -> ")
        url = input("What's the url: -> ")
        password = input("What's the password: -> ")

        print(app_name, email, username, url, password)

        # SQL -> key inserted
        insert_entry(password, email, username, url, app_name)

    else:
        print('\nPlease choose from the designated options.\n')
        pass


def find_account_entry():
    param = input("what parameter do you want to search by?\n*** WILL automatically add app_name ***\n'q' to go back.\nCOLUMNS: Password | Email | Username | URL | App_name : -> ").lower()
    if param == 'q':
        pass
    else:
        # SQL -> key inserted
        find_entry(param)


def replace_account_entry():
    #SHOW RECORDS:
    show_all_records()

    param = input("what app_name data to change?\n'q' to go back. -> ").lower()
    if param == 'q':
        pass
    else:
        update_entry(param)


def delete_account_entry():
    #SHOW RECORDS:
    show_all_records()

    param = input("'1' for custom search, '2' to search by app_name, 'q' to go back. -> ").lower()
    if param == 'q':
        pass
    else:
        delete_entry(param)