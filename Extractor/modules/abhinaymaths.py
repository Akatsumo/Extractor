import os, json
import time
import asyncio
import requests
from Extractor import app
from pyrogram import filters 
from Extractor.core import main_func



headers = {}
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
        cookies.update({"csrf_name": csrf_name}) 

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
              "password": password,
              "submit": "Login",
              "device_token": "null",
            }
            response = requests.post(login_url, headers=headers, cookies=cookies, data=login_data)
            decoded = json.loads(main_func.decode_base64(response.json().get('response', '')))
          
            if decoded['status'] != True:
                return await msg.edit_text("😒 **Login failed, incorrect credentials.**")

            await msg.edit_text("✅ **Login Successful**")

            login_url = "https://abhinaymaths.in/web/Profile/my_course"
            data = {
              "type": "Paid",
              "csrf_name": cookies["csrf_name"],
              "sort": "0"
            }
                    
            response = session.post(login_url, headers=headers, cookies=cookies, data=data)
            course_data = json.loads(main_func.decode_base64(response.json().get('response', ''))).get("get_course_categorywise", {}).get("data", [])))
            print(course_data)
            batch_list = "**📚 Available Batches:**\n\n"
            batch_data = {}
            for category in course_data:
                for course in category.get("courses", []):
                    if course.get("is_purchased") == "1":
                        batch_list += f"{course.get('id')} - {course.get('title')}"
                        batch_data.update({"_id": course.get('id'), "batch_name": course.get('title'), "category_name": category.get("category"), "batch_price": course.get('course_sp'), "batch_validity": course.get('validity')})
        
            await msg.edit_text(f"{batch_list}\n\n**📊 Now send the Batch ID to Download**")

           

    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        print(f"Error: {str(e)}")
