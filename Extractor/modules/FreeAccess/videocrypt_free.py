import json, os
import time
import asyncio
import requests
from Extractor import app
from pyrogram import filters
from base64 import b64decode
from pyromod.exceptions import ListenerTimeout
from Extractor.core import main_func, script, core_func
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def header_definer(name):
    name = name.replace(" ", "").lower()
    if name == "abhinaymaths":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_586"
        version = "103"
        appid = "586"
        return authorization, version, appid
    elif name == "eduteria":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_166"
        version = "40"
        appid = "166"
        return authorization, version, appid
    elif name == "kotamentors":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_675"
        version = "3"
        appid = "675"
        return authorization, version, appid
    elif name == "missionselection":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_746"
        version = "23"
        appid = "746"
        return authorization, version, appid
    elif name == "rankbuddy":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_583"
        version = "4"
        appid = "583"
        return authorization, version, appid
    elif name == "rajputtutorials":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_681"
        version = "50"
        appid = "681"
        return authorization, version, appid
    elif name == "pateltutorials":
        authorization = "Bearer 117#Nerglnw3@@OI)30@I*Dm'@@_263"
        version = "59"
        appid = "263"
        return authorization, version, appid
    elif name == "mypathsala":
        authorization = "Bearer 01*#NerglnwwebOI)30@I*Dm'@@"
        version = "1"
        appid = "810"
        return authorization, version, appid
        
    else:
        return None, None, None
        


# --------------- VideoCrypt Extractor --------------- #

