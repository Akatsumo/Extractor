import os
import time
import json
import aiohttp
import asyncio
import requests
import json_repair
import cloudscraper
from Extractor import app
from pyrogram import filters
from Extractor.core import main_func
from Extractor.modules.start import keyboard


cookies = {"csrf_name": "", "ci_session": ""}
v_count = 0
p_count = 0


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://online.utkarsh.com',
    'Pragma': 'no-cache',
    'Referer': '',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



async def process_uk(session, raw_text, token, ids):
    global v_count, p_count
    lecture = ""

    for id in ids:
        d_text = json.dumps(
            {
                "course_id": id,
                "page": 1,
                "revert_api": "1#0#0#1",
                "parent_id": raw_text,
                "tile_id": "0",
                "layer": 1,
                "type": "content",
            }
        )
        course_id1 = main_func.utkarsh_encrypt(d_text)
        data = {"tile_input": course_id1, "csrf_name": token}

        response1 = await session.post("https://online.utkarsh.com/web/Course/tiles_data", cookies=cookies, data=data)
        output1 = json.loads(await response1.text())
        decode_output1 = main_func.utkarsh_decrypt(output1["response"])
        decoded1 = json_repair.repair_json(decode_output1, return_objects=True)
        x_ids = [sx["id"] for sx in decoded1["data"]["list"]]

        for i in x_ids:
            e_text = json.dumps(
                {
                    "course_id": id,
                    "parent_id": raw_text,
                    "layer": 2,
                    "page": 1,
                    "revert_api": "1#0#0#1",
                    "subject_id": i,
                    "tile_id": 0,
                    "topic_id": i,
                    "type": "content",
                }
            )
            course_id2 = main_func.encode_base64(e_text)
            data = {"layer_two_input_data": course_id2, "content": "content", "csrf_name": token}

            response2 = await session.post("https://online.utkarsh.com/web/Course/get_layer_two_data", cookies=cookies, data=data)
            output2 = json.loads(await response2.text())
            decode_output2 = main_func.utkarsh_decrypt(output2["response"])
            decoded2 = json_repair.repair_json(decode_output2, return_objects=True)
            s_ids = [item["id"] for item in decoded2["data"]["list"]]

            for j in s_ids:
                f_text = json.dumps(
                    {
                        "course_id": id,
                        "parent_id": raw_text,
                        "layer": 3,
                        "page": 1,
                        "revert_api": "1#0#0#1",
                        "subject_id": i,
                        "tile_id": 0,
                        "topic_id": j,
                        "type": "content",
                    }
                )
                course_id3 = main_func.encode_base64(f_text)
                data = {"layer_two_input_data": course_id3, "content": "content", "csrf_name": token}

                response = await session.post("https://online.utkarsh.com/web/Course/get_layer_two_data", cookies=cookies, data=data)
                output3 = json.loads(await response.text())         
                decode_output3 = main_func.utkarsh_decrypt(output3["response"])
                decoded3 = json_repair.repair_json(decode_output3, return_objects=True)

                print(decoded3)
                for data in decoded3["data"]["list"]:
                    title = data["title"]
                    vid = data["id"]
                    url = None
                    if data.get("bitrate_urls", []):
                         f_text = json.dumps(
                         {
                          "course_id": id,
                          "parent_id": raw_text,
                          "layer": 4,
                          "page": 1,
                          "revert_api": "1#0#0#1",
                          "subject_id": vid,
                          "tile_id": 0,
                          "topic_id": j,
                          "type": "content",
                         })
                
                         course_id3 = main_func.encode_base64(f_text)
                         data = {"layer_two_input_data": course_id3, "content": "content", "csrf_name": token}

                         response = await session.post("https://online.utkarsh.com/web/Course/get_layer_two_data", cookies=cookies, data=data)
                         output3 = json.loads(await response.text())         
                         decode_output3 = main_func.utkarsh_decrypt(output3["response"])
                         decoded3 = json_repair.repair_json(decode_output3, return_objects=True)
                         print(decoded3)
 #                       for item in data.get("bitrate_urls", []):             
  #                          if item["title"] == "720x1280.mp4" and item["url"]:
 #                               lecture += f"{title}: {url}\n"
                                v_count += 1
                                                              

                    if data.get("file_type") == "1":
                        pdf = data["file_url"]
                        lecture += f"{title}: {pdf}\n"
                        p_count += 1

    return lecture



