import flet as ft
import requests
import json
import os
import time

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
    page.title = "J.A.R.V.I.S. MAINFRAME"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000b1a"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # --- 🌀 หน้าจอโหลดระบบ (Loading Screen) ---
    def start_loading():
        page.clean()
        progress_bar = ft.ProgressBar(width=300, color="cyan", bgcolor="#002233")
        loading_text = ft.Text("INITIALIZING SYSTEM...", color="cyan", italic=True)
        
        page.add(
            ft.Icon(ft.icons.TERMINAL, size=50, color="cyan"),
            loading_text,
            progress_bar,
            ft.Text("DECRYPTING INTERFACE v8.0", size=10, color="grey")
        )
        page.update()
        
        # จำลองการโหลด
        steps = ["CONNECTING TO SATELLITE...", "LOADING DATABASE...", "BYPASSING FIREWALL...", "SYSTEM READY!"]
        for i, step in enumerate(steps):
            time.sleep(0.8)
            loading_text.value = step
            progress_bar.value = (i + 1) / len(steps)
            page.update()
        
        time.sleep(0.5)
        show_login()

    def show_dashboard(name):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.HUB, size=60, color="cyan"),
                    ft.Text("J.A.R.V.I.S. ONLINE", size=30, weight="bold", color="cyan"),
                    ft.Divider(color="cyan"),
                    ft.Text(f"WELCOME BACK: {name}", size=20),
                    ft.ElevatedButton("SHUTDOWN", on_click=lambda _: start_loading(), color="red")
                ], horizontal_alignment="center"),
                padding=40, border=ft.border.all(2, "cyan"), border_radius=20, bgcolor="#001529"
            )
        )
        page.update()

    def show_login():
        page.clean()
        u = ft.TextField(label="USER ID", border_color="cyan", width=300)
        p = ft.TextField(label="ACCESS CODE", password=True, border_color="cyan", width=300)
        
        def login_click(e):
            db = load_db()
            if u.value == ADMIN_USER and p.value == ADMIN_CODE:
                send_telegram("⚡ ADMIN ACCESS GRANTED")
                show_dashboard("SIR")
            elif u.value in db and db[u.value] == p.value:
                send_telegram(f"👤 USER: {u.value} LOGGED IN")
                show_dashboard(u.value)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("INVALID CREDENTIALS"), open=True)
                page.update()

        page.add(
            ft.Icon(ft.icons.SECURITY, size=80, color="cyan"),
            ft.Text("AUTHENTICATION REQUIRED", size=18, weight="bold"),
            u, p,
            ft.ElevatedButton("LOG IN", on_click=login_click, width=200, style=ft.ButtonStyle(color="black", bgcolor="cyan")),
            ft.TextButton("REGISTER NEW ACCOUNT", on_click=lambda _: show_reg(), color="grey")
        )
        page.update()

    def show_reg():
        page.clean()
        nu = ft.TextField(label="NEW USER ID", border_color="cyan", width=300)
        np = ft.TextField(label="NEW ACCESS CODE", border_color="cyan", width=300)
        
        def reg_click(e):
            if nu.value and np.value:
                save_user(nu.value, np.value)
                send_telegram(f"📝 NEW REGISTRATION: {nu.value}")
                show_login()

        page.add(
            ft.Text("CREATE ACCESS ID", size=20, color="cyan"),
            nu, np,
            ft.ElevatedButton("REGISTER", on_click=reg_click, width=200),
            ft.TextButton("BACK TO LOGIN", on_click=lambda _: show_login())
        )
        page.update()

    start_loading() # เริ่มต้นด้วยหน้าโหลดระบบ

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
    
