import os
import re
import shutil
import tempfile
import zipfile
import asyncio
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from pyrogram import filters
from Extractor import app
from pyrogram.types import Message



# ----------------- Helpers (same logic as earlier) -----------------
def slugify(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r'[\\/*?:"<>|]', "", s)
    s = re.sub(r'\s+', ' ', s)
    s = s.replace(' ', '_')
    return s[:150]

def is_pdf_link(url: str) -> bool:
    return url.lower().split('?')[0].endswith('.pdf')

def is_youtube_link(url: str) -> bool:
    return ("youtube.com" in url) or ("youtu.be" in url)

def youtube_embed_url(url: str) -> str:
    if "youtu.be" in url:
        vid = urlparse(url).path.lstrip('/')
        return f"https://www.youtube.com/embed/{vid}"
    q = parse_qs(urlparse(url).query)
    if "v" in q:
        return f"https://www.youtube.com/embed/{q['v'][0]}"
    if "/embed/" in url:
        return url
    return url

def parse_line(line: str):
    subject = None
    class_title = None
    link = None

    if '|' in line:
        left, right = line.split('|', 1)
        subject = left.strip()
        right = right.strip()
    else:
        right = line.strip()

    if ': ' in right:
        title_part, link_part = right.rsplit(': ', 1)
        class_title = title_part.strip()
        link = link_part.strip()
    else:
        parts = right.rsplit(':', 1)
        if len(parts) == 2 and re.search(r'https?://', parts[1]):
            class_title = parts[0].strip()
            link = parts[1].strip()
        else:
            if re.search(r'https?://', right):
                class_title = "(Video)"
                link = right
            else:
                class_title = right
                link = ""

    if not subject:
        if ' - ' in class_title:
            subject, class_title = [p.strip() for p in class_title.split(' - ',1)]
        else:
            subject = "Miscellaneous"

    return subject or "Miscellaneous", class_title or "Untitled", link or ""

# Minimal CSS + templates (royal-ish)
ROOT_CSS = """/* shortened CSS for brevity - use full CSS if you want */ body{font-family:Arial,Helvetica,sans-serif;background:#0d0327;color:#fff;padding:20px;} .logo{background:linear-gradient(90deg,#f6d365,#fda085);padding:8px;border-radius:8px;display:inline-block} .card{background:rgba(255,255,255,0.03);padding:12px;border-radius:12px;margin:8px 0} .primary-btn{background:linear-gradient(90deg,#f6d365,#fda085);color:#2b0b00;padding:8px 12px;border-radius:8px;text-decoration:none} .player-wrap{position:relative;padding-top:56.25%;background:#000;border-radius:8px;overflow:hidden} iframe,embed{position:absolute;top:0;left:0;width:100%;height:100%;border:0}"""

ROOT_INDEX_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lecture Library</title><style>{css}</style></head><body><div><h1 class="logo">Lecture Library</h1><div>{subject_cards}</div></div></body></html>"""

SUBJECT_INDEX_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{subject}</title><style>{css}</style></head><body><div><h1 class="logo">{subject}</h1><div>{list_items}</div><div style="margin-top:12px"><a href="../index.html" class="primary-btn">All Subjects</a></div></div></body></html>"""

CLASS_PAGE_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body><div><h2>{title}</h2><div class="player-wrap">{embed}</div><p>Original link: <a href="{link}" target="_blank">{short}</a></p><p><a href="index.html" class="primary-btn">Back</a></p></div></body></html>"""

def embed_code_for_link(link: str) -> str:
    if not link:
        return '<div style="padding:20px;color:#ddd">No link.</div>'
    if is_pdf_link(link):
        return f'<embed src="{link}" type="application/pdf" />'
    if is_youtube_link(link):
        emb = youtube_embed_url(link)
        return f'<iframe src="{emb}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    return f'<iframe src="{link}" allow="autoplay; encrypted-media" allowfullscreen></iframe>'

def generate_site_from_text_lines(lines, out_dir: Path):
    data = {}
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        subj, title, link = parse_line(ln)
        data.setdefault(subj, []).append((title, link))

    subject_cards_html = []
    for subj, items in sorted(data.items(), key=lambda x: x[0].lower()):
        slug = slugify(subj) or "subject"
        folder = out_dir / slug
        folder.mkdir(parents=True, exist_ok=True)

        list_items = []
        for title, link in items:
            class_slug = slugify(title) or "class"
            fname = f"{class_slug}.html"
            short = (link[:60] + "...") if link and len(link) > 60 else (link or "(no link)")
            list_items.append(f'<div class="card"><a href="{fname}" target="_blank">{title}</a><div style="color:#bdb0a0">{short}</div></div>')
            embed = embed_code_for_link(link)
            class_html = CLASS_PAGE_TEMPLATE.format(css=ROOT_CSS, title=title, embed=embed, link=link, short=short)
            (folder / fname).write_text(class_html, encoding="utf-8")

        subj_index_html = SUBJECT_INDEX_TEMPLATE.format(css=ROOT_CSS, subject=subj, list_items="\n".join(list_items))
        (folder / "index.html").write_text(subj_index_html, encoding="utf-8")
        subject_cards_html.append(f'<div class="card"><h3>{subj}</h3><div>{len(items)} items</div><a class="primary-btn" href="{slug}/index.html">Open</a></div>')

    root_html = ROOT_INDEX_TEMPLATE.format(css=ROOT_CSS, subject_cards="\n".join(subject_cards_html))
    (out_dir / "index.html").write_text(root_html, encoding="utf-8")



@app.on_message(filters.command("html"))
async def html_cmd(c, m: Message):
    doc_msg = None
    if m.reply_to_message and m.reply_to_message.document:
        doc_msg = m.reply_to_message
    elif m.document:
        doc_msg = m
    else:
        await m.reply_text("Please reply to a message that contains the `.txt` file (or attach it with the command).")
        return

    # ensure it's a text file
    file_name = doc_msg.document.file_name or ""
    if not file_name.lower().endswith(".txt"):
        await m.reply_text("File must be a .txt file (each line: Subject | Class Title: LINK).")
        return

    # create temp dirs
    tmpdir = Path(tempfile.mkdtemp(prefix="html_gen_"))
    txt_path = tmpdir / file_name
    out_dir = tmpdir / "site"
    try:
        await doc_msg.download(file_name=str(txt_path))
        # read lines
        with txt_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # generate site
        out_dir.mkdir(exist_ok=True)
        generate_site_from_text_lines(lines, out_dir)

        # zip the result
        zip_path = tmpdir / "site.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(out_dir):
                for file in files:
                    full = Path(root) / file
                    zf.write(full, arcname=str(full.relative_to(out_dir)))

        # send zip back
        await m.reply_document(document=str(zip_path), caption="Yeh lo — generated site ZIP. Extract and open index.html")
    except Exception as e:
        await m.reply_text(f"Error: {e}")
    finally:
        # cleanup local temp (optional). keep small; remove everything
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass


