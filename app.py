from flask import Flask, request, redirect, jsonify, send_from_directory
import json, os
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "db.json"
ADMIN_PHONE = "01021049645"
ADMIN_NAME = "وائل القضابي"
GOVS = ["القاهرة","الجيزة","القليوبية","الاسكندرية","الشرقية","الدقهلية","الغربية","المنوفية","البحيرة","كفر الشيخ","دمياط","بورسعيد","الاسماعيلية","السويس","الفيوم","بني سويف","المنيا","اسيوط","سوهاج","قنا","الاقصر","اسوان","مطروح","شمال سيناء","جنوب سيناء","البحر الاحمر","الوادي الجديد"]

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_featured_active(item):
    if not item.get('featured'): return False
    until_str = item.get('featured_until')
    if not until_str: return False
    try:
        until = datetime.fromisoformat(until_str)
        return datetime.now() < until
    except: return False

def page(content):
    return f"""<html dir=rtl lang=ar><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
    <link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#0d5a3c"><link rel="icon" href="/icon.png">
    <title>لقيتها - امانة اولاد الحلال</title>
    <style>@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap');
    body{{font-family:'Tajawal',sans-serif;background:#f4f6f3;margin:0}}
.box{{background:white;margin:12px;padding:20px;border-radius:22px;box-shadow:0 4px 15px #0001;line-height:1.7;position:relative}}
.dibaja{{background:linear-gradient(135deg,#0d3d2a,#146b48);color:white;text-align:center}}
.alert{{background:#fff8e1;border:1px solid #ffb74d;padding:14px;border-radius:14px;font-size:14px;line-height:1.8}}
.btn{{display:block;padding:16px;text-align:center;border-radius:14px;color:white;text-decoration:none;font-size:17px;font-weight:bold;margin:10px 0}}
input,textarea,select{{width:100%;padding:14px;margin:8px 0;border-radius:12px;border:1px solid #ddd;box-sizing:border-box;font-size:16px}}
   .featured{{border:2px solid #ffb300;background:linear-gradient(135deg,#fff8e1,#ffecb3)}}
   .badge{{background:#ffb300;color:#000;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:800;position:absolute;top:10px;left:15px}}
    </style></head><body><div style=max-width:550px;margin:auto;padding-bottom:100px>{content}</div>
    <script>if('serviceWorker' in navigator){{navigator.serviceWorker.register('/sw.js')}}</script></body></html>"""

@app.route("/manifest.json")
def manifest(): return jsonify({"name":f"لقيتها - {ADMIN_NAME}","short_name":"لقيتها","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#0d5a3c","icons":[{"src":"/icon.png","sizes":"512x512","type":"image/png"}]})
@app.route("/sw.js")
def sw(): return "self.addEventListener('install', e=>self.skipWaiting());",200,{'Content-Type':'application/javascript'}
@app.route("/icon.png")
def icon_file(): return send_from_directory('.', 'icon.png')

