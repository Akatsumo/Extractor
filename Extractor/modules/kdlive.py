from aiohttp import ClientSession, TCPConnector
import aiofiles
import hashlib
import asyncio
import time
import os
from Extractor import app
from Extractor.core.func import send_file

API_KEY = "kdc123"

# Global aiohttp session
session = ClientSession(
    connector=TCPConnector(limit=100),  # limit concurrent connections
    timeout=aiohttp.ClientTimeout(total=30),
    headers={
        "User-Agent": "okhttp/4.10.0",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json; charset=UTF-8"
    }
)

async def list_batches(token, userid):
    url = f'https://web.kdcampus.live/android/Dashboard/get_mycourse_data_renew_new/{token}/{userid}/4'
    async with session.get(url) as resp:
        if resp.status != 200:
            return []
        data = await resp.json()
        return [(f"{i['batch_id']}_{i['course_id']}", i['batch_name']) for i in data] if data else []

async def fetch_videos_pdfs(token, userid, course_id, bid, sid=0):
    v_url = f"https://web.kdcampus.live/android/Dashboard/course_details_video/{token}/{userid}/{course_id}/{bid}/0/{sid}/0"
    p_url = f"https://web.kdcampus.live/android/Dashboard/course_details_pdf/{token}/{userid}/{course_id}/{bid}/0/{sid}/0"

    async with session.get(v_url) as v_resp, session.get(p_url) as p_resp:
        videos = await v_resp.json(content_type=None)
        pdfs = await p_resp.json(content_type=None)

    results = []
    for v in reversed(videos or []):
        title = v.get('content_title', '').strip()
        url = v.get('jwplayer_id', '')
        if title and url:
            results.append(f"{title}: https://{url}")
    for p in reversed(pdfs or []):
        title = p.get('content_title', '').strip()
        filename = p.get('file_name', '')
        if title and filename:
            results.append(f"{title}: https://kdcampus.live/uploaded/content_data/{filename}")
    return results

async def extract_content(token, userid, batch_id):
    bid, course_id = batch_id.split('_')
    subj_url = f"https://web.kdcampus.live/android/Dashboard/course_subject/{token}/{userid}/{course_id}/{bid}"
    async with session.get(subj_url) as r:
        subj_data = await r.json(content_type=None)
        subjects = subj_data.get("subjects", [])

    tasks = []
    if not subjects:
        tasks.append(fetch_videos_pdfs(token, userid, course_id, bid))
    else:
        for s in subjects:
            sid = s["id"]
            tasks.append(fetch_videos_pdfs(token, userid, course_id, bid, sid))
    results = await asyncio.gather(*tasks)
    return [item for sublist in results for item in sublist]

async def kdcampus(app, query, message):
    try:
        ask_msg = await app.ask(message.chat.id, "**🔑 Send ID*Password**")
        mob, pwd = ask_msg.text.split('*', 1)
        password = hashlib.sha512(pwd.encode()).hexdigest()

        payload = {
            "code": "",
            "valid_id": "",
            "api_key": API_KEY,
            "mobilenumber": mob,
            "password": password
        }

        async with session.post("https://web.kdcampus.live/android/Usersn/login_user", json=payload) as r:
            resp = await r.json(content_type=None)

        if 'data' not in resp:
            return await message.reply_text("❌ Login Failed.")

        user_data = resp['data']
        token, userid = user_data['connection_key'], user_data['id']

        batches = await list_batches(token, userid)
        if not batches:
            return await message.reply_text("⚠️ No courses found.")

        batch_list_str = "\n".join([f"{bid}: {name}" for bid, name in batches])
        await message.reply_text(f"📦 **Available Batches:**\n\n{batch_list_str}")

        batch_id_msg = await app.ask(message.chat.id, "🔢 Enter batch ID:")
        batch_id = batch_id_msg.text.strip()

        start = time.time()
        all_urls = await extract_content(token, userid, batch_id)
        elapsed = round(time.time() - start, 2)

        if not all_urls:
            return await message.reply_text("⚠️ No content found.")

        v_count = sum('content_data' not in x for x in all_urls)
        p_count = sum('content_data' in x for x in all_urls)
        batch_name = next((n for b, n in batches if b == batch_id), "KD_Content")
        filename = f"{batch_name}.txt"

        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write('\n'.join(all_urls))

        caption = (
            f"**✅ App Name:** Kd Campus\n"
            f"**📚 Batch:** `{batch_name}`\n\n"
            f"🍿 **Videos:** `{v_count}` | 📝 **PDFs:** `{p_count}`\n"
            f"⏱️ **Time:** `{elapsed}s`"
        )

        await send_file(filename, caption, message, query)
        os.remove(filename)

    except Exception as e:
        await message.reply_text(f"❌ Error: `{e}`")
