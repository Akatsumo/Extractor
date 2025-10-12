import asyncio
import aiohttp
import json
import time
from pyrogram.enums import ParseMode
from Extractor.core.func import send_file
from Extractor.core.c_func import encrypt, decrypt, decode_jwt


async def nextias(app, query, message):
    try:
        msg = await message.reply_text(
            "**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n"
            "🔒 Send like this: ID*Password\n\nOr Send Token....**"
        )
        
        input1 = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
        raw_text = input1.text
        await input1.delete(True)

        connector = aiohttp.TCPConnector(limit=50)
        timeout = aiohttp.ClientTimeout(total=300)

        key = "!*@#)($^%1fgv&C=!*@#)($^%1fgv&C="
        iv = "gqLOHUioQ0QjhuvI"

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            token = raw_text.strip()
            user_id = decode_jwt(token)['sub']

            headers = {
                'Host': 'appprod.nextias.com',
                'auth': f'Bearer {token}',
                'device-type': '1',
                'version-code': '55',
                'user_id': user_id,
                'language': 'EN',
                'database-type': '1',
                'content-type': 'application/json; charset=utf-8',
                'user-agent': 'okhttp/4.12.0',
            }

            # Get course list
            data = {"course_id":"","course_type":"video","user_id": user_id}
            json_data = json.dumps(data)
            encrypted_data = encrypt(key, iv, json_data)
            
            # Make the request asynchronously
            async with session.post(
                'https://appprod.nextias.com/index.php/api/v1/my-course-list', 
                headers=headers, 
                data=json_data
            ) as response:
                _courses_data = await response.text()
                courses_data = json.loads(decrypt(key, iv, _courses_data))
                courses = courses_data['data']['course_list']
                
                batch_list = "\n".join(
                    f"<code>{batch['id']}</code> - <b>{batch['title']}</b>"
                    for batch in courses
                )
                
                await msg.edit_text(
                    f"<b>📚 Available Batches:</b>\n\n{batch_list}\n\n"
                    "<b>Send Batch ID to download:</b>",
                    parse_mode=ParseMode.HTML
                )
                
                batch_msg = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
                batch_id = batch_msg.text.strip()
                await batch_msg.delete()

                batch = next(
                    (c for c in courses if str(c['id']) == batch_id),
                    None
                )
                
                if not batch:
                    await msg.edit_text("**⚠️ Invalid Batch ID. Please try again.**")
                    return

                batch_name = batch['title']
                video_tile_id = batch['video_tile_id']
                pdf_tile_id = batch['pdf_tile_id']
                
                await msg.edit_text("**Extracting Videos Links Please Wait  📥**")
                start_time = time.time()

                data = {
                    "id": batch['id'],
                    "layer": 1,
                    "revert_api": "0#1",
                    "tile_id": video_tile_id,
                    "type": "video",
                    "user_id": user_id
                }
                
                json_data = json.dumps(data)
                encrypted_data = encrypt(key, iv, json_data)
                
                async with session.post(
                    'https://appprod.nextias.com/index.php/api/v1/course-details', 
                    headers=headers, 
                    data=json_data
                ) as response:
                    _course_detail = await response.text()
                    course_detail = json.loads(decrypt(key, iv, _course_detail))
                    print(course_detail)
                    
                    video_links = []
                    for d in course_detail['data']['recorded_video']:
                        data = {
                            "course_id": batch['id'],
                            "subject_id": d['subject_id'],
                            "tile_id": video_tile_id,
                            "topic_id": d['topic_id'],
                            "type": "Video",
                            "user_id": user_id
                        }
                        
                        json_data = json.dumps(data)
                        encrypted_data = encrypt(key, iv, json_data)
                        
                        async with session.post(
                            'https://appprod.nextias.com/index.php/api/v1/recorded-videos-by', 
                            headers=headers, 
                            data=json_data
                        ) as response:
                            _videos_by = await response.text()
                            videos_by = json.loads(decrypt(key, iv, _videos_by))
                            print(videos_by)

                            for d2 in videos_by['data']['list']:
                                data = {
                                    "course_id": batch['id'],
                                    "subject_id": d['subject_id'],
                                    "tile_id": video_tile_id,
                                    "topic_id": d2['id'],
                                    "user_id": user_id
                                }
                                
                                json_data = json.dumps(data)
                                encrypted_data = encrypt(key, iv, json_data)
                                
                                async with session.post(
                                    'https://appprod.nextias.com/index.php/api/v1/recorded-videos', 
                                    headers=headers, 
                                    data=json_data
                                ) as response:
                                    _videos = await response.text()
                                    videos = json.loads(decrypt(key, iv, _videos))
                                    print(videos)
                                    
                                    for v in videos['data']:
                                        if v['video_type'] == 8:
                                            video_info = f"{v['subject_name']}-{v['title']} : {v['file_url']}\n"
                                        else:
                                            video_info = f"{v['subject_name']}-{v['title']} : {v['token']}\n"
                                        video_links.append(video_info)
                    
                    # Format and display results
                    elapsed_time = time.time() - start_time
                    vt = "".join(video_links)
                    
                    filename = f"{batch_name}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(vt)
                    caption = (
                        f"**App Name :- Next IAS**\n"
                    )
                    return await message.reply_document(filename)
                    
    except Exception as e:
        await msg.edit_text(f"**❌ Error: {str(e)}**")
        import traceback
        print(traceback.format_exc())