@app.on_message(filters.command("utkarsh"))
async def utkarsh_login(_, message):
    user_id = message.from_user.id
    async with aiohttp.ClientSession() as session:        
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

        login_url = "https://online.utkarsh.com/web/Auth/login"
        data = {
          "csrf_name": cookie["csrf_name"],
          "mobile": "",
          "url": "0",
          "password": "",
          "submit": "LogIn",
          "device_token": "null",
        }
        
        msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
        try:
            input1 = await app.listen(user_id, timeout=30)  
            if "*" in input1.text:
                data["mobile"], data["password"] = input1.text.split("*")
                response = await session.post(login_url, cookies=cookies, data=data)
                if response.status != 200:
                    return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
                output = await response.text()
                decode_output = main_func.utkarsh_decrypt(json.loads(output)["response"])
                token = json.loads(decode_output)["token"]                                
            else:
                token = input1.text.strip()
        except:
            return await message.reply_text("⏳ Timeout! Please try again.")
                     
        await input1.delete()        
        await msg.edit_text("✅ **Login Successfully**")
            
        data = {"type": "Paid", "csrf_name": token, "sort": "0"}

        headers['Referer'] = 'https://online.utkarsh.com/web/Profile/my_course'
    
        response = await session.post("https://online.utkarsh.com/web/Profile/my_course", cookies=cookies, headers=headers, data=data) 
        output = await response.text()
        decode_response = json.loads(main_func.utkarsh_decrypt(json.loads(output)["response"]))
        
        FFF = "**BATCH ID   -   BATCH NAME**\n\n"
        for course in decode_response["data"].get("data"):
            FFF += f"**`{course['id']}`   -   {course['title']}**\n\n"
        
        await msg.edit_text(f"{FFF}\n\n**📊 Now send the Batch ID to Download**")
        try:
            input2 = await app.listen(user_id, timeout=30)  
            raw_text2 = input2.text
        except:
            return await message.reply_text("⏳ Timeout! Please try again.")
            
        batch_name = next(
            (course["title"].replace("/", "") for course in decode_response["data"]["data"] if course["id"] == raw_text2), ""
        )
        
        combo_text = '{"course_id": "' + raw_text2 + '", "revert_api": "1#0#0#1", "parent_id": 0, "tile_id": "0", "layer": 1, "type": "course_combo"}'        
        course_id = main_func.utkarsh_encrypt(combo_text)
        
        data = {'tile_input': course_id, 'csrf_name': token}
        response = await session.post('https://online.utkarsh.com/web/Course/tiles_data', cookies=cookies, data=data)
        output = json.loads(await response.text())          
        decode_output = main_func.utkarsh_decrypt(output["response"])
        decoded = json_repair.repair_json(decode_output, return_objects=True)
        
        if decoded["status"] is not True:
            return await msg.edit_text("✏️ **Invalid Course ID**")
                           
        await msg.edit_text("**Extracting Video Links, Please Wait  📥**")
        start_time = time.time()
        links = ""
        
        tasks = [process_uk(session, raw_text2, token, [item["id"]]) for item in decoded['data']]
        results = await asyncio.gather(*tasks)
        links = "".join(results)

        elapsed = main_func.get_time(time.time() - start_time)
        caption = f"**App Name** : `Utkarsh`\n\n**Batch Name** : `{batch_name}`\n🍿 **Total Video** : `{v_count}`\n📝 **Total pdf** : `{p_count}`\n⌚️ **Time Taken** : `{elapsed}`"
        
        file_path = f"{batch_name}_{user_id}.txt"
        with open(file_path, "w") as f:
            f.write(links)

        me = await app.get_me()
        big_file_id = me.photo.big_file_id
        thumb = await asyncio.create_task(app.download_media(big_file_id))
        await app.send_document(chat_id=message.chat.id, document=file_path, caption=caption, thumb=thumb, reply_markup=keyboard)
        await msg.delete()
        os.remove(file_path)
        await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")


