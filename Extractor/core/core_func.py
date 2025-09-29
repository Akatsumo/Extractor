from Extractor import modules
from Extractor.modules import vajiramias, utkarsh
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    #"appx_": {"name": "Appx", "func": modules.appx.appx_logins},
    "khan_": {"name": "Khan", "func": modules.khan.khan_login},
    "careerwill_": {"name": "Careerwill", "func": modules.careerwill.careerwill_login},
    "cdsjourney_": {"name": "CdsJourney", "func": modules.cdsjourney.cdsjourney_login},
    "adda247_": {"name": "Adda 247", "func": modules.adda247.adda_login},
    "classplus_": {"name": "Classplus", "func": modules.classplus.classplus_login},
    "vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    "kpias_": {"name": "kpIAS", "func": modules.kpias.kpias_login},
}

