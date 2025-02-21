import os
import time
import requests
from Extractor import app
from pyrogram import filters
from bs4 import BeautifulSoup
from Extractor.core import main_func







soup = BeautifulSoup(html_content, "html.parser")
study_materials = {}

modules = soup.find_all("div", class_="container_sm")
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
                download_link = "https://visionias.in/student/" + (cols[1].find("a")["href"] if cols[1].find("a") else "N/A")
                subjects.append(f"{subject_name}: {download_link}")
    study_materials[file_name] = {"course_name": course_name, "subjects": subjects}

for file_name, data in study_materials.items():
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(f"Course: {data['course_name']}\n\n")
        for subject in data["subjects"]:
            f.write(subject + "\n")

@app.on_message(pyrogram.filters.command("send_materials"))
def send_materials(client, message):
    chat_id = message.chat.id
    for file_name, data in study_materials.items():
        app.send_document(chat_id, file_name, caption=f"Course: {data['course_name']}")
        time.sleep(2)

app.run()





@app.on_message(filters.command("vision"))
async def vision_login(_, message):
    user_id = message.from_user.id
    msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
    input1 = await app.listen(user_id)
    raw_text = input1.text
    if "*" in raw_text:
    session = requests.Session()

login_url = "https://visionias.in/student/module/login-exec2test.php"
dashboard_url = "https://visionias.in/student/study_material_dashboard.php"

data = {
    "login": "jalpaptl8789@gmail.com",
    "password": "321nvp",
    "returnUrl": "student"
}

response = session.post(login_url, data=data)

if response.status_code == 200:
    dashboard_response = session.get(dashboard_url)
    if dashboard_response.status_code == 200:
        html_content = dashboard_response.text
    else:
        exit()
else:
    exit()

