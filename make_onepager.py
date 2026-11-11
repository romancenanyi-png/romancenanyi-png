"""One-page intro PDF (CN + EN): readable in 3 seconds."""
import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
PHOTO = "data:image/jpeg;base64," + base64.b64encode((HERE / "photo.jpg").read_bytes()).decode()

CSS = """
@page { size: A4; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }
body { width:210mm; height:297mm; font-family:"Microsoft YaHei","Segoe UI",sans-serif; color:#13241c; background:#fff; }
.top { background:#0e4d3a; color:#fff; padding:16mm 16mm 12mm; display:flex; gap:10mm; align-items:center; }
.top img { width:38mm; height:50mm; object-fit:cover; border-radius:4mm; border:1.2mm solid #f2d65c; }
.name { font-size:30pt; font-weight:900; }
.role { font-size:15pt; color:#f2d65c; font-weight:700; margin-top:2mm; }
.line { font-size:12.5pt; margin-top:4mm; line-height:1.5; color:#dcefe6; }
.nums { display:flex; gap:5mm; padding:11mm 16mm 0; }
.n { flex:1; background:#f6f4ec; border-radius:4mm; padding:7mm 4mm; text-align:center; }
.n b { display:block; font-size:34pt; color:#0e4d3a; font-weight:900; line-height:1.1; }
.n span { font-size:11.5pt; color:#4a5a52; }
h2 { font-size:17pt; color:#0e4d3a; margin:12mm 16mm 5mm; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:7mm 7mm; padding:0 16mm; }
.c { border-left:1.4mm solid #f2d65c; padding:2mm 0 2mm 4mm; }
.c b { font-size:14pt; } .c p { font-size:11.5pt; color:#4a5a52; margin-top:1mm; line-height:1.45; }
.how { margin:12mm 16mm 0; background:#0e4d3a; color:#fff; border-radius:4mm; padding:8mm 8mm; font-size:14pt; line-height:1.6; }
.how em { font-style:normal; color:#f2d65c; font-weight:800; }
.foot { position:absolute; left:16mm; right:16mm; bottom:12mm; display:flex; justify-content:space-between;
        font-size:11pt; color:#0e4d3a; border-top:0.4mm solid #cfdcd5; padding-top:4mm; }
"""

CN = dict(
    name="岑荣马 Matcen", role="AI 外贸获客 · AI 工作流搭建",
    line="2023 年进入外贸 · 深圳<br>用 ChatGPT + Claude，一个人跑通外贸获客全流程",
    nums=[("150+", "网站自然询盘"), ("90分", "第三方 SEO 审核"), ("55+", "Facebook 线索"), ("28", "AI 主动开发询盘")],
    h2="我能帮你做",
    cards=[("外贸独立站 + 谷歌 SEO / GEO", "建站、关键词、内容，30 分钟看出网站问题"),
           ("Facebook 投流 + 自动分析", "表单 / 互动广告，AI 自动算线索成本"),
           ("海外社媒与视频", "TikTok、YouTube、Facebook 选题、脚本、剪辑"),
           ("AI 主动开发客户", "谷歌地图 + 社媒找真实买家、写开发信"),
           ("海外账号 + AI 部署", "账号注册维护、稳定办公环境、教会团队用 AI"),
           ("AI 办公 + CRM / 报价系统", "重复工作交给 AI，搭建业务系统")],
    how="我的做法：<em>AI 做 80%</em>，我负责 <em>20%</em> 的诊断、核实和拍板。<br>只要 AI 能解决的问题，都可以找我。",
    foot=("📞 +86 136 1031 4007", "✉ romancenanyi@gmail.com", "github.com/romancenanyi-png"),
)
EN = dict(
    name="Matcen (Rongma Cen)", role="AI Workflow Builder · B2B Growth",
    line="In foreign trade since 2023 · Shenzhen, China<br>Runs the full B2B lead-generation funnel with ChatGPT + Claude",
    nums=[("150+", "organic website inquiries"), ("90/100", "independent SEO audit"), ("55+", "Facebook ad leads"), ("28", "AI-prospected inquiries")],
    h2="What I can do for you",
    cards=[("B2B website + SEO / GEO", "Build, keyword-map and audit sites; spot fatal issues in 30 min"),
           ("Facebook ads + automated analysis", "Lead-form and engagement ads; AI tracks cost per qualified lead"),
           ("Social content & video", "TikTok, YouTube, Facebook: topics, scripts, AI editing"),
           ("AI buyer prospecting", "Find and verify real buyers on Google Maps and social media"),
           ("Overseas accounts + AI rollout", "Set up platform accounts and AI tools; train the team"),
           ("AI office + CRM / quotation tools", "Automate repetitive work; prototype business systems")],
    how="How I work: <em>AI does 80%</em> of the execution; I own the <em>20%</em> — diagnosis, fact-checking, approval.<br>If AI can solve it, I can deliver it.",
    foot=("📞 +86 136 1031 4007", "✉ romancenanyi@gmail.com", "github.com/romancenanyi-png"),
)

def page(d):
    nums = "".join(f'<div class="n"><b>{a}</b><span>{b}</span></div>' for a, b in d["nums"])
    cards = "".join(f'<div class="c"><b>{a}</b><p>{b}</p></div>' for a, b in d["cards"])
    foot = "".join(f"<span>{x}</span>" for x in d["foot"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="position:relative">
<div class="top"><img src="{PHOTO}"><div><div class="name">{d['name']}</div><div class="role">{d['role']}</div><div class="line">{d['line']}</div></div></div>
<div class="nums">{nums}</div><h2>{d['h2']}</h2><div class="grid">{cards}</div><div class="how">{d['how']}</div>
<div class="foot">{foot}</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for d, out in [(CN, "岑荣马-一页简介.pdf"), (EN, "Matcen-One-Page-Intro.pdf")]:
        pg.set_content(page(d)); pg.wait_for_timeout(300)
        pg.pdf(path=str(HERE / out), format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        pg.screenshot(path=str(HERE / (out + ".png")), full_page=True)
        print(out)
    b.close()
