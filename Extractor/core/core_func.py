from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Extractor.modules import khan, adda247, classplus, vajiramias, videocrypt, careerwill, utkarsh
from Extractor.modules.FreeAccess import (cdsjourney_free, classplus_free, civilguruji_free, studyiq_free, qualityEducation_free, 
testpaper_free, jincjodhpur_free, geologicalConcepts_free, selectionWay_free, taiyariKarlo_free, sscpinnacle_free, 
chandraInstitute_free, jchemistry_free, pathfinder_free)

# ---------------------------------- AppName-Dict ---------------------------------- #
appNameDict = {
    "khan_": {"name": "ᴋʜᴀɴ", "func": khan.khan_handler},
    "careerwill_": {"name": "ᴄᴀʀᴇᴇʀᴡɪʟʟ", "func": careerwill.careerwill_login},
    "adda247_": {"name": "ᴀᴅᴅᴀ 247", "func": adda247.adda_login},
    "classplus_": {"name": "ᴄʟᴀꜱꜱᴘʟᴜꜱ", "func": classplus.classplus_login},
    "vajiram_": {"name": "ᴠᴀᴊɪʀᴀᴍ", "func": vajiramias.vajiram_login},
    "videocrypt_": {"name": "ᴠɪᴅᴇᴏᴄʀʏᴘᴛ", "func": videocrypt.videocrypt_login},
}

# ---------------------------------- WithoutApp-Dict ---------------------------------- #
WithoutAppDict = {
    "wcdsjourney_": {"name": "ᴄᴅꜱ ᴊᴏᴜʀɴᴇʏ", "func": cdsjourney_free.cdsjourney_access},
    "wclassplus_": {"name": "ᴄʟᴀꜱꜱᴘʟᴜꜱ", "func": classplus_free.classplus_access},
    "wcivilguruji_": {"name": "ᴄɪᴠɪʟ ɢᴜʀᴜᴊɪ", "func": civilguruji_free.civilguruji_access},
    "wstudyiq_": {"name": "ꜱᴛᴜᴅʏ ɪQ", "func": studyiq_free.studyiq_access},
    "wqualityEducation_": {"name": "Qᴜᴀʟɪᴛʏ ᴇᴅᴜᴄᴀᴛɪᴏɴ", "func": qualityEducation_free.qualityEducation_access},
    "wtestpaper_": {"name": "ᴛᴇꜱᴛ ᴘᴀᴘᴇʀ", "func": testpaper_free.testpaper_access},
    "wjincjodhpur_": {"name": "ᴊɪɴᴄ ᴊᴏᴅʜᴘᴜʀ", "func": jincjodhpur_free.jincJodhpur_access},
    "wgeologicalConcepts_": {"name": "ɢᴇᴏʟᴏɢɪᴄᴀʟ ᴄᴏɴᴄᴇᴘᴛꜱ", "func": geologicalConcepts_free.geologicalConcepts_access},
    "wselectionway_": {"name": "ꜱᴇʟᴇᴄᴛɪᴏɴ ᴡᴀʏ", "func": selectionWay_free.selectionWay_access},
    "wtaiyarikrlo_": {"name": "ᴛᴀɪʏᴀʀɪ ᴋʀʟᴏ", "func": taiyariKarlo_free.taiyarKarlo_access},
    "wsscpinnacle_": {"name": "ꜱꜱᴄ ᴘɪɴɴᴀᴄʟᴇ", "func": sscpinnacle_free.sscpinnacle_access},
    "wchandraInstitute_": {"name": "ᴄʜᴀɴᴅʀᴀ ɪɴꜱᴛɪᴛᴜᴛᴇ", "func": chandraInstitute_free.chandraInstitute_access},
    "wjchemistry_": {"name": "ᴊ ᴄʜᴇᴍɪꜱᴛʀʏ", "func": jchemistry_free.jchemistry_access},
    "wpathfinder_": {"name": "ᴘᴀᴛʜ ꜰɪɴᴅᴇʀ", "func": pathfinder_free.patherfinder_access},
    "wutkarsh_": {"name": "ᴜᴛᴋᴀʀꜱʜ", "func": utkarsh.utkarsh_start},
    # "wjrfadda_": {"name": "ᴊʀꜰ ᴀᴅᴅᴀ", "func": jrfadda_free.jrfadda_access},
}


# ---------------------------------- VideocryptApp-Dict ---------------------------------- #
videoCryptDict = {
    "abhinaymaths_": {"name": "ᴀʙʜɪɴᴀʏ ᴍᴀᴛʜꜱ", "func": videocrypt},
    "eduteria_": {"name": "ᴇᴅᴜᴛᴇʀɪᴀ", "func": videocrypt},
    "kotamentors_": {"name": "ᴋᴏᴛᴀ ᴍᴇɴᴛᴏʀꜱ", "func": videocrypt},
    "missionselection_": {"name": "ᴍɪꜱꜱɪᴏɴ ꜱᴇʟᴇᴄᴛɪᴏɴ", "func": videocrypt},
    "rankbuddy_": {"name": "ʀᴀɴᴋ ʙᴜᴅᴅʏ", "func": videocrypt},
    "rajputtutorials_": {"name": "ʀᴀᴊᴘᴜᴛ ᴛᴜᴛᴏʀɪᴀʟꜱ", "func": videocrypt},
    "pateltutorials_": {"name": "ᴘᴀᴛᴇʟ ᴛᴜᴛᴏʀɪᴀʟꜱ", "func": videocrypt},
    "mypathsala_": {"name": "ᴍʏ ᴘᴀᴛʜꜱᴀʟᴀ", "func": videocrypt},
    "nexttoppers_": {"name": "ɴᴇxᴛ ᴛᴏᴘᴘᴇʀꜱ", "func": videocrypt},
}



