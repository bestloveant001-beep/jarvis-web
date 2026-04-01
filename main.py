import flet as ft
import requests
import json
import os
import time
import google.generativeai as genai
from datetime import datetime

# --- 🔐 CONFIG ---
ADMIN_USER = "ADMIN"
ADMIN_CODE = "159753"
GEMINI_API_KEY = "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4" 
DB_FILE = "users_db.json"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. ULTIMATE"
    page.theme_mode = "dark"
    page.bgcolor = "#000814"
    page.padding = 20

    # --- UI STATE ---
    current_user = "SIR"

    def change_tab(e):
        idx = e.control.selected_index
        if idx == 0: show_home()
        elif idx == 1: show_ai()
        elif idx == 2: show_sys()
        elif idx == 3: show_logs()

    # --- 1. HOME PAGE ---
    def show_home():
        page.clean()
        now = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d %B %Y")
        page.add(
            ft.Column([
                ft.Text("WELCOME BACK, " + current_user, size=30, weight="bold", color="cyan"),
                ft.Text(date, size=20, color="grey"),
                ft.Text(now, size=60, weight="bold", color="cyan"),
                ft.Divider(),
                ft.Text("SYSTEM STATUS: OPTIMAL", color="green"),
                ft.ProgressBar(width=400, color="cyan", value=0.4),
                ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login())
            ], horizontal_alignment="center")
        )
        page.add(nav_bar)
        page.update()

    # --- 2. AI PAGE ---
    chat_log = ft.Column(scroll="always", height=300)
    ai_selector = ft.Dropdown(value="Dola", options=[ft.dropdown.Option("Dola"), ft.dropdown.Option("CatGPT")], width=120)
    user_input = ft.TextField(hint_text="Message...", expand=True)

    def ask_ai(e):
        if not user_input.value: return
        msg = user_input.value
        who = ai_selector.value
        chat_log.controls.append(ft.Text("YOU: " + msg, weight="bold"))
        user_input.value = ""
        page.update()
        try:
            resp = model.generate_content("คุณคือ " + who + " ตอบเจ้านายว่า: " + msg)
            color = "cyan" if who == "Dola" else "orange"
            chat_log.controls.append(ft.Text(who.upper() + ": " + resp.text, color=color))
        except:
            chat_log.controls.append(ft.Text("AI OFFLINE (Check API Key)", color="red"))
        page.update()

    def show_ai():
        page.clean()
        page.add(
            ft.Text("AI COMMAND CENTER", size=25, color="cyan", weight="bold"),
            chat_log,
            ft.Row([ai_selector, user_input, ft.ElevatedButton("SEND", on_click=ask_ai)]),
            nav_bar
        )
        page.update()

    # --- 3. SYSTEM MONITOR ---
    def show_sys():
        page.clean()
        page.add(
            ft.Text("HARDWARE MONITOR", size=25, color="cyan"),
            ft.Column([
                ft.Text("CPU CORE: 49%"), ft.ProgressBar(value=0.49, color="red"),
                ft.Text("MEMORY: 2.4GB / 8GB"), ft.ProgressBar(value=0.3, color="blue"),
                ft.Text("NETWORK: 150 Mbps"), ft.ProgressBar(value=0.8, color="green"),
                ft.Text("SATELLITE LINK: ACTIVE", color="cyan")
            ]),
            nav_bar
        )
        page.update()

    # --- 4. LOGS PAGE ---
    def show_logs():
        page.clean()
        db = load_db()
        user_list = ft.Column()
        for u in db: user_list.controls.append(ft.Text("- USER: " + u))
        page.add(
            ft.Text("DATABASE ACCESS", size=25, color="cyan"),
            ft.Text("REGISTERED USERS:"),
            user_list,
            nav_bar
        )
        page.update()

    # --- NAVIGATION BAR (Legacy Compatible) ---
    nav_bar = ft.Tabs(
        selected_index=0,
        on_change=change_tab,
        tabs=[
            ft.Tab(text="HOME"),
            ft.Tab(text="AI"),
            ft.Tab(text="SYS"),
            ft.Tab(text="LOGS"),
        ]
    )

    # --- LOGIN SYSTEM ---
    def show_login():
        page.clean()
        u = ft.TextField(label="USER ID", width=300)
        p = ft.TextField(label="ACCESS CODE", password=True, width=300)
        def login_click(e):
            db = load_db()
            if u.value == ADMIN_USER and p.value == ADMIN_CODE: 
                show_home()
            elif u.value in db and db[u.value] == p.value: 
                show_home()
            else: 
                page.add(ft.Text("DENIED", color="red"))
                page.update()
        page.add(ft.Text("J.A.R.V.I.S. OS", size=30, weight="bold"), u, p, ft.ElevatedButton("ACCESS", on_click=login_click))
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
