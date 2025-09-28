from Extractor import module
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    "utkarsh_": {"name": "Utkarsh", "func": module.utkarsh.handle_utk_logic},
    "appx_": {"name": "Appx", "func": module.appx.appx_logins},
    "khan_": {"name": "Khan", "func": module.khan.khan_login},
    "careerwill_": {"name": "Careerwill", "func": module.careerwill.careerwill_login},
    "cdsjourney_": {"name": "CdsJourney", "func": module.cdsjourney.cdsjourney_login},
    "adda247_": {"name": "Adda 247", "func": module.adda247.adda_login},
    "classplus_": {"name": "Classplus", "func": module.classplus.classplus_login},
    "vajiram_": {"name": "Vajiram", "func": module.vajiram.vajiram_login},
    "kpias_": {"name": "kpIAS", "func": module.kpias.kpias_login},
}

PER_PAGE = 15

def get_page(page: int):
    keys = list(appNameDict.keys())  
    start = page * PER_PAGE
    end = start + PER_PAGE
    buttons = []

    if start >= len(keys):
        return InlineKeyboardMarkup([[InlineKeyboardButton("🚫 No more pages", callback_data="noop")]])

    row = []
    for i, key in enumerate(keys[start:end], 1):
        row.append(InlineKeyboardButton(appNameDict[key]["name"], callback_data=key))
        if i % 3 == 0:  
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton("🔙 Back", callback_data="home_"))
    if end < len(keys):
        nav.append(InlineKeyboardButton("➡️ Next", callback_data=f"page_{page+1}"))
    buttons.append(nav)

    return InlineKeyboardMarkup(buttons)
