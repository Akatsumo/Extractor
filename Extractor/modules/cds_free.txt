import re
import aiohttp
import datetime
import os
from pyrogram import filters
from pyrogram.types import Message
from Extractor import app
from Extractor.core.func import send_file
from config import API


DEFAULT_HEADERS = {
    "User-Agent": "Dart/3.2 (dart:io)",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "Accept-Encoding": "gzip"
}

BATCH_INFO = {
    "29": "ZULU OTA BATCH (CDS-2 2025)",
    "30": "ZULU MATHS BATCH (CDS-2 2025)",
    "31": "YANKEE BATCH (AFCAT-2 2025)",
    "32": "XRAY BATCH (NDA-2 2025)"
}
BATCH_TEXT = """
`29` : ZULU OTA BATCH (CDS-2 2025)  
`30` : ZULU MATHS BATCH (CDS-2 2025)  
`31` : YANKEE BATCH (AFCAT-2 2025)  
`32` : XRAY BATCH (NDA-2 2025)
"""


 
async def cds_free(app, query, message):
    await message.reply("Send your email or token:")
    raw_text = (await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)).text.strip()
    
    async with aiohttp.ClientSession() as session:
        headers = DEFAULT_HEADERS.copy()
        
        if "@" in raw_text:
            payload = {"url": "https://www.cdsjourney.com/api/login_or_register/", "method": "POST", "data": {"email": raw_text}, "headers": headers}
            async with session.post(f"{API}/proxy", json=payload) as resp:
                if resp.status != 200:
                    return await message.reply("Failed to generate OTP.")
            
            await message.reply("Enter OTP received on your email:")
            otp = (await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)).text.strip()
            
            if not otp.isdigit():
                return await message.reply("Invalid OTP format.")

            payload = {"url": "https://www.cdsjourney.com/api/verify_otp/", "method": "POST", "data": {"email": raw_text, "otp": otp}, "headers": headers}
            async with session.post(f"{API}/proxy", json=payload) as resp:
                if resp.status != 200:
                    return await message.reply("OTP verification failed.")
                token = (await resp.json())["access_token"]
                await message.reply(f"Login successful.\nYour token: `{token}`")
                headers["Authorization"] = f"Bearer {token}"
        else:
            headers["Authorization"] = f"Bearer {raw_text}"
            await message.reply("Token accepted.")

        await message.reply(f"{BATCH_TEXT}\nSend Batch ID(s) (use & to separate multiple):")
        batch_ids = (await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)).text.strip().split("&")

        for batch_id in batch_ids:
            start_time = datetime.datetime.now()
            urls = []
            batch_id = batch_id.strip()

            # Get batch name from BATCH_INFO dictionary
            batch_name = BATCH_INFO.get(batch_id)
            if not batch_name:
                await message.reply(f"Invalid batch ID: {batch_id}")
                continue

            try:
                # Get batch subjects
                payload = {"url": f"https://www.cdsjourney.com/api/batch-subject/{batch_id}/", "headers": headers}
                async with session.post(f"{API}/proxy", json=payload) as resp:
                    subjects = (await resp.json()).get("list", [])

                # Get recordings for each subject
                for subject in subjects:
                    s_id = subject['subject']['id']
                    s_name = subject['subject']['name']
                    
                    payload = {"url": f"https://www.cdsjourney.com/api/recordings/{s_id}/", "headers": headers}
                    async with session.post(f"{API}/proxy", json=payload) as resp:
                        recordings = (await resp.json()).get('recordings', [])
                        
                        for rec in recordings:
                            name = rec['title'].replace(":", "").replace("::", "").replace("||", "-")
                            urls.append(f"[{s_name}]-{name}: {rec['file_url']}")

                if urls:
                    # Use batch_name in the filename instead of batch_id
                    filename = f"{batch_name.replace(' ', '_').replace('(', '').replace(')', '')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("\n".join(urls))

                    duration = (datetime.datetime.now() - start_time).seconds

                    caption = (
                        f"**App Name: CDS JOURNEY**\n"
                        f"**Batch Name:** `{batch_name}`\n\n"
                        f"📝 **Total Links:** `{len(urls)}`\n"
                        f"⌚️ **Time Taken:** `{duration} seconds`"
                    )
    
                    return await send_file(filename, caption, message, query)
                    
            except Exception as e:
                await message.reply(f"Error processing batch {batch_id}: {str(e)}")
