"""One-page intro PDF (CN + EN): readable in 3 seconds."""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
PHOTO = "data:image/jpeg;base64," + base64.b64encode((HERE / "photo_client.jpg").read_bytes()).decode()

CSS = """
@page { size: A4; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }
body { width:210mm; height:297mm; font-family:"Microsoft YaHei","Segoe UI",sans-serif; color:#13241c; background:#fff; position:relative; }
.top { background:#0e4d3a; color:#fff; height:118mm; display:flex; }
.txt { flex:1; padding:18mm 0 0 16mm; }
.name { font-size:32pt; font-weight:900; line-height:1.15; }
.role { font-size:17pt; color:#f2d65c; font-weight:800; margin-top:4mm; line-height:1.35; }
.line { font-size:13pt; margin-top:6mm; line-height:1.6; color:#dcefe6; }
.pic { width:84mm; height:118mm; position:relative; overflow:hidden; }
.pic img { width:100%; height:100%; object-fit:cover; object-position:50% 0%; }
.pic span { position:absolute; left:4mm; bottom:5mm; background:#f2d65c; color:#0e4d3a; font-weight:800;
            font-size:11pt; padding:1.5mm 4mm; border-radius:10mm; }
.nums { display:flex; gap:4mm; padding:10mm 16mm 0; }
.n { flex:1; background:#f6f4ec; border-radius:4mm; padding:6mm 2mm; text-align:center; }
.n b { display:block; font-size:32pt; color:#0e4d3a; font-weight:900; line-height:1.1; }
.n span { font-size:11pt; color:#4a5a52; }
h2 { font-size:17pt; color:#0e4d3a; margin:11mm 16mm 5mm; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:5mm 7mm; padding:0 16mm; }
.c { display:flex; align-items:center; gap:4mm; font-size:14pt; font-weight:700; }
.c i { font-style:normal; width:10mm; height:10mm; border-radius:50%; background:#f2d65c; color:#0e4d3a;
       display:flex; align-items:center; justify-content:center; font-size:12pt; font-weight:900; flex:none; }
.how { margin:11mm 16mm 0; background:#0e4d3a; color:#fff; border-radius:4mm; padding:7mm 8mm; font-size:15pt; line-height:1.55; font-weight:700; }
.how em { font-style:normal; color:#f2d65c; }
.foot { position:absolute; left:16mm; right:16mm; bottom:12mm; display:flex; justify-content:space-between;
        font-size:11pt; color:#0e4d3a; border-top:0.4mm solid #cfdcd5; padding-top:4mm; }
"""

CN = dict(
    name="岑荣马<br>Matcen", role="AI 外贸获客<br>AI 工作流搭建",
    line="2023 年进入外贸 · 深圳<br>ChatGPT + Claude 双模型<br>一个人跑通外贸获客全流程",
    tag="海外客户到厂来访",
    nums=[("150+", "网站自然询盘"), ("90分", "SEO 审核"), ("55+", "投流线索"), ("28", "主动开发询盘")],
    h2="我能帮你做",
    cards=["独立站 + 谷歌 SEO", "Facebook 投流", "海外社媒视频", "AI 开发客户", "海外账号 + AI 部署", "AI 办公 + CRM"],
    how="<em>AI 做 80%，我把关 20%。</em><br>只要 AI 能解决的问题，都可以找我。",
    foot=("📞 +86 136 1031 4007", "✉ romancenanyi@gmail.com", "github.com/romancenanyi-png"),
)
EN = dict(
    name="Matcen<br>(Rongma Cen)", role="AI Workflow Builder<br>B2B Growth",
    line="In foreign trade since 2023 · Shenzhen<br>ChatGPT + Claude power user<br>Runs the full B2B lead funnel solo",
    tag="Overseas buyer factory visit",
    nums=[("150+", "organic inquiries"), ("90/100", "SEO audit"), ("55+", "ad leads"), ("28", "prospected inquiries")],
    h2="What I can do for you",
    cards=["B2B website + SEO / GEO", "Facebook ads", "Social video", "AI buyer prospecting", "Accounts + AI rollout", "AI office + CRM"],
    how="<em>AI does 80%, I own the 20% that matters.</em><br>If AI can solve it, I can deliver it.",
    foot=("📞 +86 136 1031 4007", "✉ romancenanyi@gmail.com", "github.com/romancenanyi-png"),
)


def page(d):
    nums = "".join(f'<div class="n"><b>{a}</b><span>{b}</span></div>' for a, b in d["nums"])
    cards = "".join(f'<div class="c"><i>{i + 1:02d}</i>{t}</div>' for i, t in enumerate(d["cards"]))
    foot = "".join(f"<span>{x}</span>" for x in d["foot"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="top"><div class="txt"><div class="name">{d['name']}</div><div class="role">{d['role']}</div><div class="line">{d['line']}</div></div>
<div class="pic"><img src="{PHOTO}"><span>{d['tag']}</span></div></div>
<div class="nums">{nums}</div><h2>{d['h2']}</h2><div class="grid">{cards}</div><div class="how">{d['how']}</div>
<div class="foot">{foot}</div></body></html>"""


with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for d, out in [(CN, "岑荣马-一页简介.pdf"), (EN, "Matcen-One-Page-Intro.pdf")]:
        pg.set_content(page(d)); pg.wait_for_timeout(300)
        pg.pdf(path=str(HERE / out), format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        print(out)
    b.close()