class VideoCryptExtractor:
    def __init__(self, name):
        self.v_count = 0
        self.p_count = 0
        self.name = name
        self.session = requests.Session()
        self.DEFAULT_BASE = "0117108641864451"
        self.BASE = "1171086418644515_166"
        self.API_BASE = "https://appapi.videocrypt.in/index.php"
        authorization, version, appid = header_definer(name)
        self.HEADERS = {
            "userid": "0",
            "devicetype": "1",
            "lang": "1",
            "authorization": authorization,
            "version": version,
            "appid": appid,
            "user-agent": "okhttp/4.11.0",
        }
        self.LOGIN_DATA = {
            "device_id": "e0d97edefabd9635",
            "device_token": "f9c8b1a4d7e34c1aa6e89f17e5b2d3c76a5e8d9f12a34b6c8d0e1f2a3b4c5d6e",
            "is_social": "0",
        }

    def fetch(self, endpoint, headers, data, key, iv):
        url = f"{self.API_BASE}/{endpoint}"
        enc = main_func.encrypt(key, iv, json.dumps(data))
        res = self.session.post(url, headers=headers, data=enc)
        if res.status_code != 200:
            return {'status': False, 'message': 'something went wrong!'}
        text = res.text
        try:
            return json.loads(main_func.decrypt(key, iv, text))
        except Exception:
            try:
                part = text.split(":")
                if len(part) == 2:
                    dyn_base = b64decode(part[1]).decode("utf-8")
                    k, v = main_func.gen_key_iv(self.BASE, dyn_base)
                    dec = main_func.decrypt(k, v, part[0])
                    return json.loads(dec)
            except Exception:
                pass
        raise ValueError(f"Failed to decrypt: {text}")

    def get_content_url(self, course_id, content, headers, key, iv):
        url = None
        if content.get("file_type") == "3":
            if content.get("is_drm") == "1":
                url = f"https://abhinaymaths.in/drm/{content.get('vdc_id')}/{headers.get('userid')}" if self.name == "abhinaymaths" else f"https://www.videocrypt.in/drm/{content.get('vdc_id')}/{headers.get('userid')}"
            elif content.get("video_type") == "1":
                url = f"https://youtu.be/{content['file_url']}"
            else:
                url = content["file_url"].replace("\\/", "/").replace("https\\:", "https:")
            self.v_count += 1
            if content.get("had_pdf") == "1":
                data = {"course_id": course_id, "video_id": content.get("id")}
                result = self.fetch("data_model/poll/get_content_pdf", headers, data, key, iv)
                for pdf in result["data"]:
                    url += f"\n{pdf['pdf_title']} : {pdf['pdf_url']}"
        else:
            url = content["file_url"].replace("\\/", "/").replace("https\\:", "https:")
            self.p_count += 1
        return url

    def process_topic(self, course_id, batch_id, topic_id, subject_id, tile_type, tile_id, revert_api, headers, key, iv):
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
            "type": tile_type,
        }
        topic_data = self.fetch("data_model/course/get_master_data", headers, data, key, iv)
        contents = ""
        if not topic_data.get("data", []):
            return ""
        for content in topic_data["data"]["list"]:
            if content.get("file_type") in ("3", "1", "7"):
                url = self.get_content_url(course_id, content, headers, key, iv)
                if url:
                    contents += f"{content['title']} : {url}\n"
        return contents

    def process_course(self, course_id, batch_id, headers, key, iv):
        data = {"course_id": course_id, "parent_id": batch_id}
        course_detail = self.fetch("data_model/course_deprecated/get_course_detail", headers, data, key, iv)
        results = ""
        for tile in course_detail["data"]["tiles"]:
            if tile["type"] not in ["video", "pdf"]:
                continue
            for topic in tile["meta"]["list"]:
                for subtopic in topic["list"]:
                    results += self.process_topic(course_id, batch_id, subtopic["id"], topic["id"], tile["type"], tile["id"], tile["revert_api"], headers, key, iv)
        return results


    async def start_login(self, app, message, user_id=None):
        user_id = user_id if user_id else message.from_user.id
        try:
            msg = await message.reply_text("🔑 Enter login credentials (Mobile*Password or Token): ")
            input1 = await app.listen(user_id=user_id, timeout=30)
            raw = input1.text.strip()
            await input1.delete()
    
            key, iv = main_func.gen_key_iv(self.DEFAULT_BASE)

            if "*" in raw:
                email, password = raw.split("*")
                login_data = {**self.LOGIN_DATA, "mobile": email.strip(), "password": password.strip()}
                result = self.fetch("data_model/users/login_auth", self.HEADERS, login_data, key, iv)
                if result.get("status") == False:
                    return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
                token = result["data"].get("jwt")
            else:
                token = raw

            userId = main_func.jwt_decoder(token).get("id")
            key, iv = main_func.gen_key_iv(self.BASE, userId)
            headers = {**self.HEADERS, "jwt": token, "userid": userId}

            data = {"user_id": userId}
            courses_data = self.fetch("data_model/course/get_my_courses", headers, data, key, iv)
            courses = courses_data.get("data", [])
            # if not courses:
            #     return await msg.edit_text("No Batch Data found!!")

            course_batches = "📚 **Available Batches:**\n\n"
            for c in courses:
                course_batches += f"`{c['id']}` - **{c['title']}**\n"

            await msg.edit_text(f"{course_batches}\n**📊 Now send the Batch ID to Download**")
            input2 = await app.listen(user_id=user_id, timeout=30)
            batch_id = input2.text.strip()
            await input2.delete()
            batch_name = next((c["title"] for c in courses if str(c["id"]) == batch_id), "Unknown Batch")
            # if batch_name == "Unknown Batch":
            #     return await msg.edit_text("Only valid batch IDs are accepted")

            await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
            start = time.time()
            all_contents = self.process_course(batch_id, batch_id, headers, key, iv)
            if not all_contents:
                return await msg.edit_text("📭 **No content found in this batch.**")

            file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(all_contents)

            elapsed = main_func.get_time(time.time() - start)
    
            caption = f"**App Name** : `{self.name.title()}`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(all_contents.split("\n"))}`\n🍿 **Videos** : {self.v_count} | 📝 **PDFs** : {self.p_count}\n⌚️ **Time Taken** : `{elapsed} sec`"

            me = await app.get_me()
            big_file_id = me.photo.big_file_id
            thumb = await asyncio.create_task(app.download_media(big_file_id))
            await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
            os.remove(file_name)
            await msg.delete()
            await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        except ListenerTimeout:
            await message.reply_text("Oops! You didn't reply in time. ⏰")
        except Exception as e:
            await message.reply_text(f"Error: `{str(e)}`")




async def videocrypt_access(_, message, user_id=None):
    buttons = main_func.get_page(0, core_func.videoCryptDict, DictID="VideoDecrypt1", back_data="without_pass", withoutIdPass=False)
    if user_id:
        await message.edit_text(script.TOOLS_TEXT, reply_markup=buttons)
    else:
        await message.reply_text(script.TOOLS_TEXT, reply_markup=buttons)
    
