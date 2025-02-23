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


async def process_uk(session, raw_text, token, ids):
    global v_count, p_count
    lecture = ""
    
    for course_id in ids:
        request_data = json.dumps({
            "course_id": course_id,
            "page": 1,
            "revert_api": "1#0#0#1",
            "parent_id": raw_text,
            "tile_id": "0",
            "layer": 1,
            "type": "content",
        })
        encrypted_data = main_func.utkarsh_encrypt(request_data)
        payload = {"tile_input": encrypted_data, "csrf_name": token}
        
        try:
            response = await session.post("https://online.utkarsh.com/web/Course/tiles_data", cookies=cookies, data=payload)
            response_data = json.loads(await response.text())
            decrypted_data = main_func.utkarsh_decrypt(response_data["response"])
            decoded_data = json_repair.repair_json(decrypted_data, return_objects=True)
        except Exception as e:
            return f"Error processing course {course_id}: {e}\n"
        
        topic_ids = [item["id"] for item in decoded_data["data"]["list"]]
        
        for topic_id in topic_ids:
            e_text = json.dumps({
                "course_id": course_id,
                "parent_id": raw_text,
                "layer": 2,
                "page": 1,
                "revert_api": "1#0#0#1",
                "subject_id": topic_id,
                "tile_id": 0,
                "topic_id": topic_id,
                "type": "content",
            })
            course_id_encoded = main_func.encode_base64(e_text)
            payload = {"layer_two_input_data": course_id_encoded, "content": "content", "csrf_name": token}
            
            try:
                response = await session.post("https://online.utkarsh.com/web/Course/get_layer_two_data", cookies=cookies, data=payload)
                response_data = json.loads(await response.text())
                decrypted_data = main_func.utkarsh_decrypt(response_data["response"])
                decoded_data = json_repair.repair_json(decrypted_data, return_objects=True)
            except Exception as e:
                return f"Error processing topic {topic_id}: {e}\n"
            
            for content in decoded_data["data"]["list"]:
                title = content["title"]
                url = next((u['url'] for u in content.get("bitrate_urls", []) if u["title"] == "720x1280.mp4"), None)
                
                if url:
                    lecture += f"{title}: {url}\n"
                    v_count += 1
                if content.get("file_type") == "1":
                    lecture += f"{title}: {content['file_url']}\n"
                    p_count += 1
    
    return lecture


@app.on_message(filters.command("utkarsh"))
async def utkarsh_login(_, message):
    user_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        try:
            response = requests.get("https://online.utkarsh.com/")
            cookies.update(response.cookies.get_dict())
        except requests.exceptions.RequestException as e:
            return await message.reply_text(f"**Error** : `{e}`")

        login_url = "https://online.utkarsh.com/web/Auth/login"
        
        msg = await message.reply_text("🔑 Send ID*Password for login.")
        try:
            input1 = await app.listen(user_id, timeout=30)
            if "*" in input1.text:
                mobile, password = input1.text.split("*")
                login_data = {
                    "csrf_name": cookies.get("csrf_name", ""),
                    "mobile": mobile,
                    "password": password,
                    "submit": "LogIn",
                    "device_token": "null",
                }
                response = await session.post(login_url, cookies=cookies, data=login_data)
                if response.status != 200:
                    return await msg.edit_text("😒 **Login failed, incorrect credentials.**")
                
                output = json.loads(await response.text())
                token = json.loads(main_func.utkarsh_decrypt(output["response"]))["token"]
            else:
                token = input1.text.strip()
        except:
            return await message.reply_text("⏳ Timeout! Please try again.")
        
        await msg.edit_text("✅ **Login Successfully**")
        
        await msg.edit_text("📊 Send the Batch ID to Download")
        try:
            input2 = await app.listen(user_id, timeout=30)
            batch_id = input2.text
        except:
            return await message.reply_text("⏳ Timeout! Please try again.")
        
        combo_text = json.dumps({"course_id": batch_id, "revert_api": "1#0#0#1", "parent_id": 0, "tile_id": "0", "layer": 1, "type": "course_combo"})
        encrypted_course_id = main_func.utkarsh_encrypt(combo_text)
        payload = {"tile_input": encrypted_course_id, "csrf_name": token}
        response = await session.post("https://online.utkarsh.com/web/Course/tiles_data", cookies=cookies, data=payload)
        output = json.loads(await response.text())
        decrypted_output = main_func.utkarsh_decrypt(output["response"])
        decoded_output = json_repair.repair_json(decrypted_output, return_objects=True)
        if not decoded_output["status"]:
            return await msg.edit_text("✏️ **Invalid Course ID**")
        
        await msg.edit_text("**Extracting Video Links, Please Wait  📥**")
        start_time = time.time()
        results = await asyncio.gather(*[process_uk(session, batch_id, token, [item["id"]]) for item in decoded_output['data']])
        
        elapsed = main_func.get_time(time.time() - start_time)
        caption = f"App: `Utkarsh`\nBatch: `{batch_id}`\n🍿 Videos: `{v_count}`\n📝 PDFs: `{p_count}`\n⌚ Time: `{elapsed}`"
        
        file_path = f"{batch_id}_{user_id}.txt"
        with open(file_path, "w") as f:
            f.write("".join(results))
        
        await app.send_document(chat_id=message.chat.id, document=file_path, caption=caption, reply_markup=keyboard)
        os.remove(file_path)
        await msg.delete()
        await message.reply_text(f"✅ Done\n\n✏️ Token: `{token}`")


