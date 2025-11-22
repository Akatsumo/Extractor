import os
import tempfile
import shutil
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from pyrogram import filters
from Extractor import app
from pyrogram.types import Message


# -------------------- HELPERS --------------------
def slugify(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r'[\\/*?:"<>|]', "", s)
    s = re.sub(r'\s+', ' ', s)
    return s[:150]


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
        class_title = right
        link = ""

    if not subject:
        subject = "Miscellaneous"

    return subject, class_title, link


# -------------------- HTML GENERATOR --------------------
def generate_single_html(lines):
    data = {}

    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        subj, title, link = parse_line(ln)
        data.setdefault(subj, []).append((title, link))

    # =========== BEAUTIFUL CSS ==============
    CSS = """
    body {
        font-family: 'Poppins', sans-serif;
        background: radial-gradient(circle at top, #1a002b, #090014);
        color: #fff;
        padding: 20px;
    }
    h1 {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        background: linear-gradient(90deg,#f6d365,#fda085);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 25px;
    }
    .subject-box {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        margin: 10px 0;
        border-radius: 14px;
        backdrop-filter: blur(6px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .subject-title {
        font-size: 22px;
        cursor: pointer;
        padding: 8px;
    }
    .class-list { display: none; margin-top: 10px; }
    .class-card {
        background: rgba(255,255,255,0.07);
        padding: 12px;
        border-radius: 12px;
        margin-top: 8px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .btn {
        display: inline-block;
        margin-top: 8px;
        padding: 8px 14px;
        border-radius: 10px;
        font-weight: bold;
        text-decoration: none;
        color: #2b0b00;
        background: linear-gradient(90deg,#f6d365,#fda085);
    }
    """

    # =========== BUILT HTML ==============
    final_html = []
    final_html.append("<!DOCTYPE html><html><head><meta charset='utf-8'>")
    final_html.append("<meta name='viewport' content='width=device-width,initial-scale=1'>")
    final_html.append(f"<style>{CSS}</style></head><body>")
    final_html.append("<h1>Lecture Library</h1>")

    # SUBJECTS
    for subj, items in data.items():
        subject_id = slugify(subj)

        final_html.append(f"""
        <div class='subject-box'>
            <div class='subject-title' onclick="toggle('{subject_id}')">{subj} ({len(items)} classes)</div>
            <div id='{subject_id}' class='class-list'>
        """)

        for title, link in items:
            btn_html = ""

            if link:
                if ".pdf" in link:
                    btn_html = f"<a href='{link}' target='_blank' class='btn'>Open PDF</a>"
                else:
                    btn_html = f"<a href='{link}' target='_blank' class='btn'>Watch Now</a>"
            else:
                btn_html = "<small style='color:#bbb'>No Link</small>"

            final_html.append(f"""
                <div class='class-card'>
                    <div style="font-size:18px;font-weight:600">{title}</div>
                    {btn_html}
                </div>
            """)

        final_html.append("</div></div>")

    # JS TOGGLE
    final_html.append("""
    <script>
    function toggle(id){
        var el = document.getElementById(id);
        el.style.display = (el.style.display === "block") ? "none" : "block";
    }
    </script>
    """)

    final_html.append("</body></html>")
    return "\n".join(final_html)


# ================= PYROGRAM COMMAND =================
@app.on_message(filters.command("html"))
async def html_cmd(c, m: Message):
    doc_msg = m.reply_to_message if m.reply_to_message and m.reply_to_message.document else m

    if not doc_msg.document:
        return await m.reply("Reply to a .txt file containing your data.")

    if not doc_msg.document.file_name.lower().endswith(".txt"):
        return await m.reply("Sirf .txt file hi support hoti hai.")

    tmp = Path(tempfile.mkdtemp())
    txt_path = tmp / doc_msg.document.file_name

    await doc_msg.download(str(txt_path))

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        html_content = generate_single_html(lines)
        out_path = tmp / "Lectures.html"
        out_path.write_text(html_content, encoding="utf-8")

        await m.reply_document(out_path, caption="🎉 Ready! — Beautiful Single HTML Page")

    except Exception as e:
        await m.reply(f"Error: {e}")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)
