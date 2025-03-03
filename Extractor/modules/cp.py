import aiofiles
import aiohttp
import requests, os, sys, re
import json, asyncio
import subprocess
import datetime
from Extractor import app
from pyrogram import filters, idle
from subprocess import getstatusoutput
import time
from Extractor.core.more_func import get_time


api = 'https://api.classplusapp.com/v2'

headers = {
    "Host": "api.classplusapp.com",
    "User-Agent": "Mobile-Android",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Origin": "https://web.classplusapp.com",
    "Referer": "https://web.classplusapp.com/",
    "Region": "IN",
    "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

v_count = 0
p_count = 0


async def get_course_content(session, course_id, msg, folder_id=0):
    vt = ""
    async with session.get(f'{api}/course/content/get', headers=headers, params={'courseId': course_id, 'folderId': folder_id}) as res:
        if res.status == 200:
            res_json = await res.json()
            contents = res_json.get('data', {}).get('courseContent', [])
            tasks = [get_data(session, course_id, msg, content) for content in contents]
            results = await asyncio.gather(*tasks)
            for result in results:
                vt += result
            return vt
                
        else:
            raise Exception('Failed to fetch course content.')


async def get_data(session, course_id, msg, content):
    global v_count, p_count
    prev_v_count = v_count
    prev_p_count = p_count
    counter = 0
    try:
        fetched_contents = ""
        if content['contentType'] == 1:
            sub_contents = await get_course_content(session, course_id, msg, content['id'])
            fetched_contents += sub_contents
        elif content['contentType'] == 2:
            name = content.get('name', '')
            id = content.get('contentHashId', '')
            async with session.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params={'contentId': id}) as r:
                signed_url_data = await r.json()
                url = signed_url_data['url']
                content = f'{name}:{url}\n'
                fetched_contents += content
                v_count += 1
        else:
            name = content.get('name', '')
            url = content.get('url', '')
            content = f'{name}:{url}\n'
            fetched_contents += content
            p_count += 1

        counter += 1
        if counter % 3 == 0 and (prev_v_count != v_count or prev_p_count != p_count):
            await msg.edit_text(f"**Extracting Videos Links Please Wait  📥**\n\n🍿 **Total Video**  - `{v_count}`\n📝 **Total Pdf**  - `{p_count}`")
            prev_v_count = v_count
            prev_p_count = p_count
            
        return fetched_contents
    except Exception as e:
        print(f"An error occurred in course_content2: {str(e)}")
        raise


async def classplus_data(session, query, message, user_id, msg):
    global v_count, p_count
    try:
        start = time.time()
        params = {'userId': user_id, 'tabCategoryId': 3}
        async with session.get(f'{api}/profiles/users/data', headers=headers, params=params) as res:
            if res.status == 200:
                courses_data = await res.json()
                courses = courses_data.get('data', {}).get('responseData', {}).get('coursesData', [])
                if courses:
                    text = '\n'.join([f"{cnt + 1}. {course['name']}" for cnt, course in enumerate(courses)])
                    await msg.edit_text(f"**send index number of the course to download\n\n{text}**")
                    input2 = await app.listen(user_id=query.from_user.id)
                    num = int(input2.text.strip())
                    await input2.delete(True)
                    if 1 <= num <= len(courses):
                        selected_course = courses[num - 1]
                        await msg.edit_text("**Extracting Videos Links Please Wait  📥 **")
                        course_content = await get_course_content(session, selected_course['id'], msg)
                        if course_content:
                            end = time.time()
                            duration_seconds = end - start
                            elapsed = get_time(duration_seconds)
                            cap = f"**App Name :- Classplus\nBatch Name :-** `{selected_course['name']}`\n\n🍿 **Total Video**: `{v_count}`\n📝 **Total pdf**: `{p_count}`\n⌚️**Time Taken**: `{elapsed}`"
                            async with aiofiles.open("Classplus.txt", mode='w') as f:
                                await f.write(course_content)
                            await message.reply_document(document="Classplus.txt", caption=cap)
                            await msg.delete()
                            os.remove("Classplus.txt")
                        else:
                            raise Exception('Did not find any content in the course.')
                    else:
                        raise Exception('Invalid input or index out of range.')
                else:
                    raise Exception('No courses found.')
            else:
                raise Exception('Failed to get courses.')
    except Exception as e:
        print(f"Error: {e}")



async def classplus_txt(app, query, message):
    try:
        async with aiohttp.ClientSession() as session:
            msg = await message.reply_text("**SEND YOUR CREDENTIALS AS SHOWN BELOW\n\nORGANISATION CODE:\nPHONE NUMBER:\n\nOR SEND\nACCESS TOKEN:**")
            input1 = await app.listen(user_id=query.from_user.id)
            creds = input1.text.strip()
            await input1.delete(True)
            if '\n' in creds:
                org_code, phone_no = [cred.strip() for cred in creds.split('\n')]
                if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                    async with session.get(f'{api}/orgs/{org_code}') as resp:
                        if resp.status == 200:
                            org_data = await resp.json()
                            org_id = int(org_data['data']['orgId'])
                        else:
                            raise Exception('Failed to get organization Id.')
                    
                    data = {
                        'countryExt': '91',
                        'orgCode': org_code,
                        'viaSms': '1',
                        'viaEmail': '0',
                        'retry': 0,
                        'orgId': org_id,
                        'otpCount': 0,
                        'mobile': phone_no,
                    }

                    async with session.post(f'{api}/otp/generate', json=data, headers=headers) as otp_resp:
                        if otp_resp.status == 200:
                            otp_data = await otp_resp.json()
                            session_id = int(otp_data['data']['sessionId'])
                        else:
                            raise Exception('Failed to generate OTP.')

                    await msg.edit_text("**SEND YOUR OTP...**")
                    user_otp = await app.listen(user_id=query.from_user.id)
                    if user_otp.text.isdigit():
                        otp = user_otp.text.strip()
                    else:
                        raise Exception('OTP is not a number.')

                    json_data = {
                        'otp': otp,
                        'countryExt': '91',
                        'sessionId': session_id,
                        'orgId': org_id,
                        'fingerprintId': '',
                        'mobile': phone_no,
                    }

                    async with session.post(f'{api}/users/verify', json=json_data, headers=headers) as verify_resp:
                        verify_data = await verify_resp.json()
                        if verify_data['status'] == 'success':
                            user_id = verify_data['data']['user']['id']
                            token = verify_data['data']['token']
                            headers['x-access-token'] = token
                            await msg.edit_text(f"Login Successfully\n\n`{token}`")
                            await classplus_data(session, query, message, user_id, msg)
                        else:
                            raise Exception('Failed to verify OTP.')
                else:
                    raise Exception('Invalid organization code or phone number.')
            else:
                token = creds
                headers['x-access-token'] = token
                async with session.get(f'{api}/users/details', headers=headers) as user_details_resp:
                    if user_details_resp.status == 200:
                        user_data = await user_details_resp.json()
                        user_id = user_data['data']['responseData']['user']['id']
                        await classplus_data(session, query, message, user_id, msg)
                    else:
                        raise Exception('Failed to get user details.')
    except Exception as e:
        print("An error occurred:", e)
    finally:
        await session.close()
