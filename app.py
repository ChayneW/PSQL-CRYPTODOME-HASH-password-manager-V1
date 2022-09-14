from menu_choices import add_account_entry, find_account_entry, menu_outline, replace_account_entry, delete_account_entry
import sys
from hash_and_encrypt import hash_password
from sql_commands import create_table


def exit_program():
    sys.exit()


entry = input('Password: ') 

check_entry = hash_password(entry)

if check_entry == False:
    print('Please run again for access.')
    sys.exit()

else:
    IN_USE = True

    while IN_USE:
        
        '''Establishes connection to psql:
            - Provide your own data for database connection.  '''
        # connection = create_connection('password_manager','chaynewhite','Abcd1234','localhost','5432')

        # Creates database if none created, if one available, will skip.
        create_table()

        menu_outline()

        choice = int(input('what your choice? '))

        if choice == 1:
            add_account_entry()
              
        elif choice == 2:
            find_account_entry()
        
        elif choice == 3:
            replace_account_entry()

        elif choice == 4:
            delete_account_entry()
        
        elif choice == 0:
            exit_program()

