import os
import time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Course-Content --------------------------- #

async def course_content(session, batch_id, parent_id):
    lectures, v_count, p_count = [], 0, 0
    data = {
        "categoryplanid": batch_id,
        "loggedinkey": "",
        "loginid": "",
        "categoryparentid": parent_id
    }
    response_data = session.post("http://onlineclass.pathfinderacademy.in/api/category/getcategory", data=data)

    if response_data.status_code != 200:
        return lectures, v_count, p_count

    content_data = response_data.json().get("message", [])
    if not content_data:
        return lectures, v_count, p_count

    for content in content_data:
        cat_name = content.get("category_name", "N/A")
        sub_heading = content.get("category_sub_heading", "")
        cat_id = content.get("category_id", "")
        no_of_cat = int(content.get("no_of_category", 0))

        if no_of_cat > 0:
            sub_lectures, sub_v, sub_p = await course_content(session, batch_id, cat_id)
            lectures.extend(sub_lectures)
            v_count += sub_v
            p_count += sub_p
        else:
            data = {
                "categoryplanid": batch_id,
                "loggedinkey": "",
                "loginid": "",
                "categoryid": cat_id,
                "categorymainid": parent_id
            }
            response_video = session.post("http://onlineclass.pathfinderacademy.in/api/video/getvideo", data=data)
            if response_video.status_code != 200:
                continue

            video_data = response_video.json().get("message", [])
            for video in video_data:
                title = video.get("video_title", "N/A")
                file_url = video.get("video_file")
                pdf_url = video.get("video_pdf_document")

                if file_url:
                    v_count += 1
                    lectures.append(f"{sub_heading} | {title} : {file_url}")
                if pdf_url:
                    p_count += 1
                    lectures.append(f"{sub_heading} | {title} : {pdf_url}")

    return lectures, v_count, p_count


# --------------------------- Path-Finder-Access --------------------------- #

async def patherfinder_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("**Fetching All Path Finder Category, Please Wait...**")
        data = {"loggedinkey": "", "loginid": "", "categoryparentid": 0}
        response = session.post("http://onlineclass.pathfinderacademy.in/api/category/gethead", data=data)

        print(response.json())
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Path Finder Category")

        category_data = response.json().get("message", [])
        if not category_data:
            return await msg.edit_text("No Category data found")

        category_list = "📚 **Available Category:**\n\n"
        for category in category_data:
            category_list += f"{category.get('head_id')} - {category.get('head_name')}\n"

        await msg.edit_text(f"{category_list}\n**📊 Now send the Category ID to Download**")
        input1 = await app.listen(user_id=user_id, timeout=30)
        category_id = input1.text.strip()
        await input1.delete()

        category_name = next((category.get('head_name') for category in category_data if str(category.get('head_id')) == category_id), None)
        if not category_name:
            return await msg.edit_text("**Invalid Category ID. Please try again.**")

        await msg.edit_text("**Fetching All Path Finder Batches, Please Wait...**")

        data = {"loggedinkey": "", "loginid": "", "headid": category_id}
        response = session.post("http://onlineclass.pathfinderacademy.in/api/plan/getplanbyhead", data=data)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Path Finder batches")

        batch_data = response.json().get("message", [])
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('plan_id')}` - **{course.get('plan_name')}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"{category_name}_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")

        input2 = await app.listen(user_id=user_id, timeout=30)
        batch_id = input2.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()

        batch_name, parent_id = next(((course["plan_name"], course["category_id"]) for course in batch_data if str(course["plan_id"]) == batch_id), (None, None))
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id, parent_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Path Finder`\n"
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
