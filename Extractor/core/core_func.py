from Extractor.modules import vajiramias, utkarsh, appx, khan, careerwill, adda247, kpias
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    "khan_": {"name": "Khan", "func": khan.khan_login},
    "careerwill_": {"name": "Careerwill", "func": careerwill.careerwill_login},
    #"cdsjourney_": {"name": "CdsJourney", "func": modules.cdsjourney.cdsjourney_login},
    "adda247_": {"name": "Adda 247", "func": adda247.adda_login},
    #"classplus_": {"name": "Classplus", "func": modules.classplus.classplus_login},
    #"vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    "kpias_": {"name": "kpIAS", "func": kpias.kpias_login},
}

