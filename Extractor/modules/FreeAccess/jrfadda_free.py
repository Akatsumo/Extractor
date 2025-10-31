import os, time
import asyncio
import requests
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Course-Content --------------------------- #

async def course_content(session, headers, data, group_id, package_id):
    lectures, v_count, p_count = [], 0, 0

    data.update({"dlb_grp_id": group_id, "dlb_pkg_id": package_id})
    response_data = session.post("https://www.jrfadda.com/app_version_2/course-subject", headers=headers, data=data)

    if response_data.status_code != 200:
        return lectures, v_count, p_count

    subject_data = response_data.json().get("list", [])
    if not subject_data:
        return lectures, v_count, p_count

    for subject in subject_data:
        subject_name = subject.get("name")

        response_data = session.post("https://www.jrfadda.com/app_version_2/class-videos-list-new", headers=headers, data=data)
        if response_data.status_code != 200:
            continue

        class_data = response_data.json().get("homedata", [])
        if not class_data:
            continue

        for item in class_data:
            class_name = item.get("title", "N/A")
            pdf_url = item.get("post_pdf_url")
            video_url = item.get("videoUrl")
            aws_hsl = item.get("aws_hsl_path")
            video_post_url = item.get("post_url")

            if pdf_url:
                p_count += 1
                lectures.append(f"{subject_name} | {class_name}: {pdf_url}")
            else:
                v_url = video_url or aws_hsl or video_post_url
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
        for c in categories_data:
            categories_list += f"`{c.get('id')}` - **{c.get('name')}**\n"

        await msg.edit_text(f"{categories_list}\n**📊 Now send the Category ID to Download**")
        input1 = await app.listen(user_id=user_id, timeout=30)
        categorie_id = input1.text.strip()
        await input1.delete()

        categorie_name = next((c.get('name') for c in categories_data if str(c.get('id')) == categorie_id), None)
        if not categorie_name:
            return await msg.edit_text("**Invalid Category ID. Please try again.**")

        await msg.edit_text(f"**Fetching All {categorie_name} Batches, Please Wait...**")

        data1 = {**data, "cat_id": categorie_id}
        response = session.post("https://www.jrfadda.com/app_version_2/allgroups", headers=headers, data=data1)

        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch group data")

        group_data = response.json().get("grouplist", [])
        if not group_data:
            return await msg.edit_text("No Group data found.")

        group_list = "📚 **Available Groups:**\n\n"
        exam_list = []

        for group in group_data:
            for exam in group.get("exams", []):
                group_list += f"`{exam.get('dlb_xm_id')}` - **{exam.get('dlb_xm_name')}**\n"
                exam_list.append({exam.get('dlb_xm_id'): {"name": exam.get('dlb_xm_name'), "group_id": exam.get('dlb_grp_id')}})

        thumb = await main_func.send_file(app, None, None, None, None, onlyThumb=True)
        caption = "**📊 Now send the Exam ID to Download**"
        batch_file = None

        if len(group_list) > 4000:
            fname = f"{categorie_name}_groupList_{user_id}.txt"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(group_list)
            batch_file = await app.send_document(user_id, fname, caption=caption, thumb=thumb)
            os.remove(fname)
        else:
            await msg.edit_text(f"{group_list}\n{caption}")

        input2 = await app.listen(user_id=user_id, timeout=30)
        exam_id = input2.text.strip()
        await input2.delete()
        if batch_file: await batch_file.delete()

        exam_name, group_id = next(((v["name"], v["group_id"]) for d in exam_list for k,v in d.items() if str(k)==exam_id), (None, None))
        if not exam_name:
            return await msg.edit_text("**Invalid Exam ID. Please try again.**")

        data.update({"groupId": group_id, "examId": exam_id})
        response = session.post("https://www.jrfadda.com/app_version_2/exam/video-series", headers=headers, data=data)

        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch series data")

        series_data = response.json().get("list", [])
        if not series_data:
            return await msg.edit_text("Series data not found")

        series_list = "📚 **Available Series:**\n\n"
        for s in series_data:
            series_list += f"`{s.get('dlb_pkg_id')}` - {s.get('dlb_pkg_title')}\n"

        caption = "**📊 Send Series ID to Download**"
        if len(series_list) > 4000:
            fname = f"{exam_name}_seriesList_{user_id}.txt"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(series_list)
            batch_file = await app.send_document(user_id, fname, caption=caption, thumb=thumb)
            os.remove(fname)
        else:
            await msg.edit_text(f"{series_list}\n{caption}")

        input3 = await app.listen(user_id=user_id, timeout=30)
        package_id = input3.text.strip()
        await input3.delete()
        if batch_file: await batch_file.delete()

        series_name = next((s.get('dlb_pkg_title') for s in series_data if str(s.get('dlb_pkg_id')) == package_id), None)
        if not series_name:
            return await msg.edit_text("**Invalid Series ID.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start = time.time()
        lectures, v_count, p_count = await course_content(session, headers, data, group_id, package_id)
        elapsed = main_func.get_time(time.time() - start)

        if not lectures:
            return await msg.edit_text("No Batch Content Found")

        file_name = f"{series_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        caption = (
            f"**App Name:** `JRF Adda`\n"
            f"**Series:** `{series_name}`\n"
            f"📜 Total: `{len(lectures)}`\n"
            f"🍿 Videos: `{v_count}` | 📝 PDFs: `{p_count}`\n"
            f"⌚ Time: `{elapsed}`"
        )
        await main_func.send_file(app, file_name, user_id, caption, thumb)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("**⏳ Timeout! Reply Faster Next Time.**")
    except Exception as e:
        await message.reply_text(f"**Error:** `{e}`")
