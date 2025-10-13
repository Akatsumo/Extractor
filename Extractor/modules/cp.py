import re
import os
import time
import json
import asyncio
import aiohttp
import cloudscraper
import hashlib
import platform
import uuid
from Extractor import app
from pyrogram import filters
from Extractor.core.main_func import get_time


class ClassplusExtractor:
    BASE_URL = "https://api.classplusapp.com"
    API_VERSION = "52"

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.system_fingerprint = self._get_system_fingerprint()

    def _get_system_fingerprint(self):
        system_info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "uuid": str(uuid.getnode()),
        }
        fingerprint_string = "_".join(system_info.values())
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()

    def _default_headers(self):
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en",
            "api-version": self.API_VERSION,
            "content-type": "application/json;charset=UTF-8",
        }

    async def get_org_info(self, org_code, session):
        try:
            async with session.get(f"https://{org_code}.courses.store") as response:
                html_content = await response.text()
                org_id_match = re.search(r'"orgId":(\d+)', html_content)
                name_match = re.search(r'"name":"([^"]+)"', html_content)
                org_id = org_id_match.group(1) if org_id_match else None
                name = name_match.group(1) if name_match else None
                return org_id, name
        except Exception:
            return None, None

    async def request_otp(self, session, org_code, org_id, phone):
        url = f"{self.BASE_URL}/v2/otp/generate"
        data = {
            "countryExt": "91",
            "orgCode": org_code,
            "viaSms": "1",
            "viaEmail": "0",
            "retry": 0,
            "orgId": org_id,
            "otpCount": 0,
            "mobile": str(phone.strip()),
        }
        async with session.post(url, headers=self._default_headers(), json=data) as resp:
            result = await resp.json()
            if result.get("status") == "success":
                return result["data"]["sessionId"]
            return None

    async def verify_otp(self, session, otp, org_id, phone, session_id):
        url = f"{self.BASE_URL}/v2/users/verify"
        headers = self._default_headers()
        headers["origin"] = "https://web.classplusapp.com"
        headers["referer"] = "https://web.classplusapp.com/"
        data = {
            "otp": otp,
            "countryExt": "91",
            "sessionId": session_id,
            "orgId": org_id,
            "fingerprintId": self.system_fingerprint,
            "mobile": str(phone.strip()),
        }
        async with session.post(url, headers=headers, json=data) as resp:
            result = await resp.json()
            if result.get("status") == "success":
                return result["data"]["token"]
            return None

    async def fetch_courses(self, session, token):
        url = f"{self.BASE_URL}/v2/courses?tabCategoryId=1&categoryId=[]&"
        headers = self._default_headers()
        headers["x-access-token"] = token
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data.get("data", {}).get("courses", [])

    async def extract_course_content(self, session, headers, course_id, folder_id=0):
        try:
            lectures = []
            url = f"{self.BASE_URL}/v2/course/content/get?courseId={course_id}&folderId={folder_id}&storeContentEvent=false"
            async with session.get(url, headers=headers) as resp:
                output = await resp.json()
            for content in output.get("data", {}).get("courseContent", []):
                ctype = content.get("contentType")
                if ctype == 1:
                    lectures.extend(await self.extract_course_content(session, headers, course_id, content["id"]))
                elif ctype == 2:
                    content_id = content.get("contentHashId", "")
                    video_data = self.scraper.get(
                        f"{self.BASE_URL}/cams/uploader/video/jw-signed-url",
                        headers=headers,
                        params={"contentId": content_id},
                    ).json()
                    video_url = video_data.get("url", "").split("m3u8")[0] if "url" in video_data else "Not Found"
                    lectures.append(f"{content['name']}: {video_url}")
                elif ctype == 3:
                    lectures.append(f"{content['name']}: {content.get('url')}")
            return lectures
        except Exception:
            return []

    @staticmethod
    def _is_valid_input(org_code, phone):
        return org_code.isalpha() and phone.isdigit() and len(phone) == 10

    async def handle_classplus(self, message):
        user_id = message.from_user.id
        async with aiohttp.ClientSession() as session:
            try:
                msg = await message.reply_text("**🔑 Send your OrgID & Phone in this format:** `OrgID*Phone`")
                input1 = await app.listen(user_id, timeout=30)
                if "*" in input1.text:
                    org_code, phone = input1.text.split("*")
                    org_id, _ = await self.get_org_info(org_code, session)
                    if not self._is_valid_input(org_code, phone):
                        return await msg.edit_text("😑 Invalid format. Use like: `OrgID*1234567890`")
                    session_id = await self.request_otp(session, org_code, org_id, phone)
                    if not session_id:
                        return await msg.edit_text("⚠️ Failed to send OTP. Try again later.")
                    await msg.edit_text("📨 Send your OTP now.")
                    otp_msg = await app.listen(user_id, timeout=50)
                    token = await self.verify_otp(session, otp_msg.text.strip(), org_id, phone, session_id)
                    if not token:
                        return await msg.edit_text("❌ Invalid OTP. Please try again.")
                else:
                    token = input1.text.strip()
                await input1.delete()
                courses = await self.fetch_courses(session, token)
                if not courses:
                    return await msg.edit_text("📭 No courses found or invalid token.")
                batch_map = {str(c["id"]): c["name"] for c in courses}
                batch_text = "\n".join([f"`{cid}` - **{name}**" for cid, name in batch_map.items()])
                await msg.edit_text(f"**Available Batches:**\n\n{batch_text}\n\n📊 Send the Batch ID to start download.")
                input2 = await app.listen(user_id)
                course_id = input2.text.strip()
                batch_name = batch_map.get(course_id, "Unknown Batch")
                await msg.edit_text("📥 Extracting course contents, please wait...")
                start = time.time()
                headers = {"x-access-token": token, **self._default_headers()}
                lectures = await self.extract_course_content(session, headers, course_id)
                elapsed = round(time.time() - start, 2)
                filename = f"{batch_name.replace('/', '')}_{user_id}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(lectures))
                caption = (
                    f"**Batch Name:** `{batch_name}`\n"
                    f"**Total Materials:** `{len(lectures)}`\n"
                    f"**Time Taken:** `{elapsed} sec`"
                )
                me = await app.get_me()
                thumb = await app.download_media(me.photo.big_file_id)
                await app.send_document(message.chat.id, filename, caption=caption, thumb=thumb)
                os.remove(filename)
                await msg.delete()
                await message.reply_text(f"✅ **Done!**\n\n🔐 **Token:** `{token}`")
            except asyncio.TimeoutError:
                await message.reply_text("⏳ Timeout! Please try again.")
            except Exception as e:
                await message.reply_text(f"**Error:** `{str(e)}`")
            finally:
                await session.close()


@app.on_message(filters.command("cpt"))
async def classplus_handler(_, message):
    extractor = ClassplusExtractor()
    await extractor.handle_classplus(message)
