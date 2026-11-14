# -*- coding: utf-8 -*-
import hashlib, html, re, pathlib

SRC = pathlib.Path.home() / "龙虾文件夹/总管家专家团/清单/海外物品清单_2026越南香港国内_Robin.md"
OUT = pathlib.Path(__file__).resolve().parent.parent / "index.html"
md = SRC.read_text(encoding="utf-8")

# extract version
m = re.search(r"\*\*📌 版本\*\*：\*\*(v[\d.]+)\*\* ｜ 刷新时间：([^（]*)", md)
ver, vtime = (m.group(1), m.group(2).strip()) if m else ("v1.7", "2026-11-14")

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = s.replace("⚠️", '<span class="warn">⚠️</span>').replace("💰", '<span class="money">💰</span>')
    return s

lines = md.splitlines()
sections, cur = [], None
for ln in lines:
    if ln.startswith("# "):
        continue
    if ln.startswith("## ") or ln.startswith("### "):
        cur = {"title": ln.lstrip("#").strip(), "items": [], "note": None}
        sections.append(cur); continue
    if cur is None: continue
    mi = re.match(r"- \[( |x|X)\] (?:\*\*([A-Z]\d+)\*\* )?(.*)", ln)
    if mi:
        code = mi.group(2) or hashlib.md5(mi.group(3).encode()).hexdigest()[:8]
        badge = f'<b class="code">{code}</b>' if mi.group(2) else ""
        cur["items"].append({"id": code, "done": mi.group(1) != " ", "text": badge + inline(mi.group(3))})
    elif ln.startswith("- ") and not cur["items"] and cur["note"] is None:
        cur["note"] = inline(ln[2:].strip())
    elif ln.startswith("> ") and not cur["items"] and cur["note"] is None:
        cur["note"] = inline(ln[2:].strip())

sec_html = ""
for i, s in enumerate(sections):
    total = len(s["items"])
    if not s["items"] and not s["note"]:
        continue
    sec_html += f'<section class="card" id="sec{i}"><h2>{s["title"]}'
    if total:
        sec_html += f' <span class="cnt" id="cnt{i}">0/{total}</span>'
    sec_html += "</h2>"
    if s["note"]:
        sec_html += f'<p class="note">{s["note"]}</p>'
    for it in s["items"]:
        sec_html += f'<label class="item"><input type="checkbox" data-k="{it["id"]}" data-sec="{i}"{" data-md=1 checked" if it["done"] else ""}><span>{it["text"]}</span></label>'
    sec_html += "</section>"

chlog_html = '<br>'.join(inline(l.strip("- ")) for l in lines if re.match(r"^- \*\*v\d", l))
page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>海外物品清单 · 2026 越南香港国内 · {ver}</title>
<style>
:root{{--ink:#1c2430;--bg:#f4f6f9;--card:#fff;--accent:#0a7d4f;--warnb:#b45309;--moneyb:#7c3aed;--line:#e3e8ef}}
*{{box-sizing:border-box}}body{{margin:0;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--ink);line-height:1.55}}
header{{position:sticky;top:0;z-index:9;background:var(--accent);color:#fff;padding:14px 18px;box-shadow:0 2px 8px rgba(0,0,0,.15)}}
header h1{{margin:0;font-size:19px}}header .meta{{font-size:12.5px;opacity:.92;margin-top:3px}}
#bar{{height:6px;background:rgba(255,255,255,.3);border-radius:3px;margin-top:8px;overflow:hidden}}
#barfill{{height:100%;width:0;background:#ffe27a;transition:width .3s}}
main{{max-width:860px;margin:0 auto;padding:14px}}
.card{{background:var(--card);border-radius:14px;padding:16px 18px;margin:14px 0;box-shadow:0 1px 4px rgba(16,32,64,.08);border:1px solid var(--line)}}
h2{{font-size:16.5px;margin:0 0 8px;color:var(--accent);border-bottom:2px solid var(--line);padding-bottom:6px}}
.cnt{{font-size:12px;background:#e6f4ee;color:var(--accent);border-radius:10px;padding:2px 9px;vertical-align:2px;font-weight:600}}
.item{{display:flex;gap:10px;align-items:flex-start;padding:7px 4px;border-bottom:1px dashed var(--line);cursor:pointer;font-size:14.5px}}
.item:last-child{{border-bottom:none}}
.item input{{width:19px;height:19px;margin-top:2px;accent-color:var(--accent);flex:none}}
.item:has(input:checked) span{{color:#9aa4b2;text-decoration:line-through}}
.note{{font-size:13px;color:#5a6572;background:#f0f4f8;border-radius:8px;padding:8px 12px;margin:6px 0}}
.warn{{color:var(--warnb);font-weight:700}}.money{{color:var(--moneyb);font-weight:700}}
.sig{{text-align:center;font-size:16px;font-weight:700;color:var(--accent);padding:18px}}
footer{{text-align:center;font-size:11.5px;color:#93a0af;padding:18px}}
.code{{display:inline-block;min-width:30px;margin-right:6px;font-size:12px;color:#fff;background:#64748b;border-radius:5px;padding:0 5px;text-align:center}}
.chlog{{font-size:12px;color:#5a6572}}
@media print{{header{{position:static}}#bar{{display:none}}.item:has(input:checked) span{{text-decoration:none}}}}
</style></head><body>
<header><h1>🧳 海外物品清单 · 越南—香港—中国 13 天</h1>
<div class="meta">📌 {ver} ｜ 刷新 {vtime}（Sydney）｜ 勾选自动保存在本机 · 改 md 或让文亮改 → 版本号会升级</div>
<div id="bar"><div id="barfill"></div></div></header>
<main>
{sec_html}
<div class="card sig">—— 全部装齐 ✅ 时间：＿＿＿＿＿＿ ——</div>
</main>
<footer>Robin 专用 · noindex ｜ 数据源：海外物品清单 md（龙虾文件夹）｜ 由总管家文亮生成</footer>
<script>
const VER="{ver}",KEY="ck2";
let saved={{}};try{{const raw=localStorage.getItem(KEY);if(raw){{const o=JSON.parse(raw);saved=o.ck;}}}}catch(e){{}}
document.querySelectorAll('input[type=checkbox]').forEach(cb=>{{cb.checked=!!saved[cb.dataset.k]||cb.hasAttribute('data-md');
cb.addEventListener('change',()=>{{const o={{ver:VER,ck:{{}}}};document.querySelectorAll('input[type=checkbox]').forEach(c=>{{if(c.checked)o.ck[c.dataset.k]=1;c.closest('.card').querySelector('.cnt')&&updateCnt(c.closest('.card'))}});
localStorage.setItem(KEY,JSON.stringify(o));updateAll();}});}});
function updateCnt(card){{const cbs=card.querySelectorAll('input');const n=[...cbs].filter(c=>c.checked).length;const el=card.querySelector('.cnt');if(el)el.textContent=n+'/'+cbs.length;}}
function updateAll(){{let t=0,d=0;document.querySelectorAll('.card').forEach(updateCnt);document.querySelectorAll('input').forEach(c=>{{t++;if(c.checked)d++}});
document.getElementById('barfill').style.width=(t?100*d/t:0)+'%';}}
updateAll();
</script></body></html>"""
OUT.write_text(page, encoding="utf-8")
print("WROTE", OUT, len(page), "bytes,", len(sections), "sections,", sum(len(s['items']) for s in sections), "items")
