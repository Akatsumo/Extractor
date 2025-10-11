import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode, b64encode

ArrayKey = "JSFGKiZeJClfKiUzZiZCKw=="
Arrayvector = "IyokREp2eXcydyUhXy0kQA=="

def gen_value(base, source):
    ref = b64decode(source).decode('utf-8')
    combined = base[:16]
    return "".join(ref[int(c)] for c in combined)

def gen_key_iv(de, id=None):
    if id:
        base = id + de
    else:
        base = de
    key = gen_value(base, ArrayKey)
    iv = gen_value(base, Arrayvector)
    return key, iv
    
# --------------------------------------------------------------------------- #

def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.DecodeError as e:
        return f"Invalid token: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

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
        
def decrypt(key, iv, encoded_data):
    try:
        if ':' in encoded_data:
            encoded_data = encoded_data.split(':')[0]
        key = key.encode("utf8")
        iv = iv.encode("utf8")
        decoded_data = b64decode(encoded_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error decrypting data: {str(e)}\nData: {encoded_data}")

def encrypt(key, iv, plaintext):
    try:
        key = key.encode("utf8")
        iv = iv.encode("utf8")
        padded_data = pad(plaintext.encode("utf-8"), AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(padded_data)
        encoded_data = b64encode(encrypted_data).decode('utf-8')
        return encoded_data + ':'
    except Exception as e:
        raise ValueError(f"Error encrypting data: {str(e)}")
# --------------------------------------------------------------------------- #
_key = b'%!$!%_$&!%F)&^!^'
_iv = b'#*y*#2yJ*#$wJv*v'

def utkarsh_encrypt(plain_text: str) -> str:
    try:
        cipher = AES.new(_key, AES.MODE_CBC, _iv)
        padded_text = pad(plain_text.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return b64encode(encrypted).decode('utf-8')
    except Exception as e:
        print(plain_text)
        raise ValueError(f"Error encrypting data: {str(e)}")

def utkarsh_decrypt(encrypted_text: str) -> str:
    try:
        if ':' in encrypted_text:
            encrypted_text = encrypted_text.split(':')[0]
        cipher = AES.new(_key, AES.MODE_CBC, _iv)
        decoded_encrypted = b64decode(encrypted_text)
        decrypted = cipher.decrypt(decoded_encrypted)
        return unpad(decrypted, AES.block_size).decode('utf-8')
    except Exception as e:
        print(encrypted_text)
        raise ValueError(f"Error decrypting data: {str(e)}")
# --------------------------------------------------------------------------- #

def encode_base64(data):
    encoded_bytes = b64encode(data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

# --------------------------------------------------------------------------- #

def decode_base64(data):
    decoded_bytes = b64decode(data)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string
