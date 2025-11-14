import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout



# ----------------------- CSRF Token ----------------------- #

async def csrf_token(session):
  url = "https://userapi.adda247.com/csrf/token?src=aweb"
  response = session.get(url)
  data = response.json()
  if data["success"]:
    return data["data"]
  else:
    return None



# ----------------------- Course Extractor ----------------------- #

async def course_extract(session, headers, course_id):
    lectures = []
    try:
        params = {
            'purchasedPackage': course_id,
            'src': 'aweb'
        }

        response = await session.get(
            "https://store.adda247.com/api/v1/ppc/package/bookmark",
            headers=headers,
            params=params
        )
        package_output = (await response.json())["data"]["bookmarkedPackages"]

        for package in package_output:
            package_id = package.get('packageId')
            title = package.get('title')

            params = {
                'packageId': package_id,
                'contentType': 'ONLINE_LIVE_CLASSES',
                'pageNo': 0,
                'src': 'aweb'
            }

            response = await session.get(
                "https://store.adda247.com/api/v1/syllabus/ppc/subjects",
                headers=headers,
                params=params
            )
            response_json = await response.json()
            syllabus_output = response_json.get('data', {}).get('syllabus', [])

            for syllabus in syllabus_output:
                syllabus_id = syllabus.get('id')
                syllabus_level = syllabus.get('level')

                params = {
                    'packageId': package_id,
                    'contentType': 'ONLINE_LIVE_CLASSES',
                    'syllabusId': syllabus_id,
                    'level': syllabus_level,
                    'pageNo': 0,
                    'src': 'aweb'
                }

                response = await session.get(
                    "https://store.adda247.com/api/v1/syllabus/ppc/getSubjectGroupAndChapter",
                    headers=headers,
                    params=params
                )
                response_json = await response.json()
                subject_output = response_json.get('data', {}).get('syllabus', [])

                for subject in subject_output:
                    subject_id = subject.get('id')
                    subject_level = subject.get('level')

                    params = {
                        'contentType': 'ONLINE_LIVE_CLASSES',
                        'packageId': package_id,
                        'level': subject_level,
                        'syllabusId': subject_id,
                        'pageNo': 0,
                        'pageSize': 20,
                        'status': 1,
                        'src': 'aweb'
                    }

                    response = await session.get(
                        "https://liveclasses.adda247.com/api/v1/ppc/OLC/content",
                        headers=headers,
                        params=params
                    )
                    response_json = await response.json()
                    content_output = response_json.get('data', {}).get('content', [])

                    total_items = response_json.get('data', {}).get('total', 0)
                    page_size = 20
                    page_count = math.ceil(total_items / page_size)

                    for page_number in range(page_count):
                        params['pageNo'] = page_number
                        response = await session.get(
                            "https://liveclasses.adda247.com/api/v1/ppc/OLC/content",
                            headers=headers,
                            params=params
                        )
                        response_json = await response.json()
                        content_output = response_json.get('data', {}).get('content', [])

                        for content in content_output:
                            name = content.get('name', 'Unknown')
                            url = content.get('url', None)
                            pdf = content.get('pdfFileName', None)
                            dpp_files = content.get('dppFileNames', [])

                            if url:
                               lectures.append(f"{name}: {url}")

                            if pdf:
                               lectures.append(f"{name}: https://store.adda247.com/{pdf}")

                            if dpp_files:
                               for dpp_file in dpp_files:
                                 lectures.append(f"{name}: https://store.adda247.com/{dpp_file}")

    except Exception as e:
        print(f"Error In Course Extract: {e}")

    return lectures


# ----------------------- Direct-Links ----------------------- #

