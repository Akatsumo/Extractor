from Extractor.modules import FreeAccess
from Extractor.modules import khan, adda247, classplus, vajiramias, videocrypt, kpias, careerwill, cdsjourney
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

appNameDict = {
    # "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    "khan_": {"name": "Khan", "func": khan.khan_handler},
    "careerwill_": {"name": "Careerwill", "func": careerwill.careerwill_login},
    "cdsjourney_": {"name": "CdsJourney", "func": cdsjourney.cdsjourney_login},
    "adda247_": {"name": "Adda 247", "func": adda247.adda_login},
    "classplus_": {"name": "Classplus", "func": classplus.classplus_login},
    "vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    "kpias_": {"name": "kpIAS", "func": kpias.kpias_login},
    "videocrypt_": {"name": "Videocrypt", "func": videocrypt.videocrypt_login},
}

WithoutAppDict = {
    "wcdsjourney_": {"name": "Cds Journey", "func": FreeAccess.cdsjourney_free.cdsjourney_access},
    "wclassplus_": {"name": "Classplus", "func": FreeAccess.classplus_free.classplus_access},
    "wcivilguruji_": {"name": "Civil Guruji", "func": FreeAccess.civilguruji_free.civilguruji_access},
    "wstudyiq_": {"name": "Study IQ", "func": FreeAccess.studyiq_free.studyiq_access},
    "wqualityEducation_": {"name": "Quality Education", "func": FreeAccess.qualityEducation_free.qualityEducation_access},
    "wtestpaper_": {"name": "Test Paper", "func": FreeAccess.testpaper_free.testpaper_access},
    "wjincjodhpur_": {"name": "Jinc Jodhpur", "func": FreeAccess.jincjodhpur_free.jincJodhpur_access},
    "wcareerwill_": {"name": "Careerwill", "func": FreeAccess.careewill_free.careerwill_access},
    "wgeologicalConcepts_": {"name": "Geological Concepts", "func": FreeAccess.geologicalConcepts_free.geologicalConcepts_access},
    "wselectionway_": {"name": "Selection Way", "func": FreeAccess.selectionWay_free.selectionWay_access},
    "wtaiyarikrlo_": {"name": "Taiyari Krlo", "func": FreeAccess.taiyariKarlo_free.taiyarKarlo_access},
}

videoCryptDict = {
    "abhinaymaths_": {"name": "Abhinay Maths", "func": videocrypt},
    "eduteria_": {"name": "Eduteria", "func": videocrypt},
    "kotamentors_": {"name": "Kota Mentors", "func": videocrypt},
    "missionselection_": {"name": "Mission Selection", "func": videocrypt},
    "rankbuddy_": {"name": "Rank Buddy", "func": videocrypt},
    "rajputtutorials_": {"name": "Rajput Tutorials", "func": videocrypt},
    "pateltutorials_": {"name": "Patel Tutorials", "func": videocrypt},
    "mypathsala_": {"name": "My Pathsala", "func": videocrypt},
}
