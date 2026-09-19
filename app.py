from flask import Flask, request, redirect, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
DB_FILE = "db.json"
ADMIN_PHONE = "01021049645"
ADMIN_NAME = "وائل القضابي"
GOVS = ["القاهرة","الجيزة","القليوبية","الاسكندرية","الشرقية","الدقهلية","الغربية","المنوفية","البحيرة","كفر الشيخ","دمياط","بورسعيد","الاسماعيلية","السويس","الفيوم","بني سويف","المنيا","اسيوط","سوهاج","قنا","الاقصر","اسوان","مطروح","شمال سيناء","جنوب سيناء","البحر الاحمر","الوادي الجديد"]

if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        items = json.load(f)
else:
    items = []

def save():
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)

def page(content):
    return f"""
    <html dir=rtl lang=ar><head><meta charset=utf-8>
    <meta name=viewport content="width=device-width,initial-scale=1">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#0d5a3c">
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/484/484167.png">
    <title>لقيتها - امانة اولاد الحلال</title>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap');
    body{{font-family:'Tajawal',sans-serif;background:#f4f6f3;margin:0}}
.box{{background:white;margin:12px;padding:20px;border-radius:22px;box-shadow:0 4px 15px #0001;line-height:1.7}}
.dibaja{{background:linear-gradient(135deg,#0d3d2a,#146b48);color:white;text-align:center;position:relative;overflow:hidden}}
.dibaja::before{{content:'☪️';position:absolute;font-size:120px;opacity:.07;top:-20px;left:-20px}}
.alert{{background:#fff8e1;border:1px solid #ffb74d;padding:14px;border-radius:14px;font-size:14px;line-height:1.8}}
.btn{{display:block;padding:16px;text-align:center;border-radius:14px;color:white;text-decoration:none;font-size:17px;font-weight:bold;margin:10px 0}}
    input,textarea,select{{width:100%;padding:14px;margin:8px 0;border-radius:12px;border:1px solid #ddd;box-sizing:border-box;font-size:16px}}
    </style></head><body><div style=max-width:550px;margin:auto;padding-bottom:30px>{content}</div></body></html>"""

@app.route("/manifest.json")
def manifest():
    return jsonify({"name":f"لقيتها - {ADMIN_NAME}","short_name":"لقيتها","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#0d5a3c","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/484/484167.png","sizes":"512x512","type":"image/png"}]})

@app.route("/")
def home():
    return page(f"""
    <div class="box dibaja">
    <h2 style=margin:0>بسم الله الرحمن الرحيم</h2>
    <h1 style=margin:10px 0 5px 0>📍 لقيتها</h1>
    <p style=font-size:15px;opacity:.9;margin:0>منصة الأمانة لإرجاع المفقودات في كل محافظات مصر</p>

    <div style=background:#ffffff15;padding:15px;border-radius:15px;margin:18px 0;text-align:right>
    <p style=margin:0;font-size:14px;line-height:2>
    التطبيق ده معمول لوجه الله ولأولاد الحلال فقط<br>
    اللي بيلاقي حاجة في الشارع ونفسه يرجعها لصاحبها ومش عارف يوصله،<br>
    واللي ضايع منه حاجة وقلبه محروق عليها.
    </p>
    <hr style=border-color:#ffffff30;margin:15px 0>
    <p style=margin:0;font-size:14px;line-height:1.9>
    قال تعالى:<br>
    <b style=font-size:16px;color:#ffecb3>"إِنَّ اللَّهَ يَأْمُرُكُمْ أَن تُؤَدُّوا الْأَمَانَاتِ إِلَىٰ أَهْلِهَا"</b><br>
    <small>[النساء: 58]</small><br><br>
    وقال رسول الله ﷺ:<br>
    <b style=color:#ffecb3>"من آوى ضالة فهو ضال ما لم يُعرِّفها"</b><br>
    <small>رواه مسلم - يعني اللي يلاقي حاجة لازم يعرّف عنها</small><br><br>
    وقال ﷺ: <b style=color:#ffecb3>"والله في عون العبد ما كان العبد في عون أخيه"</b>
    </p>
    </div>
    <p style=font-size:12px;opacity:.8;margin:0>بإشراف وضمان: {ADMIN_NAME} - {ADMIN_PHONE}<br>اللهم اجعل هذا العمل خالصا لوجهك 🤲</p>
    </div>

    <div class="box alert">
    <b>⚖️ نظام الأمانة عندنا:</b><br>
    1- اللي بيلاقي يقول "لقيت كذا في محافظة كذا" فقط، بدون أي تفاصيل دقيقة.<br>
    2- الحاجة بتفضل معه هو في بيته، <b>مش بتتسلم للإدارة.</b><br>
    3- صاحب الحاجة هو اللي يتواصل مع الوسيط ويثبت بمواصفات دقيقة ومكان الوقوع.<br>
    4- التسليم النهائي يتم بشكل قانوني برعاية مكتب محاماة لضمان حق الطرفين.
    </div>

    <a href=/found class=btn style=background:linear-gradient(135deg,#0d5a3c,#2e7d32)>😊 انا لقيت حاجة وعايز ارجعها</a>
    <a href=/lost class=btn style=background:linear-gradient(135deg,#b71c1c,#e53935)>😢 حاجة ضايعة مني وبدور عليها</a>
    <a href=/all class=btn style=background:#263238>🔍 تصفح بلاغات مصر كلها ({len([x for x in items if x.get('status')!='تم'])})</a>
    <a href=/terms class=btn style=background:#fff;color:#0d5a3c;border:1px solid #0d5a3c>⚖️ الشروط القانونية للتسليم</a>
    """)

