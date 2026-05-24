# -*- coding: utf-8 -*-
"""
iHerb MPD0133 multilingual landing-page generator.
Usage:  python3 generate.py [SITE_URL]
Outputs a static, SEO/GEO/AEO-optimized site into ../site/
"""
import os, sys, json, html, datetime, shutil
from translations import T

# ---------------------------------------------------------------- config
SITE_URL = (sys.argv[1] if len(sys.argv) > 1 else "https://YOURNAME.github.io/iherb-deal").rstrip("/")
CODE     = "MPD0133"
REF_URL  = "https://www.iherb.com/?rcode=" + CODE
UPDATED  = datetime.date.today().isoformat()
YEAR     = datetime.date.today().year
OUT      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")

LANGS = [
    dict(code="en",    hl="en",      folder="",      native="English",          dir="ltr", og="en_US", cur="USD", match=["en"]),
    dict(code="zh-TW", hl="zh-Hant", folder="zh-tw", native="繁體中文",          dir="ltr", og="zh_TW", cur="TWD", match=["zh-tw","zh-hk","zh-mo","zh-hant"]),
    dict(code="zh-CN", hl="zh-Hans", folder="zh-cn", native="简体中文",          dir="ltr", og="zh_CN", cur="CNY", match=["zh-cn","zh-sg","zh-hans","zh"]),
    dict(code="ja",    hl="ja",      folder="ja",    native="日本語",            dir="ltr", og="ja_JP", cur="JPY", match=["ja"]),
    dict(code="ko",    hl="ko",      folder="ko",    native="한국어",            dir="ltr", og="ko_KR", cur="KRW", match=["ko"]),
    dict(code="es",    hl="es",      folder="es",    native="Español",          dir="ltr", og="es_ES", cur="EUR", match=["es"]),
    dict(code="pt",    hl="pt",      folder="pt",    native="Português",        dir="ltr", og="pt_BR", cur="BRL", match=["pt"]),
    dict(code="de",    hl="de",      folder="de",    native="Deutsch",          dir="ltr", og="de_DE", cur="EUR", match=["de"]),
    dict(code="fr",    hl="fr",      folder="fr",    native="Français",         dir="ltr", og="fr_FR", cur="EUR", match=["fr"]),
    dict(code="it",    hl="it",      folder="it",    native="Italiano",         dir="ltr", og="it_IT", cur="EUR", match=["it"]),
    dict(code="ru",    hl="ru",      folder="ru",    native="Русский",          dir="ltr", og="ru_RU", cur="RUB", match=["ru"]),
    dict(code="ar",    hl="ar",      folder="ar",    native="العربية",          dir="rtl", og="ar_AE", cur="AED", match=["ar"]),
    dict(code="id",    hl="id",      folder="id",    native="Bahasa Indonesia", dir="ltr", og="id_ID", cur="IDR", match=["id","in"]),
    dict(code="th",    hl="th",      folder="th",    native="ไทย",              dir="ltr", og="th_TH", cur="THB", match=["th"]),
    dict(code="vi",    hl="vi",      folder="vi",    native="Tiếng Việt",       dir="ltr", og="vi_VN", cur="VND", match=["vi"]),
    dict(code="hi",    hl="hi",      folder="hi",    native="हिन्दी",            dir="ltr", og="hi_IN", cur="INR", match=["hi"]),
]

CATS = [
    ("cat_vitamins", "\U0001F48A", "vitamins-supplements"),
    ("cat_beauty",   "✨",     "beauty"),
    ("cat_sports",   "\U0001F4AA", "sports"),
    ("cat_grocery",  "\U0001F957", "grocery"),
    ("cat_baby",     "\U0001F37C", "baby-kids"),
    ("cat_bath",     "\U0001F6C1", "bath-personal-care"),
]

def esc(s):  # body / attribute escaping
    return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- template
