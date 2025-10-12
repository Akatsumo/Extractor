import asyncio, json, re, time, base64, traceback
import requests, cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pyrogram.enums import ParseMode
from Extractor.core.func import get_time, send_file
from config import LOGGER_ID

# Thread pool for blocking requests
executor = ThreadPoolExecutor(max_workers=15)

# Regex patterns
DIV_PATTERN = re.compile(r'<div[^>]*class="[^"]*courseItem[^"]*"[^>]*>')
TITLE_PATTERN = re.compile(r'data-title="([^"]+)"')
TYPE_PATTERN = re.compile(r'data-type="([^"]+)"')
ID_PATTERN = re.compile(r'data-id="([^"]+)"')


def decrypt_p(data: str) -> str:
    """AES Decryption helper for protected 'p' data."""
    try:
        iv = bytes.fromhex(data[:32])
        cipher_data = base64.b64decode(data[32:-32])
        key = bytes.fromhex(data[-32:])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(cipher_data), AES.block_size).decode("utf-8")
    except Exception:
        return ""


def extract_key(url: str) -> str:
    """Extract HLS decryption key."""
    try:
        key_url = url.replace('index.m3u8', 'k/timestamp').replace('/w/', '/m/')
        r = requests.get(key_url, timeout=10)
        first, second = r.content[:16], r.content[32:48]
        cipher = AES.new(key=second, mode=AES.MODE_ECB)
        key_data = cipher.decrypt(cipher.decrypt(first))
        return key_data.hex()
    except Exception:
        return ""


