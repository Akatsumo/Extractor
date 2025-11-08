from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Extractor.modules import khan, adda247, classplus, vajiramias, videocrypt, kpias, careerwill
from Extractor.modules.FreeAccess import (cdsjourney_free, classplus_free, civilguruji_free, studyiq_free, qualityEducation_free, 
testpaper_free, jincjodhpur_free, careerwill_free, geologicalConcepts_free, selectionWay_free, taiyariKarlo_free, sscpinnacle_free, 
chandraInstitute_free, jchemistry_free, pathfinder_free)

# ---------------------------------- AppName-Dict ---------------------------------- #
appNameDict = {
    # "utkarsh_": {"name": "Utkarsh", "func": utkarsh.handle_utk_logic},
    "khan_": {"name": "Khan", "func": khan.khan_handler},
    "careerwill_": {"name": "Careerwill", "func": careerwill.careerwill_login},
    "adda247_": {"name": "Adda 247", "func": adda247.adda_login},
    "classplus_": {"name": "Classplus", "func": classplus.classplus_login},
    "vajiram_": {"name": "Vajiram", "func": vajiramias.vajiram_login},
    "kpias_": {"name": "kpIAS", "func": kpias.kpias_login},
    "videocrypt_": {"name": "Videocrypt", "func": videocrypt.videocrypt_login},
}

# ---------------------------------- WithoutApp-Dict ---------------------------------- #
WithoutAppDict = {
    "wcdsjourney_": {"name": "Cds Journey", "func": cdsjourney_free.cdsjourney_access},
    "wclassplus_": {"name": "Classplus", "func": classplus_free.classplus_access},
    "wcivilguruji_": {"name": "Civil Guruji", "func": civilguruji_free.civilguruji_access},
    "wstudyiq_": {"name": "Study IQ", "func": studyiq_free.studyiq_access},
    "wqualityEducation_": {"name": "Quality Education", "func": qualityEducation_free.qualityEducation_access},
    "wtestpaper_": {"name": "Test Paper", "func": testpaper_free.testpaper_access},
    "wjincjodhpur_": {"name": "Jinc Jodhpur", "func": jincjodhpur_free.jincJodhpur_access},
    "wcareerwill_": {"name": "Careerwill", "func": careerwill_free.careerwill_access},
    "wgeologicalConcepts_": {"name": "Geological Concepts", "func": geologicalConcepts_free.geologicalConcepts_access},
    "wselectionway_": {"name": "Selection Way", "func": selectionWay_free.selectionWay_access},
    "wtaiyarikrlo_": {"name": "Taiyari Krlo", "func": taiyariKarlo_free.taiyarKarlo_access},
    "wsscpinnacle_": {"name": "SSC Pinnacle", "func": sscpinnacle_free.sscpinnacle_access},
    "wchandraInstitute_": {"name": "Chandra Institute", "func": chandraInstitute_free.chandraInstitute_access},
    "wjchemistry_": {"name": "J Chemistry", "func": jchemistry_free.jchemistry_access},
    "wpathfinder_": {"name": "Path Finder", "func": pathfinder_free.patherfinder_access},
    # "wjrfadda_": {"name": "Jrf Adda", "func": jrfadda_free.jrfadda_access},
}


# ---------------------------------- VideocryptApp-Dict ---------------------------------- #
videoCryptDict = {
    "abhinaymaths_": {"name": "Abhinay Maths", "func": videocrypt},
    "eduteria_": {"name": "Eduteria", "func": videocrypt},
    "kotamentors_": {"name": "Kota Mentors", "func": videocrypt},
    "missionselection_": {"name": "Mission Selection", "func": videocrypt},
    "rankbuddy_": {"name": "Rank Buddy", "func": videocrypt},
    "rajputtutorials_": {"name": "Rajput Tutorials", "func": videocrypt},
    "pateltutorials_": {"name": "Patel Tutorials", "func": videocrypt},
    "mypathsala_": {"name": "My Pathsala", "func": videocrypt},
    "nexttoppers_": {"name": "Next Toppers", "func": videocrypt},
}



