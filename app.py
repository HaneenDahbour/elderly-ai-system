from flask import Flask, render_template, request
import joblib
import numpy as np
import csv
import os
from collections import Counter

app = Flask(__name__)

# Load the trained AI model and encoder
model = joblib.load("model.pkl")
le = joblib.load("encoder.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    age = int(request.form["age"])
    health = int(request.form["health"])
    mobility = int(request.form["mobility"])
    mood = int(request.form["mood"])
    lonely = int(request.form["lonely"])
    interest = int(request.form["interest"])

    data = np.array([[age, health, mobility, mood, lonely, interest]])

    prediction = model.predict(data)
    activity = le.inverse_transform(prediction)[0]
    
    # روابط الأنشطة الحقيقية على الإنترنت
    activity_link = ""
    
    if activity == "نادي حوار":
        activity_link = "https://meet.jit.si"  # منصة اجتماعات مجانية
        
    elif activity == "جلسة ألغاز":
        activity_link = "https://www.puzzle-sudoku.com"  # ألعاب ألغاز متنوعة
        
    elif activity == "تمارين خفيفة":
        activity_link = "https://www.youtube.com/watch?v=8BcPHWGQO44"  # فيديو تمارين للكبار
        
    elif activity == "نشاط فني":
        activity_link = "https://sketch.io/sketchpad/"  # لوحة رسم أونلاين
    
    # Activity suggestions
    suggestions = []

    if activity == "نادي حوار":
        suggestions = ["جلسة حوار جماعي", "مناقشة قصة", "نادي ذكريات", "لقاء عائلي", "مشاركة تجارب الحياة"]

    elif activity == "جلسة ألغاز":
        suggestions = ["حل كلمات متقاطعة", "ألعاب ذاكرة", "ألغاز منطقية", "سودوكو", "ألعاب الذكاء"]

    elif activity == "تمارين خفيفة":
        suggestions = ["تمارين تمدد", "مشي جماعي", "حركات كرسي خفيفة", "يوغا للمبتدئين", "تمارين توازن"]

    elif activity == "نشاط فني":
        suggestions = ["رسم وتلوين", "أشغال يدوية", "تشكيل بالصلصال", "موسيقى هادئة", "خط عربي"]

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

    # Save history
    file_exists = os.path.isfile("history.csv")

    with open("history.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["age", "health", "mobility", "mood", "lonely", "interest", "activity"])
        writer.writerow([age, health, mobility, mood, lonely, interest, activity])

    return render_template(
        "result.html",
        activity=activity,
        activity_link=activity_link,
        explanation=explanation,
        suggestions=suggestions
    )


@app.route('/stats')
@app.route('/stats/')
def stats():
    """صفحة الإحصائيات - قراءة البيانات من history.csv"""
    
    # القيم الافتراضية
    total = 0
    most_common = "لا توجد بيانات بعد"
    
    # التحقق من وجود ملف السجل
    if os.path.isfile("history.csv"):
        try:
            # قراءة البيانات من الملف
            activities_list = []
            
            with open("history.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    activities_list.append(row["activity"])
            
            # حساب العدد الإجمالي
            total = len(activities_list)
            
            # إيجاد النشاط الأكثر شيوعاً
            if total > 0:
                counter = Counter(activities_list)
                most_common = counter.most_common(1)[0][0]
        
        except Exception as e:
            print(f"خطأ في قراءة البيانات: {e}")
            total = 0
            most_common = "حدث خطأ في قراءة البيانات"
    
    return render_template('stats.html', 
                         total=total, 
                         most_common=most_common)


@app.errorhandler(404)
def page_not_found(e):
    """معالجة خطأ 404"""
    return """
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
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
                box-shadow: 0 8px 32px rgba(61, 90, 76, 0.12);
                max-width: 600px;
                margin: 0 auto;
            }
            h1 { color: #E07A5F; font-size: 4rem; margin-bottom: 1rem; }
            p { font-size: 1.4rem; color: #2C3E3C; margin-bottom: 2rem; }
            a { 
                display: inline-block;
                padding: 1rem 2rem;
                background: linear-gradient(135deg, #E07A5F 0%, #D66A4F 100%);
                color: white; 
                text-decoration: none; 
                font-size: 1.2rem;
                border-radius: 16px;
                font-weight: bold;
                transition: transform 0.3s ease;
            }
            a:hover {
                transform: translateY(-3px);
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1>404</h1>
            <p>عذراً، الصفحة التي تبحث عنها غير موجودة.</p>
            <a href="/">← العودة للصفحة الرئيسية</a>
        </div>
    </body>
    </html>
    """, 404


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)