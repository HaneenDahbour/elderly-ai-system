from flask import Flask, render_template, request
import joblib
import numpy as np
import csv
import os
from collections import Counter


app = Flask(__name__)

# ========== تكوين النظام - Ozwa Configuration ==========
app.config['APP_NAME_AR'] ='عزوتي'
app.config['APP_NAME_EN'] = 'Ozwati'
app.config['APP_TAGLINE_AR'] = 'نظام قطري ذكي لرعاية كبار السن'
app.config['APP_TAGLINE_EN'] = 'Qatar Smart Elderly Care System'

# Load the trained AI model and encoder
model = joblib.load("model.pkl")
le = joblib.load("encoder.pkl")


@app.route("/")
def home():
    """الصفحة الرئيسية"""
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """معالجة البيانات وإعطاء التوصية"""
    age = int(request.form["age"])
    health = int(request.form["health"])
    mobility = int(request.form["mobility"])
    mood = int(request.form["mood"])
    lonely = int(request.form["lonely"])
    interest = int(request.form["interest"])



    data = np.array([[age, health, mobility, mood, lonely, interest]])

    prediction = model.predict(data)
    activity = le.inverse_transform(prediction)[0]
    
    # روابط YouTube للفيديوهات (جاهزة للنشر على Render!)
    suggestions_with_links = []
    activity_video_url = None  # رابط YouTube للفيديو الرئيسي
    
    if activity == "نادي حوار":
        # ضعي رابط الفيديو الخاص بك هنا
        activity_video_url = "https://www.youtube.com/embed/4q1dgn_C0AU"
        
        suggestions_with_links = [
            {
                "name": "استمع لقصة ملهمة", 
                "link": "https://www.youtube.com/watch?v=4q1dgn_C0AU",
                "icon": "📖",
                "video_url": "https://www.youtube.com/embed/4q1dgn_C0AU",
                "type": "story"
            },
            {
                "name": "قصص من التراث القطري", 
                "link": "https://www.youtube.com/watch?v=YjJp0S6AEDY",
                "icon": "🏛️",
                "video_url": "https://www.youtube.com/embed/YjJp0S6AEDY",
                "type": "story"
            },
            {
                "name": "جلسة دردشة جماعية", 
                "link": "https://meet.jit.si",
                "icon": "💬",
                "video_url": None,
                "type": "activity"
            },
            {
                "name": "قصة قصيرة مسموعة", 
                "link": "https://www.youtube.com/watch?v=m7dhMcPE4Vo&pp=ygUc2YLYtdi1INmC2LXZitix2Kkg2YXYudio2LHYqQ%3D%3D",
                "icon": "🎧",
                "video_url": "https://www.youtube.com/watch?v=m7dhMcPE4Vo&pp=ygUc2YLYtdi1INmC2LXZitix2Kkg2YXYudio2LHYqQ%3D%3D",
                "type": "story"
            },
            {
                "name": "لقاء عائلي افتراضي", 
                "link": "https://zoom.us",
                "icon": "👨‍👩‍👧‍👦",
                "video_url": None,
                "type": "activity"
            }
        ]

    elif activity == "جلسة ألغاز":
        activity_video_url = "https://www.youtube.com/embed/5n_4eVG1wqY"
        
        suggestions_with_links = [
            {
                "name": "قصة ممتعة ومشوقة", 
                "link": "https://www.youtube.com/embed/J-lXDwuq_14",
                "icon": "🕵️",
                "video_url": "https://www.youtube.com/embed/J-lXDwuq_14",
                "type": "story"
            },
            {
                "name": "كلمات متقاطعة", 
                "link": "https://www.wordgames.com/crossword.html",
                "icon": "🔤",
                "video_url": None,
                "type": "game"
            },
            {
                "name": "سودوكو", 
                "link": "https://www.sudoku.com",
                "icon": "🔢",
                "video_url": None,
                "type": "game"
            },
            {
                "name": "قصة للتفكير", 
                "link": "https://www.youtube.com/watch?v=oP3c1h8v2ZQ",
                "icon": "🧩",
                "video_url": "https://www.youtube.com/embed/oP3c1h8v2ZQ",
                "type": "story"
            },
            {
                "name": "ألعاب ذاكرة", 
                "link": "https://www.memozor.com/memory-games",
                "icon": "🧠",
                "video_url": None,
                "type": "game"
            }
        ]

    elif activity == "تمارين خفيفة":
        activity_video_url = "https://www.youtube.com/embed/8BcPHWGQO44"
        
        suggestions_with_links = [
            {
                "name": "تمارين كرسي", 
                "link": "https://www.youtube.com/watch?v=8BcPHWGQO44",
                "icon": "🪑",
                "video_url": "https://www.youtube.com/embed/8BcPHWGQO44",
                "type": "video"
            },
            {
                "name": "مشي منزلي", 
                "link": "https://www.youtube.com/watch?v=enYITYwvPAQ",
                "icon": "🚶",
                "video_url": "https://www.youtube.com/embed/enYITYwvPAQ",
                "type": "video"
            },
            {
                "name": "يوغا للمبتدئين", 
                "link": "https://www.youtube.com/watch?v=v7AYKMP6rOE",
                "icon": "🧘",
                "video_url": "https://www.youtube.com/watch?v=O8YxV3UupjM&pp=ygU52YrZiNi62Kcg2YTZhNmF2KjYqtiv2KbZitmGINin2YTZhdix2YjZhtipINiv2YLZitmC2KrZitmG",
                "type": "video"
            },
            {
                "name": "تمارين توازن", 
                "link": "https://www.youtube.com/watch?v=FNY3bKfE8gA",
                "icon": "⚖️",
                "video_url": "https://www.youtube.com/embed/FNY3bKfE8gA",
                "type": "video"
            },
            {
                "name": "تمارين تمدد", 
                "link": "https://www.youtube.com/watch?v=g_tea8ZNk5A",
                "icon": "🤸",
                "video_url": "https://www.youtube.com/embed/g_tea8ZNk5A",
                "type": "video"
            }
        ]

    elif activity == "نشاط فني":
        activity_video_url = "https://www.youtube.com/embed/kpk2tdsPh0A"
        
        suggestions_with_links = [
            {
                "name": "قصة فنان ملهم", 
                "link": "https://www.youtube.com/watch?v=kpk2tdsPh0A",
                "icon": "🎨",
                "video_url": "https://www.youtube.com/embed/kpk2tdsPh0A",
                "type": "story"
            },
            {
                "name": "رسم أونلاين", 
                "link": "https://sketch.io/sketchpad/",
                "icon": "🖌️",
                "video_url": None,
                "type": "activity"
            },
            {
                "name": "تعلم الخط العربي", 
                "link": "https://www.youtube.com/watch?v=zOwTqYS5nOY",
                "icon": "✍️",
                "video_url": "https://www.youtube.com/embed/zOwTqYS5nOY",
                "type": "video"
            },
            {
                "name": "موسيقى هادئة", 
                "link": "https://www.youtube.com/watch?v=lFcSrYw-ARY",
                "icon": "🎵",
                "video_url": "https://www.youtube.com/embed/lFcSrYw-ARY",
                "type": "audio"
            },
            {
                "name": "تلوين للكبار", 
                "link": "https://www.thecolor.com",
                "icon": "🖍️",
                "video_url": None,
                "type": "activity"
            }
        ]

    # توليد التفسير
    explanation = generate_explanation(lonely, mood, interest, mobility)

    # حفظ السجل في قاعدة البيانات
    save_to_history(age, health, mobility, mood, lonely, interest, activity)

    return render_template(
        "result.html",
        activity=activity,
        activity_video_url=activity_video_url,
        explanation=explanation,
        suggestions=suggestions_with_links
    )


