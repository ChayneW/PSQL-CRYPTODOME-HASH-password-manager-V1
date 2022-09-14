import hashlib
from hashlib import sha256
from base64 import b64encode, b64decode
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad


#MASTER = password123

'''Salt and Key of desired password to test hashing. Can save items into environment variables'''
master_salt = b'\xf2\x9a\xfc\\\x1e\xb6\xc6o\x99\x1dV\x8e\xe2\xe6]\xb0\xbc\xde\xd2\xef\xaf\x9a\xec\xaf\xf1\xdb9\xd9\xd0\x81\xac\x8b'

m_key = b'0\xe2\xee^\xdd\x87\xce\xb5\xfd\x0fYY\x8c\x92\x0c7\x1aV\xc6\xb2;\xf4Y0!\xaf\x9bs\x800\x8b\xc6'

salt = master_salt

'''Uses salt and key already saved to test password param to see if the salt and hash == desired password salt and hash.'''
def hash_password(password):
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    if m_key == new_key:
        print(f'input matches password')
        return True

    else:
        print(f"input doesn't match!!")
        return False


#cryptodome procedure:
'''Key needs to be a 16 byte string for Cryptodome Module to work...
    - Can save key into environment variable.'''

key = b'mysecretpassword'


'''Encryption string function():
    -Requires param to be a str, then funct converts to bytes and returns data.'''
def encrypt_string(password_plaintext):

        # Encryption:
    # data = b'secret message'

    data = f'{password_plaintext}'.encode('utf-8') 
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')

    return (iv, ct)


'''Decrypting string function():
    -  Requires data to be 'MEMORYVIEW' then converts to 'BYTES' '''
def decrypt_string(password, ciph_iv):#

    ct = password
    iv = ciph_iv

    # Decryption
    try:
        iv = b64decode(iv)
        ct = b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
 
        return pt

    except (ValueError, KeyError) as error:
        print(error)
        print('INCORRECT DECRYPTION.')


'''Change password with existing entries:'''
def change_password(password_plaintext):
    pass_changed = encrypt_string(password_plaintext)
    return pass_changed




