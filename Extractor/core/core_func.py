from Extractor.modules import vajiramias, khan, careerwill, adda247, kpias, classplus, cdsjourney, videodecrypt
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
    "videodecrypt_": {"name": "VideoDecrypt", "func": videodecrypt.videoDecryptButtons},
}

videoDecryptDict = {
    "abhinaymaths_": {"name": "Abhinay Maths", "func": videoDecrypt},
    "eduteria_": {"name": "Eduteria", "func": videoDecrypt},
    "kotamentors_": {"name": "Kota Mentors", "func": videoDecrypt},
    "missionselection_": {"name": "Mission Selection", "func": videoDecrypt},
    "rankbuddy_": {"name": "Rank Buddy", "func": videoDecrypt},
    "rajputtutorials_": {"name": "Rajput Tutorials", "func": videoDecrypt},
    "pateltutorials_": {"name": "Patel Tutorials", "func": videoDecrypt},
}
