from Extractor import module
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

callbackDict = {
           "utkarsh_" : {"func" : module.utkarsh.handle_utk_logic},
           "appx_" : {"func" : module.appx.appx_logins},
           "khan_" : {"func" : module.khan.khan_login},
           "careerwill_" : {"func" : module.careerwill.careerwill_login},
           "cdsjourney_" : {"func" : module.cdsjourney.cdsjourney_login},
           "adda247_" : {"func" : module.adda247.adda_login},
           "classplus_" : {"func" : mdoule.classplus.classplus_login},
           "vajiram_" : {"func" : module.vajiram.vajiram_login},
           "kpias_" : {"func" : module.kpias.kpias_login},
}




appName = ["CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",
           "CareerWill", "Utkarsh", "Khan", "appx", "CdsJourney",]

PER_PAGE = 15

def get_page(page: int):
    start = page * PER_PAGE
    end = start + PER_PAGE
    buttons = []

    if start >= len(appName):
        return [[InlineKeyboardButton("🚫 No more pages", callback_data="noop")]]

    data = appName[start:end]
    row = []
    for i, d in enumerate(data, 1):
        row.append(InlineKeyboardButton(d, callback_data=f"item_{d}"))
        if i % 3 == 0:
            buttons.append(row)
            row = []
    if row: 
        buttons.append(row)
        
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton("🔙 Back", callback_data="home_"))
    if end < len(appName):
        nav.append(InlineKeyboardButton("➡️ Next", callback_data=f"page_{page+1}"))
    buttons.append(nav)

    return InlineKeyboardMarkup(buttons)





