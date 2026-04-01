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
GEMINI_API_KEY = "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4" 
DB_FILE = "users_db.json"

# ตั้งค่าสมองกล AI
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_user(u, p):
    db = load_db()
    db[u] = p
    with open(DB_FILE, "w") as f: json.dump(db, f)

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. LEGACY"
    page.theme_mode = "dark"
    page.bgcolor = "#000814"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def start_loading():
        page.clean()
        pb = ft.ProgressBar(width=300)
        lt = ft.Text("SYSTEM STARTING...", size=20)
        page.add(lt, pb)
        page.update()
        time.sleep(1)
        show_login()

    def show_dashboard(name):
        page.clean()
        chat_log = ft.Column(scroll="always", height=300)
        user_input = ft.TextField(hint_text="Message...", expand=True)
        ai_selector = ft.Dropdown(
            value="Dola",
            options=[ft.dropdown.Option("Dola"), ft.dropdown.Option("CatGPT")],
            width=120
        )

        def ask_ai(e):
            if not user_input.value: return
            msg = user_input.value
            who = ai_selector.value
            chat_log.controls.append(ft.Text("YOU: " + msg))
            user_input.value = ""
            page.update()
            
            try:
                p = "คุณคือ " + who + " ตอบคำถามนี้: " + msg
                resp = model.generate_content(p)
                chat_log.controls.append(ft.Text(who.upper() + ": " + resp.text))
            except:
                chat_log.controls.append(ft.Text("SYSTEM ERROR"))
            
            page.update()

        page.add(
            ft.Text("MAIN CONSOLE", size=25, weight="bold"),
            chat_log,
            ft.Row([ai_selector, user_input, ft.ElevatedButton("SEND", on_click=ask_ai)]),
            ft.ElevatedButton("LOGOUT", on_click=lambda _: start_loading())
        )
        page.update()

    def show_login():
        page.clean()
        u = ft.TextField(label="USER ID", width=300)
        p = ft.TextField(label="ACCESS CODE", password=True, width=300)
        def login_click(e):
            db = load_db()
            if u.value == ADMIN_USER and p.value == ADMIN_CODE: show_dashboard("SIR")
            elif u.value in db and db[u.value] == p.value: show_dashboard(u.value)
            else: 
                page.add(ft.Text("DENIED", color="red"))
                page.update()
        page.add(
            ft.Text("SECURITY CHECK", size=30, weight="bold"),
            u, p, 
            ft.ElevatedButton("LOGIN", on_click=login_click),
            ft.ElevatedButton("REGISTER", on_click=lambda _: show_reg())
        )
        page.update()

    def show_reg():
        page.clean()
        nu = ft.TextField(label="NEW USER", width=300)
        np = ft.TextField(label="NEW PASS", width=300)
        def reg_click(e):
            if nu.value and np.value: 
                save_user(nu.value, np.value)
                show_login()
        page.add(ft.Text("NEW ID"), nu, np, ft.ElevatedButton("SAVE", on_click=reg_click))
        page.update()

    start_loading()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
        
