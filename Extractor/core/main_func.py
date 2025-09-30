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

# --------------------------------------------------------------------------- #
allDics = {}
PER_PAGE = 15

def get_page(page: int, appNameDict, DictID="Dic1", query=None, tools=False, page_row=3):
    keys = list(appNameDict.keys())  
    start = page * PER_PAGE
    end = start + PER_PAGE
    allDics[DictID] = appNameDict
    back_data = "tools_" if tools else "home_"

    if start >= len(keys) and query:
        return query.answer("🚫 No more pages", show_alert=True)

    buttons = []
    row = []
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



                                        
