import string

a_to_zList = {
    f"appxSection_{letter}": {"name": letter}
    for letter in string.ascii_uppercase
}

PER_PAGE = 15

def get_AppxPage(page: int, appNameDict=a_to_zList, appx: bool = False):
    keys = list(appNameDict.keys())  
    start = page * PER_PAGE
    end = start + PER_PAGE

    # ✅ Agar start >= len(keys), matlab ek bhi button bacha hi nahi
    if start >= len(keys):
        return InlineKeyboardMarkup([[InlineKeyboardButton("🚫 No more pages", callback_data="noop")]])

    buttons = []

    # ✅ Fixed Appx button top pe har page par
    if appx:
        buttons.append([InlineKeyboardButton("🌿 Appx Manual", callback_data="appx_manual")])

    # Normal app buttons
    row = []
    for i, key in enumerate(keys[start:end], 1):
        row.append(InlineKeyboardButton(appNameDict[key]["name"], callback_data=key))
        if i % 3 == 0:  
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # Navigation buttons
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("＜ ᴘʀᴇᴠ", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton("↺ ʙ ᴀ ᴄ ᴋ ↻", callback_data="home_"))
    if end < len(keys):  
        nav.append(InlineKeyboardButton("ɴᴇxᴛ ＞", callback_data=f"page_{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(buttons)
