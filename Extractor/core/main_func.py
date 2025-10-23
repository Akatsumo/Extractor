import time, os
import base64
import json, asyncio
from Crypto.Cipher import AES
from config import CHANNEL_ID, LOGS_CHANNEL
from Extractor.core import script
from base64 import b64decode, b64encode
from Crypto.Util.Padding import unpad, pad
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --------------------------------------------------------------------------- #

async def send_file(app, file_name, user_id, caption, thumb=None, onlyThumb=False):
    if not thumb:
        me = await app.get_me()
        thumb = await asyncio.create_task(app.download_media(me.photo.big_file_id)) if me.photo else None
    if onlyThumb:
        return thumb
    msg = await app.send_document(chat_id=user_id, document=file_name, caption=caption, thumb=thumb)
    if LOGS_CHANNEL:
        try:
            await app.copy_message(LOGS_CHANNEL, user_id, msg.id)
            print("Successfully Send TxT in Log Channel")
        except Exception as e:
            print(f"Failed to send message to log channel: {e}")
            pass
    os.remove(file_name)
    os.remove(thumb)    
    return True
   
# --------------------------------------------------------------------------- #

async def gen_link(app,chat_id):
   link = await app.export_chat_invite_link(chat_id)
   return link
  

async def subscribe(app, message, user_id=None, name=None):
   update_channel = CHANNEL_ID
   user_id = user_id if user_id else message.from_user.id
   name = name if name else message.from_user.mention
   url = await gen_link(app, update_channel)
   if update_channel:
      try:
         user = await app.get_chat_member(update_channel, user_id)
         if user.status == "kicked":
            await message.reply_text("Sorry Sir, You are Banned. Contact My Support Group @DiabloForge")
            return 1
      except UserNotParticipant:
         await message.reply_photo(photo="https://telegra.ph/file/b7a933f423c153f866699.jpg",caption=script.FORCE_MSG.format(name), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 🤖", url=f"{url}")]]))
         return 1
      except Exception:
         await message.reply_text("Something Went Wrong. Contact My Support Group")
         return 1

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

def get_page(page: int, appNameDict, DictID="Dic1", back_data="tools_", query=None, appx=False, withoutIdPass=True. page_row=3):
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
    if withoutIdPass:
        buttons.append([InlineKeyboardButton("🔐 Without Pass", callback_data="without_pass")])
        
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

# --------------------------------------------------------------------------- #

def jwt_decoder(token):
    try:
        payload_part = token.split('.')[1]
        padding = '=' * (-len(payload_part) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_part + padding)
        return json.loads(payload_bytes)
    except Exception as e:
        return {"error": str(e)}

# --------------------------------------------------------------------------- #





# --------------------------------------------------------------------------- #
