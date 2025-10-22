import re, time
import asyncio
import requests 
from Extractor import app
from urllib.parse import urlparse
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout



def clean_video_url(video_html):
    if not video_html:
        return None
    match = re.search(r'src="([^"]+)"', video_html)
    if match:
        return match.group(1)
    return video_html.split()[0] if video_html.strip() else None

def extract_url_parts(original_url):
    parsed = urlparse(original_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) != 3 or parts[0] != "package":
        raise ValueError("Invalid Civil Guruji URL format.")
    return parts[1], parts[2]

async def parse_package_data(courses):
    lectures, v_count, p_count = [], 0, 0
    for course_wrapper in courses:
        course = course_wrapper.get("course", {})
        course_name = course.get("name")
        if not course_name:
            continue
        course_contents = course.get("courseDetail", {}).get("courseContents", [])
        for content in course_contents:
            for sub in content.get("courseSubContents", []):
                sub_name = sub.get("name")
                video_src = clean_video_url(sub.get("videoUrl"))
                if video_src:
                    lectures.append(f"{course_name} | {sub_name}: {video_src.split("?")[0]}")
    return lectures, v_count, p_count


async def civilGuruji_access(_, message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    session = requests.Session()
    try:
        msg = await message.reply_text("🔗 Send the Civil Guruji course URL:")
        input1 = await app.listen(user_id=user_id, timeout=30)
        original_url = input1.text.strip()
        await input1.delete()
        try:
          slug, course_id = extract_url_parts(original_url)
        except ValueError as e:
          return await msg.edit_text(f"❌ Error: {e}")
          
        await msg.edit_text(f"✅ Extracted → url: {slug} | id: {course_id}")
        api_url = f"https://civilguruji.com/_next/data/d25i7ctvZnLYFXs1xZbVS/package/{slug}/{course_id}.json"
        params = {"url": slug, "id": course_id}
        headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0", "x-nextjs-data": "1"}
        response = session.get(api_url, headers=headers, params=params)
        if response.status_code != 200:
            return await msg.edit_text("Failed to fetch Civil Guruji batches")
          
        data = response.json()
        package_data = data.get("pageProps", {}).get("packageDataz", {}).get("packageData", {})
        batch_name = package_data.get("name", "unknown_batch").replace("/", "-")
        batch_courses = package_data.get("courses", [])

        if not batch_name and not batch_courses:
            return await msg.edit_text("No course data found.")

        await msg.edit_text("**Extracting Course Content, Please Wait 📥**")
        start_time = time.time()
        lectures, p_count, v_count = await asyncio.create_task(parse_package_data(batch_courses))
        end_time = time.time()

        if not lectures:
            return await msg.edit_text("No Batch Content found.")

        file_name = f"{batch_name.replace('/', '')}_{user_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(lectures[::-1]))

        elapsed = main_func.get_time(end_time - start_time)
        caption = (
            f"**App Name** : `Study IQ`\n"
            f"**Batch Name** : `{batch_name}`\n\n"
            f"📜 **Total Materials** : `{len(lectures)}`\n"
            f"🍿 **Videos** : `{v_count}` | 📝 **PDFs** : `{p_count}`\n"
            f"⌚️ **Time Taken** : `{elapsed}`"
        )
        await main_func.send_file(app, file_name, user_id, caption)
        await msg.delete()

    except ListenerTimeout:
        await message.reply_text("⏰ You didn’t reply in time. Please try again.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: `{e}`")
