import re
import json
import os
import asyncio
import aiohttp
import requests
import threading
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from pyrogram import filters
from Extractor import app
from config import LOGGER_ID
from Extractor.core.func import send_file



async def check_url(url: str, session) -> bool:
    """Check if a URL is reachable"""
    try:
        async with session.head(url) as response:
            return response.status == 200
    except aiohttp.ClientError:
        return False


async def unc_data(message, code, token):
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        burl = f"https://unacademy.com/api/v3/batch/{code}/details/"
        bd = requests.get(burl, headers=headers).json()
        mm = bd['name']
        start = bd['starts_at']
        epoch = int(datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").timestamp())
        limit = int(bd['lessons_count'])

        batch_results = []

        url = f"https://unacademy.com/api/v1/batch/{code}/schedule/"
        while True:
            payload = {
                'offset': epoch,
                'timezone_difference': 330,
                'limit': 200
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=payload, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    results = data.get('results', [])

                    batch_results.extend(results)

                    for result in reversed(results):
                        if result.get('type') == 'post':
                            date_string = result.get('properties', {}).get('started_at')
                            if date_string:
                                date_time = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
                                next_day = date_time + timedelta(days=1)
                                epoch = int(next_day.timestamp())
                                break

                    if len(batch_results) >= limit:
                        break
            
        vj = ""
        for result in batch_results:
            if result.get('type') == 'post':
                try:
                    m = result['properties']
                    title = m['name']
                    faculty = f"#{m['author']['first_name'].replace(' ', '_')}_{m['author']['last_name'].replace(' ', '_')}"
                    date_string = m.get('started_at')
                    if date_string:
                        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d-%m-%Y")
                    else:
                        date = "Class Cancelled"
         
                    video_url = m.get('video_url')
                    if video_url:
                        vurl = f"https://uamedia.uacdn.net/lesson-raw/{re.search(r'uid=([^&]+)', video_url).group(1)}/output.webm"
                        async with aiohttp.ClientSession() as session:
                            if not await check_url(vurl, session):
                                vurl = f"https://uamedia.uacdn.net/lesson-raw/{re.search(r'uid=([^&]+)', video_url).group(1)}/hls/master.m3u8"
                    else:
                        vurl = 'None'

                    p = m.get('slides_pdf', {})
                    if p:
                        purl = p.get('with_annotation')
                    else:
                        purl = 'None'
         
                    vj += f"{title} »» {faculty} »» {date} : {vurl}\n{title} : {purl}\n"
                except KeyError:
                    continue

        cap = f"**App Name :- Unacademy\nBatch Name :-** `{mm}`"
        file_path = f"{mm}.txt"
        with open(file_path, 'w') as f:
            f.write(f"{vj}")

        return file_path, cap

    except Exception as e:
        print(str(e))



async def unac_batch(app, query, message):
    await message.reply_text("**Send your Unacademy Token...**")
    input1 = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
    token = input1.text
    await input1.delete()

    await message.reply_text("✅ **Login Successful \n\n NOW SEND BATCH LINK...**")
    input2 = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
    link = input2.text
    await input2.delete()
    code = link.split('/')[-1]
   
    prog = await message.reply_text("**Extracting Videos Links Please Wait  📥 **")

    try:
        filename, cap = await unc_data(message, code, token)
        return await send_file(filename, cap, prog, query)
    except Exception as e:
        print(str(e))
        await message.reply_text(f"❌ **An error occurred: {str(e)}**")
        return None
