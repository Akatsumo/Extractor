import asyncio
import requests
import os
import time
import re
import secrets
import json
from Extractor import app
from Extractor.core import main_func
from pyromod.exceptions import ListenerTimeout

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# ---------------- Crypto helper (same as yours) ----------------
class CryptoHandler:
    def __init__(self):
        self.key = b'%!$!%_$&!%F)&^!^'        
        self.iv = b'#*y*#2yJ*#$wJv*v'        

    def encrypt(self, plain_text: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_base64

    def decrypt(self, encrypted_text: str) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(encrypted_text)), AES.block_size)
        return decrypted_bytes.decode('utf-8')

crypto = CryptoHandler()

# ---------------- Utility ----------------
def gen_device_id(length=16):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# ---------------- Main extractor class ----------------
class UtkarshExtractor:
    def __init__(self):
        self.v_count = 0
        self.p_count = 0
        self.session = requests.Session()
        self.DEFAULT_BASE = "0199456706643659"
        self.BASE = "1994567066436599"
        self.API_BASE = "https://application.utkarshapp.com/index.php"

        self.headers = {
            'userid': '0',
            'devicetype': '1',
            'lang': '1',
            'authorization': 'Bearer 199#sif346a45ybhbr34yredk799',
            'version': '199',
            'user-agent': 'okhttp/4.11.0',
        }

    # Generic POST + decrypt using main_func
    def fetch(self, url, data, key, iv):
        response = self.session.post(url, headers=self.headers, data=data)
        # guard: sometimes API returns non-json or unexpected; handle exceptions
        try:
            decrypted = main_func.decrypt(key, iv, response.text)
            response_data = json.loads(decrypted)
        except Exception:
            return None

        if response_data.get("status") is not True and response_data.get("status") != "true":
            # sometimes API returns status as string "true"
            return None
        return response_data

    # Master categories from online.utkarsh.com (uses site's response encrypted by our crypto)
    def get_master_courses(self):
        r = self.session.get("https://online.utkarsh.com/web/Home/getMasterCat")
        # ensure site returned JSON with 'response' key
        try:
            response_text = r.json().get("response")
            response_data = json.loads(crypto.decrypt(response_text))
        except Exception:
            return []

        master_cats = response_data["data"].get("master_cat", [])
        all_cats = response_data["data"].get("all_cat", [])

        master_dict = {}
        for m in master_cats:
            master_dict[str(m["id"])] = {
                "master_id": m["id"],
                "master_name": m["cat"],
                "popular_sub_cats": m.get("popular_sub_cats", ""),
                "image": m.get("image", ""),
                "sub_categories": []
            }

        for sub in all_cats:
            m_id = str(sub.get("master_type"))
            parent_id = str(sub.get("parent_id", "")).strip()
            if not parent_id or parent_id == "0" or m_id not in master_dict:
                continue

            master_dict[m_id]["sub_categories"].append({
                "sub_id": sub["id"],
                "sub_name": sub["name"],
                "parent_id": parent_id,
                "is_child": sub.get("is_child", "0")
            })
        return list(master_dict.values())

    # Get courses for given category/subcategory (site API; response encrypted by crypto)
    def get_courses(self, cat_id, sub_cat_id):
        cookies = {
            "csrf_name": "efcded0e551a154f509163c665fb7cec",
            "ci_session": "irkdqsvrd1ketajm4g8b0beics2ko3na",
        }
        url = "https://online.utkarsh.com/web/Home/getCourses"
        data = {
            "csrf_name": "efcded0e551a154f509163c665fb7cec",
            "cat": cat_id,
            "sub_cat": sub_cat_id,
            "catBranch_text": "",
            "course_type": "0",
            "page": "1",
        }
        response = requests.post(url, cookies=cookies, data=data)
        try:
            response_text = response.json().get("response", "")
            # sometimes response might have suffix after colon; keep original splitting approach but safer
            if ":" in response_text:
                part = response_text.split(":")[0]
            else:
                part = response_text
            response_data = json.loads(crypto.decrypt(part))
        except Exception:
            return {}
        return response_data

    # ---------------- Recursive fetcher ----------------
    async def fetch_recursive(self, course_id, batch_id, subject_id, node, key, iv, lectures):
        """
        Recursively traverse node which can be:
        - a content dict with 'file_type' (leaf)
        - or a grouping dict with 'list' (children)
        This ensures we never miss deeply nested contents.
        """
        if not isinstance(node, dict):
            return

        # If this is a leaf/content with file_type
        if node.get("file_type") is not None:
            file_type = str(node.get("file_type"))
            title = node.get("title") or node.get("name") or "N/A"

            # video handling
            if file_type == '3':
                # some nodes may not have payload or tile_id - guard it
                tile_id = node.get("payload", {}).get("tile_id") if node.get("payload") else node.get("tile_id")
                data = {
                    "course_id": course_id,
                    "device_id": gen_device_id(),
                    "device_name": "samsungSM-F9360",
                    "download_click": "0",
                    "name": node.get('file_url') or node.get('name', ''),
                    "tile_id": tile_id or 0,
                    "type": "video"
                }

                try:
                    enc = main_func.encrypt(key, iv, json.dumps(data))
                    result = self.fetch(
                        f"{self.API_BASE}/data_model/meta_distributer/on_request_meta_source",
                        enc, key, iv
                    )
                except Exception:
                    result = None

                if result and result.get("data"):
                    urls = result.get('data', {}).get('bitrate_urls', []) or []
                    if urls:
                        try:
                            best = max(urls, key=lambda x: int(x.get('sort', 0)))
                            best_url = best.get('url', '')
                            url = re.sub(r'\\/', '/', best_url.split('?', 1)[0]).replace("https\\:", "https:")
                            self.v_count += 1
                            lectures.append(f"{title}: {url}")
                        except Exception:
                            pass
                    else:
                        link = result['data'].get('link')
                        if link:
                            self.v_count += 1
                            url = link if link.startswith("https") else f"https://youtu.be/{link}"
                            lectures.append(f"{title}: {url}")
                return

            # non-video leaf (pdf, doc, notes, images, etc.)
            else:
                # prefer file_url else fallback to direct name
                raw_url = node.get("file_url") or node.get("url") or node.get("name", "")
                if raw_url:
                    self.p_count += 1
                    url = re.sub(r'\\/', '/', raw_url).replace("https\\:", "https:")
                    lectures.append(f"{title}: {url}")
                return

        # If node has children in 'list' or nested keys -> descend
        # Common patterns: node["list"] is list of children; sometimes 'meta' or 'data' holds list
        child_lists = []
        if "list" in node and isinstance(node["list"], list):
            child_lists.append(node["list"])

        # some nodes wrap children in meta.list
        if node.get("meta") and isinstance(node["meta"], dict) and isinstance(node["meta"].get("list"), list):
            child_lists.append(node["meta"]["list"])

        # direct children fields
        for key_name in ("children", "subtopics", "topics"):
            if node.get(key_name) and isinstance(node[key_name], list):
                child_lists.append(node[key_name])

        # Flatten and recurse
        for cl in child_lists:
            for child in cl:
                await self.fetch_recursive(course_id, batch_id, subject_id, child, key, iv, lectures)

    # ---------------- Process course (entry point) ----------------
    async def process_course(self, course_id, batch_id, key, iv):
        data = {"course_id": course_id, "parent_id": batch_id}
        encrypted_data = main_func.encrypt(key, iv, json.dumps(data))

        course_detail = self.fetch(
            f"{self.API_BASE}/data_model/course_deprecated/get_course_detail",
            encrypted_data, key, iv
        )

        lectures = []
        if not course_detail or "data" not in course_detail:
            return lectures

        # iterate tiles; some tiles may contain 'list' directly or under meta
        for tile in course_detail["data"].get("tiles", []):
            # process both 'content' and 'course_combo' depending on structure
            if tile.get("type") not in ("content", "course_combo", "course_list"):
                continue

            # some tiles use tile["meta"]["list"]
            topic_list = tile.get("meta", {}).get("list", []) or tile.get("meta", {}).get("data", []) or tile.get("meta", {}).get("items", []) or tile.get("meta", {}).get("list", [])
            # fallback: tile might directly have 'list'
            if not topic_list and isinstance(tile.get("list"), list):
                topic_list = tile.get("list")

            for topic in topic_list or []:
                await self.fetch_recursive(course_id, batch_id, topic.get("id"), topic, key, iv, lectures)

        return lectures

    # ---------------- Interactive login + flow ----------------
    async def start_login(self, app, message, user_id=None):
        user_id = user_id if user_id else message.from_user.id
        try:
            msg = await message.reply_text("🔑 Enter login credentials (Mobile*Password or Token):")
            input1 = await app.listen(user_id=user_id, timeout=30)
            raw_text = input1.text.strip()
            await input1.delete()

            if '*' in raw_text:
                email, password = raw_text.split("*", 1)
                key, iv = main_func.gen_key_iv(self.DEFAULT_BASE)
                login_data = {
                    "device_id": gen_device_id(),
                    "device_token": "utkarsh_device",
                    "is_social": "0",
                    "mobile": email.strip(),
                    "password": password.strip()
                }

                encrypted_data = main_func.encrypt(key, iv, json.dumps(login_data))
                response = self.fetch(
                    f"{self.API_BASE}/data_model/users/login_auth",
                    encrypted_data, key, iv
                )

                if not response or "data" not in response:
                    return await msg.edit_text("❌ Login failed. Please try again.")
                token = response["data"].get("jwt")
            else:
                token = raw_text

            await msg.edit_text("✅ Login Successful")
            user_data = main_func.jwt_decoder(token)
            user_id_api = user_data.get('id')
            self.headers.update({"jwt": token, "userid": str(user_id_api)})

            key, iv = main_func.gen_key_iv(self.BASE, user_id_api)
            data = {"user_id": user_id_api}
            encrypted_data = main_func.encrypt(key, iv, json.dumps(data))

            master_data = self.get_master_courses()
            if not master_data:
                return await msg.edit_text("Master course not found !!")

            master_list_text = "📚 **Available Masters:**\n\n"
            for master in master_data:
                master_list_text += f"`{master.get('master_id')}` - {master.get('master_name')}\n"

            await msg.edit_text(f"{master_list_text}\n\n📊 **Now send the Master ID to Download**")
            input2 = await app.listen(user_id=user_id, timeout=30)
            master_id = input2.text.strip()
            await input2.delete()

            master_name, sub_content = next(((c['master_name'], c['sub_categories']) for c in master_data if str(c['master_id']) == str(master_id)), (None, None))
            if not master_name:
                return await msg.edit_text("Only valid Master IDs are accepted")

            await msg.edit_text(f"Fetching All {master_name} Batches, Please Wait...")
            batch_list = []
            seen_ids = set()
            course_batches = "📚 **Available Batches:**\n\n"

            for sub in sub_content:
                parent_id = str(sub.get("parent_id"))
                sub_cat_id = str(sub.get("sub_id"))
                course_response = self.get_courses(parent_id, sub_cat_id)
                course_data = course_response.get("data", []) if isinstance(course_response, dict) else []
                for course in course_data:
                    cid = str(course.get("id"))
                    if cid in seen_ids:
                        continue
                    seen_ids.add(cid)
                    batch_list.append(course)
                    course_batches += f"`{cid}` - **{course.get('title')}**\n"

            thumb = await main_func.send_file(app, file_name=None, user_id=None, caption=None, thumb=None, onlyThumb=True)
            caption = "**📊 Now send the Batch ID to Download**"
            batch_file = None

            if len(course_batches) > 1000:
                batch_list_name = f"{master_name}_batchList_{user_id}.txt"
                with open(batch_list_name, "w", encoding="utf-8") as f:
                    f.write(course_batches)
                batch_file = await app.send_document(chat_id=user_id, document=batch_list_name, caption=caption, thumb=thumb)
                os.remove(batch_list_name)
            else:
                # show small summary if not too large
                await msg.edit_text(f"{course_batches}\n{caption}")

            input3 = await app.listen(user_id=user_id, timeout=30)
            batch_id = input3.text.strip()
            await input3.delete()
            if batch_file:
                await batch_file.delete()

            batch_name = next((c['title'] for c in batch_list if str(c['id']) == str(batch_id)), None)
            if not batch_name:
                return await msg.edit_text("Only valid batch IDs are accepted")

            await msg.edit_text("📥 Extracting Course Content, Please Wait...")

            start_time = time.time()
            data = {"course_id": batch_id, "parent_id": ""}
            encrypted_data = main_func.encrypt(key, iv, json.dumps(data))
            course_data = self.fetch(f"{self.API_BASE}/data_model/course_deprecated/get_course_detail", encrypted_data, key, iv)

            lectures = []
            if not course_data or 'data' not in course_data:
                return await msg.edit_text("No course data found.")

            # Prioritize tiles that contain course combos (nested courses)
            for tile in course_data["data"].get("tiles", []):
                # We want course_combo as it lists nested courses; but also handle content tiles
                if tile.get("type") not in ("course_combo", "content", "course_list"):
                    continue

                for course in tile.get("meta", {}).get("list", []) or tile.get("meta", {}).get("data", []) or []:
                    sub_lectures = await self.process_course(course.get('id'), batch_id, key, iv)
                    lectures.extend(sub_lectures)

            if not lectures:
                return await msg.edit_text("📭 **No content found in this batch.**")

            end_time = time.time()
            file_name = f"{re.sub(r'[/\\\\]', '_', batch_name)}_{user_id}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(lectures))

            elapsed = main_func.get_time(end_time - start_time)
            caption = (
                f"**App Name** : `Utkarsh`\n"
                f"**Batch Name** : `{batch_name}`\n\n"
                f"📜 **Total Materials** : `{len(lectures)}`\n"
                f"🍿 **Videos** : `{self.v_count}` | 📝 **PDFs** : `{self.p_count}`\n"
                f"⌚️ **Time Taken** : `{elapsed}`"
            )
            await main_func.send_file(app, file_name, user_id, caption, thumb=None)
            # cleanup
            try:
                os.remove(file_name)
            except Exception:
                pass

            await msg.delete()
            await message.reply_text(f"✅ Done\n\n✏️ **Token** : `{token}`")

        except ListenerTimeout:
            await message.reply_text("⏰ Timeout! You took too long to reply.")
        except Exception as e:
            # give full traceback in text mode is sometimes too large; keep concise
            await message.reply_text(f"Error: `{repr(e)}`")


# ---------------- Top-level helper to call from outside ----------------
async def utkarsh_start(_, message, user_id=None):
    uk = UtkarshExtractor()
    await uk.start_login(_, message, user_id)