TEMPLATE = r'''<!DOCTYPE html>
<html lang="%%HTMLLANG%%" dir="%%DIR%%" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESC%%">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="keywords" content="iHerb, MPD0133, iHerb promo code, iHerb discount code, iHerb coupon, iHerb rewards code, vitamins, supplements">
<link rel="canonical" href="%%CANONICAL%%">
%%HREFLANG%%
<meta name="theme-color" content="#1f9d57">
<meta name="author" content="iHerb Savings Guide">
<meta property="og:type" content="website">
<meta property="og:site_name" content="iHerb Code MPD0133">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESC%%">
<meta property="og:url" content="%%CANONICAL%%">
<meta property="og:image" content="%%SITEURL%%/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="%%OGLOCALE%%">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%%TITLE%%">
<meta name="twitter:description" content="%%DESC%%">
<meta name="twitter:image" content="%%SITEURL%%/og.png">
<link rel="icon" href="%%SITEURL%%/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="%%SITEURL%%/icon-180.png">
<link rel="manifest" href="%%SITEURL%%/manifest.webmanifest">
<link rel="preconnect" href="https://www.iherb.com">
<script type="application/ld+json">%%JSONLD%%</script>
%%ROOTREDIRECT%%
<style>
:root{--bg:#f4f7f4;--surface:#ffffff;--surface2:#eef4ee;--text:#13211a;--muted:#5b6b61;
--brand:#1f9d57;--brand2:#16804a;--brand3:#0d5c34;--accent:#ff9f1c;--gold:#f6c453;
--border:#dfe7e0;--shadow:0 6px 24px rgba(13,60,40,.10);--radius:18px;--ok:#1f9d57;--bad:#d25c4d}
html[data-theme=dark]{--bg:#0e1512;--surface:#16201b;--surface2:#1d2a23;--text:#e9f1ec;
--muted:#9db0a4;--border:#27352c;--shadow:0 8px 30px rgba(0,0,0,.45)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue","Noto Sans","Noto Sans TC","Noto Sans JP","Noto Sans KR","Noto Sans Arabic","Noto Sans Thai","Noto Sans Devanagari",Arial,sans-serif;
background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}
img{max-width:100%}
a{color:var(--brand2)}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px}.skip:focus{left:12px;top:12px;background:var(--surface);padding:8px 14px;border-radius:8px;z-index:99}
/* header */
header{position:sticky;top:0;z-index:40;background:color-mix(in srgb,var(--surface) 88%,transparent);
backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.bar{display:flex;align-items:center;gap:12px;padding:10px 0}
.brand{font-weight:800;font-size:18px;display:flex;align-items:center;gap:8px;color:var(--text);text-decoration:none}
.dot{width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,var(--brand),var(--brand3));
display:grid;place-items:center;color:#fff;font-weight:900;font-size:14px}
.spacer{flex:1}
select,.iconbtn{font:inherit;color:var(--text);background:var(--surface);border:1px solid var(--border);
border-radius:10px;padding:7px 10px;cursor:pointer}
.iconbtn{width:38px;height:38px;display:grid;place-items:center;font-size:16px}
/* hero */
.hero{text-align:center;padding:54px 0 30px;
background:radial-gradient(900px 380px at 50% -60px,color-mix(in srgb,var(--brand) 22%,transparent),transparent)}
.badge{display:inline-flex;align-items:center;gap:7px;background:var(--surface);border:1px solid var(--border);
color:var(--brand2);font-weight:700;font-size:13px;padding:6px 13px;border-radius:999px;box-shadow:var(--shadow)}
h1{font-size:clamp(28px,5.4vw,46px);line-height:1.18;margin:16px auto 10px;max-width:18ch;letter-spacing:-.02em}
.lead{color:var(--muted);max-width:60ch;margin:0 auto 22px;font-size:clamp(15px,2.2vw,18px)}
.codecard{background:var(--surface);border:2px dashed var(--brand);border-radius:var(--radius);
box-shadow:var(--shadow);max-width:430px;margin:0 auto;padding:18px}
.codecard .lbl{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:700}
.coderow{display:flex;gap:10px;margin-top:8px}
.code{flex:1;font-size:clamp(24px,5vw,32px);font-weight:900;letter-spacing:.13em;color:var(--brand3);
background:var(--surface2);border-radius:12px;padding:10px;text-align:center;user-select:all}
.btn{font:inherit;font-weight:800;border:0;border-radius:12px;cursor:pointer;padding:13px 20px;
background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;text-decoration:none;
display:inline-flex;align-items:center;justify-content:center;gap:8px;box-shadow:var(--shadow);transition:transform .12s}
.btn:hover{transform:translateY(-2px)}
.btn.alt{background:var(--surface);color:var(--brand2);border:1px solid var(--brand)}
.btn.big{padding:16px 26px;font-size:17px}
.btn.block{display:flex;width:100%}
.copy{padding:0 16px;white-space:nowrap}
.cta-main{margin-top:16px}
.note{font-size:13px;color:var(--muted);margin-top:10px}
.trust{margin-top:18px;font-size:13px;color:var(--muted);font-weight:600}
/* sections */
section{padding:40px 0}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
box-shadow:var(--shadow);padding:24px}
h2{font-size:clamp(21px,3.6vw,30px);letter-spacing:-.02em;margin-bottom:6px}
.sub{color:var(--muted);margin-bottom:20px}
.eyebrow{color:var(--brand2);font-weight:800;font-size:13px;letter-spacing:.08em;text-transform:uppercase}
/* calculator */
.calc{display:grid;gap:14px}
.field label{font-weight:700;font-size:14px;display:block;margin-bottom:6px}
.field input,.field select{width:100%;padding:12px;border-radius:12px;border:1px solid var(--border);
background:var(--surface2);color:var(--text);font:inherit}
.chk{display:flex;align-items:center;gap:10px;font-weight:600}
.chk input{width:20px;height:20px;accent-color:var(--brand)}
.calcgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.res{background:var(--surface2);border-radius:14px;padding:14px;text-align:center}
.res .k{font-size:12px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.05em}
.res .v{font-size:clamp(20px,4vw,28px);font-weight:900;color:var(--brand2);margin-top:3px}
.res.big{grid-column:1/-1;background:linear-gradient(135deg,color-mix(in srgb,var(--brand) 16%,transparent),transparent)}
/* compare */
table{width:100%;border-collapse:collapse;overflow:hidden;border-radius:14px}
th,td{padding:13px 12px;text-align:start;border-bottom:1px solid var(--border);font-size:15px}
thead th{background:var(--surface2);font-size:13px}
th.win{color:var(--brand2)}
td.win{font-weight:800;color:var(--brand2)}
td.lose{color:var(--muted)}
/* steps + grid */
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.step .n{width:34px;height:34px;border-radius:10px;background:var(--brand);color:#fff;font-weight:900;
display:grid;place-items:center;margin-bottom:10px}
.step h3,.cat h3,.ben h3{font-size:16px;margin-bottom:4px}
.muted{color:var(--muted);font-size:14px}
.catgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cat{position:relative;display:block;text-decoration:none;color:var(--text);text-align:center;
background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px 10px;transition:transform .12s,border-color .12s}
.cat:hover{transform:translateY(-3px);border-color:var(--brand)}
.cat .emoji{font-size:30px}
.cat .tag{position:absolute;top:8px;inset-inline-end:8px;background:var(--accent);color:#3a2400;
font-size:10px;font-weight:800;padding:3px 7px;border-radius:999px;display:none}
.cat.today .tag{display:block}
.ben{display:flex;gap:14px;align-items:flex-start}
.ben .ic{font-size:26px;flex:none}
/* deal */
.deal{background:linear-gradient(135deg,var(--brand3),var(--brand2));color:#fff;border:0}
.deal h2,.deal .sub{color:#fff}
.deal .sub{opacity:.9}
.deal .btn{background:#fff;color:var(--brand3)}
/* faq */
details{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:4px 16px;margin-bottom:10px}
summary{font-weight:700;cursor:pointer;padding:13px 0;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--brand);font-weight:900;font-size:20px}
details[open] summary::after{content:"\2212"}
details p{padding:0 0 14px;color:var(--muted)}
/* final + footer */
.final{text-align:center;background:var(--surface2);border-radius:var(--radius);padding:38px 22px}
footer{border-top:1px solid var(--border);padding:30px 0 50px;color:var(--muted);font-size:13px}
.langlinks{display:flex;flex-wrap:wrap;gap:8px 16px;margin:14px 0}
.langlinks a{color:var(--muted);text-decoration:none}
.langlinks a:hover{color:var(--brand2)}
.disc{font-size:12px;line-height:1.7;margin-top:14px;opacity:.85}
.toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(120px);
background:var(--brand3);color:#fff;padding:12px 22px;border-radius:999px;font-weight:700;
box-shadow:var(--shadow);transition:transform .3s;z-index:80}
.toast.show{transform:translateX(-50%) translateY(0)}
@media(max-width:680px){.grid3,.catgrid{grid-template-columns:1fr 1fr}.grid2,.calcgrid{grid-template-columns:1fr}
.coderow{flex-direction:column}}
</style>
</head>
<body>
<a class="skip" href="#main">%%SKIP%%</a>
<header>
 <div class="wrap bar">
  <a class="brand" href="%%SITEURL%%/"><span class="dot">iH</span> iHerb · MPD0133</a>
  <span class="spacer"></span>
  <select id="langsel" aria-label="%%LANG_LABEL%%">%%LANGOPTIONS%%</select>
  <button class="iconbtn" id="theme" aria-label="%%THEME%%">◐</button>
 </div>
</header>

<main id="main">
<section class="hero">
 <div class="wrap">
  <span class="badge">✅ %%BADGE%%</span>
  <h1>%%H1%%</h1>
  <p class="lead">%%SUB%%</p>
  <div class="codecard">
   <div class="lbl">%%CODE_LABEL%%</div>
   <div class="coderow">
    <div class="code" id="code">%%CODE%%</div>
    <button class="btn copy" id="copy">%%COPY%%</button>
   </div>
   <a class="btn block cta-main" id="cta" href="%%REFURL%%" target="_blank" rel="noopener nofollow">%%CTA%% →</a>
   <p class="note">%%CTA_NOTE%%</p>
  </div>
  <p class="trust">%%TRUST%%</p>
 </div>
</section>

<section id="calc">
 <div class="wrap card">
  <span class="eyebrow">%%CALC_TITLE%%</span>
  <h2>%%CALC_TITLE%%</h2>
  <p class="sub">%%CALC_SUB%%</p>
  <div class="calc">
   <div class="calcgrid">
    <div class="field"><label for="amt">%%CALC_AMOUNT%%</label><input id="amt" type="number" min="0" inputmode="decimal" value="60"></div>
    <div class="field"><label for="cur">%%CALC_CUR%%</label><select id="cur"></select></div>
   </div>
   <label class="chk"><input type="checkbox" id="newc" checked> %%CALC_NEW%%</label>
   <div class="calcgrid">
    <div class="res"><div class="k">%%CALC_SAVE%%</div><div class="v" id="rSave">-</div></div>
    <div class="res"><div class="k">%%CALC_CREDIT%%</div><div class="v" id="rCredit">-</div></div>
    <div class="res big"><div class="k">%%CALC_TOTAL%%</div><div class="v" id="rTotal">-</div></div>
   </div>
   <a class="btn block" href="%%REFURL%%" target="_blank" rel="noopener nofollow">%%CTA%% →</a>
  </div>
 </div>
</section>

<section id="compare">
 <div class="wrap">
  <h2>%%COMPARE_TITLE%%</h2>
  <div class="card" style="padding:0;overflow:hidden">
  <table>
   <thead><tr><th>%%COMPARE_FEATURE%%</th><th>%%COMPARE_WITHOUT%%</th><th class="win">%%COMPARE_WITH%%</th></tr></thead>
   <tbody>
    <tr><td>%%COMPARE_R1%%</td><td class="lose">0%</td><td class="win">20%</td></tr>
    <tr><td>%%COMPARE_R2%%</td><td class="lose">—</td><td class="win">10%</td></tr>
    <tr><td>%%COMPARE_R3%%</td><td class="lose">0%</td><td class="win">5%</td></tr>
   </tbody>
  </table>
  </div>
 </div>
</section>

<section id="how">
 <div class="wrap">
  <h2>%%STEPS_TITLE%%</h2>
  <div class="grid3" style="margin-top:18px">
   <div class="card step"><div class="n">1</div><h3>%%STEP1_T%%</h3><p class="muted">%%STEP1_D%%</p></div>
   <div class="card step"><div class="n">2</div><h3>%%STEP2_T%%</h3><p class="muted">%%STEP2_D%%</p></div>
   <div class="card step"><div class="n">3</div><h3>%%STEP3_T%%</h3><p class="muted">%%STEP3_D%%</p></div>
  </div>
 </div>
</section>

<section id="shop">
 <div class="wrap">
  <h2>%%CAT_TITLE%%</h2>
  <div class="catgrid" style="margin-top:18px">%%CATGRID%%</div>
 </div>
</section>

<section>
 <div class="wrap card deal">
  <span class="eyebrow" style="color:#ffe9b8">%%DEAL_TITLE%%</span>
  <h2 id="dealHead">%%DEAL_TITLE%%</h2>
  <p class="sub">%%DEAL_DESC%%</p>
  <a class="btn" id="dealBtn" href="%%REFURL%%" target="_blank" rel="noopener nofollow">%%DEAL_BTN%% →</a>
 </div>
</section>

<section id="why">
 <div class="wrap">
  <h2>%%BENEFITS_TITLE%%</h2>
  <div class="grid3" style="margin-top:18px">
   <div class="card ben"><div class="ic">💸</div><div><h3>%%BENEFIT1_T%%</h3><p class="muted">%%BENEFIT1_D%%</p></div></div>
   <div class="card ben"><div class="ic">🎁</div><div><h3>%%BENEFIT2_T%%</h3><p class="muted">%%BENEFIT2_D%%</p></div></div>
   <div class="card ben"><div class="ic">🌍</div><div><h3>%%BENEFIT3_T%%</h3><p class="muted">%%BENEFIT3_D%%</p></div></div>
  </div>
 </div>
</section>

<section id="faq">
 <div class="wrap">
  <h2>%%FAQ_TITLE%%</h2>
  <div style="margin-top:18px">
   <details open><summary>%%Q1%%</summary><p>%%A1%%</p></details>
   <details><summary>%%Q2%%</summary><p>%%A2%%</p></details>
   <details><summary>%%Q3%%</summary><p>%%A3%%</p></details>
   <details><summary>%%Q4%%</summary><p>%%A4%%</p></details>
  </div>
 </div>
</section>

<section>
 <div class="wrap">
  <div class="final">
   <h2>%%FINAL_TITLE%%</h2>
   <p class="sub">%%TRUST%%</p>
   <a class="btn big" href="%%REFURL%%" target="_blank" rel="noopener nofollow">%%FINAL_BTN%% →</a>
  </div>
 </div>
</section>
</main>

<footer>
 <div class="wrap">
  <strong>%%FOOTER_ABOUT%%</strong> · %%CODE%%
  <nav class="langlinks" aria-label="%%LANG_LABEL%%">%%LANGLINKS%%</nav>
  <div>%%FOOTER_UPDATED%%: %%UPDATED%%</div>
  <p class="disc">%%FOOTER_DISCLAIMER%%</p>
 </div>
</footer>

<div class="toast" id="toast">%%COPIED%%</div>

<script>
var CODE="%%CODE%%",REF="%%REFURL%%",BASE="%%SITEURL%%",PAGECUR="%%PAGECUR%%";
var LANGS=%%LANGDATA%%;
var RATE={USD:1,EUR:.92,GBP:.79,JPY:155,KRW:1360,CNY:7.2,TWD:32,BRL:5.4,RUB:91,INR:84,IDR:16100,THB:36,VND:25400,AED:3.67,MXN:18,AUD:1.52,CAD:1.37,SGD:1.34,PHP:57,MYR:4.6,TRY:34,PLN:4,SAR:3.75};
var CURLOCALE={USD:"en-US",EUR:"de-DE",GBP:"en-GB",JPY:"ja-JP",KRW:"ko-KR",CNY:"zh-CN",TWD:"zh-TW",BRL:"pt-BR",RUB:"ru-RU",INR:"hi-IN",IDR:"id-ID",THB:"th-TH",VND:"vi-VN",AED:"ar-AE",MXN:"es-MX",AUD:"en-AU",CAD:"en-CA",SGD:"en-SG",PHP:"en-PH",MYR:"ms-MY",TRY:"tr-TR",PLN:"pl-PL",SAR:"ar-SA"};
var REGIONCUR={US:"USD",GB:"GBP",JP:"JPY",KR:"KRW",CN:"CNY",TW:"TWD",HK:"USD",BR:"BRL",RU:"RUB",IN:"INR",ID:"IDR",TH:"THB",VN:"VND",AE:"AED",SA:"SAR",MX:"MXN",AU:"AUD",CA:"CAD",SG:"SGD",PH:"PHP",MY:"MYR",TR:"TRY",PL:"PLN",DE:"EUR",FR:"EUR",IT:"EUR",ES:"EUR",NL:"EUR"};
var DEFAMT={USD:60,EUR:55,GBP:48,JPY:9000,KRW:80000,CNY:430,TWD:1900,BRL:320,RUB:5500,INR:5000,IDR:950000,THB:2100,VND:1500000,AED:220,MXN:1100,AUD:90,CAD:80,SGD:80,PHP:3400,MYR:270,TRY:2000,PLN:240,SAR:225};

/* theme */
var root=document.documentElement;
try{var ts=localStorage.getItem('iherb_theme');if(ts)root.setAttribute('data-theme',ts);
else if(matchMedia('(prefers-color-scheme:dark)').matches)root.setAttribute('data-theme','dark');}catch(e){}
document.getElementById('theme').onclick=function(){
 var d=root.getAttribute('data-theme')==='dark'?'light':'dark';
 root.setAttribute('data-theme',d);try{localStorage.setItem('iherb_theme',d);}catch(e){}};

/* language switcher */
var sel=document.getElementById('langsel');
if(sel)sel.onchange=function(){
 try{localStorage.setItem('iherb_lang',sel.value);}catch(e){}
 var f=sel.value;location.href=BASE+'/'+(f?f+'/':'');};

/* copy code */
var toast=document.getElementById('toast');
function showToast(){toast.classList.add('show');setTimeout(function(){toast.classList.remove('show');},1700);}
function doCopy(){
 var ok=function(){showToast();};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(CODE).then(ok,function(){legacy();});}
 else legacy();
 function legacy(){var t=document.createElement('textarea');t.value=CODE;document.body.appendChild(t);
  t.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);ok();}}
document.getElementById('copy').onclick=doCopy;
document.getElementById('code').onclick=doCopy;

/* currency calculator */
var amt=document.getElementById('amt'),cur=document.getElementById('cur'),newc=document.getElementById('newc');
(function(){
 var list=Object.keys(RATE),detected=PAGECUR;
 try{var loc=(navigator.language||'en-US').split('-');if(loc[1]&&REGIONCUR[loc[1].toUpperCase()])detected=REGIONCUR[loc[1].toUpperCase()];}catch(e){}
 if(list.indexOf(detected)<0)detected=PAGECUR;
 for(var i=0;i<list.length;i++){var o=document.createElement('option');o.value=list[i];o.textContent=list[i];
  if(list[i]===detected)o.selected=true;cur.appendChild(o);}
 amt.value=DEFAMT[detected]||60;
})();
function money(n,c){try{return new Intl.NumberFormat(CURLOCALE[c]||'en-US',{style:'currency',currency:c,maximumFractionDigits:(['JPY','KRW','VND','IDR'].indexOf(c)>=0?0:2)}).format(n);}catch(e){return c+' '+Math.round(n);}}
function calc(){
 var a=parseFloat(amt.value)||0,c=cur.value,d=newc.checked?0.20:0.05;
 document.getElementById('rSave').textContent=money(a*d,c);
 document.getElementById('rCredit').textContent=money(a*0.10,c);
 document.getElementById('rTotal').textContent=money(a*(1-d),c);}
amt.oninput=calc;cur.onchange=function(){amt.value=DEFAMT[cur.value]||amt.value;calc();};newc.onchange=calc;calc();

/* deal of the day -> highlight a category */
(function(){
 var cards=document.querySelectorAll('.cat');if(!cards.length)return;
 var day=Math.floor((Date.now()/864e5))%cards.length;
 var pick=cards[day];pick.classList.add('today');
 var btn=document.getElementById('dealBtn');if(btn&&pick.href)btn.href=pick.href;
})();

/* PWA */
if('serviceWorker' in navigator){window.addEventListener('load',function(){
 navigator.serviceWorker.register(BASE+'/sw.js').catch(function(){});});}
</script>
</body>
</html>
'''

