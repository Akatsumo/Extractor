import os
import re
import base64
import aiohttp
import asyncio
import aiofiles
from Mimiko import app
from pyrogram import filters
from Mimiko.core.main_func import subscribe, chk_user, bot_thumb


def encode_base64(data):
    encoded_data = base64.b64encode(data.encode())
    return encoded_data.decode()


def decode_base64(encoded_data):
    decoded_data = base64.b64decode(encoded_data.encode())
    return decoded_data.decode()


async def classplus_org_id(org_id, session):
    async with session.get(f"https://{org_id}.courses.store") as response:
        html_content = await response.text()
        org_id_match = re.search(r'"orgId":(\d+)', html_content)
        name_match = re.search(r'"name":"([^"]+)"', html_content)
        org_id = org_id_match.group(1) if org_id_match else None
        name = name_match.group(1) if name_match else None
    return org_id, name
