import asyncio
import requests
import os, time, re, secrets, json
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


def gen_device_id(length=16):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


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

    async def fetch(self, url, data, key, iv):
        try:
            response = self.session.post(url, headers=self.headers, data=data)
            response_data = json.loads(main_func.decrypt(key, iv, response.text))
            if response_data.get("status") is not True:
                return None
            return response_data
        except Exception as e:
            print(f"[Fetch Error] {e}")
            return None

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
                print("✅ Login Successfully")
            else:
                token = raw_text

            user_data = main_func.jwt_decoder(token)
            user_id_api = user_data.get('id')
            self.headers.update({"jwt": token, "userid": str(user_id_api)})

            key, iv = main_func.gen_key_iv(self.BASE, user_id_api)
            data = {"user_id": user_id_api}
            encrypted_data = main_func.encrypt(key, iv, json.dumps(data))

            courses_data = await self.fetch(
                f"{self.API_BASE}/data_model/course/get_my_courses",
                encrypted_data, key, iv
            )

            if not courses_data or not courses_data.get("data"):
                return await msg.edit_text("No Batch Data found!!")

            courses = courses_data["data"]
            course_batches = "📚 **Available Batches:**\n\n"
            for c in courses:
                course_batches += f"`{c['id']}` - **{c['title']}**\n"

            await msg.edit_text(f"{course_batches}\n\n📊 **Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id, timeout=30)
            batch_id = input2.text.strip()
            await input2.delete()

            batch_name = next((c['title'] for c in courses if str(c['id']) == batch_id), None)
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
                f.write(lectures)
                
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