# ---------------------------------------------------------------- helpers
def jsonld(meta, t):
    folder = meta["folder"]
    url = SITE_URL + ("/" + folder + "/" if folder else "/")
    data = [
        {
            "@context": "https://schema.org", "@type": "WebSite",
            "name": "iHerb Code MPD0133", "url": url, "inLanguage": meta["hl"],
            "description": t["desc"],
        },
        {
            "@context": "https://schema.org", "@type": "Offer",
            "name": t["h1"], "description": t["desc"],
            "url": REF_URL, "priceCurrency": meta["cur"],
            "seller": {"@type": "Organization", "name": "iHerb"},
            "category": "Vitamins & Supplements discount",
            "eligibleCustomerType": "https://schema.org/NewCondition",
            "availability": "https://schema.org/InStock",
        },
        {
            "@context": "https://schema.org", "@type": "FAQPage",
            "inLanguage": meta["hl"],
            "mainEntity": [
                {"@type": "Question", "name": t[q],
                 "acceptedAnswer": {"@type": "Answer", "text": t[a]}}
                for q, a in (("q1", "a1"), ("q2", "a2"), ("q3", "a3"), ("q4", "a4"))
            ],
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "iHerb", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": t["h1"], "item": url},
            ],
        },
    ]
    return json.dumps(data, ensure_ascii=False)


