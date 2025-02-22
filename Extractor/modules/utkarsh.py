import os
import time
import json
import aiohttp
import asyncio
import requests
import json_repair
from Extractor import app
from pyrogram import filters
from Extractor.core import main_func
from Extractor.modules.start import keyboard



cookies = {"csrf_name": "", "ci_session": ""}
v_count = 0
p_count = 0


async def process_uk(msg, session, raw_text2, token, ids):
    lecture = ""

    for id in ids:
        d_text = json.dumps(
            {
                "course_id": id,
                "page": 1,
                "revert_api": "1#0#0#1",
                "parent_id": raw_text2,
                "tile_id": "0",
                "layer": 1,
                "type": "content",
            }
        )
        course_id1 = main_func.utkarsh_encrypt(d_text)
        data = {"tile_input": course_id1, "csrf_name": token}

        async with session.post(
            "https://online.utkarsh.com/web/Course/tiles_data",
            cookies=cookies,
            data=data,
        ) as response:
            ror = await response.text()
            res = json.loads(ror)
            x2 = main_func.utkarsh_decrypt(res.get("response"))
            decoded2 = json_repair.repair_json(x2, return_objects=True)
            x_ids = [sx["id"] for sx in decoded2["data"]["list"]]

        for i in x_ids:
            e_text = json.dumps(
                {
                    "course_id": id,
                    "parent_id": raw_text2,
                    "layer": 2,
                    "page": 1,
                    "revert_api": "1#0#0#1",
                    "subject_id": i,
                    "tile_id": 0,
                    "topic_id": i,
                    "type": "content",
                }
            )
            c = main_func.encode_base64(e_text)
            data = {"layer_two_input_data": c, "content": "content", "csrf_name": token}

            async with session.post(
                "https://online.utkarsh.com/web/Course/get_layer_two_data",
                cookies=cookies,
                data=data,
            ) as response:
                ror = await response.text()
                res2 = json.loads(ror)
                data2 = main_func.utkarsh_decrypt(res2.get("response"))
                decoded3 = json_repair.repair_json(data2, return_objects=True)
                s_ids = [item["id"] for item in decoded3["data"]["list"]]

            for j in s_ids:
                f_text = json.dumps(
                    {
                        "course_id": id,
                        "parent_id": raw_text2,
                        "layer": 3,
                        "page": 1,
                        "revert_api": "1#0#0#1",
                        "subject_id": i,
                        "tile_id": 0,
                        "topic_id": j,
                        "type": "content",
                    }
                )
                d = main_func.encode_base64(f_text)
                data3 = {"layer_two_input_data": d, "content": "content", "csrf_name": token}

                async with session.post(
                    "https://online.utkarsh.com/web/Course/get_layer_two_data",
                    cookies=cookies,
                    data=data3,
                ) as response:
                    ror = await response.text()
                    res3 = json.loads(ror)
                    data3 = main_func.utkarsh_decrypt(res3.get("response"))
                    decoded4 = json_repair.repair_json(data3, return_objects=True)

                for data in decoded4["data"]["list"]:
                    title = data["title"]
                    url = None
                    if data.get("bitrate_urls", []):
                        for u in data.get("bitrate_urls", []):
                            if u["title"] == "720x1280.mp4":
                                url = f"{u['url']}"
                              
                    if url:
                        lecture += f"{title}: {url}\n"
                        v_count += 1

                    if data.get("file_type") == "1":
                        pdf = data["file_url"]
                        lecture += f"{title}: {pdf}\n"
                        p_count += 1

    return lecture


