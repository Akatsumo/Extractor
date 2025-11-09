import asyncio
import requests
import os, time, re, secrets, json
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


def gen_device_id(length=16):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class CryptoHandler:
    def __init__(self):
        self.key = b'%!$!%_$&!%F)&^!^'        # 16 bytes key
        self.iv = b'#*y*#2yJ*#$wJv*v'         # 16 bytes IV

    def encrypt(self, plain_text: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_base64

    def decrypt(self, encrypted_text: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(encrypted_text)), AES.block_size)
        return decrypted_bytes.decode('utf-8')



crypto = CryptoHandler()



class UtkarshExtractor:
    def __init__(self):
        self.v_count = 0
        self.p_count = 0
        self.session = requests.Session()
        self.DEFAULT_BASE = "0199456706643659"
        self.BASE = "1994567066436599"
        self.API_BASE = "https://application.utkarshapp.com/index.php"

        self.headers = {
            'userid': '0',
            'devicetype': '1',
            'lang': '1',
            'authorization': 'Bearer 199#sif346a45ybhbr34yredk799',
            'version': '199',
            'user-agent': 'okhttp/4.11.0',
        }

    def fetch(self, url, data, key, iv):
        response = self.session.post(url, headers=self.headers, data=data)
        response_data = json.loads(main_func.decrypt(key, iv, response.text))
        if response_data.get("status") is not True:
            return None
        return response_data
        
    def get_master_courses(session):
        r = session.get("https://online.utkarsh.com/web/Home/getMasterCat")
        response_data = json.loads(crypto.decrypt(r.json().get("response")))
        master_cats = response_data["data"]["master_cat"]
        all_cats = response_data["data"]["all_cat"]

        master_dict = {}

        for m in master_cats:
            master_dict[m["id"]] = {
                "master_id": m["id"],
                "master_name": m["cat"],
                "popular_sub_cats": m.get("popular_sub_cats", ""),
                "image": m.get("image", ""),
                "sub_categories": []
            }

        for sub in all_cats:
            m_id = sub.get("master_type")
            parent_id = str(sub.get("parent_id", "")).strip()
            if not parent_id or parent_id == "0" or m_id not in master_dict:
               continue
               
           master_dict[m_id]["sub_categories"].append({
            "sub_id": sub["id"],
            "sub_name": sub["name"],
            "parent_id": parent_id,
            "is_child": sub.get("is_child", "0")
           })
        final_output = list(master_dict.values())
        return json.dumps(final_output, indent=4, ensure_ascii=False)


    def get_courses(session, cat_id, sub_cat_id, page=1):
        cookies = {
            "csrf_name": "efcded0e551a154f509163c665fb7cec",
            "ci_session": "irkdqsvrd1ketajm4g8b0beics2ko3na",
        }
        url = "https://online.utkarsh.com/web/Home/getCourses"
        data = {
            "csrf_name": "efcded0e551a154f509163c665fb7cec",
            "cat": cat_id,
            "sub_cat": sub_cat_id,
            "catBranch_text": "",
            "course_type": "0",
            "page": page,
        }
        response = session.post(url, cookies=cookies, data=data)
        response_data = json.loads(crypto.decrypt(response.json().get("response").split(":")[0]))
        return response_data

    async def process_topic(self, course_id, batch_id, subject_id, topic_id, key, iv):
        lectures = []
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
            f"{self.API_BASE}/data_model/course/get_master_data",
            main_func.encrypt(key, iv, json.dumps(data)),
            key, iv
        )

        if not topic_data or 'data' not in topic_data:
            return lectures

        for content in topic_data['data'].get('list', []):
            subject_name = content.get('title', 'N/A')
            if content.get('file_type') not in ('3', '1', '7'):
                continue

            if content.get('file_type') == '3':
                data = {
                    "course_id": course_id,
                    "device_id": gen_device_id(),
                    "device_name": "samsungSM-F9360",
                    "download_click": "0",
                    "name": content['file_url'],
                    "tile_id": content['payload']['tile_id'],
                    "type": "video"
                }

                result = await self.fetch(
                    f"{self.API_BASE}/data_model/meta_distributer/on_request_meta_source",
                    main_func.encrypt(key, iv, json.dumps(data)),
                    key, iv
                )
                if not result:
                    continue

                urls = result.get('data', {}).get('bitrate_urls', [])
                if urls:
                    best = max(urls, key=lambda x: int(x['sort']))['url']
                    url = re.sub(r'\\/', '/', best.split('?', 1)[0]).replace("https\\:", "https:")
                    self.v_count += 1
                    lectures.append(f"{subject_name}: {url}")
                else:
                    link = result['data'].get('link')
                    if link:
                        self.v_count += 1
                        url = link if link.startswith("https") else f"https://youtu.be/{link}"
                        lectures.append(f"{subject_name}: {url}")

            else:
                self.p_count += 1
                url = re.sub(r'\\/', '/', content['file_url']).replace("https\\:", "https:")
                lectures.append(f"{subject_name}: {url}")

        return lectures

    async def process_course(self, course_id, batch_id, key, iv):
        data = {"course_id": course_id, "parent_id": batch_id}
        encrypted_data = main_func.encrypt(key, iv, json.dumps(data))
        course_detail = await self.fetch(
            f"{self.API_BASE}/data_model/course_deprecated/get_course_detail",
            encrypted_data, key, iv
        )

        lectures = []
        if not course_detail or 'data' not in course_detail:
            return lectures

        for tile in course_detail['data'].get('tiles', []):
            if tile.get("type") != "content":
                continue

            for topic in tile.get('meta', {}).get('list', []):
                for subtopic in topic.get('list', []):
                    topic_lectures = await self.process_topic(
                        course_id, batch_id, topic.get('id'), subtopic.get('id'), key, iv
                    )
                    lectures.extend(topic_lectures)

        return lectures

    async def start_login(self, app, message, user_id=None):
        user_id = user_id if user_id else message.from_user.id
        try:
            msg = await message.reply_text("🔑 Enter login credentials (Mobile*Password or Token):")
            input1 = await app.listen(user_id=user_id, timeout=30)
            raw_text = input1.text.strip()
            await input1.delete()

            if '*' in raw_text:
                email, password = raw_text.split("*")
                key, iv = main_func.gen_key_iv(self.DEFAULT_BASE)
                login_data = {
                    "device_id": gen_device_id(),
                    "device_token": "utkarsh_device",
                    "is_social": "0",
                    "mobile": email.strip(),
                    "password": password.strip()
                }

                encrypted_data = main_func.encrypt(key, iv, json.dumps(login_data))
                response = await self.fetch(
                    f"{self.API_BASE}/data_model/users/login_auth",
                    encrypted_data, key, iv
                )

                if not response or "data" not in response:
                    return await msg.edit_text("❌ Login failed. Please try again.")
                token = response["data"].get("jwt")
            else:
                token = raw_text

            await msg.edit_text("Login Successfull")
            user_data = main_func.jwt_decoder(token)
            user_id_api = user_data.get('id')
            self.headers.update({"jwt": token, "userid": str(user_id_api)})
            
            key, iv = main_func.gen_key_iv(self.BASE, user_id_api)
            data = {"user_id": user_id_api}
            encrypted_data = main_func.encrypt(key, iv, json.dumps(data))

            # courses_data = await self.fetch(
            #     f"{self.API_BASE}/data_model/course/get_my_courses",
            #     encrypted_data, key, iv
            # )
            
            # if not courses_data or not courses_data.get("data"):
            #     return await msg.edit_text("No Batch Data found!!")

            # courses = courses_data["data"]
            
            master_data = get_master_courses(session)
            if not master_data:
                return await msg.edit_text("Master course not found !!")

            master_list = "📚 **Available Masters:**\n\n"
            for master in master_list:
                master_list += f"{master.get('master_id')} - {master.get('master_name')}\n"

            await msg.edit_text(f"{master_list}\n\n📊 **Now send the Master ID to Download**")
            input2 = await app.listen(user_id=user_id, timeout=30)
            master_id = input2.text.strip()
            await input2.delete()

            master_name sub_content = next(((c['master_name'], c['sub_categories']) for c in master_data if str(c['master_data']) == master_id), (None, None))
            if not master_name:
                return await msg.edit_text("Only valid Master IDs are accepted")

            batch_list = []
            course_batches = "📚 **Available Batches:**\n\n"
            for sub in sub_content:
                course_data = get_courses(session, sub.get("parent_id"), sub.get("sub_id")).get("data")
                for course in course_data:
                    course_batches += f"`{course.get('id')}` - **{course.get('title')}**\n"
                    batch_list.append(course)

            thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
            caption = "**📊 Now send the Batch ID to Download**"
            batch_file = None

            if len(batch_list) > 4000:
                batch_list_name = f"{master_name}_batchList_{user_id}.txt"
                with open(batch_list_name, "w", encoding="utf-8") as f:
                    f.write(batch_list)
                batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
                os.remove(batch_list_name)
            else:
                await msg.edit_text(f"{batch_list}\n\n{caption}")

            input3 = await app.listen(user_id=user_id, timeout=30)
            batch_id = input3.text.strip()
            await input3.delete()
            if batch_file:
                await batch_file.delete()

            batch_name = next((c['title'] for c in batch_list if str(c['id']) == batch_id), None)
            if not batch_name:
                return await msg.edit_text("Only valid batch IDs are accepted")

            await msg.edit_text("📥 Extracting Course Content, Please Wait...")
            start_time = time.time()
            data = {"course_id": batch_id, "parent_id": ""}
            encrypted_data = main_func.encrypt(key, iv, json.dumps(data))
            course_data = await self.fetch(
                f"{self.API_BASE}/data_model/course_deprecated/get_course_detail",
                encrypted_data, key, iv
            )

            lectures = []
            if not course_data or 'data' not in course_data:
                return await msg.edit_text("No course data found.")

            for tile in course_data["data"].get("tiles", []):
                if tile.get("type") != "course_combo":
                    continue

                for course in tile.get("meta", {}).get("list", []):
                    sub_lectures = await self.process_course(
                        course.get('id'), batch_id, key, iv
                    )
                    lectures.extend(sub_lectures)

            if not lectures:
                return await msg.edit_text("📭 **No content found in this batch.**")
                
            end_time = time.time()
            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(lectures))
                
            elapsed = main_func.get_time(end_time - start_time)
            caption = (
                f"**App Name** : `Utkarsh`\n"
                f"**Batch Name** : `{batch_name}`\n\n"
                f"📜 **Total Materials** : `{len(lectures)}`\n"
                f"🍿 **Videos** : `{self.v_count}` | 📝 **PDFs** : `{self.p_count}`\n"
                f"⌚️ **Time Taken** : `{elapsed}`"
            )
            await main_func.send_file(app, file_name, user_id, caption, thumb=None)
            await msg.delete()
            await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        except ListenerTimeout:
            await message.reply_text("⏰ Timeout! You took too long to reply.")
        except Exception as e:
            await message.reply_text(f"Error: `{e}`")




