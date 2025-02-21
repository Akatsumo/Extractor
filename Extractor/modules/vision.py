import os
import asyncio
import requests
from Extractor import app
from pyrogram import filters
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


study_materials = {}

def study_material(session):
    url = "https://visionias.in/student/study_material_dashboard.php"
    response = session.get(url)
    if response.status_code != 200:
        return False

    soup = BeautifulSoup(response.text, "html.parser")  

    modules = soup.find_all("div", class_="container_sm")
    study_materials.clear()  

    for module in modules:  
        course_name = module.find("h4").text.strip()
        file_name = f"{course_name.replace(' ', '_').replace('-', '_')}.txt"
        table = module.find_next("table")
        subjects = []

        if table:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    subject_name = cols[0].text.strip()
                    link_tag = cols[1].find("a")
                    download_link = "https://visionias.in/student/" + (link_tag["href"] if link_tag else "N/A")
                    subjects.append(f"{subject_name}: {download_link}")

        study_materials[file_name] = {"course_name": course_name, "subjects": subjects}

    for file_name, data in study_materials.items():
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"Course: {data['course_name']}\n\n")
            for subject in data["subjects"]:
                f.write(subject + "\n")

    return True



@app.on_message(filters.command("vision"))
async def vision_login(_, message):
    user_id = message.from_user.id
    msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")

    try:
        input1 = await app.listen(user_id, timeout=30)  
        raw_text = input1.text
    except:
        await message.reply_text("⏳ Timeout! Please try again.")
        return

    session = requests.Session()
    login_url = "https://visionias.in/student/module/login-exec2test.php"
    
    data = {
        "login": "",
        "password": "",
        "returnUrl": "student"
    }

    if "*" in raw_text:
        data["login"], data["password"] = raw_text.split("*", 1)
    else:
        await message.reply_text("❌ Invalid format! Please send as: `ID*Password`")
        return 

    response = session.post(login_url, data=data)

    if response.status_code == 200:
        msg = await message.reply_text("✅ **Login Successful**")

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 Study Material", callback_data="study_material")],
            [InlineKeyboardButton("📺 Classes", callback_data="classes")]
        ])
        mm = await msg.edit_text("🕹 Select Your Preferred Mode 👇", reply_markup=buttons)

        r = await mm.wait_for_click(from_user_id=user_id)
        
        if r.data == 'study_material':
            success = study_material(session)
            if not success:
                await msg.edit_text("🛑 Study Material Fetching Failed!!")
                return 

            for file_name, data in study_materials.items():
                try:
                    await app.send_document(
                        chat_id=user_id, 
                        document=file_name, 
                        caption=f"**Course Name**: `{data['course_name']}`"
                    )
                    asyncio.sleep(2)
                except Exception as e:
                    await message.reply_text(f"⚠️ Error sending file: {str(e)}")

        elif r.data == "classes":
            await msg.edit_text("📺 **Classes will be available soon...**")
    
    else:
        await message.reply_text("❌ **Login Failed!** Check your credentials and try again.")
