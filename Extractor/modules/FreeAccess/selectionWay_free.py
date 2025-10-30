import os, time
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def course_content(session, batch_id, msg):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(f"https://backend.multistreaming.site/api/courses/{batch_id}/classes?populate=full")
    topics_data = response_data.json().get("data", {}).get("classes")
    if not topics_data:
        return lectures, v_count, p_count
        
    for topic in topics_data:
        topic_name = topic.get("topicName", "Unknown Topic")
        for cls in topic.get("classes", []):
          title = cls.get("title", "No Title")
          class_link = cls.get("class_link", "No class link")
          if class_link:
            v_count += 1
            lectures.append(f"{topic_name} | {title}: {class_link}")
          pdfs = cls.get("classPdf", [])
          if pdfs:
            for pdf in pdfs:
              p_count += 1
              pdf_name = pdf.get("name", "Unnamed PDF")
              pdf_url = pdf.get("url", "")
              lectures.append(f"{topic_name} | {pdf_name}: {pdf_url}")

    return lectures, v_count, p_count


async def selectionWay_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    try:
        api_url = "https://backend.multistreaming.site/api/courses/filter"
        data = {"userId": "0", "isRecorded": False, "isLive": False}
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 Recording", callback_data="data_recording")],
            [InlineKeyboardButton("🔴 Live", callback_data="data_live")]
        ])
        mm = await message.reply_text(
            "🕹 **Select Selection Way Batches Mode 👇**\n\nLive\nRecording",
            reply_markup=buttons
        )
        r = await mm.wait_for_click(from_user_id=user_id)
        await mm.delete()
        if r.data == "data_live":
            data.update({"isLive": True})
            mode = "Live"
        else:
            data.update({"isRecorded": True})
            mode = "Recording"
            
        msg = await message.reply_text(f"Fetching All Selection Way {mode} Batches. Please Wait...")
        response = session.post(api_url, json=data)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Selection Way batches")
            
        batch_data = response.json().get("data", {}).get("courses", [])
        if not batch_data:
            return await msg.edit_text("No course data found ")
            
        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('id')}` - **{course.get('title')}**\n"
            
        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None
        
        if len(batch_list) > 4000:
            batch_list_name = f"SelectionWay_batchList_{user_id}.txt"
            with open(batch_list_name, "w", encoding="utf-8") as f:
                f.write(batch_list)
            batch_file = await _.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
            os.remove(batch_list_name)
            await msg.delete()
        else:
            await msg.edit_text(f"{batch_list}\n{caption}")
            
        input2 = await _.listen(user_id=user_id, timeout=30)
        batch_id = input2.text.strip()
        await input2.delete()
        if batch_file:
            await batch_file.delete()
            
        batch_name = next((course["title"] for course in batch_data if str(course["id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")
            
        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id, msg))
        end_time = time.time()
        
        if not lectures:
            return await msg.edit_text("No Batch Content found")
            
        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))
            
        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Selection Way`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )
        await main_func.send_file(_, file_name, user_id, caption, thumb)
        await msg.delete()
    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"**Error:** `{e}`")

  
