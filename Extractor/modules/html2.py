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
    return s[:150].replace(' ', '_')

def detect_link_type(link: str):
    """Return ('youtube','embed_url') or ('zoom','embed_url') or ('drive','embed_url') or ('pdf','url') or ('other','url')"""
    if not link:
        return "none", ""
    low = link.lower()
    if ".pdf" in low:
        return "pdf", link
    if "youtube.com" in low or "youtu.be" in low:
        # convert to embed
        try:
            if "youtu.be" in low:
                vid = urlparse(link).path.lstrip('/')
            else:
                q = parse_qs(urlparse(link).query)
                vid = q.get("v", [None])[0]
            if vid:
                return "youtube", f"https://www.youtube.com/embed/{vid}"
        except Exception:
            pass
        return "youtube", link
    if "zoom.us/rec/share" in low:
        # try direct iframe
        return "zoom", link
    if "drive.google.com" in low:
        # transform to preview if possible
        m = re.search(r'/file/d/([^/]+)', link)
        if m:
            fid = m.group(1)
            return "drive", f"https://drive.google.com/file/d/{fid}/preview"
        # share link with id param
        q = parse_qs(urlparse(link).query)
        if 'id' in q:
            return "drive", f"https://drive.google.com/file/d/{q['id'][0]}/preview"
        return "drive", link
    # fallback
    return "other", link

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
        # try last colon without space
        parts = right.rsplit(':', 1)
        if len(parts) == 2 and re.search(r'https?://', parts[1]):
            class_title = parts[0].strip()
            link = parts[1].strip()
        else:
            # maybe only link or only title
            if re.search(r'https?://', right):
                class_title = "(Video)"
                link = right
            else:
                class_title = right
                link = ""

    if not subject or subject.strip() == "":
        subject = "Miscellaneous"

    return subject, class_title or "Untitled", link or ""

