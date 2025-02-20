from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode, b64encode


# --------------------------------------------------------------------------- #

def appx_decrypt(encoded_data):
    try:
        key = "638udh3829162018".encode("utf8")
        iv = "fedcba9876543210".encode("utf8")
        decoded_data = b64decode(encoded_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error decrypting data: {str(e)}")


# --------------------------------------------------------------------------- #
def unpad2(s):
    return s[:-ord(s[len(s) - 1:])]

def utkarsh_decrypt(encrypted_string):
    try:
        key = b'%!$!%_$&!%F)&^!^'
        iv = b'#*y*#2yJ*#$wJv*v'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_bytes = b64decode(encrypted_string)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')
    except:
        data_key = b'%!$!%_$&!%F)&^!^'
        data_vector = b'#*y*#2yJ*#$wJv*v'
        encrypted_data = b64decode(encrypted_string)
        cipher = AES.new(data_key, AES.MODE_CBC, data_vector)
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data = unpad2(decrypted_data)
        decrypted_text = decrypted_data.decode('latin-1')
        return decrypted_text
        
# --------------------------------------------------------------------------- #        

def utkarsh_encrypt(plain_text):
    key = b'%!$!%_$&!%F)&^!^'
    iv = b'#*y*#2yJ*#$wJv*v'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return b64encode(cipher_text).decode()

# --------------------------------------------------------------------------- #

def encode_base64(data):
    encoded_bytes = b64encode(data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

# --------------------------------------------------------------------------- #


