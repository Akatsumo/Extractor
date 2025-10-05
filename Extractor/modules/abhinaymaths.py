import os, json
import time
import asyncio
import requests
from Extractor import app
from pyrogram import filters 
from Extractor.core.main_func import get_time



headers = {"Referer": "https://abhinaymaths.in/"}
cookies = {}


# ----------------------- Course-Extract ----------------------- #


    

# ----------------------- Vajiram-Command ----------------------- #

@app.on_message(filters.command("abhinay"))
async def vajiram_login(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    try:
        session = requests.Session()
        login_url = 'https://abhinaymaths.in/web/Auth/login'

        response = session.get(login_url)
        csrf_name = session.cookies.get('csrf_name')
        cookies["csrf_name"] = csrf_name

        if not csrf_name:
            return await message.reply_text("csrf name did not found !!")

        headers.update({'Referer': login_url})    
        msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")

        try:
            input1 = await app.listen(user_id=user_id, timeout=30)
        except:
            return await msg.edit_text("⏳ Timeout! Please try again.")
            
        if "*" in input1.text.strip():
            username, password = input1.text.split("*")
            login_data = {
              "csrf_name": cookies["csrf_name"],
              "mobile": username,
              "url": "0",
              "password": passwor,
              "submit": "Login",
              "device_token": "null",
            }
            response = requests.post(url, headers=headers, cookies=cookies, data=login_data)
            decoded = json.loads(main_func.decode_base64(response.get('response', '')))
            print(decoded)
           
            if decoded['status'] != True:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            await msg.edit_text("✅ **Login Successful**")
                    
            # response = session.get('https://vajiramias.com/courses/')
            # if response.status_code != 200:
            #     return await msg.edit_text("😒 **Login failed, incorrect OTP.**")

            # soup = BeautifulSoup(response.text, 'html.parser')
            # courses = soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12')

            # purchased_courses = []  
            # free_courses = []  

            # for course in courses:
            #     purchased_label = course.find('span', class_='label label-success text-bold font-14')
            #     free_label = course.find('span', class_='label label-success text-bold font-14')
                
            #     if purchased_label and 'Purchased' in purchased_label.text:
            #         course_name = course.find('h2', class_='item_header text-center').text.strip()
            #         details_button = course.find('a', class_='margin-t-10 btn btn-sm btn-success btn-block font-14 text-bold')
                
            #         if details_button:
            #             course_url = details_button['href']
            #             course_info = {
            #                 'course_name': course_name,
            #                 'course_url': f"https://vajiramias.com{course_url}",
            #                 'course_type': 'Purchased'
            #             }
            #             purchased_courses.append(course_info)
            
            #     elif free_label and 'Free Access' in free_label.text:
            #         course_name = course.find('h2', class_='item_header text-center').text.strip()
            #         details_button = course.find('a', class_='btn btn-sm btn-info btn-block font-14 text-bold')
                
            #         if details_button:
            #             course_url = details_button['href']
            #             course_info = {
            #                 'course_name': course_name,
            #                 'course_url': f"https://vajiramias.com{course_url}",
            #                 'course_type': 'Free Access'
            #             }
            #             free_courses.append(course_info)

            # free_courses.extend(purchased_courses)
            # batch_list = "**BATCH-ID  -  BATCH NAME**\n\n"
            # batch_data = {}
            # s_no = 1  
            # for course in free_courses:
            #     batch_list += f"`{s_no}`  -   **{course['course_name']}-{course['course_type']}**\n\n"
            #     batch_data[s_no] = {'batch_name': course['course_name'], 'batch_url': course['course_url']}
            #     s_no += 1

            # await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")

            # try:
            #     input3 = await app.listen(user_id=user_id, timeout=30)
            #     batch_id = int(input3.text.strip()) 
            #     await input3.delete()
            # except:
            #     return await msg.edit_text("⏳ Timeout! Please try again.")

            # batch_url = batch_data.get(batch_id, {}).get('batch_url')
            # batch_name = batch_data.get(batch_id, {}).get('batch_name')

            # if not batch_name:
            #     return await msg.edit_text("**Invalid Batch ID. Please try again.**")

            # await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
            # start_time = time.time()
            # lectures = await asyncio.create_task(course_extract(session, batch_url))
            # end_time = time.time()
            # duration_seconds = end_time - start_time
            # elapsed = get_time(duration_seconds)

            # file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
            # with open(file_name, "w") as f:
            #     f.write("\n".join(lectures))

            # caption = f"**App Name** : `VAJIRAM IAS`\n**Batch Name** : `{batch_name}`\n\n📜 **Total Materials** : `{len(lectures)}`\n⌚️ **Time Taken** : `{elapsed}`"
            # me = await app.get_me()
            # big_file_id = me.photo.big_file_id
            # thumb = await asyncio.create_task(app.download_media(big_file_id))

            # await app.send_document(chat_id=message.chat.id, document=file_name, caption=caption, thumb=thumb)
            # os.remove(file_name)
            # await msg.delete()

    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        print(f"Error: {str(e)}")
