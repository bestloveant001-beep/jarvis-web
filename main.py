import flet as ft
import requests
import json
import os

ADMIN_USER = "ADMIN"
ADMIN_CODE = "159753"
TELEGRAM_TOKEN = "8680149233:AAEmvZHLil3FaiEeAVMAiSi2-Ef3XBzSd5c"
CHAT_ID = "8108462137"
DB_FILE = "users_db.json"

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
    page.title = "JARVIS ONLINE"
    page.theme_mode = ft.ThemeMode.DARK
    
    def go_dash(name):
        page.clean()
        page.add(ft.Text(f"SYSTEM ONLINE: {name}", size=30, color="cyan"))
        page.add(ft.ElevatedButton("LOGOUT", on_click=lambda _: go_login()))
        page.update()

    def go_login(e=None):
        page.clean()
        u = ft.TextField(label="USER")
        p = ft.TextField(label="PASS", password=True)
        def check(e):
            db = load_db()
            if u.value == ADMIN_USER and p.value == ADMIN_CODE: go_dash("SIR")
            elif u.value in db and db[u.value] == p.value: go_dash(u.value)
            else: 
                page.snack_bar = ft.SnackBar(ft.Text("DENIED"), open=True)
                page.update()
        page.add(ft.Text("J.A.R.V.I.S. LOGIN"), u, p, ft.ElevatedButton("ACCESS", on_click=check), ft.TextButton("REG", on_click=go_reg))
        page.update()

    def go_reg(e):
        page.clean()
        nu = ft.TextField(label="NEW USER")
        np = ft.TextField(label="NEW PASS")
        def save(e):
            if nu.value and np.value:
                save_user(nu.value, np.value)
                send_telegram(f"NEW MEMBER: {nu.value}")
                go_login()
        page.add(ft.Text("CREATE ACCOUNT"), nu, np, ft.ElevatedButton("SAVE", on_click=save), ft.TextButton("BACK", on_click=go_login))
        page.update()
    go_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
