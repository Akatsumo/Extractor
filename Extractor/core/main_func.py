import time
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode, b64encode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# --------------------------------------------------------------------------- #

def get_time(duration_seconds):
    if duration_seconds < 60:
        elapsed = str(round(duration_seconds)) + " seconds"
    elif duration_seconds < 3600:
        duration_minutes = int(duration_seconds // 60)
        remaining_seconds = duration_seconds % 60
        elapsed = str(duration_minutes) + " minutes " + str(round(remaining_seconds)) + " seconds"
    else:
        duration_hours = int(duration_seconds // 3600)
        remaining_minutes = int((duration_seconds % 3600) // 60)
        remaining_seconds = duration_seconds % 60
        elapsed = str(duration_hours) + " hours " + str(remaining_minutes) + " minutes " + str(round(remaining_seconds)) + " seconds"
    
    return elapsed
    
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

def decode_base64(encoded_data):
    decoded_bytes = b64decode(encoded_data)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

# --------------------------------------------------------------------------- #
allDics = {}
PER_PAGE = 15

def get_page(page: int, appNameDict, DictID="Dic1", back_data="home_", query=None, appx=False, page_row=3):
    keys = list(appNameDict.keys())  
    start = page * PER_PAGE
    end = start + PER_PAGE
    allDics[DictID] = appNameDict
    
    if start >= len(keys) and query:
        return query.answer("🚫 No more pages", show_alert=True)
        
    buttons = []
    row = []
    
    if appx:
        buttons.append([InlineKeyboardButton("🔐 Manual Login", callback_data="manual_login")])
        
    for i, key in enumerate(keys[start:end], 1):
        row.append(InlineKeyboardButton(appNameDict[key]["name"], callback_data=f"autoCallback#{key}"))
        if i % page_row == 0:  
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("＜ ᴘʀᴇᴠ", callback_data=f"page_{DictID}_{page-1}"))
    nav.append(InlineKeyboardButton("↺ ʙ ᴀ ᴄ ᴋ ↻", callback_data=back_data))
    if end < len(keys):  
        nav.append(InlineKeyboardButton("ɴᴇxᴛ ＞", callback_data=f"page_{DictID}_{page+1}"))

    if nav:
        buttons.append(nav)
    return InlineKeyboardMarkup(buttons)

# --------------------------------------------------------------------------- #

def get_enc_key(ts=None):
    k, v = b"E12K7l97Z7wCo3Gu", b"mOk15J2m12qZ2tKI"
    ts = int(time.time() * 1000) if ts is None else int(ts)
    pt = f"{ts}||careerwillapp".encode()
    cipher = AES.new(k, AES.MODE_CBC, v)
    ct = cipher.encrypt(pad(pt, 16))
    return b64encode(ct).decode()


# --------------------------------------------------------------------------- #
                                        
def gen_value(base, source):
    ref = b64decode(source).decode("utf-8")
    combined = base[:16]
    return "".join(ref[int(c)] for c in combined)

def gen_key_iv(de, id=None):
    base = id + de if id else de
    ArrayKey = "JSFGKiZeJClfKiUzZiZCKw=="
    Arrayvector = "IyokREp2eXcydyUhXy0kQA=="
    key = gen_value(base, ArrayKey)
    iv = gen_value(base, Arrayvector)
    return key, iv

def encrypt(key, iv, plaintext):
    key = key.encode("utf8")
    iv = iv.encode("utf8")
    padded = pad(plaintext.encode("utf-8"), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    return b64encode(encrypted).decode("utf-8")

def decrypt(key, iv, encoded_data):
    if ":" in encoded_data:
        encoded_data = encoded_data.split(":")[0]
    key = key.encode("utf8")
    iv = iv.encode("utf8")
    decoded_data = b64decode(encoded_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(decoded_data), AES.block_size)
    return decrypted.decode("utf-8")


def jwt_decoder(token):
    try:
        payload_part = token.split('.')[1]
        padding = '=' * (-len(payload_part) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_part + padding)
        return json.loads(payload_bytes)
    except Exception as e:
        return {"error": str(e)}


# --------------------------------------------------------------------------- #