@app.route("/terms")
def terms():
    return page(f"""
    <div class=box>
    <h2 style=text-align:center>⚖️ الشروط القانونية واخلاء المسؤولية</h2>
    <div style=line-height:2.2;font-size:14px>
    <b>1- طبيعة التطبيق:</b> تطبيق "لقيتها" هو منصة وسيط تعارف فقط بين فاقد الشيء وواجده على مستوى الجمهورية، بإشراف وضمان الأستاذ {ADMIN_NAME}.<br><br>
    <b>2- عدم الاستلام:</b> إدارة التطبيق <b>لا تستلم أي مفقودات بيدها نهائيا</b> ولا تحتفظ بها، المفقودات تظل في حيازة الشخص الذي وجدها في بيته حتى ظهور صاحبها.<br><br>
    <b>3- نظام التحقق:</b> الذي يدعي ملكية الشيء هو المطالب بإثبات المواصفات الدقيقة والمكان الدقيق للفقد، والذي وجد الشيء غير مطالب بذكر أي مواصفات دقيقة على العام.<br><br>
    <b>4- التسليم القانوني:</b> حفاظا على حقوق الطرفين ومنع النزاع مستقبلا، <b>يتم التسليم النهائي بين الطرفين بشكل قانوني برعاية مكتب محاماة معتمد</b> يتم تحديده بمعرفة الإدارة، مع توقيع إقرار استلام وتسليم رسمي يضمن حق الطرفين.<br><br>
    <b>5- اخلاء المسؤولية:</b> إدارة التطبيق غير مسؤولة عن صحة بيانات المعلنين أو عن أي خلاف ينشأ بين الطرفين بعد التسليم.<br><br>
    <b>6- التقدير:</b> أي تقدير أو إكرامية من صاحب الشيء للشخص الأمين الذي وجده هي <b>أمر تطوعي واختياري تماما</b> بينهما ولا تتدخل فيه الإدارة، والأصل أن رد الأمانة لوجه الله.<br><br>
    </div>
    <a href=/ class=btn style=background:#0d5a3c>موافق والعودة للرئيسية ✅</a>
    <p style=text-align:center;font-size:12px>للتواصل القانوني: {ADMIN_NAME} - {ADMIN_PHONE}</p>
    </div>
    """)

@app.route("/<t>", methods=["GET","POST"])
def add(t):
    is_lost = t == 'lost'
    gov_options = "".join([f"<option>{g}</option>" for g in GOVS])
    if request.method == "POST":
        items.append({"id": len(items), "type": request.form['type'], "gov": request.form['gov'], "phone": request.form['phone'], "proof": request.form.get('proof',''), "kind": "🔴 ضايع" if is_lost else "🟢 لقيت", "date": datetime.now().strftime("%d/%m"), "status": "مفتوح"})
        save()
        return redirect("/all")
    if is_lost:
        return page(f"""<div class=box><h2>بلغ عن اللي ضايع منك</h2><div class=alert>اذكر هنا المكان الدقيق اللي وقعت فيه والعلامات السرية - ده سري للوسيط فقط.</div><form method=post><input name=type placeholder='ايه اللي ضايع؟ مثال: بطاقة' required><label>المحافظة:</label><select name=gov required>{gov_options}</select><input name=phone placeholder='رقمك (مخفي للادارة فقط)' required><textarea name=proof placeholder='المواصفات الدقيقة اللي تثبت ملكيتك (المكان بالظبط + ايه اللي جواها)' required></textarea><button class=btn style=background:#c62828;width:100%;border:none>انشر 🤲</button></form></div>""")
    else:
        return page(f"""<div class=box><h2>ربنا يجازيك خير</h2><div class=alert>قول لقيت ايه والمحافظة فقط. متذكرش تفاصيل دقيقة.</div><form method=post><input name=type placeholder='لقيت ايه بشكل عام؟ مثال: محفظة' required><label>المحافظة:</label><select name=gov required>{gov_options}</select><input name=phone placeholder='رقمك (مخفي للادارة فقط)' required><button class=btn style=background:#0d5a3c;width:100%;border:none>ابلغ لوجه الله ✅</button></form></div>""")

@app.route("/all")
def all_items():
    q = request.args.get('q','')
    filtered = [x for x in items if x.get('status')!='تم']
    if q:
        filtered = [x for x in filtered if q in x['type'] or q in x['gov']]
    html = f"""<div class=box><a href=/>⬅️ الرئيسية</a> - <a href=/terms>⚖️ الشروط</a><form method=get style=display:flex;gap:5px;margin-top:10px><input name=q value='{q}' placeholder='ابحث: بطاقة، محافظة...'><button class=btn style=background:#0d5a3c;padding:10px;margin:0>بحث</button></form></div>"""
    for it in reversed(filtered):
        html += f"""<div class=box><small>{it['date']} - {it['kind']} - 📍 {it['gov']}</small><h2 style=margin:8px 0>{it['type']}</h2><p style=font-size:13px;color:#555>التسليم قانوني بمكتب محاماة برعاية {ADMIN_NAME}</p><a class=btn style=background:#25D366 href='https://wa.me/2{ADMIN_PHONE}?text=السلام عليكم استاذ {ADMIN_NAME} - بخصوص {it['type']} في {it['gov']} - انا صاحبها' target=_blank>تواصل مع الوسيط {ADMIN_NAME} 💬</a><a href=/done/{it['id']} class=btn style=background:#eee;color:#333;padding:6px;font-size:11px>تم التسليم (ادمن)</a></div>"""
    return page(html)

@app.route("/done/<int:id>")
def done(id):
    items[id]['status'] = 'تم'
    save()
    return redirect("/all")

app.run(host='0.0.0.0', port=5000, debug=True)