# -------------------- HTML GENERATOR --------------------
def generate_single_html(lines):
    data = {}
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        subj, title, link = parse_line(ln)
        data.setdefault(subj, []).append((title, link))

    css = """
    :root{
      --bg1:#070016; --bg2:#1a0033; --glass: rgba(255,255,255,0.04);
      --accent1:#f6d365; --accent2:#fda085;
      --muted: #bdb0a0;
    }
    *{box-sizing:border-box;font-family:Inter,ui-sans-serif,Poppins,system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;}
    html,body{height:100%;margin:0;padding:0;background:linear-gradient(180deg,var(--bg1),var(--bg2));color:#fff;}
    .wrap{max-width:1100px;margin:28px auto;padding:20px;}
    header{display:flex;gap:16px;align-items:center;justify-content:space-between;margin-bottom:18px}
    .brand{display:flex;gap:12px;align-items:center}
    .logo{width:64px;height:64px;border-radius:12px;background:linear-gradient(135deg,var(--accent1),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:800;color:#2b0b00;font-size:20px;box-shadow:0 8px 30px rgba(0,0,0,0.5)}
    .title{font-size:20px;font-weight:700}
    .subtitle{color:var(--muted);font-size:13px}
    .controls{display:flex;gap:10px;align-items:center}
    .search{padding:10px 12px;border-radius:10px;border:0;outline:0;background:var(--glass);color:#fff;width:320px}
    .toggle{cursor:pointer;padding:8px;border-radius:10px;background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#2b0b00;font-weight:700;border:none}
    .subjects{margin-top:12px;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}
    .subject-card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.03);backdrop-filter: blur(6px)}
    .subject-header{display:flex;align-items:center;justify-content:space-between;gap:8px}
    .subject-left{display:flex;gap:10px;align-items:center}
    .subject-icon{width:46px;height:46px;border-radius:10px;background:linear-gradient(135deg,#7b2ff7,#ff8a00);display:flex;align-items:center;justify-content:center;font-weight:800}
    .subject-name{font-weight:700}
    .subject-count{color:var(--muted);font-size:13px}
    .class-list{margin-top:12px;display:flex;flex-direction:column;gap:8px}
    .class-item{display:flex;align-items:center;justify-content:space-between;padding:10px;border-radius:10px;background:rgba(0,0,0,0.25);border:1px solid rgba(255,255,255,0.02)}
    .class-left{max-width:68%}
    .class-title{font-weight:600}
    .class-meta{color:var(--muted);font-size:13px;margin-top:6px}
    .btns{display:flex;gap:8px;align-items:center}
    .btn{padding:8px 12px;border-radius:8px;text-decoration:none;font-weight:700;border:none;cursor:pointer}
    .watch{background:linear-gradient(90deg,var(--accent1),var(--accent2));color:#2b0b00}
    .pdf{background:rgba(255,255,255,0.06);color:#fff;border:1px solid rgba(255,255,255,0.04)}
    /* modal */
    .modal{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,0.6);z-index:9999;padding:20px}
    .modal-content{width:100%;max-width:1000px;background:linear-gradient(180deg,#050014,#0b0520);border-radius:12px;overflow:hidden;padding:12px;border:1px solid rgba(255,255,255,0.04)}
    .modal-header{display:flex;justify-content:space-between;align-items:center;padding:8px}
    .modal-close{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer}
    .embed-wrap{position:relative;padding-top:56.25%;background:#000}
    .embed-wrap iframe,.embed-wrap embed{position:absolute;top:0;left:0;width:100%;height:100%;border:0}
    /* responsive */
    @media(max-width:720px){
      .search{width:100%}
      .subjects{grid-template-columns:1fr}
    }
    """

    js = """
    function toggleSubject(id){
      const el = document.getElementById(id);
      if(!el) return;
      el.style.display = (el.style.display==='block') ? 'none' : 'block';
    }
    function openModal(kind, url, title){
      const m = document.getElementById('modal');
      const embedWrap = document.getElementById('embedWrap');
      const hdr = document.getElementById('modalTitle');
      hdr.textContent = title || '';
      // clear
      embedWrap.innerHTML = '';
      if(kind==='pdf'){
        const iframe = document.createElement('iframe');
        iframe.src = url;
        iframe.style.width='100%'; iframe.style.height='100%'; iframe.style.border='0';
        embedWrap.appendChild(iframe);
      } else {
        const iframe = document.createElement('iframe');
        iframe.src = url;
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.setAttribute('allowfullscreen','');
        embedWrap.appendChild(iframe);
      }
      m.style.display = 'flex';
    }
    function closeModal(){
      const m = document.getElementById('modal');
      const embedWrap = document.getElementById('embedWrap');
      m.style.display='none';
      embedWrap.innerHTML='';
    }
    // live search
    function liveSearch(q){
      q = q.trim().toLowerCase();
      const items = document.querySelectorAll('.class-item');
      items.forEach(it=>{
        const txt = it.getAttribute('data-search') || '';
        if(q==='' || txt.indexOf(q)!==-1){
          it.style.display='flex';
        } else it.style.display='none';
      });
    }
    // dark/light toggle - simple invert
    function toggleTheme(){
      const root = document.documentElement;
      if(root.style.getPropertyValue('--bg1') === '#070016'){
        // switch to light-ish
        root.style.setProperty('--bg1','#f6f7fb');
        root.style.setProperty('--bg2','#e9eef8');
        root.style.setProperty('--glass','rgba(0,0,0,0.04)');
        document.body.style.color='#111';
      } else {
        root.style.setProperty('--bg1','#070016');
        root.style.setProperty('--bg2','#1a0033');
        root.style.setProperty('--glass','rgba(255,255,255,0.04)');
        document.body.style.color='#fff';
      }
    }
    """

    # Build body
    parts = []
    parts.append("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>")
    parts.append(f"<style>{css}</style></head><body><div class='wrap'>")
    parts.append("<header><div class='brand'><div class='logo'>R</div><div><div class='title'>Lecture Library</div><div class='subtitle'>Auto-generated — click Watch / PDF to preview</div></div></div>")
    parts.append("<div class='controls'><input class='search' placeholder='Search subjects or class titles...' oninput='liveSearch(this.value)'>")
    parts.append("<button class='toggle' onclick='toggleTheme()'>Toggle Theme</button></div></header>")

    # subjects grid
    parts.append("<div class='subjects'>")
    for subj, items in data.items():
        sid = "S_" + slugify(subj)
        parts.append(f"<div class='subject-card'>")
        parts.append(f"<div class='subject-header'><div class='subject-left'><div class='subject-icon'>{subj[:2].upper()}</div><div><div class='subject-name'>{subj}</div><div class='subject-count'>{len(items)} classes</div></div></div><div><button class='btn' onclick=\"toggleSubject('{sid}')\">Toggle</button></div></div>")
        parts.append(f"<div id='{sid}' style='display:none' class='class-list'>")
        for title, link in items:
            kind, embed = detect_link_type(link)
            short = (link[:80] + '...') if link and len(link) > 80 else (link or "(no link)")
            data_search = (subj + " " + title + " " + (link or "")).lower().replace("'", "")
            # Choose action button
            if kind == "none":
                btn_html = "<span style='color:var(--muted)'>No Link</span>"
            elif kind == "pdf":
                # Open in modal as pdf
                btn_html = f"<button class='btn pdf' onclick=\"openModal('pdf','{embed}','{title}')\">Open PDF</button>"
            else:
                # video/embed: open modal with embed URL
                btn_html = f"<button class='btn watch' onclick=\"openModal('{kind}','{embed}','{title}')\">Watch Now</button>"

            parts.append(f"<div class='class-item' data-search='{data_search}'>"
                         f"<div class='class-left'><div class='class-title'>{title}</div><div class='class-meta'>{short}</div></div>"
                         f"<div class='btns'>{btn_html}<a class='btn pdf' href='{link}' target='_blank' style='text-decoration:none;margin-left:6px'>Open Original</a></div>"
                         f"</div>")
        parts.append("</div></div>")  # class-list + subject-card
    parts.append("</div>")  # subjects

    # modal html
    parts.append("""
    <div id="modal" class="modal" onclick="if(event.target.id==='modal') closeModal()">
      <div class="modal-content" role="dialog" aria-modal="true">
        <div class="modal-header"><div id="modalTitle" style="font-weight:700"></div><button class="modal-close" onclick="closeModal()">✕</button></div>
        <div class="embed-wrap" id="embedWrap"></div>
      </div>
    </div>
    """)

    # footer & scripts
    parts.append(f"<script>{js}</script>")
    parts.append("</div></body></html>")
    return "\n".join(parts)

# ================= PYROGRAM COMMAND =================
@app.on_message(filters.command("html2"))
async def html_cmd(c, m: Message):
    doc_msg = m.reply_to_message if m.reply_to_message and m.reply_to_message.document else m

    if not doc_msg.document:
        return await m.reply_text("Reply to a .txt file containing your data (each line: Subject | Class Title: LINK).")

    if not doc_msg.document.file_name.lower().endswith(".txt"):
        return await m.reply_text("Sirf .txt file hi support hoti hai.")

    tmp = Path(tempfile.mkdtemp(prefix="lect_html_"))
    txt_path = tmp / doc_msg.document.file_name

    await doc_msg.download(str(txt_path))

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        html_content = generate_single_html(lines)
        out_path = tmp / "Lectures.html"
        out_path.write_text(html_content, encoding="utf-8")

        await m.reply_document(document=str(out_path), caption="✨ Here — upgraded single HTML (search, modal viewer, theme toggle).")

    except Exception as e:
        await m.reply_text(f"Error: {e}")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)
