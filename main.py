import flet as ft
import requests
import json
import os
import time
import google.generativeai as genai

# --- 🔐 ตั้งค่าระบบ ---
ADMIN_USER = "ADMIN"
ADMIN_CODE = "159753"
TELEGRAM_TOKEN = "8680149233:AAEmvZHLil3FaiEeAVMAiSi2-Ef3XBzSd5c"
CHAT_ID = "8108462137"
GEMINI_API_KEY = "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4" # <--- อย่าลืมใส่ Key นะครับเจ้านาย
DB_FILE = "users_db.json"

# ตั้งค่าสมองกล AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_user(u, p):
    db = load_db()
    db[u] = p
    with open(DB_FILE, "w") as f: json.dump(db, f)

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except: pass

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. ULTIMATE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000814"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def start_loading():
        page.clean()
        pb = ft.ProgressBar(width=300, color="cyan")
        lt = ft.Text("BOOTING DOLA & CAT-GPT...", color="cyan", italic=True)
        page.add(ft.Icon(ft.icons.AUTO_AWESOME, size=50, color="cyan"), lt, pb)
        page.update()
        for s in ["LOADING CORE AI...", "SYNCING DOLA...", "SYNCING CAT-GPT...", "SYSTEMS ONLINE!"]:
            time.sleep(0.6); lt.value = s; page.update()
        show_login()

    def show_dashboard(name):
        page.clean()
        chat_log = ft.Column(scroll="always", height=350, spacing=10)
        user_input = ft.TextField(hint_text="Talk to Dola or CatGPT...", expand=True, border_color="cyan")
        
        # ตัวเลือกผู้ช่วย
        ai_selector = ft.Dropdown(
            value="Dola",
            options=[ft.dropdown.Option("Dola"), ft.dropdown.Option("CatGPT")],
            width=120, border_color="cyan", color="cyan"
        )

        def ask_ai(e):
            if not user_input.value: return
            msg = user_input.value
            who = ai_selector.value
            chat_log.controls.append(ft.Text(f"You: {msg}", color="white", weight="bold"))
            user_input.value = ""; page.update()
            
            try:
                # กำหนดบุคลิกตามตัวเลือก
                prompt = ""
                if who == "Dola":
                    prompt = f"คุณคือ Dola ผู้ช่วยส่วนตัวที่สุภาพ ฉลาด และเป็นกันเอง คอยสนับสนุนเจ้านายอย่างดีที่สุด ตอบคำถามนี้: {msg}"
                    icon = "🤖 Dola"
                    color = "cyan"
                else:
                    prompt = f"คุณคือ CatGPT แมวอัจฉริยะที่กวนๆ ชอบตอบแบบติดตลกและมีเสียงร้องเมี๊ยวๆ ตอบคำถามนี้: {msg}"
                    icon = "🐱 CatGPT"
                    color = "orange"

                response = model.generate_content(prompt)
                chat_log.controls.append(ft.Text(f"{icon}: {response.text}", color=color))
            except:
                chat_log.controls.append(ft.Text("SYSTEM ERROR: API Key Missing!", color="red"))
            
            chat_log.scroll_to(offset=-1, duration=300)
            page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Row([ft.Icon(ft.icons.HUB, color="cyan"), ft.Text("J.A.R.V.I.S. CORE", size=25, color="cyan", weight="bold")], alignment="center"),
                    ft.Divider(color="cyan"),
                    ft.Container(content=chat_log, padding=15, bgcolor="#001529", border_radius=15, border=ft.border.all(1, "#003366")),
                    ft.Row([ai_selector, user_input, ft.IconButton(ft.icons.SEND_ROUNDED, on_click=ask_ai, icon_color="cyan")], alignment="center"),
                    ft.Text(f"LOGGED IN AS: {name}", size=12, color="grey"),
                    ft.ElevatedButton("SHUTDOWN", on_click=lambda _: start_loading(), bgcolor="#220000", color="red")
                ], horizontal_alignment="center"),
                padding=25, border=ft.border.all(2, "cyan"), border_radius=25, width=600, bgcolor="#000c18"
            )
        )
        page.update()

    # --- Login/Reg Functions ---
    def show_login():
        page.clean()
        u = ft.TextField(label="USER ID", width=300, border_color="cyan")
        p = ft.TextField(label="ACCESS CODE", password=True, width=300, border_color="cyan")
        def login_click(e):
            db = load_db()
            if u.value == ADMIN_USER and p.value == ADMIN_CODE: show_dashboard("SIR")
            elif u.value in db and db[u.value] == p.value: show_dashboard(u.value)
            else: page.snack_bar = ft.SnackBar(ft.Text("ACCESS DENIED"), open=True); page.update()
        page.add(ft.Icon(ft.icons.LOCK_PERSON, size=80, color="cyan"), u, p, 
                 ft.ElevatedButton("ACCESS", on_click=login_click, width=200, bgcolor="cyan", color="black"),
                 ft.TextButton("CREATE NEW ID", on_click=lambda _: show_reg(), color="grey"))
        page.update()

    def show_reg():
        page.clean()
        nu, np = ft.TextField(label="NEW USER", width=300), ft.TextField(label="NEW PASS", width=300)
        def reg_click(e):
            if nu.value and np.value: save_user(nu.value, np.value); send_telegram(f"NEW ID: {nu.value}"); show_login()
        page.add(ft.Text("REGISTRATION SYSTEM"), nu, np, ft.ElevatedButton("SAVE", on_click=reg_click), ft.TextButton("BACK", on_click=lambda _: show_login()))
        page.update()

    start_loading()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
    
