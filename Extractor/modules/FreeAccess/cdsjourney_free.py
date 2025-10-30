import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout

# --------------------------- Batch-Data --------------------------- #
batch_data = {
    "29": "Zulu OTA batch (CDS-2 2025)",
    "30": "Zulu MATHS batch (CDS-2 2025)",
    "31": "Yankee batch (AFCAT-2 2025)",
    "32": "Xray batch (NDA-2 2025)",
    "34": "Alpha OTA batch (CDS 1 2026)",
    "35": "Alpha MATH batch (CDS 1 2026)",
    "36": "Bravo GAT batch (NDA 1 2026)",
    "37": "Charlie Batch (AFCAT 1 2026)",
    "38": "Bravo MATH batch (NDA 1 2026)",
    "39": "CAPF Paper 1 + Paper 2 Delta batch (CAPF 2026)",
    "40": "CAPF Paper 2 Delta batch (CAPF 2026)",
}

# --------------------------- Course-Content --------------------------- #

async def course_content(session, headers, batch_id):
    lectures, v_count, p_count = [], 0, 0

    response = session.get(f"https://www.cdsjourney.com/api/batch-subject/{batch_id}/", headers=headers)
    if response.status_code != 200:
        return lectures, v_count, p_count

    subjects = response.json().get("list", [])
    if not subjects:
        return lectures, v_count, p_count
        
    for subject in subjects:
        sub_id = subject['subject']['id']
        sub_name = subject['subject']['name']

        response = session.get(f"https://www.cdsjourney.com/api/recordings/{sub_id}/", headers=headers)
        if response.status_code != 200:
            return [], 0, 0

        data = response.json()
        recordings = data.get('recordings', [])
        if not recordings:
            continue

        for rec in recordings:
            v_count += 1
            name = rec['title'].replace(":", "").replace("::", "").replace("||", "-")
            url = rec.get('file_url', 'N/A')
            lectures.append(f"[{sub_name}] - {name}: {url}")

    return lectures, v_count, p_count


# --------------------------- Cds-Journey-Access --------------------------- #

async def cdsjourney_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    try:
        msg = await message.reply_text("**Fetching CDS Journey All Batches, Please Wait...**")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Accept-Encoding": "gzip"
        }
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2MzQwMjc2LCJpYXQiOjE3NjExNTYyNzYsImp0aSI6ImZiMjFlYjA4MmJiNjRhYTk5MmQ0N2M0NjE5YjNkYmQ3IiwidXNlcl9pZCI6NDE5NDEyfQ.rmpi91wHnhn3NiHmfyQEJ0CeqB2dZ6qGUgEMMDlqQxI"

        if not token:
            await msg.edit_text("Enter your login Gmail:")
            input1 = await app.listen(user_id=user_id, timeout=30)
            email = input1.text.strip()
            await input1.delete()

            response = session.post("https://www.cdsjourney.com/api/login_or_register/", data={"email": email})
            if response.status_code != 200:
                return await msg.edit_text("Failed to login, Something went wrong!")

            await msg.edit_text("Enter OTP received on your email:")
            input2 = await app.listen(user_id=user_id, timeout=30)
            otp = input2.text.strip()
            await input2.delete()

            response = session.post("https://www.cdsjourney.com/api/verify_otp/", data={"email": email, "otp": otp})
            if response.status_code != 200:
                return await msg.edit_text("OTP verification failed, Try again!")

            token = response.json().get("access_token")
            await message.reply(f"✅ Login successful.\n\nYour token: `{token}`")

        headers["Authorization"] = f"Bearer {token}"

        batch_list = "📚 **Available Batches:**\n\n"
        for course_id, name in batch_data.items():
            batch_list += f"`{course_id}` - **{name}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"civilguruji_batchList_{user_id}.txt"
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

        batch_name = batch_data.get(batch_id)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        msg = await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, headers, batch_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No batch content found.")

        file_name = f"{batch_name.replace('/', '_')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Cds Journey`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )

        await main_func.send_file(app, file_name, user_id, caption, thumb)
        await msg.delete()
    except ListenerTimeout:
        await message.reply_text("**⏳ Oops! Time's Up, You didn’t reply in time.**")
    except Exception as e:
        await message.reply_text(f"**Error**: `{e}`")