def hreflang_block(current):
    lines = []
    for m in LANGS:
        href = SITE_URL + ("/" + m["folder"] + "/" if m["folder"] else "/")
        lines.append('<link rel="alternate" hreflang="%s" href="%s">' % (m["hl"], href))
    lines.append('<link rel="alternate" hreflang="x-default" href="%s/">' % SITE_URL)
    return "\n".join(lines)


def lang_options(current):
    out = []
    for m in LANGS:
        s = ' selected' if m["code"] == current else ''
        out.append('<option value="%s"%s>%s</option>' % (m["folder"], s, esc(m["native"])))
    return "".join(out)


def lang_links():
    out = []
    for m in LANGS:
        href = SITE_URL + ("/" + m["folder"] + "/" if m["folder"] else "/")
        out.append('<a href="%s">%s</a>' % (href, esc(m["native"])))
    return "".join(out)


def cat_grid(t):
    out = []
    for key, emoji, path in CATS:
        url = "https://www.iherb.com/c/%s?rcode=%s" % (path, CODE)
        out.append(
            '<a class="cat" href="%s" target="_blank" rel="noopener nofollow">'
            '<span class="tag">%s</span><div class="emoji">%s</div>'
            '<h3>%s</h3></a>' % (url, esc(t["cat_today"]), emoji, esc(t[key]))
        )
    return "".join(out)


