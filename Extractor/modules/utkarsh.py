import json_repair
import os
import requests
import aiohttp
import asyncio
import time
import json
from Extractor import app
from Extractor.core.main_func import utkarsh_decrypt, utkarsh_encrypt, encode_base64, get_time



cookies = {
    'csrf_name': '',
    'ci_session': '',
}


async def process_uk(msg, session, raw_text2, token, ids):
    global v_count, p_count
    try:        
        v_count = 0
        p_count = 0
        
        lec = ""
        for id in ids:
            d_text = '{"course_id": "' + id + '", "page": 1, "revert_api": "1#0#0#1", "parent_id": "' + raw_text2 + '", "tile_id": "0", "layer": 1, "type": "content"}'
            course_id1 = utkarsh_encrypt(d_text)
            data = {
                'tile_input': course_id1,
                'csrf_name': token,
            }
            async with session.post('https://online.utkarsh.com/web/Course/tiles_data', cookies=cookies, data=data) as response:
                ror = await response.text()
                res = json.loads(ror)
                x2 = utkarsh_decrypt(res.get("response"))
                decoded2 = json_repair.repair_json(x2, return_objects=True)
                x_ids = [sx['id'] for sx in decoded2['data']['list']]
        
            for i in x_ids:
           #     await msg.edit_text(f"**Extracting Videos Links Please Wait  📥**\n\n🍿 **Total Video**  - `{v_count}`\n📝 **Total Pdf**  - `{p_count}`\n\n♻️ **Course ID** : {i}")            
                headers['Referer'] = 'https://online.utkarsh.com/web/Course/single_book_details?id='+i
                e_text = '{"course_id": "' + id + '","parent_id": "' + raw_text2 + '","layer":2,"page":1,"revert_api":"1#0#0#1","subject_id": "' + i + '","tile_id":0,"topic_id": "' + i + '","type":"content"}'
                c = encode_base64(e_text)
                data = {
                    'layer_two_input_data': c,
                    'content': 'content',
                    'csrf_name': token,
                }
                async with session.post('https://online.utkarsh.com/web/Course/get_layer_two_data', cookies=cookies, data=data) as response:
                    ror = await response.text() 
                    res2 = json.loads(ror)
                    data2 = utkarsh_decrypt(res2.get("response"))
                    decoded3 = json_repair.repair_json(data2, return_objects=True)
                    s_ids = [item['id'] for item in decoded3['data']['list']]
                
                for j in s_ids:
                    f_text = '{"course_id": "' + id + '","parent_id": "' + raw_text2 + '","layer":3,"page":1,"revert_api":"1#0#0#1","subject_id": "' + i + '","tile_id":0,"topic_id": "' + j + '","type":"content"}'
                    d = encode_base64(f_text)
                    data3 = {
                        'layer_two_input_data': d,
                        'content': 'content',
                        'csrf_name': token,
                    }
                    async with session.post('https://online.utkarsh.com/web/Course/get_layer_two_data', cookies=cookies, data=data3) as response:
                        ror = await response.text() 
                        res3 = json.loads(ror)
                        data3 = utkarsh_decrypt(res3.get("response"))
                        decoded4 = json_repair.repair_json(data3, return_objects=True)
                        
                    for data in decoded4['data']['list']:
                        title = data['title']
                        url = None
                        if data.get('bitrate_urls', []):
                            for u in data.get('bitrate_urls', []):
                                if u['title'] == '720x1280.mp4':
                                    url = f"{'/'.join(u['url'].split('/')[:-2])}/plain/720x1280.mp4"
                        if url:
                            lec += f"{title}:{url}\n"
                            v_count += 1

                        if data.get('file_type') == '1':
                            pdf = data['file_url']
                            lec += f"{title}:{pdf}\n"
                            p_count += 1

        return lec   
    
    except Exception as e:
        await msg.reply_text(str(e))




