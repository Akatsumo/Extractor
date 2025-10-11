import os, traceback, time, re, asyncio, secrets, ujson as json
import aiohttp
from datetime import datetime
from pyrogram.enums import ParseMode
from config import LOGGER_ID
from Extractor.core.func import get_time, send_file
from Extractor.core.c_func import gen_key_iv, encrypt, decrypt, decode_jwt


def gen_device_id(length=16):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
    

class UtkarshExtractor:
    def __init__(self):
        self.v_count = 0
        self.p_count = 0
        self.DEFAULT_BASE = "0199456706643659"
        self.BASE = "1994567066436599"
        self.API_BASE = "https://application.utkarshapp.com/index.php"

        self.HEADERS = {
            'userid': '0',
            'devicetype': '1',
            'lang': '1',
            'authorization': 'Bearer 199#sif346a45ybhbr34yredk799',
            'version': '199',
            'user-agent': 'okhttp/4.11.0',
        }

        self.device_id = None
        self.semaphore = asyncio.Semaphore(30)

    async def fetch(self, session: aiohttp.ClientSession, url, headers, data, key, iv):
        async with self.semaphore:
            async with session.post(url, headers=headers, data=data) as resp:
                response_data = await resp.text()
                decrypted = decrypt(key, iv, response_data.split(':', 1)[0])
                return json.loads(decrypted)

    async def get_content_url(self, session, content, course_id, headers, key, iv):
        try:
            if content.get('file_type') == '3':  # video
                data = {
                    "course_id": course_id,
                    "device_id": self.device_id,
                    "device_name": "samsungSM-F9360",
                    "download_click": "0",
                    "name": content['file_url'],
                    "tile_id": content['payload']['tile_id'],
                    "type": "video"
                }
                result = await self.fetch(
                    session,
                    f"{self.API_BASE}/data_model/meta_distributer/on_request_meta_source",
                    headers,
                    encrypt(key, iv, json.dumps(data)),
                    key, iv
                )

                urls = result.get('data', {}).get('bitrate_urls', [])
                if urls:
                    best = max(urls, key=lambda x: int(x['sort']))['url']
                    url = re.sub(r'\\/', '/', best.split('?', 1)[0]).replace("https\\:", "https:")
                    self.v_count += 1
                    return url
                else:
                    link = result['data'].get('link')
                    self.v_count += 1
                    return link if link.startswith("https") else f"https://youtu.be/{link}"

            else:  # pdf / doc
                self.p_count += 1
                return re.sub(r'\\/', '/', content['file_url']).replace("https\\:", "https:")

        except Exception as e:
            print(f"Error in get_content_url: {e} | Course ID: {course_id}")
            return None

    async def process_topic(self, session, course_id, batch_id, subject_id, topic_id, headers, key, iv):
        data = {
            "course_id": course_id,
            "layer": "3",
            "page": "1",
            "parent_id": batch_id,
            "revert_api": "1#0#0#1",
            "subject_id": subject_id,
            "tile_id": "0",
            "topic_id": topic_id,
            "type": "content"
        }
        topic_data = await self.fetch(
            session,
            f"{self.API_BASE}/data_model/course/get_master_data",
            headers,
            encrypt(key, iv, json.dumps(data)),
            key, iv
        )

        tasks = [
            self.get_content_url(session, c, course_id, headers, key, iv)
            for c in topic_data['data']['list']
            if c.get('file_type') in ('3', '1', '7')
        ]
        urls = await asyncio.gather(*tasks)
        return [(c['title'], u) for c, u in zip(topic_data['data']['list'], urls) if u]

    async def process_course(self, session, course_id, batch_id, headers, key, iv):
        data = {"course_id": course_id, "parent_id": batch_id}
        course_detail = await self.fetch(
            session,
            f"{self.API_BASE}/data_model/course_deprecated/get_course_detail",
            headers,
            encrypt(key, iv, json.dumps(data)),
            key, iv
        )

        tasks = []
        for tile in course_detail['data']['tiles']:
            if tile['type'] == "content":
                for topic in tile['meta']['list']:
                    for subtopic in topic['list']:
                        tasks.append(
                            self.process_topic(session, course_id, batch_id, topic['id'], subtopic['id'], headers, key, iv)
                        )

        results = await asyncio.gather(*tasks)
        return [item for sub in results for item in sub]

    async def extract_content(self, app, query, message):
        try:
            msg = await message.reply_text(
                "**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n"
                "🔒 Send like this: ID*Password\n\nOr Send Token....**"
            )

            input1 = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
            raw_text = input1.text
            await input1.delete(True)

            async with aiohttp.ClientSession() as session:
                if '*' in raw_text:
                    email, password = raw_text.split("*")
                    self.device_id = gen_device_id()

                    key, iv = gen_key_iv(self.DEFAULT_BASE)
                    login_data = {
                        "device_id": self.device_id,
                        "device_token": "utkarsh_device",
                        "is_social": "0",
                        "mobile": email.strip(),
                        "password": password.strip(),
                        "location": {
                            "device_model": "SM-F9360",
                            "ip": "",
                            "lat": "N/A",
                            "lng": "N/A",
                            "manufacturer": "samsung",
                            "os_version": "14"
                        },
                    }
                    encrypted_data = encrypt(key, iv, json.dumps(login_data))

                    result = await self.fetch(
                        session,
                        f"{self.API_BASE}/data_model/users/login_auth",
                        self.HEADERS,
                        encrypted_data,
                        key, iv
                    )
                    token = result['data']['jwt']
                    await message.reply_text(f"ʏᴏᴜʀ ᴛᴏᴋᴇɴ:\n`{token}`")
                    id_pass = f"ɪᴅ ᴘᴀssᴡᴏʀᴅ: <code>{email}*{password}</code>\n"

                else:
                    token = raw_text.strip()
                    id_pass = ""

                user_id = decode_jwt(token)['id']
                key, iv = gen_key_iv(self.BASE, user_id)
                headers = {**self.HEADERS, 'jwt': token, 'userid': str(user_id)}

                data = {"user_id": user_id}
                encrypted_data = encrypt(key, iv, json.dumps(data))
                courses_data = await self.fetch(
                    session,
                    f"{self.API_BASE}/data_model/course/get_my_courses",
                    headers,
                    encrypted_data,
                    key, iv
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
                try:
                    await app.send_message(
                        chat_id=LOGGER_ID,
                        text=f"✅ UTKARSH\n\n{id_pass}ᴛᴏᴋᴇɴ: <code>{token}</code>\n\n{batch_list}",
                        reply_to_message_id=1426,
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass

                batch_msg = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
                batch_id = batch_msg.text.strip()
                await batch_msg.delete()

                batch_name = next((c['title'] for c in courses if str(c['id']) == batch_id), None)

                await msg.edit_text("**Extracting Videos Links Please Wait  📥**")
                start_time = time.time()

                data = {"course_id": batch_id, "parent_id": ""}
                encrypted_data = encrypt(key, iv, json.dumps(data))

                course_data = await self.fetch(
                    session,
                    f"{self.API_BASE}/data_model/course_deprecated/get_course_detail",
                    headers,
                    encrypted_data,
                    key, iv
                )

                all_contents = []
                tasks = []
                for tile in course_data['data']['tiles']:
                    if tile['type'] != "course_combo":
                        continue
                    for course in tile['meta']['list']:
                        tasks.append(self.process_course(session, course['id'], batch_id, headers, key, iv))

                results = await asyncio.gather(*tasks)
                for contents in results:
                    for title, url in contents:
                        all_contents.append(f"{title}:{url}")

                filename = f"{batch_name.replace('/', '') if batch_name else 'Unknown'}_{int(time.time())}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("\n".join(all_contents))

                elapsed = get_time(time.time() - start_time)

                caption = (
                    f"**App Name :- Utkarsh**\n"
                    f"**Batch Name :-** `{batch_name}`\n\n"
                    f"🍿 **Total Video**: `{self.v_count}`\n"
                    f"📝 **Total pdf**: `{self.p_count}`\n"
                    f"⌚️**Time Taken**: `{elapsed}`"
                )

                return await send_file(filename, caption, msg, query)

        except Exception as e:
            traceback.print_exc()
            await message.reply_text(f"An error occurred: {str(e)}")


async def utkarsh(app, query, message):
    extractor = UtkarshExtractor()
    return await extractor.extract_content(app, query, message)