@app.route("/")
def home():
    items=load_db()
    active=[x for x in items if x.get('status')!='تم']
    return page(f"""<div class="box dibaja"><h2 style=margin:0>بسم الله الرحمن الرحيم</h2><h1>📍 لقيتها</h1>
    <p style=font-size:15px;opacity:.9>منصة الأمانة لإرجاع المفقودات</p>
    <div style=background:#ffffff15;padding:15px;border-radius:15px;margin:18px 0;text-align:right>
    <p style=margin:0;font-size:14px;line-height:2>التطبيق ده معمول لوجه الله ولأولاد الحلال فقط<br>اللي بيلاقي حاجة ومش عارف يوصله، واللي ضايع منه حاجة وقلبه محروق عليها.</p>
    <hr style=border-color:#ffffff30;margin:15px 0>
    <p style=margin:0;font-size:14px;line-height:1.9>قال تعالى:<br><b style=font-size:16px;color:#ffecb3>"إِنَّ اللَّهَ يَأْمُرُكُمْ أَن تُؤَدُّوا الْأَمَانَاتِ إِلَىٰ أَهْلِهَا"</b><br><br>وقال ﷺ: <b style=color:#ffecb3>"والله في عون العبد ما كان العبد في عون أخيه"</b></p></div>
    <p style=font-size:12px>بإشراف وضمان: {ADMIN_NAME} - {ADMIN_PHONE}</p></div>
    <div class="box alert"><b>⚖️ نظام الأمانة:</b><br>1- اللي بيلاقي يقول "لقيت كذا في محافظة كذا" فقط.<br>2- الحاجة بتفضل معه هو، مش مع الإدارة.<br>3- التسليم النهائي برعاية مكتب محاماة.</div>
    <a href=/found class=btn style=background:linear-gradient(135deg,#0d5a3c,#2e7d32)>😊 انا لقيت حاجة وعايز ارجعها</a>
    <a href=/lost class=btn style=background:linear-gradient(135deg,#b71c1c,#e53935)>😢 حاجة ضايعة مني</a>
    <a href=/all class=btn style=background:#263238>🔍 تصفح بلاغات مصر ({len(active)})</a>
    <a href=/terms class=btn style=background:#fff;color:#0d5a3c;border:1px solid #0d5a3c>⚖️ الشروط القانونية</a>
    <a href=/pay class=btn style="background:linear-gradient(135deg,#ff8f00,#ff3d00);color:#000">⭐ ثبت مفقوداتك ب 20 ج 💰</a>
    <div style=height:80px></div>
<button id="installBtn" style="position:fixed;bottom:15px;left:50%;transform:translateX(-50%);width:90%;max-width:520px;background:#0d5a3c;color:#fff;padding:18px;border-radius:18px;border:2px solid #fff;font-weight:800;font-size:19px;z-index:999999;box-shadow:0 8px 25px #0005;display:none">📲 ثبت التطبيق</button>
<script>let p=null;const b=document.getElementById('installBtn');window.addEventListener('beforeinstallprompt',(e)=>{{e.preventDefault();p=e;b.style.display='block';}});b.addEventListener('click',async()=>{{if(p){{p.prompt();await p.userChoice;p=null;b.style.display='none';}}else{{alert('من 3 نقط فوق اختار إضافة إلى الشاشة الرئيسية');}}}});</script></div>""")

@app.route("/terms")
def terms(): return page(f"""<div class=box><h2 style=text-align:center>⚖️ الشروط القانونية</h2><div style=line-height:2.2;font-size:14px><b>1-</b> منصة وسيط تعارف فقط بإشراف {ADMIN_NAME}.<br><br><b>2-</b> الإدارة لا تستلم أي مفقودات.<br><br><b>3-</b> التسليم برعاية مكتب محاماة مع إقرار استلام.<br><br><b>4-</b> الإدارة غير مسؤولة عن صحة بيانات المعلنين.</div><a href=/ class=btn style=background:#0d5a3c>موافق والعودة ✅</a></div>""")

@app.route("/<t>", methods=["GET","POST"])
def add(t):
    if t not in ['found','lost']: return redirect("/")
    is_lost=t=='lost'
    gov_options="".join([f"<option>{g}</option>" for g in GOVS])
    if request.method=="POST":
        data=load_db()
        data.append({"id":len(data),"type":request.form['type'],"gov":request.form['gov'],"phone":request.form['phone'],"proof":request.form.get('proof',''),"kind":"🔴 ضايع" if is_lost else "🟢 لقيت","date":datetime.now().strftime("%d/%m"),"status":"مفتوح","featured":False})
        save_db(data)
        return redirect("/all")
    if is_lost: return page(f"""<div class=box><h2>بلغ عن اللي ضايع منك</h2><div class=alert>اذكر المواصفات الدقيقة - سري للوسيط فقط.</div><form method=post><input name=type placeholder='ايه اللي ضايع؟' required><select name=gov required>{gov_options}</select><input name=phone placeholder='رقمك (مخفي)' required><textarea name=proof placeholder='المواصفات الدقيقة' required></textarea><button class=btn style=background:#c62828;width:100%;border:none>انشر 🤲</button></form></div>""")
    else: return page(f"""<div class=box><h2>ربنا يجازيك خير</h2><div class=alert>قول لقيت ايه والمحافظة فقط.</div><form method=post><input name=type placeholder='لقيت ايه؟' required><select name=gov required>{gov_options}</select><input name=phone placeholder='رقمك (مخفي)' required><button class=btn style=background:#0d5a3c;width:100%;border:none>ابلغ لوجه الله ✅</button></form></div>""")