async def direct_links(session, headers, course_id):
    lectures = []
    params = {
        'packageId': course_id,
        'category': 'ONLINE_LIVE_CLASSES',
        'isComingSoon': 'false',
        'pageNumber': '0',
        'pageSize': '10',
        'src': 'aweb'
    }

    try:
        response = session.get("https://store.adda247.com/api/v3/ppc/package/child", headers=headers, params=params)
        subject_output = response.json().get('data', {}).get('packages', [])
        total_items = response.json().get('data', {}).get('packagesCount', 0)
        page_size = 10
        page_count = math.ceil(total_items / page_size)
      
        print(f"Total pages: {page_count}")
        for page_number in range(page_count):
            params['pageNumber'] = str(page_number)
            response = session.get("https://store.adda247.com/api/v3/ppc/package/child", headers=headers, params=params)
            subject_output = response.json().get('data', {}).get('packages', [])

            for data in subject_output:
                try:
                    package_id = data.get("packageId")
                    response = session.get(f"https://store.adda247.com/api/v1/my/purchase/OLC/{package_id}?src=aweb", headers=headers)
                    content_output = response_json.get('data', {}).get('onlineClasses', [])

                    for content in content_output:
                        name = content.get('name', 'Unknown')
                        url = content.get('url', None)
                        pdf = content.get('pdfFileName', None)
                        dpp_files = content.get('dppFileNames', [])

                        if url:
                            lectures.append(f"{name}: {url}")

                        if pdf:
                            lectures.append(f"{name}: https://store.adda247.com/{pdf}")

                        if dpp_files:
                            for dpp_file in dpp_files:
                                lectures.append(f"{name}: https://store.adda247.com/{dpp_file}")

                except Exception as e:
                    print(f"Error fetching package details for package {package_id}: {e}")
            
    except Exception as e:
        print(f"Error fetching course details: {e}")

    return lectures



# ----------------------- Adda-Command ----------------------- #

async def adda_login(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    try:
        session = requests.Session()
        headers = {
            "X-Auth-Token": "fpoa43edty5",
            "Content-Type": "application/json",
            "dName": "Chrome on Windows Desktop",
            "LOGIN_TYPE": "1",
            "X-JWT-Token": ""
        }

        crf_token = await csrf_token(session)
        headers.update({"X-CSRF-Token": crf_token})

        msg = await message.reply_text("🔑 Enter login credentials (Email*Password or Token):")
        input1 = await app.listen(user_id=user_id, timeout=30)

        if "*" in input1.text:
            email, password = input1.text.strip().split("*")
            payload = {"email": email, "providerName": "email", "sec": password}
            response = session.post("https://userapi.adda247.com/v2/login?src=aweb", json=payload, headers=headers)

            if response.status_code != 200:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            login_data = response.json()
            login_token = login_data.get("loginToken")
            alreadyLoggedIn = login_data.get("alreadyLoggedIn")

            headers.update({"LOGIN_TOKEN": login_token})
            response = session.post("https://userapi.adda247.com/forceLogout?src=aweb", headers=headers)
            output_response = response.json()

            if response.status_code != 200:
                return await msg.edit_text("😒 **Login failed, did not fetch token.**")

            token = output_response['data']['jwtToken']
            jwt_token_new = output_response['data']['jwtTokenNew']

        else:
            token = input1.text.strip()
            await input1.delete()

        await msg.edit_text("✅ **Login Successful**")

        headers.update({"X-JWT-Token": token})
        params = {"pageNumber": 0, "pageSize": 10, "src": "aweb"}

        response = session.get("https://store.adda247.com/api/v2/ppc/package/purchased", headers=headers, params=params)
        if response.status_code != 200:
            return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

        batch_data = response.json().get("data", [])
        if not batch_data:
            return await msg.edit_text("No batch data found.")

        batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
        for data in batch_data:
            batch_list += f"`{data['packageId']}`  -   **{data['title']}**\n"

        await msg.edit_text(f"{batch_list}\n**📊 Now send the Batch ID to Download**")
        input2 = await app.listen(user_id=user_id, timeout=30)
        course_id = input2.text.strip()
        await input2.delete()

        batch_name = next(
            (course["title"].replace("/", "") for course in batch_data if int(course["packageId"]) == int(course_id)),
            None
        )
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        maha_pack = next((item.get("mahaPack", False) for item in batch_data if str(item["packageId"]) == str(course_id)), False)
        start_time = time.time()

        if maha_pack:
            lectures = await asyncio.create_task(course_extract(session, headers, course_id))
        else:
            lectures = await asyncio.create_task(direct_links(session, headers, course_id))

        end_time = time.time()
        elapsed = main_func.get_time(end_time - start_time)

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        caption = (
            f"**App Name** : `ADDA 247`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"⌚️ **Time Taken** : `{elapsed} sec`"
        )

        me = await app.get_me()
        big_file_id = me.photo.big_file_id
        thumb = await asyncio.create_task(app.download_media(big_file_id))

        await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
        os.remove(file_name)
        await msg.delete()
        await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        session.close()
    except ListenerTimeout:
        await message.reply_text("⏰ Timeout! You took too long to reply.")
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")




