from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Client("my_bot")

# 👇 Apni list yaha do
ITEMS = ["appx", "utkarsh", "aese", "rohan", "sumit", "yadav", "test1", "test2", "test3", "test4", "test5"]
PER_PAGE = 9   # kyunki 3x3 = 9 buttons ek page par

def get_page(page: int):
    start = page * PER_PAGE
    end = start + PER_PAGE
    buttons = []

    if start >= len(ITEMS):
        return [[InlineKeyboardButton("🚫 No more pages", callback_data="noop")]]

    data = ITEMS[start:end]

    # 3 horizontal per row
    row = []
    for i, d in enumerate(data, 1):
        row.append(InlineKeyboardButton(d, callback_data=f"item_{d}"))
        if i % 3 == 0:
            buttons.append(row)
            row = []
    if row:  # agar last row me 3 se kam ho
        buttons.append(row)

    # Navigation row
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton("🔙 Back", callback_data="home_"))
    if end < len(ITEMS):
        nav.append(InlineKeyboardButton("➡️ Next", callback_data=f"page_{page+1}"))
    buttons.append(nav)

    return buttons


@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "🔘 Choose from the list:",
        reply_markup=InlineKeyboardMarkup(get_page(0))
    )


@app.on_callback_query()
async def callback_query_handler(_, query):
    if query.data.startswith("page_"):
        page = int(query.data.split("_")[1])
        await query.message.edit_text(
            "🔘 Choose from the list:",
            reply_markup=InlineKeyboardMarkup(get_page(page))
        )
    elif query.data == "home_":
        await query.message.edit_text(
            "🏠 Home",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📚 Open Menu", callback_data="page_0")]]
            )
        )
    elif query.data.startswith("item_"):
        item = query.data.split("_", 1)[1]
        await query.answer(f"✅ You clicked {item}", show_alert=True)
    elif query.data == "noop":
        await query.answer("🚫 No more pages", show_alert=True)


app.run()