@app.route("/all")
def all_items():
    items=load_db()
    q=request.args.get('q','')
    key=request.args.get('key','')
    is_admin = key == ADMIN_PHONE
    filtered=[x for x in items if x.get('status')!='تم']
    if q: filtered=[x for x in filtered if q in x['type'] or q in x['gov']]
    # ترتيب: المميز النشط فوق
    featured=[x for x in filtered if is_featured_active(x)]
    normal=[x for x in filtered if not is_featured_active(x)]
    sorted_list = featured + list(reversed(normal))

    html=f"""<div class=box><a href=/>⬅️ الرئيسية</a> {'<b style=color:green> - وضع الأدمن ✅</b>' if is_admin else ''}<form method=get style=display:flex;gap:5px;margin-top:10px><input name=q value='{q}' placeholder='ابحث...'><button class=btn style=background:#0d5a3c;padding:10px;margin:0>بحث</button></form></div>"""
    if is_admin: html+=f"<div class=box alert>انت في وضع الأدمن. زرار التثبيت ظاهر تحت كل إعلان.</div>"
    for it in sorted_list:
        is_f = is_featured_active(it)
        until_txt = ""
        if is_f:
            try:
                until = datetime.fromisoformat(it['featured_until'])
                remain = until - datetime.now()
                until_txt = f" (متبقي {remain.days} يوم)"
            except: pass
        html+=f"""<div class="box {'featured' if is_f else ''}">{'<span class=badge>⭐ مميز'+until_txt+'</span>' if is_f else ''}<small>{it['date']} - {it['kind']} - 📍 {it['gov']} - ID:{it['id']}</small><h2 style=margin:8px 0>{it['type']}</h2>
        <a class=btn style=background:#25D366 href='https://wa.me/20{ADMIN_PHONE[1:]}?text=بخصوص {it['type']} في {it['gov']}' target=_blank>تواصل مع الوسيط {ADMIN_NAME} 💬</a>"""
        if is_admin:
            if is_f:
                html+=f"<a href=/unpin/{it['id']}?key={ADMIN_PHONE} class=btn style=background:#ff6f00;padding:8px;font-size:13px>إلغاء التثبيت</a>"
            else:
                html+=f"<a href=/pin/{it['id']}?key={ADMIN_PHONE} class=btn style=background:linear-gradient(135deg,#ffb300,#ff8f00);color:#000;padding:8px;font-size:13px>📌 ثبت هذا 3 أيام (20ج)</a>"
            html+=f"<a href=/done/{it['id']}?key={ADMIN_PHONE} class=btn style=background:#eee;color:#333;padding:6px;font-size:11px>تم التسليم</a>"
        html+="</div>"
    return page(html)

@app.route("/pin/<int:id>")
def pin(id):
    key=request.args.get('key','')
    if key!=ADMIN_PHONE: return "غير مصرح",403
    data=load_db()
    if 0<=id<len(data):
        data[id]['featured']=True
        data[id]['featured_until']=(datetime.now()+timedelta(days=3)).isoformat()
        save_db(data)
    return redirect(f"/all?key={ADMIN_PHONE}")

@app.route("/unpin/<int:id>")
def unpin(id):
    key=request.args.get('key','')
    if key!=ADMIN_PHONE: return "غير مصرح",403
    data=load_db()
    if 0<=id<len(data):
        data[id]['featured']=False
        data[id].pop('featured_until',None)
        save_db(data)
    return redirect(f"/all?key={ADMIN_PHONE}")

@app.route("/done/<int:id>")
def done(id):
    key=request.args.get('key','')
    if key!=ADMIN_PHONE and request.args.get('key') is None: pass
    data=load_db()
    if 0<=id<len(data):
        data[id]['status']='تم'
        save_db(data)
    return redirect("/all?key="+key if key==ADMIN_PHONE else "/all")

@app.route("/pay")
def pay_page():
    return page(f"""<div class=box style=text-align:center><h2>⭐ تثبيت إعلانك أول الصفحة 3 أيام</h2><div class=alert style=text-align:right>حول <b>20 جنيه</b> على فودافون كاش وهيثبت فوق الكل ⭐</div><div style=background:#f1f8e9;padding:20px;border-radius:15px;margin:15px 0><p>رقم فودافون كاش</p><h1 style=color:#0d5a3c>{ADMIN_PHONE}</h1><p>باسم: {ADMIN_NAME}</p></div><a class=btn style=background:#25D366 href='https://wa.me/20{ADMIN_PHONE[1:]}?text=حولت ال20 جنيه' target=_blank>📸 ابعت سكرين التحويل واتساب</a><a href=/ class=btn style=background:#eee;color:#333>رجوع</a></div>""")

@app.route('/.well-known/assetlinks.json')
def assetlinks(): return jsonify([{"relation":["delegate_permission/common.handle_all_urls"],"target":{"namespace":"android_app","package_name":"com.laqetaha.app","sha256_cert_fingerprints":["F3:8D:1D:3A:55:88:82:DF:70:60:03:10:5D:B2:B8:C3:C9:CC:20:01:66:82:50:21:6B:6F:4E:85:8A:26:C3:00"]}}])

if __name__=="__main__": app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
