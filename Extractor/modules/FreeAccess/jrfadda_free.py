
import os, time
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Get-Headers --------------------------- #

def get_headers(session):
    url = 'https://backend.studyiq.net/user-auth-ws/v1/auth/generate/admin'
    headers = {
        'api-key': '9A3BDDEEBD4DFB213D3C15D29126151206E47E4F',
        'content-type': 'application/json'
    }
    payload = {
        'platform': 'ADMIN',
        'id': '1013'
    }
    response = session.post(url, headers=headers, json=payload)
    token = response.json()['token']
    return {"Authorization": f"Bearer {token}"}


# --------------------------- Course-Content --------------------------- #

async def course_content(session, headers, data,  group_id, package_id):
    lectures, v_count, p_count = [], 0, 0
  
    data.update({"dlb_grp_id": group_id, "dlb_pkg_id": package_id})
    response_data = session.get("https://www.jrfadda.com/app_version_2/course-subject", headers=headers, data=data)
    if response_data.status_code != 200:
        return lectures, v_count, p_count
        
    subject_data = response_data.json().get("list", [])
    if not subject_data:
        return lectures, v_count, p_count
        
    for subject in subject_data:
        subject_id = subject.get("id")
        subject_name = subject.get("name")
        response_data = session.post("https://www.jrfadda.com/app_version_2/class-videos-list-new", headers=headers, data=data)
        if response_data.status_code != 200:
          continue
        class_data = response_data.json().get("homedata")
        if not class_data:
          continue

        for class in class_data:
           class_name = class.get("title", "N/A")
           pdf_url = class.get("post_pdf_url")
           video_url = class.get("videoUrl")
           aws_hsl = class.get("aws_hsl_path")
           video_post_url = class.get("post_url")
            
            if pdf_url:
                p_count += 1
                lectures.append(f"{subject_name} | {class_name}: {pdf_url}")
            else:
                v_url = video_url if video_url else aws_hsl if aws_hsl else video_post_url
                v_count += 1
                lectures.append(f"{subject_name} | {class_name}: {v_url}")
           

    return lectures, v_count, p_count


# --------------------------- Jrf-Adda-Access --------------------------- #

async def jrfadda_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept-Encoding": "gzip",
      "User-Agent": "okhttp/4.9.3"
    }

    try:
        msg = await message.reply_text("**Fetching All Jrf Adda Categories, Please Wait...**")
      
        data = {"token": "123456789", "dlb_u_id": "58304"}
        response = session.post("https://www.jrfadda.com/app_version_2/main-home", headers=headers, data=data)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch jrf Categories.")
          
        categories_data = response.json().get("category")
        if not categories_data:
            return await msg.edit_text("No categories data found.")
        
        categories_list = "📚 **Available Categories:**\n\n"
        for categorie in categories_data:
            categories_list += f"`{categorie.get('id')}` - **{categorie.get('name')}**\n"
          
        await msg.edit_text(f"{categories_list}\n**📊 Now send the Category ID to Download**")  
        input1 = await app.listen(user_id=user_id, timeout=30)
        categorie_id = input1.text.strip()
        await input1.delete()

        categorie_name = next((categorie.get('name') for categorie in categories_data if str(categorie.get('id')) == categorie_id), None)
        if not categorie_name:
            return await msg.edit_text("**Invalid Categorie ID. Please try again.**")

        await msg.edit_text(f"**Fetching All Jrf Adda {categorie_name} Batches, Please Wait...**")
      
        data.update({"cat_id": categorie_id})
        response = session.get("https://www.jrfadda.com/app_version_2/allgroups", headers=headers, data=data)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Jrf Adda Group Data")

        group_data = response.json().get("grouplist", [])
        if not group_data:
            return await msg.edit_text("No Group data found.")

        group_list = "📚 **Available Groups:**\n\n"
        exam_list = []
        for group in group_data:
            for exam in group.get("exams"):
              group_list += f"`{exam.get('dlb_xm_id')}` - **{exam.get('dlb_xm_name')}**\n"
              exam_list.append({exam.get('dlb_xm_id'): {"name": exam.get('dlb_xm_name'), "group_id": exam.get('dlb_grp_id')}})
            
        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Exam ID to Download**"
        batch_file = None
        
        if len(group_list) > 4000:
            group_list_name = f"{categorie_name}_groupList_{user_id}.txt"
            with open(group_list_name, "w", encoding="utf-8") as f:
                f.write(group_list)
            batch_file = await app.send_document(chat_id=user_id, document=group_list_name, caption=caption, thumb=thumb)
            os.remove(group_list_name)
        else:
            await msg.edit_text(f"{group_list}\n{caption}")

        input2 = await app.listen(user_id=user_id, timeout=30)
        exam_id = input2.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()

        exam_name, group_id = next(((e.get('name'), e.get('group_id')) for e in exam_list if str(e.get('dlb_xm_id')) == exam_id), (None, None))
        if not exam_name or not group_id:
            return await msg.edit_text("**Invalid Exam ID. Please try again.**")
          
        data.update({"groupId": group_id, "examId": exam_id})
        response_data = session.get("https://www.jrfadda.com/app_version_2/exam/video-series", headers=headers, data=data)
        if response_data.status_code != 200:
            return await msg.edit_text("Failed to fetch Jrf Adda Series Data")
          
        series_data = response_data.json().get("list", [])
        if not series_data:
          return await msd.edit_text("Not found series data")

        series_list = "📚 **Available Series:**\n\n"
        for series in series_data:
          series_list += f"`{series.get('dlb_pkg_id')}` - {series.get('dlb_pkg_title')}"

        caption = "**📊 Now send the Series ID to Download**"
        if len(series_list) > 4000:
            series_list_name = f"{exam_name}_seriesList_{user_id}.txt"
            with open(series_list_name, "w", encoding="utf-8") as f:
                f.write(series_list)
            batch_file = await app.send_document(chat_id=user_id, document=series_list_name, caption=caption, thumb=thumb)
            os.remove(series_list_name)
        else:
            await msg.edit_text(f"{series_list}\n{caption}")

        input3 = await app.listen(user_id=user_id, timeout=30)
        package_id = input3.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()
          
        series_name = next((series.get('dlb_pkg_title') for series in series_data if str(series.get('dlb_pkg_id')) == package_id), None)
        if not series_name:
            return await msg.edit_text("**Invalid Series ID. Please try again.**")
          
        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, headers, data, group_id, package_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Study IQ`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )
        await main_func.send_file(app, file_name, user_id, caption, thumb)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("**⏳ Oops! Time's Up, You didn’t reply in time.**")
    except Exception as e:
        await message.reply_text(f"**Error**: `{e}`")