class Graphy:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.loop = asyncio.get_event_loop()
        self.semaphore = asyncio.Semaphore(10)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        self.domain = ""
        self.cookies = None
        self.stats = {"videos": 0, "pdfs": 0, "total": 0, "done": 0}
        self.processed_ids = set()

    # ---------- Utility ----------
    async def _req(self, method: str, url: str, **kwargs):
        """Run blocking requests asynchronously."""
        return await self.loop.run_in_executor(
            executor, lambda: self.scraper.request(method, url, **kwargs)
        )

    # ---------- Domain ----------
    async def domain_info(self, domain: str) -> str:
        """Fetch org name from domain."""
        self.domain = urlparse(domain).netloc
        params = {
            'os': 'android', 'domainName': self.domain,
            'version': '3.29.1', 'mobile': 'mobile'
        }

        resp = await self._req(
            "GET", "https://spayeeservers1.com/readerapi/organizations/domainName", params=params
        )
        data = resp.json()
        return data["response"]["name"]

    # ---------- Auth ----------
    async def login(self, email: str, password: str) -> bool:
        """Authenticate user."""
        data = {'email': email, 'password': password}
        resp = await self._req(
            "POST", f"https://{self.domain}/s/authenticate", data=data, headers=self.headers
        )
        if resp.status_code == 200:
            self.cookies = resp.cookies
            return True
        return False

    # ---------- Fetch ----------
    async def fetch_courses(self):
        """Fetch user's courses."""
        params = {'skip': 0, 'limit': 500, 'archived': 'false'}
        resp = await self._req(
            "GET", f"https://{self.domain}/s/mycourses/get",
            params=params, cookies=self.cookies, headers=self.headers
        )
        return resp.json().get('data', {}).get('data', [])

    # ---------- Content Extraction ----------
    async def _get_url(self, url_type, course_id, data_id, item_id=None):
        """Generic resource fetcher with retry and semaphore."""
        async with self.semaphore:
            try:
                if url_type == "video":
                    url = f"https://{self.domain}/s/courses/{course_id}/videos/{data_id}/get"
                elif url_type == "pdf":
                    url = f"https://{self.domain}/s/courses/{course_id}/pdfs/{data_id}/preview/url"
                elif url_type == "liveclass":
                    if not item_id:
                        info = await self._req(
                            "GET", f"https://{self.domain}/s/courses/{course_id}/liveclasses/{data_id}/get",
                            cookies=self.cookies, headers=self.headers
                        )
                        parsed = json.loads(decrypt_p(info.json()['data']))
                        item_id = parsed['spayee:resource'].get('spayee:recordingId')
                        if parsed['spayee:resource'].get('spayee:type') == 'graphylive':
                            return "No recording found"
                    url = f"https://{self.domain}/s/courses/{course_id}/liveclasses/{data_id}/videos/{item_id}/get"
                else:
                    return "Invalid type"

                resp = await self._req("GET", url, cookies=self.cookies, headers=self.headers)
                data = resp.json()

                # Video or Liveclass
                if url_type in {"video", "liveclass"}:
                    stream = data.get('spayee:resource', {}).get('spayee:streamUrl')
                    if not stream:
                        return "No URL"
                    key = extract_key(stream)
                    self.stats["videos"] += 1
                    return f"{stream}HLS_KEY={key}" if key else stream

                # PDF
                elif url_type == "pdf":
                    if not data.get('url'):
                        return "No URL"
                    self.stats["pdfs"] += 1
                    password = decrypt_p(data['p'])
                    return f"{data['url']}PSWD={password}"

            except Exception:
                return "Error retrieving"
            return "No URL"

    async def fetch_content(self, course_id):
        """Fetch all items from one course."""
        resp = await self._req(
            "GET", f"https://{self.domain}/s/courses/{course_id}/take",
            cookies=self.cookies, headers=self.headers
        )

        divs = DIV_PATTERN.findall(resp.text)
        items = []
        for div in divs:
            title = TITLE_PATTERN.search(div)
            dtype = TYPE_PATTERN.search(div)
            did = ID_PATTERN.search(div)
            if not (title and dtype and did):
                continue

            key = f"{dtype.group(1)}:{did.group(1)}"
            if key in self.processed_ids:
                continue
            self.processed_ids.add(key)
            items.append((title.group(1), dtype.group(1), did.group(1)))

        self.stats["total"] += len(items)

        results = []
        for i in range(0, len(items), 5):  # batch = 5
            batch = items[i:i + 5]
            tasks = [
                self._get_url(t, course_id, d)
                for _, t, d in batch
            ]
            urls = await asyncio.gather(*tasks)
            results.extend(f"{title}: {url}\n" for (title, _, _), url in zip(batch, urls))
            self.stats["done"] += len(batch)

        return ''.join(results)

    async def fetch_batch(self, batch_id):
        """Fetch content from all courses in a batch."""
        params = {'skip': 0, 'limit': 100, 'queryData': f'{{"packageId":"{batch_id}"}}'}
        resp = await self._req(
            "GET", f"https://{self.domain}/s/mycourses/get",
            params=params, cookies=self.cookies, headers=self.headers
        )
        data = resp.json()
        courses = [c['_id'] for c in data.get('data', {}).get('data', []) if c.get('isValid', True)]

        results = []
        for i in range(0, len(courses), 3):
            batch = courses[i:i + 3]
            res = await asyncio.gather(*(self.fetch_content(cid) for cid in batch))
            results.extend(res)
        return ''.join(results)

    # ---------- Extraction Main ----------
    async def extract(self, app, query, msg):
        """Main orchestrator."""
        try:
            ask = await msg.reply_text("🌐 Enter Graphy domain:")
            domain_msg = await app.listen(msg.chat.id, query.from_user.id)
            domain = domain_msg.text.strip()
            await domain_msg.delete()

            await ask.edit("🔄 Connecting...")
            org = await self.domain_info(domain)
            await ask.edit(f"🏫 Connected to: {org}\n🔑 Send `ID*Password`")

            creds = await app.listen(msg.chat.id, query.from_user.id)
            await creds.delete()
            if "*" not in creds.text:
                return await ask.edit("❌ Invalid format (use ID*Password)")
            email, password = creds.text.split("*", 1)

            await ask.edit("🔄 Logging in...")
            if not await self.login(email, password):
                return await ask.edit("❌ Login failed")

            if LOGGER_ID:
                try:
                    await app.send_message(
                        LOGGER_ID,
                        f"✅ <b>{org}</b>\nDomain: <code>{domain}</code>\nCreds: <code>{email}*{password}</code>",
                        parse_mode=ParseMode.HTML,
                    )
                except:
                    pass

            await ask.edit("📚 Fetching batches...")
            batches = await self.fetch_courses()
            if not batches:
                return await ask.edit("❌ No batches found")

            batch_list = "\n".join(
                f"{i+1}. {b.get('spayee:resource', {}).get('spayee:title','Batch')}"
                for i, b in enumerate(batches)
            )
            await ask.edit(f"<b>Available Batches:</b>\n\n{batch_list}\n\nSend Batch No:", parse_mode=ParseMode.HTML)

            chosen = await app.listen(msg.chat.id, query.from_user.id)
            idx = int(chosen.text.strip()) - 1
            await chosen.delete()
            if not (0 <= idx < len(batches)):
                return await ask.edit("❌ Invalid batch number")

            batch = batches[idx]
            title = batch['spayee:resource']['spayee:title']
            await ask.edit(f"📥 Extracting: {title}...")

            start = time.time()
            progress_task = asyncio.create_task(self._progress_loop(ask, title))
            content = await (self.fetch_content(batch['_id'])
                             if batch['spayee:resource']['spayee:courseType'] == "normal"
                             else self.fetch_batch(batch['_id']))
            progress_task.cancel()

            filename = f"{title.replace('/', '_')}_{datetime.now():%Y%m%d_%H%M%S}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            elapsed = get_time(time.time() - start)
            caption = (
                f"**App Name:** {org}\n"
                f"**Domain:** `{domain}`\n"
                f"**Batch:** `{title}`\n\n"
                f"🎥 Videos: `{self.stats['videos']}`\n"
                f"📄 PDFs: `{self.stats['pdfs']}`\n"
                f"⏱ Time Taken: `{elapsed}`"
            )
            await send_file(filename, caption, ask, query)

        except Exception as e:
            traceback.print_exc()
            await msg.reply_text(f"❌ Error: {e}")

    async def _progress_loop(self, msg, title):
        """Periodic progress updates."""
        while True:
            await asyncio.sleep(3)
            if self.stats["total"] > 0:
                await msg.edit_text(
                    f"📥 Extracting: {title}\n"
                    f"🎥 Videos: {self.stats['videos']} | 📄 PDFs: {self.stats['pdfs']}\n"
                    f"Progress: {self.stats['done']}/{self.stats['total']}"
                )
            if self.stats["done"] >= self.stats["total"]:
                break


async def graphy(app, query, message):
    """Entry point for bot."""
    return await Graphy().extract(app, query, message)
