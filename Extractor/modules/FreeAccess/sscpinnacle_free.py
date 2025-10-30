import os, time
import asyncio
import requests 
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout


# --------------------------- Course-Content --------------------------- #

async def course_content(session, batch_id):
    lectures, v_count, p_count = [], 0, 0
    response_data = session.get(f"https://auth.ssccglpinnacle.com/api/youtubeChapters/course/{batch_id}")
    if response_data.status_code != 200:
        return lectures, v_count, p_count
        
    fetch_data = response_data.json().get("data", [])
    if not fetch_data:
        return lectures, v_count, p_count
        
    for item in fetch_data:
        chapter_name = item.get("chapterTitle", "N/A")
        topics = item.get("topics")
      
        if not topics:
          continue
          
        for topic in topics:
          name = topic.get("videoTitle", "N/A")
          video_url = topic.get("videoYoutubeLink", "N/A")
          pdf_name = topic.get("pdfTitle", "N/A")
          pdf_url = topic.get("selectedPdf", "N/A")
          
          if video_url:
            v_count += 1
            lectures.append(f"{chapter_name} | {name}: {video_url}")
            
          if pdf_url:
            p_count += 1
            lectures.append(f"{chapter_name} | {pdf_name}: {pdf_url}")
            
    return lectures, v_count, p_count


# --------------------------- SSC-Pinnacle-Access --------------------------- #

async def sscpinnacle_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()

    try:
        msg = await message.reply_text("**Fetching All SSC Pinnacle Categories, Please Wait..**")

        response_data = session.get("https://auth.ssccglpinnacle.com/categories")
        if response_data.status_code != 200:
            return await msg.edit_text("Failed to fetch SSC Pinnacle Categories.")
          
        categories = response_data.json()
        if not categories:
            return await msg.edit_text("No Categories data found.")

        categorie_text = "📚 **Available Categories:**\n\n"
        for c in categories:
            categorie_text += f"`{c.get('_id')}` - **{c.get('categoryTitle')}**\n"
          
        await msg.edit_text(f"{categorie_text}\n**📊 Now send the Category ID to Download**") 
        input1 = await app.listen(user_id=user_id, timeout=30)
        categorie_id = input1.text.strip()
        await input1.delete()

        categorie_name = next((c.get("categoryTitle") for c in categories if str(c.get("_id")) == categorie_id),None)
        if not categorie_name:
            return await msg.edit_text("**Invalid Category ID. Please try again.**")
          
        await msg.edit_text(f"**Fetching All SSC Pinnacle {categorie_name} Batches, Please Wait..**")

        response = session.get(f"https://auth.ssccglpinnacle.com/mpc/courses?category={categorie_name.strip()}")
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch SSC Pinnacle batches")

        batch_data = response.json()
        print(batch_data)
        if not batch_data:
            return await msg.edit_text("No course data found.")

        batch_list = "📚 **Available Batches:**\n\n"
        for course in batch_data:
            batch_list += f"`{course.get('_id')}` - **{course.get('courseTitle')}**\n"
            
        thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
        caption = "**📊 Now send the Batch ID to Download**"
        batch_file = None
        
        if len(batch_list) > 4000:
            batch_list_name = f"{categorie_name}_batchList_{user_id}.txt"
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

        batch_name = next((course["courseTitle"] for course in batch_data if str(course["_id"]) == batch_id), None)
        if not batch_name:
            return await msg.edit_text("**Invalid Batch ID. Please try again.**")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")

        start_time = time.time()
        lectures, v_count, p_count = await asyncio.create_task(course_content(session, batch_id))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `SSC Pinnacle`\n"
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


