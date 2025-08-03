import webbrowser
import os
from datetime import datetime

def generate_landing_page(prompt):
    folder_name = f"landing_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)

    # איתור תמונות מתוך תיקיית uploads
    upload_dir = "uploads"
    media_files = []
    for file in os.listdir(upload_dir):
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4")):
            media_files.append(file)

    gallery_html = ""
    for file in media_files:
        if file.lower().endswith(".mp4"):
            gallery_html += f'''
            <video controls width="300" style="border-radius:12px;">
                <source src="../uploads/{file}" type="video/mp4">
                הדפדפן שלך לא תומך בווידאו.
            </video>
            '''
        else:
            gallery_html += f'''
            <img src="../uploads/{file}" alt="תמונה" width="280" height="180" style="object-fit:cover;border-radius:12px;">
            '''

    html_template = f"""
    <!DOCTYPE html>
    <html lang="he">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>דף נחיתה מקצועי</title>
        <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                font-family: 'Heebo', sans-serif;
                background: linear-gradient(to bottom right, #f5f7fa, #c3cfe2);
                color: #333;
            }}
            header {{
                background-color: #4a90e2;
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            h1 {{
                margin: 0;
                font-size: 36px;
            }}
            section {{
                padding: 40px 20px;
                max-width: 900px;
                margin: auto;
            }}
            .gallery {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
            }}
            .cta {{
                text-align: center;
                margin-top: 40px;
            }}
            button {{
                background-color: #4a90e2;
                color: white;
                font-size: 18px;
                padding: 12px 32px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            button:hover {{
                background-color: #357ab8;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>דף נחיתה מותאם אישית</h1>
            <p>{prompt}</p>
        </header>

        <section>
            <h2>קצת על הלקוחה</h2>
            <p>הטקסט הזה יכול להשתנות לפי השירות שהוזמן. למשל: חני היא קוסמטיקאית מקצועית עם שנים של ניסיון בטיפולי פנים, איפור קבוע ועוד.</p>
        </section>

        <section>
            <h2>תמונות וסרטונים</h2>
            <div class="gallery">
                {gallery_html}
            </div>
        </section>

        <section class="cta">
            <h2>מעוניינת בפרטים נוספים?</h2>
            <a href="https://wa.me/972000000000"><button>שלחי לי וואטסאפ</button></a>
        </section>
    </body>
    </html>
    """

    # שמירה
    file_path = os.path.join(folder_name, "index.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    webbrowser.open(f"file://{os.path.abspath(file_path)}")
    return f"✅ דף הנחיתה נוצר בתיקייה: {folder_name}"
