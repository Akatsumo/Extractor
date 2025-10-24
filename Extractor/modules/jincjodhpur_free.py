import os, time
import asyncio
import requests, json
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


async def course_content(course_section, msg):
    lectures, v_count, p_count = [], 0, 0

    for sub in course_section.get("json", {}).get("WslUV", []):
        for topic in sub.get("to", []):
            for video in topic.get("viPl", []):
                da = video.get("da", "")
                ti = video.get("ti", "No Title")
                if da:
                    url = da if da.startswith("https://www.youtube") else f"https://b7ql8e5g.fs-vid.com/{da}/playlist.m3u8"
                    v_count += 1
                    lectures.append(f"{ti}: {url}")

            for doc in topic.get("doLi", []):
                da = doc.get("da", "")
                ti = doc.get("ti", "No Title")
                if da.endswith(".pdf"):
                    p_count += 1
                    url = f"https://jinc-jodhpur.b-cdn.net/{da}"
                    lectures.append(f"{ti}: {url}")

    return lectures, v_count, p_count


async def jincJodhpur_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    headers = {"content-type": "application/json"}
    payload = {
        "payload": "eyJhY19jbyI6ICJjb19jciIsICJzZSI6ICJmZSIsICJmbiI6ICJjb21tb25fZm4iLCAiZGF0YSI6ICIqIiwgImVuIjogZmFsc2UsICJjb25kIjogeyJPUiI6IHsiQU5EIjogeyJqc29uLT4+JWlLcFJlJVt+XSI6ICIxNjMzMDMxMTg3NDQ5X1NFZHciLCAiaWRbPl0iOiA2M319LCAiT1JERVIiOiAiaWQiLCAiTElNSVQiOiAxMDAwMH0sICJqb2luIjogbnVsbH0="
    }

    try:
        msg = await message.reply_text("Fetching All Jinc Jodhpur Batches. Please Wait...")
        response = session.post("https://cl4.jinc-jodhpur.com/common", headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Jinc Jodhpur batches")

        batch_data = response.json()
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('id')}` - **{course.get('json', {}).get('ALFvY', 'Unknown Batch')}**\n"

        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None

        if len(batch_list) > 4000:
            batch_list_name = f"batchList_{user_id}.txt"
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

        batch_name, course_section = next(((course["json"]["ALFvY"], course) for course in batch_data if str(course["id"]) == batch_id),(None, None))

        if not batch_name or not course_section:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(course_section, msg))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '_')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Jinc Jodhpur`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )

        await main_func.send_file(app, file_name, user_id, caption, thumb)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")

  