def lang_data():
    return json.dumps([{"c": m["hl"], "f": m["folder"], "n": m["native"],
                        "m": m["match"]} for m in LANGS], ensure_ascii=False)


ROOT_REDIRECT = '''<script>
(function(){try{
 if(location.search.indexOf('noredirect')>-1)return;
 if(localStorage.getItem('iherb_lang')!==null)return;
 var L=%%LANGDATA%%;
 var navs=navigator.languages||[navigator.language||'en'];
 for(var i=0;i<navs.length;i++){
  var n=(navs[i]||'').toLowerCase();var p=n.split('-')[0];
  for(var j=0;j<L.length;j++){
   if(!L[j].f)continue;
   var mm=L[j].m;
   for(var k=0;k<mm.length;k++){
    if(n===mm[k]||p===mm[k]){location.replace('%%SITEURL%%/'+L[j].f+'/');return;}
   }
  }
 }
}catch(e){}})();
</script>'''


def render(meta):
    t = T[meta["code"]]
    folder = meta["folder"]
    canonical = SITE_URL + ("/" + folder + "/" if folder else "/")
    page = TEMPLATE

    # structural tokens
    repl = {
        "HTMLLANG": meta["hl"], "DIR": meta["dir"], "OGLOCALE": meta["og"],
        "CANONICAL": canonical, "SITEURL": SITE_URL, "REFURL": REF_URL,
        "CODE": CODE, "UPDATED": UPDATED, "PAGECUR": meta["cur"],
        "HREFLANG": hreflang_block(meta["code"]),
        "JSONLD": jsonld(meta, t),
        "LANGOPTIONS": lang_options(meta["code"]),
        "LANGLINKS": lang_links(),
        "CATGRID": cat_grid(t),
        "LANGDATA": lang_data(),
        "ROOTREDIRECT": (ROOT_REDIRECT if folder == "" else ""),
    }
    # text tokens (escaped)
    for k, v in t.items():
        repl[k.upper()] = esc(v)

    # apply (longest token names first to avoid partial collisions)
    for k in sorted(repl.keys(), key=len, reverse=True):
        page = page.replace("%%" + k + "%%", str(repl[k]))
    return page


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- build
def main():
    os.makedirs(OUT, exist_ok=True)

    built = []
    for meta in LANGS:
        if meta["code"] not in T:
            print("  ! skip (no translation):", meta["code"]); continue
        html_out = render(meta)
        path = ("index.html" if meta["folder"] == "" else meta["folder"] + "/index.html")
        write(path, html_out)
        built.append(meta)
        print("  + " + (meta["folder"] or "(root)"))

    # sitemap.xml
    urls = []
    for m in built:
        loc = SITE_URL + ("/" + m["folder"] + "/" if m["folder"] else "/")
        alts = "".join(
            '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
            % (x["hl"], SITE_URL + ("/" + x["folder"] + "/" if x["folder"] else "/"))
            for x in built
        )
        alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s/"/>' % SITE_URL
        urls.append(
            '  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>'
            '\n    <changefreq>weekly</changefreq>\n    <priority>%s</priority>%s\n  </url>'
            % (loc, UPDATED, "1.0" if m["folder"] == "" else "0.9", alts)
        )
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")

    # robots.txt
    write("robots.txt",
          "User-agent: *\nAllow: /\n\n"
          "# AI / answer engines welcome\n"
          "User-agent: GPTBot\nAllow: /\n"
          "User-agent: OAI-SearchBot\nAllow: /\n"
          "User-agent: ChatGPT-User\nAllow: /\n"
          "User-agent: PerplexityBot\nAllow: /\n"
          "User-agent: ClaudeBot\nAllow: /\n"
          "User-agent: Google-Extended\nAllow: /\n"
          "User-agent: Bingbot\nAllow: /\n\n"
          "Sitemap: %s/sitemap.xml\n" % SITE_URL)

    # llms.txt (GEO)
    write("llms.txt",
          "# iHerb Discount Code MPD0133\n\n"
          "> MPD0133 is a free, verified iHerb Rewards referral code. New iHerb "
          "customers can save up to 20%% on their first order and earn up to 10%% "
          "back in loyalty credit by entering MPD0133 in the promo code field at "
          "checkout. Returning customers receive 5%% off. The code works worldwide "
          "in every supported currency.\n\n"
          "## Key facts\n"
          "- Code: MPD0133\n"
          "- Type: iHerb Rewards / referral code\n"
          "- New-customer discount: up to 20%% off the first order\n"
          "- Loyalty credit: up to 10%% back for future orders\n"
          "- Returning-customer discount: 5%%\n"
          "- Cost to use: free\n"
          "- Coverage: iHerb ships to 180+ countries; code works globally\n"
          "- How to apply: paste MPD0133 into the promo/rewards code box at checkout\n"
          "- Apply link: %s\n\n"
          "## Pages\n"
          "Available in %d languages. See %s/sitemap.xml\n"
          % (REF_URL, len(built), SITE_URL))

    # manifest
    write("manifest.webmanifest", json.dumps({
        "name": "iHerb Code MPD0133 - Save up to 20%",
        "short_name": "iHerb MPD0133",
        "description": "Save on iHerb with verified rewards code MPD0133.",
        "start_url": SITE_URL + "/?utm_source=pwa",
        "scope": SITE_URL + "/",
        "display": "standalone",
        "background_color": "#f4f7f4",
        "theme_color": "#1f9d57",
        "icons": [
            {"src": SITE_URL + "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": SITE_URL + "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": SITE_URL + "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }, ensure_ascii=False, indent=2))

    # service worker
    write("sw.js",
          "var C='iherb-mpd0133-v1';\n"
          "self.addEventListener('install',function(e){self.skipWaiting();});\n"
          "self.addEventListener('activate',function(e){e.waitUntil(clients.claim());});\n"
          "self.addEventListener('fetch',function(e){\n"
          " if(e.request.method!=='GET')return;\n"
          " e.respondWith(\n"
          "  caches.open(C).then(function(c){\n"
          "   return c.match(e.request).then(function(hit){\n"
          "    var net=fetch(e.request).then(function(r){\n"
          "     if(r&&r.status===200&&e.request.url.indexOf('iherb.com')<0)c.put(e.request,r.clone());\n"
          "     return r;}).catch(function(){return hit;});\n"
          "    return hit||net;});}));\n"
          "});\n")

    # 404 -> bounce to root
    write("404.html",
          '<!doctype html><html lang="en"><meta charset="utf-8">'
          '<title>iHerb Code MPD0133</title>'
          '<meta name="robots" content="noindex">'
          '<meta http-equiv="refresh" content="0;url=%s/">'
          '<body>Redirecting to <a href="%s/">iHerb code MPD0133</a>.</body></html>' % (SITE_URL, SITE_URL))

    # icon.svg
    write("icon.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
          '<rect width="512" height="512" rx="110" fill="#1f9d57"/>'
          '<text x="50%" y="54%" font-family="Arial,Helvetica,sans-serif" font-size="210" '
          'font-weight="900" fill="#fff" text-anchor="middle" dominant-baseline="middle">iH</text>'
          '<text x="50%" y="83%" font-family="Arial,Helvetica,sans-serif" font-size="78" '
          'font-weight="800" fill="#bff0d4" text-anchor="middle">SAVE</text></svg>')

    # CNAME-free .nojekyll so underscores/folders serve fine on GitHub Pages
    write(".nojekyll", "")

    print("\nDone. %d language pages + assets -> %s" % (len(built), OUT))
    print("Site URL configured as: %s" % SITE_URL)


if __name__ == "__main__":
    main()
