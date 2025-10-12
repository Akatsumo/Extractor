import os
import time
import math
import json
import aiohttp
import asyncio
from Extractor import app
from pyrogram import filters
from Extractor.core.main_func import get_time


class AddaExtractor:
    BASE_USER = "https://userapi.adda247.com"
    BASE_STORE = "https://store.adda247.com"
    BASE_LIVE = "https://liveclasses.adda247.com"

    def __init__(self):
        self.headers = {
            'X-Auth-Token': 'fpoa43edty5',
            'X-CSRF-Token': '',
            'X-JWT-Token': '',
            'login_token': '',
            'Referer': 'https://www.adda247.com/',
            'Content-Type': 'application/json',
            'login_type': '1',
            'dName': 'Chrome on Windows Desktop'
        }

    # ---------------- CSRF Token ---------------- #
    async def get_csrf_token(self, session):
        async with session.get(f"{self.BASE_USER}/csrf/token?src=aweb") as r:
            data = await r.json()
            return data["data"] if data.get("success") else None

    # ---------------- Login ---------------- #
    async def login(self, session, email, password):
        login_url = f"{self.BASE_USER}/v2/login?src=aweb"
        token = await self.get_csrf_token(session)
        self.headers["X-CSRF-Token"] = token

        async with session.post(login_url, json={"email": email, "providerName": "email", "sec": password}, headers=self.headers) as r:
            if r.status != 200:
                return None
            data = await r.json()

        login_token = data.get("loginToken")
        self.headers["login_token"] = login_token

        async with session.post(f"{self.BASE_USER}/forceLogout?src=aweb", headers=self.headers) as r:
            data = await r.json()
            return data["data"]["jwtToken"] if r.status == 200 else None

    # ---------------- Get Purchased Courses ---------------- #
    async def get_courses(self, session):
        params = {"pageNumber": 0, "pageSize": 20, "src": "aweb"}
        async with session.get(f"{self.BASE_STORE}/api/v2/ppc/package/purchased", headers=self.headers, params=params) as r:
            if r.status != 200:
                return []
            data = await r.json()
            return data.get("data", [])

    # ---------------- Direct Content Extract ---------------- #
    async def extract_direct(self, session, course_id):
        lectures = []
        params = {
            'packageId': course_id,
            'category': 'ONLINE_LIVE_CLASSES',
            'isComingSoon': 'false',
            'pageNumber': '0',
            'pageSize': '10',
            'src': 'aweb'
        }

        async with session.get(f"{self.BASE_STORE}/api/v3/ppc/package/child", headers=self.headers, params=params) as r:
            data = await r.json()

        total_items = data.get('data', {}).get('packagesCount', 0)
        page_count = math.ceil(total_items / 10)

        async def fetch_page(page):
            params['pageNumber'] = str(page)
            try:
                async with session.get(f"{self.BASE_STORE}/api/v3/ppc/package/child", headers=self.headers, params=params) as r:
                    resp = await r.json()
                    subjects = resp.get('data', {}).get('packages', [])
                    result = []

                    for sub in subjects:
                        pid = sub.get("packageId")
                        async with session.get(f"{self.BASE_STORE}/api/v1/my/purchase/OLC/{pid}?src=aweb", headers=self.headers) as sr:
                            cont = await sr.json()
                            for content in cont.get("data", {}).get("onlineClasses", []):
                                name = content.get("name", "Unknown")
                                url = content.get("url")
                                pdf = content.get("pdfFileName")
                                dpp_files = content.get("dppFileNames", [])

                                if url:
                                    result.append(f"{name}: {url}")
                                if pdf:
                                    result.append(f"{name}: {self.BASE_STORE}/{pdf}")
                                if dpp_files:
                                    for dpp in dpp_files:
                                        result.append(f"{name}: {self.BASE_STORE}/{dpp}")
                    return result
            except Exception:
                return []

        results = await asyncio.gather(*[fetch_page(p) for p in range(page_count)], return_exceptions=False)
        for res in results:
            lectures.extend(res)
        return lectures

    

# ---------------- Telegram Command ---------------- #

@app.on_message(filters.command("adda"))
async def adda_command(_, message):
    user_id = message.from_user.id
    adda = AddaExtractor()
    msg = await message.reply_text("🔑 **Send your credentials like:**\n`email*password`")

    try:
        input1 = await app.listen(user_id=user_id, timeout=30)
        raw = input1.text.strip)
    except:
        return await msg.edit_text("⏳ Timeout! Try again.")
      
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=200)) as session:
      if "*"  in raw:
        email, password = input1.text.split("*")
        token = await add.login(session, email, password)
      else:
        token = raw
    
      await input1.delete()            
      await msg.edit_text("✅ **Login Successful**")
      adda.headers["X-JWT-Token"] = token
      courses = await adda.get_courses(session)
      if not courses:
          return await msg.edit_text("No purchased batches found.")

      batch_courses = "**BATCH-ID  -  BATCH NAME**\n\n"
      for c in courses:
          batch_courses += f"`{c['packageId']}` - {c['title']}\n"
        
      await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")
      try:
          input2 = await app.listen(user_id=user_id, timeout=30)
          course_id = input2.text.strip()
          await input2.delete()
      except:
          return await message.reply_text("⏳ Timeout! Please try again.")

      batch_name = next((c["title"].replace("/", "") for c in courses if int(c["packageId"]) == int(course_id)), "")
      if not batch_name:
          return await msg.edit_text("**Invalid Batch ID. Please try again.**")

      await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
      start = time.time()
      lectures = await adda.extract_direct(session, course_id)
      elapsed = get_time(time.time() - start)
      file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
      with open(file_name, "w") as f:
        f.write("\n".join(lectures))

      caption = f"**App Name** : `ADDA 247`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed} sec`"
      me = await app.get_me()
      big_file_id = me.photo.big_file_id
      thumb = await asyncio.create_task(app.download_media(big_file_id))

      await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
      os.remove(file_name)
      await msg.delete()
      await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        
      caption = f"**App**: ADDA247\n**Batch**: {batch_name}\n**Total Files**: {len(lectures)}\n⏱ Time: {elapsed}"

      await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption)
      os.remove(file_name)
      await msg.delete()


