import hashlib
import httpx
import time
import os
from Extractor import app   
from pyrogram import filters


API_KEY = "kdc123"

async def list_batches(token, userid):
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://web.kdcampus.live/android/Dashboard/get_mycourse_data_renew_new/{token}/{userid}/4')
        resp = r.json()

    if not resp:
        return []

    return [(f"{i['batch_id']}_{i['course_id']}", i['batch_name']) for i in resp]

async def extract_content(token, userid, batch_id):
    all_urls = []
    bid, course_id = batch_id.split('_')

    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://web.kdcampus.live/android/Dashboard/course_subject/{token}/{userid}/{course_id}/{bid}")
        subjects_data = r.json()

        if 'subjects' not in subjects_data or not subjects_data['subjects']:
            r = await client.get(f"https://web.kdcampus.live/android/Dashboard/course_details_video/{token}/{userid}/{course_id}/{bid}/0/0/0")
            videos = r.json()
            for video in reversed(videos or []):
                title = video.get('content_title', '').strip()
                url = video.get('jwplayer_id', '')
                if title and url:
                    all_urls.append(f"{title}: https://{url}")

            r = await client.get(f"https://web.kdcampus.live/android/Dashboard/course_details_pdf/{token}/{userid}/{course_id}/{bid}/0/0/0")
            pdfs = r.json()
            for pdf in reversed(pdfs or []):
                title = pdf.get('content_title', '').strip()
                filename = pdf.get('file_name', '')
                if title and filename:
                    all_urls.append(f"{title}: https://kdcampus.live/uploaded/content_data/{filename}")
        else:
            for subject in subjects_data['subjects']:
                sid = subject['id']

                r = await client.get(f"https://web.kdcampus.live/android/Dashboard/course_details_video/{token}/{userid}/{course_id}/{bid}/0/{sid}/0")
                videos = r.json()
                for video in reversed(videos or []):
                    title = video.get('content_title', '').strip()
                    url = video.get('jwplayer_id', '')
                    if title and url:
                        all_urls.append(f"{title}: https://{url}")

                r = await client.get(f"https://web.kdcampus.live/android/Dashboard/course_details_pdf/{token}/{userid}/{course_id}/{bid}/0/{sid}/0")
                pdfs = r.json()
                for pdf in reversed(pdfs or []):
                    title = pdf.get('content_title', '').strip()
                    filename = pdf.get('file_name', '')
                    if title and filename:
                        all_urls.append(f"{title}: https://kdcampus.live/uploaded/content_data/{filename}")

    return all_urls



@app.on_message(filters.command("kd"))
async def kdcampus(app, query, message):
    try:
        ask_msg = await app.ask(
            message.chat.id,
            "**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**"
        )

        mob, pwd = ask_msg.text.split('*', 1)
        password = hashlib.sha512(pwd.encode()).hexdigest()

        payload = {
            "code": "",
            "valid_id": "",
            "api_key": API_KEY,
            "mobilenumber": mob,
            "password": password
        }

        headers = {
            "User-Agent": "okhttp/4.10.0",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json; charset=UTF-8"
        }

        async with httpx.AsyncClient() as client:
            r = await client.post("https://web.kdcampus.live/android/Usersn/login_user", json=payload, headers=headers)
            resp = r.json()

        if 'data' not in resp:
            await message.reply_text("❌ Login Failed. Please check your credentials.")
            return

        user_data = resp['data']
        token = user_data['connection_key']
        userid = user_data['id']

        batches = await list_batches(token, userid)
        if not batches:
            await message.reply_text("⚠️ No courses found.")
            return

        batch_list_str = "\n".join([f"{bid}: {name}" for bid, name in batches])
        await message.reply_text(f"📦 **Available Batches:**\n\n{batch_list_str}")
        batch_id_msg = await app.ask(message.chat.id, "🔢 Enter the batch ID from the list above:")
        batch_id = batch_id_msg.text.strip()

        start_time = time.time()
        all_urls = await extract_content(token, userid, batch_id)
        elapsed = round(time.time() - start_time, 2)

        if not all_urls:
            await message.reply_text("⚠️ No content found in the selected batch.")
            return

        v_count = len([x for x in all_urls if 'https://' in x and 'content_data' not in x])
        p_count = len([x for x in all_urls if 'content_data' in x])
        batch_name = next((name for bid, name in batches if bid == batch_id), "extracted_content")
        filename = f"{batch_name}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_urls))

        caption = (
            f"**✅ App Name:** Kd Campus\n"
            f"**📚 Batch Name:** `{batch_name}`\n\n"
            f"🍿 **Total Videos:** `{v_count}`\n"
            f"📝 **Total PDFs:** `{p_count}`\n"
            f"⏱️ **Time Taken:** `{elapsed} seconds`"
        )

        await message.reply_document(filename)
        os.remove(filename)

    except Exception as e:
        await message.reply_text(f"❌ Error:\n`{e}`")