def generate_explanation(lonely, mood, interest, mobility):
    """توليد تفسير التوصية"""
    explanation = ""

    if lonely >= 2:
        explanation += "لأن مستوى الشعور بالوحدة مرتفع، من المهم زيادة التفاعل الاجتماعي. "

    if mood == 1:
        explanation += "النشاط يساعد على تحسين الحالة المزاجية. "

    if interest == 0:
        explanation += "تم اختيار نشاط اجتماعي لأنه يتوافق مع اهتماماتك. "
    elif interest == 1:
        explanation += "تم اختيار نشاط ذهني لأنه يتوافق مع اهتماماتك. "
    elif interest == 2:
        explanation += "تم اختيار نشاط بدني لأنه يتوافق مع اهتماماتك. "

    if mobility <= 2:
        explanation += "النشاط لا يتطلب مجهودًا بدنيًا كبيرًا. "

    if explanation == "":
        explanation = "تم اختيار النشاط بناءً على توافقه مع حالتك العامة."

    return explanation


def save_to_history(age, health, mobility, mood, lonely, interest, activity):
    """حفظ البيانات في ملف CSV"""
    file_exists = os.path.isfile("history.csv")

    with open("history.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["age", "health", "mobility", "mood", "lonely", "interest", "activity"])
        writer.writerow([age, health, mobility, mood, lonely, interest, activity])


@app.route('/stats')
@app.route('/stats/')
def stats():
    """صفحة الإحصائيات"""
    total = 0
    most_common = "لا توجد بيانات بعد"
    
    if os.path.isfile("history.csv"):
        try:
            activities_list = []
            
            with open("history.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    activities_list.append(row["activity"])
            
            total = len(activities_list)
            
            if total > 0:
                counter = Counter(activities_list)
                most_common = counter.most_common(1)[0][0]
        
        except Exception as e:
            print(f"خطأ في قراءة البيانات: {e}")
            total = 0
            most_common = "حدث خطأ في قراءة البيانات"
    
    return render_template('stats.html', total=total, most_common=most_common)


@app.errorhandler(404)
def page_not_found(e):
    """صفحة خطأ 404"""
    return """
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;800&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Tajawal', Arial, sans-serif; 
                text-align: center; 
                padding: 50px;
                background: linear-gradient(135deg, #FFF8F0 0%, #FFE8D6 100%);
            }
            .error-container {
                background: white;
                padding: 3rem;
                border-radius: 24px;
                box-shadow: 0 8px 32px rgba(142, 21, 56, 0.15);
                max-width: 600px;
                margin: 0 auto;
                border-top: 6px solid #8E1538;
            }
            .qatar-flag { font-size: 4rem; margin-bottom: 1rem; }
            .logo { font-size: 2.5rem; color: #8E1538; font-weight: 800; letter-spacing: 2px; }
            h1 { color: #E07A5F; font-size: 5rem; margin: 1rem 0; }
            a { 
                display: inline-block; padding: 1.2rem 2.5rem;
                background: linear-gradient(135deg, #8E1538 0%, #6B0F2A 100%);
                color: white; text-decoration: none; border-radius: 16px;
                font-weight: bold; transition: all 0.3s ease;
            }
            a:hover { transform: translateY(-3px); }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="qatar-flag">🇶🇦</div>
            <div class="logo">عزوتي - Ozwati</div>
            <h1>404</h1>
            <p>عذراً، الصفحة غير موجودة.</p>
            <a href="/">← العودة للرئيسية</a>
        </div>
    </body>
    </html>
    """, 404


@app.context_processor
def inject_app_info():
    """إضافة متغيرات عامة للقوالب"""
    return {
        'app_name_ar': app.config['APP_NAME_AR'],
        'app_name_en': app.config['APP_NAME_EN'],
        'app_tagline_ar': app.config['APP_TAGLINE_AR'],
        'app_tagline_en': app.config['APP_TAGLINE_EN']
    }


if __name__ == "__main__":
    print("=" * 80)
    print("🇶🇦  عزوة - Ozwa System  🇶🇦")
    print("=" * 80)
    print("🚀 Qatar Smart Elderly Care System")
    print("📍 Home: http://0.0.0.0:10000/")
    print("📊 Stats: http://0.0.0.0:10000/stats")
    print("=" * 80)
    print("🎬 Using YouTube Videos - Ready for Render Deployment!")
    print("=" * 80)
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)