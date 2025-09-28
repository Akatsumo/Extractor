from Extractor import modules
from Extractor.modules import vajiramias, utkarsh
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    #"appx_": {"name": "Appx", "func": modules.appx.appx_logins},
    #"khan_": {"name": "Khan", "func": modules.khan.khan_login},
    #"careerwill_": {"name": "Careerwill", "func": modules.careerwill.careerwill_login},
    #"cdsjourney_": {"name": "CdsJourney", "func": modules.cdsjourney.cdsjourney_login},
    #"adda247_": {"name": "Adda 247", "func": modules.adda247.adda_login},
    #"classplus_": {"name": "Classplus", "func": modules.classplus.classplus_login},
    #"vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    #"kpias_": {"name": "kpIAS", "func": modules.kpias.kpias_login},
}

PER_PAGE = 15

def get_page(page: int, appNameDict=appNameDict, appx: bool = False):
    keys = list(appNameDict.keys())  
    start = page * PER_PAGE
    end = start + PER_PAGE

    if start >= len(keys):
        return InlineKeyboardMarkup([[InlineKeyboardButton("🚫 No more pages", callback_data="noop")]])

    buttons = []
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
        nav.append(InlineKeyboardButton("＜ ᴘʀᴇᴠ", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton("↺ ʙ ᴀ ᴄ ᴋ ↻", callback_data="home_"))
    if end < len(keys):  
        nav.append(InlineKeyboardButton("ɴᴇxᴛ ＞", callback_data=f"page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(buttons)

                       
