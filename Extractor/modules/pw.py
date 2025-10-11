import aiohttp
import asyncio
import time
import traceback
import re
from typing import Dict, List, Tuple, Optional, Union
from Extractor.core.func import get_time
from pyrogram.enums import ParseMode
from config import LOGGER_ID
from Extractor.core.func import send_file


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format (10 digits)"""
    return bool(re.match(r'^\d{10}$', phone))

def validate_otp(otp: str) -> bool:
    """Validate OTP format (6 digits)"""
    return bool(re.match(r'^\d{6}$', otp))

async def make_api_request(session: aiohttp.ClientSession, method: str, url: str, **kwargs) -> Dict:
    """Make API request with error handling"""
    try:
        async with session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            data = await response.json()
            if not data.get('success', True):  # Some endpoints don't have 'success' field
                raise Exception(data.get('message', 'API request failed'))
            return data
    except aiohttp.ClientError as e:
        raise Exception(f"Request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

async def get_otp(session: aiohttp.ClientSession, phone_no: str) -> bool:
    """Request OTP with validation"""
    if not validate_phone_number(phone_no):
        raise Exception("Phone number must be 10 digits")

    url = "https://api.penpencil.co/v1/users/get-otp"
    headers = {
        'client-version': '4.0.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.pw.live/',
        'randomId': '30f1f1c2-f4ca-4610-a25b-f7f5aaacc051',
        'client-id': '5eb393ee95fab7468a79d189',
        'Client-Type': 'WEB',
    }
    params = {'smsType': '0'}
    json_data = {
        'username': phone_no,
        'countryCode': '+91',
        'organizationId': '5eb393ee95fab7468a79d189',
    }
    
    response = await make_api_request(session, 'POST', url, params=params, headers=headers, json=json_data)
    return response['success']

async def get_token(session: aiohttp.ClientSession, phone_no: str, otp: str) -> str:
    """Get access token with validation"""
    if not validate_otp(otp):
        raise Exception("OTP must be 6 digits")

    url = "https://api.penpencil.co/v3/oauth/token"
    json_data = {
        'username': phone_no,
        'otp': otp,
        'client_id': 'system-admin',
        'client_secret': 'KjPXuAVfC5xbmgreETNMaL7z',
        'grant_type': 'password',
        'organizationId': '5eb393ee95fab7468a79d189',
        'latitude': 0,
        'longitude': 0,
    }
    headers = {
        'client-version': '4.0.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.pw.live/',
        'randomId': '30f1f1c2-f4ca-4610-a25b-f7f5aaacc051',
        'client-id': '5eb393ee95fab7468a79d189',
        'Client-Type': 'WEB',
    }
    
    response = await make_api_request(session, 'POST', url, headers=headers, json=json_data)
    return response['data']['access_token']

async def pw_mobile(app, query, msg):
    """Handle mobile-based authentication flow"""
    try:
        await msg.edit_text("**🔑 Enter your Mobile No. (10 digits without country code)...**")
        input1 = await app.listen(chat_id=msg.chat.id, user_id=query.from_user.id)
        phone_no = input1.text.strip()
        await input1.delete()

        if not phone_no:
            await msg.edit_text("**❌ Phone number cannot be empty!**")
            return

        async with aiohttp.ClientSession() as session:
            try:
                if await get_otp(session, phone_no):
                    await msg.edit_text("🔑 **ENTER YOUR 6-DIGIT OTP**")
                    input2 = await app.listen(chat_id=msg.chat.id, user_id=query.from_user.id)
                    otp = input2.text.strip()
                    await input2.delete()

                    if not otp:
                        await msg.edit_text("**❌ OTP cannot be empty!**")
                        return
                    
                    token = await get_token(session, phone_no, otp)
                    await msg.reply_text(f"**YOUR TOKEN** => `{token}`")
                    return await pw_login(session, query, app, msg, token)
                else:
                    await msg.edit_text("**❌ Failed to Generate OTP. Please try again.**")
            except Exception as e:
                if "must be 10 digits" in str(e):
                    await msg.edit_text("**❌ Invalid phone number! Please enter 10 digits.**")
                elif "must be 6 digits" in str(e):
                    await msg.edit_text("**❌ Invalid OTP! Please enter 6 digits.**")
                else:
                    await msg.edit_text(f"**❌ Error: {str(e)}**")
    except Exception as e:
        await msg.edit_text(f"**❌ Unexpected error: {str(e)}**")
        print(f"Error in pw_mobile_free: {traceback.format_exc()}")

async def pw_token(app, query, msg):
    """Handle token-based authentication flow"""
    try:
        await msg.edit_text("**🔑 Enter PW TOKEN...**")
        input1 = await app.listen(chat_id=msg.chat.id, user_id=query.from_user.id)
        token = input1.text.strip()
        await input1.delete()
        
        if not token:
            await msg.edit_text("**❌ Token cannot be empty!**")
            return
            
        async with aiohttp.ClientSession() as session:
            return await pw_login(session, query, app, msg, token)
    except Exception as e:
        await msg.edit_text(f"**❌ Error: {str(e)}**")
        print(f"Error in pw_token_free: {traceback.format_exc()}")

async def pw_login(session: aiohttp.ClientSession, query, app, msg, token: str):
    """Handle login process with error handling"""
    try:
        headers = {
            'Host': 'api.penpencil.co',
            'authorization': f"Bearer {token}",
            'client-id': '5eb393ee95fab7468a79d189',
            'client-version': '12.84',
            'user-agent': 'Android',
            'randomid': 'e4307177362e86f1',
            'client-type': 'MOBILE',
            'device-meta': '{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}',
            'content-type': 'application/json; charset=UTF-8',
        }
        params = {
            'mode': '1',
            'filter': 'false',
            'organisationId': '5eb393ee95fab7468a79d189',
            'limit': '100',
            'page': '1',
            'ut': '1652675230446',
        }

        # Get batches
        try:
            response = await make_api_request(
                session,
                'GET',
                'https://api.penpencil.co/v3/batches/my-batches',
                headers=headers,
                params=params
            )
            
            if not response.get('data'):
                await msg.edit_text("**❌ No batches found for this account**")
                return None, None, None
                
            batch_list = "\n".join([
                f"**{data['name']}**   :   `{data['_id']}`" 
                for data in response["data"]
            ])
            
            await msg.edit_text(
                f"**BATCH NAME   :   BATCH ID**\n\n{batch_list}\n\n"
                "**Now send the Batch ID to Download**"
            )
        except Exception as e:
            await msg.edit_text("**❌ Failed to fetch batches. Please check your token.**")
            return None, None, None

        # Get batch ID
        ip = await app.listen(chat_id=msg.chat.id, user_id=query.from_user.id)
        batch_id = ip.text.strip()
        await ip.delete()
        
        if not batch_id:
            await msg.edit_text("**❌ Batch ID cannot be empty!**")
            return None, None, None

        # Validate batch details
        try:
            response = await make_api_request(
                session,
                'GET',
                f'https://api.penpencil.co/v3/batches/{batch_id}/details',
                headers=headers,
                params=params
            )
        except Exception:
            await msg.edit_text("**❌ Invalid Batch ID or access denied**")
            return None, None, None

        batch_data = response['data']
        batch_name = batch_data['name'].replace("/", "")
        subjects = batch_data.get('subjects', [])

        if not subjects:
            await msg.edit_text("**❌ No subjects found in this batch**")
            return None, None, None

        # Format subject list
        subject_list = "\n".join([
            f"**{subject.get('subject')}**   :   `{subject.get('subjectId')}`"
            for subject in subjects
        ])
        all_subjects = "&".join([subject.get('subjectId') for subject in subjects])

        await msg.edit_text(
            f"**SUBJECT   :   SUBJECT ID**\n\n{subject_list}\n\n"
            f"Now send the **Subject IDs** to Download\n\n"
            f"Send like this **1&2&3&4** so on\n"
            f"or copy paste or edit **below ids** according to you :\n\n"
            f"**Enter this to download full batch :-**\n`{all_subjects}`"
        )

        # Get subject selection
        ip2 = await app.listen(chat_id=msg.chat.id, user_id=query.from_user.id)
        subject_ids = ip2.text.strip().split('&')
        await ip2.delete()

        if not subject_ids or not all(subject_ids):
            await msg.edit_text("**❌ Invalid subject selection**")
            return None, None, None

        await msg.edit_text("**📥 Extracting Videos Links Please Wait...**")
        start_time = time.time()

        # Process subjects
        tasks = []
        for subject_id in subject_ids:
            for subject in subjects:
                if subject.get('subjectId') == subject_id:
                    tasks.append(pw_data(
                        session,
                        subject.get('subject'),
                        subject.get('slug'),
                        batch_id,
                        headers
                    ))

        results = await asyncio.gather(*tasks)

        # Process results
        total_v_count = sum(result['v_count'] for result in results)
        total_p_count = sum(result['p_count'] for result in results)
        content = "".join(result['content'] for result in results)

        if not content.strip():
            await msg.edit_text("**❌ No content found for selected subjects**")
            return None, None, None

        end_time = time.time()
        elapsed = get_time(end_time - start_time)

        caption = (
            f"**App Name :- Physics Wallah**\n"
            f"**Batch Name :-** `{batch_name}`\n\n"
            f"🍿 **Total Videos**: `{total_v_count}`\n"
            f"📝 **Total PDFs**: `{total_p_count}`\n"
            f"⌚️ **Time Taken**: `{elapsed}`"
        )

        filename = f"{batch_name}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        return await send_file(filename, caption, msg, query)

    except Exception as e:
        await msg.edit_text(f"**❌ Error: {str(e)}**")
        print(f"Error in pw_login: {traceback.format_exc()}")
        return None, None, None

async def pw_data(
    session: aiohttp.ClientSession,
    subject: str,
    subject_slug: str,
    batch_slug: str,
    headers: Dict
) -> Dict:
    """Fetch data for a subject with error handling"""
    try:
        v_count = 0
        p_count = 0
        content = []
        
        page = 1
        max_retries = 3
        
        while True:
            for retry in range(max_retries):
                try:
                    response = await make_api_request(
                        session,
                        'GET',
                        f"https://api.penpencil.co/v2/batches/{batch_slug}/subject/{subject_slug}/topics",
                        params={'page': str(page)},
                        headers=headers
                    )
                    
                    if not response.get("data"):
                        return {
                            'content': "".join(content),
                            'v_count': v_count,
                            'p_count': p_count
                        }
                    
                    tasks = [
                        pw_data2(session, subject, subject_slug, topic, batch_slug, headers)
                        for topic in response["data"]
                    ]
                    
                    results = await asyncio.gather(*tasks)
                    
                    for result in results:
                        content.append(result['content'])
                        v_count += result['v_count']
                        p_count += result['p_count']
                    
                    page += 1
                    break
                    
                except Exception as e:
                    if retry == max_retries - 1:
                        print(f"Failed to fetch page {page} for subject {subject} after {max_retries} retries: {e}")
                        return {
                            'content': "".join(content),
                            'v_count': v_count,
                            'p_count': p_count
                        }
                    await asyncio.sleep(1)  # Wait before retry
                    
    except Exception as e:
        print(f"Error in pw_data for subject {subject}: {traceback.format_exc()}")
        return {'content': "", 'v_count': 0, 'p_count': 0}

async def pw_data2(
    session: aiohttp.ClientSession,
    subject: str,
    subject_slug: str,
    topic: Dict,
    batch_slug: str,
    headers: Dict
) -> Dict:
    """Fetch detailed content for a topic with error handling"""
    try:
        content = []
        v_count = 0
        p_count = 0
        
        content_types = ["videos", "notes", "DppNotes", "DppVideos"]
        max_retries = 3
        
        for content_type in content_types:
            page = 1
            while True:
                for retry in range(max_retries):
                    try:
                        params = {
                            "page": str(page),
                            "contentType": content_type,
                            "tag": topic['slug']
                        }
                        
                        response = await make_api_request(
                            session,
                            'GET',
                            f"https://api.penpencil.co/v2/batches/{batch_slug}/subject/{subject_slug}/contents",
                            params=params,
                            headers=headers
                        )
                        
                        if not response.get("data"):
                            break
                            
                        items = response["data"]
                        items.reverse()

                        for item in items:
                            if content_type in ["videos", "DppVideos"]:
                                video_details = item.get('videoDetails', {})
                                if video_details:
                                    video_url = (
                                        video_details.get('videoUrl')
                                        or video_details.get('embedCode')
                                        or ''
                                    )
                                    if video_url:
                                        content.append(
                                            f"({subject}) {item['topic']} : {video_url}&parentId={batch_slug}&childId={item.get('_id')}\n"
                                        )
                                        v_count += 1
                            else:
                                for homework in item.get('homeworkIds', []):
                                    topic_name = homework.get('topic', '')
                                    for attachment in homework.get('attachmentIds', []):
                                        if attachment.get('baseUrl') and attachment.get('key'):
                                            content.append(
                                                f"({subject}) {topic_name} : {attachment['baseUrl']}{attachment['key']}\n"
                                            )
                                            p_count += 1
                                            
                        page += 1
                        break
                        
                    except Exception as e:
                        if retry == max_retries - 1:
                            print(f"Failed to fetch {content_type} page {page} after {max_retries} retries: {e}")
                            break
                        await asyncio.sleep(1)  # Wait before retry
                        
                if not response.get("data"):
                    break
                    
        return {
            'content': "".join(content),
            'v_count': v_count,
            'p_count': p_count
        }
        
    except Exception as e:
        print(f"Error in pw_data2: {traceback.format_exc()}")
        return {'content': "", 'v_count': 0, 'p_count': 0}