@app.on_message(filters.command("uk"))
async def utkarsh_login(_, message):
    user_id = message.from_user.id
    msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
    input1 = await _.listen(user_id=user_id)
    raw_text = input1.text
    
    login_url = "https://online.utkarsh.com/web/Auth/login"
    url = 'https://online.utkarsh.com/'
    sos = requests.Session()
    try:
        response = sos.get(url)
        cookie = sos.cookies.get_dict()
    except requests.exceptions.RequestException as e:
        return await message.reply_text(f"**Error** : `{e}`")
    if cookie:
        cookies['ci_session'] = cookie['ci_session']
        cookies['csrf_name'] = cookie['csrf_name']
    else:
        print("Failed to get cookies.")
    
    data = {
      'csrf_name': cookie['csrf_name'],
      'mobile': '',
      'url': '0',
      'password': '',
      'submit': 'LogIn',
      'device_token': 'null',
    }
    if "*" in raw_text:
      data["mobile"] = raw_text.split("*")[0]
      data["password"] = raw_text.split("*")[1]
    else:
      token = raw_text
    await input1.delete(True)
    async with aiohttp.ClientSession() as session:
        async with session.post(login_url, cookies=cookies, data=data) as response:
            if response.status == 200:
                r = await response.text()
                t = json.loads(r)
                res = utkarsh_decrypt(t.get("response"))
                data = json.loads(res)
                token = data['token']
                await msg.edit_text(f"✅ **Login Successfully**")
            else:
                await msg.edit_text("Failed Login!! may be your password wrong")
            
        data = {
          'type': 'Paid',
          'csrf_name': token,
          'sort': '0',
        }

        async with session.post('https://online.utkarsh.com/web/Profile/my_course', cookies=cookies, data=data) as response:
            data = await response.text()
            res = json.loads(data)
            t = utkarsh_decrypt(res.get("response"))
            data = json.loads(t)
    
        FFF = "**BATCH ID   -   BATCH NAME**\n\n"
        for course in data['data'].get('data'):
            FFF += f"**`{course['id']}`   -   {course['title']}**\n\n"

        await msg.edit_text(f"{FFF}\n\n**📊 Now send the Batch ID to Download**")
        input2 = await app.listen(user_id=query.from_user.id)
        raw_text2 = input2.text

        for course in data['data'].get('data'):
            if course['id'] == raw_text2:
                batch_name = course['title'].replace("/", "")
    
        
        c_text = '{"course_id": "' + raw_text2 + '", "revert_api": "1#0#0#1", "parent_id": 0, "tile_id": "0", "layer": 1, "type": "course_combo"}'
        course_id = utkarsh_encrypt(c_text)
        data = {
            'tile_input': course_id,
            'csrf_name': token,
        }

        async with session.post('https://online.utkarsh.com/web/Course/tiles_data', cookies=cookies, data=data) as response:
            data = await response.text()  
            res = json.loads(data)
            x = utkarsh_decrypt(res.get("response"))
            decoded = json_repair.repair_json(x, return_objects=True)
                
        await msg.edit_text("**Extracting Videos Links Please Wait  📥**")
        start_time = time.time()
        vt = ""
        tasks = [process_uk(msg, session, raw_text2, token, [item['id']]) for item in decoded['data']]
        results = await asyncio.gather(*tasks)
        for result in results:
            vt += result

        end_time = time.time()
        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)

        cap = f"**App Name :- **Utkarsh**\nBatch Name :-** `{batch_name}`\n\n🍿 **Total Video**: `{v_count}`\n📝 **Total pdf**: `{p_count}`\n⌚️**Time Taken**: `{elapsed}`"
        with open(f'{batch_name}.txt', 'a') as f:
            f.write(f"{vt}")
        await app.send_document(message.chat.id, document=f"{batch_name}.txt", caption=cap)
        os.remove(f"{batch_name}.txt")
        await message.reply_text("Done")
        await msg.delete()



