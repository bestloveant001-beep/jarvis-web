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
        lt = ft.Text("SYSTEM BOOTING...", color="cyan", size=20, weight="bold")
        page.add(lt, pb)
        page.update()
        time.sleep(1.5)
        show_login()

    def show_dashboard(name):
        page.clean()
        chat_log = ft.Column(scroll="always", height=350, spacing=10)
        user_input = ft.TextField(hint_text="Message...", expand=True, border_color="cyan")
        ai_selector = ft.Dropdown(
            value="Dola",
            options=[ft.dropdown.Option("Dola"), ft.dropdown.Option("CatGPT")],
            width=120, border_color="cyan"
        )

        def ask_ai(e):
            if not user_input.value: return
            msg = user_input.value
            who = ai_selector.value
            chat_log.controls.append(ft.Text(f"YOU: {msg}", color="white", weight="bold"))
            user_input.value = ""; page.update()
            
            try:
                prompt = f"คุณคือ {who} ตอบคำถามนี้: {msg}"
                response = model.generate_content(prompt)
                color = "cyan" if who == "Dola" else "orange"
                chat_log.controls.append(ft.Text(f"{who.upper()}: {response.text}", color=color))
            except:
                chat_log.controls.append(ft.Text("ERROR: Check API Key", color="red"))
            
            chat_log.scroll_to(offset=-1, duration=300)
            page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("MAIN CONSOLE", size=25, color="cyan", weight="bold"),
                    ft.Divider(color="cyan"),
                    ft.Container(content=chat_log, padding=15, bgcolor="#001529", border_radius=15),
                    ft.Row([ai_selector, user_input, ft.ElevatedButton("SEND", on_click=ask_ai, bgcolor="cyan", color="black")]),
                    ft.TextButton("SHUTDOWN", on_click=lambda _: start_loading(), color="red")
                ], horizontal_alignment="center"),
                padding=25, border=ft.border.all(2, "cyan"), border_radius=25, width=500
            )
        )
        page.update()

    def show_login():
        page.clean()
        u = ft.TextField(label="USER ID", width=300, border_color="cyan")
        p = ft.TextField(label="ACCESS CODE", password=True, width=300, border_color="cyan")
        def login_click(e):
            db = load_db()
            if u.value == ADMIN_USER and p.value == ADMIN_CODE: show_dashboard("SIR")
            elif u.value in db and db[u.value] == p.value: show_dashboard(u.value)
            else: 
                page.snack_bar = ft.SnackBar(ft.Text("DENIED"), open=True)
                page.update()
        page.add(
            ft.Text("SECURITY CHECK", size=30, color="cyan", weight="bold"),
            u, p, 
            ft.ElevatedButton("LOGIN", on_click=login_click, width=200, bgcolor="cyan", color="black"),
            ft.TextButton("REGISTER", on_click=lambda _: show_reg(), color="grey")
        )
        page.update()

    def show_reg():
        page.clean()
        nu, np = ft.TextField(label="NEW USER", width=300), ft.TextField(label="NEW PASS", width=300)
        def reg_click(e):
            if nu.value and np.value: save_user(nu.value, np.value); show_login()
        page.add(ft.Text("NEW ID"), nu, np, ft.ElevatedButton("SAVE", on_click=reg_click), ft.TextButton("BACK", on_click=lambda _: show_login()))
        page.update()

    start_loading()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
    
