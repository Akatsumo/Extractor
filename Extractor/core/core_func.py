from Extractor.modules import vajiramias, utkarsh, appx, khan, careerwill
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    #"appx_": {"name": "Appx", "func": appx.appx_logins},
    "khan_": {"name": "Khan", "func": khan.khan_login},
    "careerwill_": {"name": "Careerwill", "func": careerwill.careerwill_login},
    #"cdsjourney_": {"name": "CdsJourney", "func": modules.cdsjourney.cdsjourney_login},
    #"adda247_": {"name": "Adda 247", "func": modules.adda247.adda_login},
    #"classplus_": {"name": "Classplus", "func": modules.classplus.classplus_login},
    #"vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    #"kpias_": {"name": "kpIAS", "func": modules.kpias.kpias_login},
}

