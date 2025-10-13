from Extractor.modules import vajiramias, khan, careerwill, adda247, kpias, classplus, cdsjourney, videocrypt
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    # "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    "khan_": {"name": "Khan", "func": khan.khan_login},
    "careerwill_": {"name": "Careerwill", "func": careerwill.careerwill_login},
    "cdsjourney_": {"name": "CdsJourney", "func": cdsjourney.cdsjourney_login},
    "adda247_": {"name": "Adda 247", "func": adda247.adda_login},
    "classplus_": {"name": "Classplus", "func": classplus.classplus_login},
    "vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    "kpias_": {"name": "kpIAS", "func": kpias.kpias_login},
    "videocrypt_": {"name": "Videocrypt", "func": videocrypt.videocrypt_login},
}

videoCryptDict = {
    "abhinaymaths_": {"name": "Abhinay Maths", "func": videocrypt},
    "eduteria_": {"name": "Eduteria", "func": videocrypt},
    "kotamentors_": {"name": "Kota Mentors", "func": videocrypt},
    "missionselection_": {"name": "Mission Selection", "func": videocrypt},
    "rankbuddy_": {"name": "Rank Buddy", "func": videocrypt},
    "rajputtutorials_": {"name": "Rajput Tutorials", "func": videocrypt},
    "pateltutorials_": {"name": "Patel Tutorials", "func": videocrypt},
}