@app.on_message(filters.command("uk"))
async def utkarsh_login(_, message):
    user_id = message.from_user.id
    msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
    try:
        input1 = await app.listen(user_id, timeout=30)  
        raw_text = input1.text
    except:
        await message.reply_text("⏳ Timeout! Please try again.")
        return

    login_url = "https://online.utkarsh.com/web/Auth/login"
    url = "https://online.utkarsh.com/"
    cook = requests.Session()

    try:
        response = cook.get(url)
        cookie = cook.cookies.get_dict()
    except requests.exceptions.RequestException as e:
        return await message.reply_text(f"**Error** : `{e}`")

    if cookie:
        cookies.update(cookie)
    else:
        return await message.reply_text("Failed to get cookies.")

    data = {
        "csrf_name": cookie["csrf_name"],
        "mobile": "",
        "url": "0",
        "password": "",
        "submit": "LogIn",
        "device_token": "null",
    }

    if "*" in raw_text:
        data["mobile"], data["password"] = raw_text.split("*")
        
    token = raw_text
    await input1.delete()
    async with aiohttp.ClientSession() as session:
        async with session.post(login_url, cookies=cookies, data=data) as response:
            if response.status == 200:
                resp = await response.text()
                res = main_func.utkarsh_decrypt(json.loads(resp)["response"])
                token = json.loads(res)["token"]
                await msg.edit_text("✅ **Login Successfully**")
                await message.reply_text(f"📋 **Token** : `{token}`")
            else:
                return await msg.edit_text("❌ Failed Login! Incorrect password.")

#        data = {"type": "Paid", "csrf_name": token, "sort": "0"}

#        async with session.post(
#            "https://online.utkarsh.com/web/Profile/my_course", cookies=cookies, data=data
#        ) as response:
#            data = await response.text() 
            
            
#            respon = main_func.utkarsh_decrypt(json.loads(data)["response"])
#            data = json.loads(respon)
             
#        FFF = "**BATCH ID   -   BATCH NAME**\n\n"
#        for course in data["data"].get("data"):
#            FFF += f"**`{course['id']}`   -   {course['title']}**\n\n"

        await msg.edit_text("**📊 Now send the Batch ID to Download**")
        try:
            input2 = await app.listen(user_id, timeout=30)  
            raw_text2 = input2.text
        except:
            await message.reply_text("⏳ Timeout! Please try again.")
            return

#        batch_name = next(
#            (course["title"].replace("/", "") for course in data["data"]["data"] if course["id"] == raw_text2), ""
#        )
        
        combo_text = '{"course_id": f"{raw_text2}", "revert_api": "1#0#0#1", "parent_id": 0, "tile_id": "70592", "layer": 1, "type": "course_combo"}'
        course_id = main_func.utkarsh_encrypt(combo_text)
        data = {'tile_input': course_id, 'csrf_name': token}
        async with session.post('https://online.utkarsh.com/web/Course/tiles_data', cookies=cookies, data=data) as response:
            data = json.loads(await response.text())          
            respon = main_func.utkarsh_decrypt(data["response"])
            decoded = json_repair.repair_json(respon, return_objects=True)
            if decide["status"] is not True:
                await message.reply_text("✏️ **Invalid Course ID**")
             
        await msg.edit_text("**Extracting Video Links, Please Wait  📥**")
        start_time = time.time()
        links = ""
        async with aiohttp.ClientSession() as session:
            tasks = [process_uk(msg, session, raw_text2, token, [item["id"]]) for item in decoded['data']]
            results = await asyncio.gather(*tasks)
            links = "".join(results)

        batch_name = "test" 
        elapsed = main_func.get_time(time.time() - start_time)
        caption = f"**App Name** : `Utkarsh`\n\n**Batch Name** : `{batch_name}`\n🍿 **Total Video** : `{v_count}`\n📝 **Total pdf** : `{p_count}`\n⌚️ **Time Taken** : `{elapsed}`"
        
        file_path = f"{batch_name}_{user_id}.txt"
        with open(file_path, "w") as f:
            f.write(links)

        me = await app.get_me()
        big_file_id = me.photo.big_file_id
        thumb = await asyncio.create_task(app.download_media(big_file_id))
        await app.send_document(chat_id=message.chat.id, document=file_path, caption=caption, thumb=thumb, reply_markup=keyboard)
        os.remove(file_path)




