import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY DATABASE ---
# รูปแบบ: {"username": {"pass": "password", "level": 10}}
USERS = {
    "ADMIN": {"pass": "159753", "level": 10},
    "TONY": {"pass": "9999", "level": 5},
    "GUEST": {"pass": "0000", "level": 1}
}

GEMINI_API_KEY = "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4" 

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. SECURITY OS"
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"
    page.padding = 0

    # ตัวแปรเก็บสถานะผู้ใช้ปัจจุบัน
    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=25)

    def route_change(route_name):
        content_area.content = None
        lv = user_session["level"]

        # --- หน้า DASHBOARD (Level 5+) ---
        if route_name == "home":
            if lv >= 5:
                content_area.content = ft.Column([
                    ft.Text(f"ACCESS GRANTED: LEVEL {lv}", color="green", weight="bold"),
                    ft.Text("SYSTEM OVERVIEW", size=30, weight="bold", color="cyan"),
                    ft.Row([
                        ft.Container(content=ft.Text("NETWORK: SECURE"), bgcolor="#001529", padding=20, border_radius=10, expand=True),
                        ft.Container(content=ft.Text("SATELLITE: LOCKED"), bgcolor="#001529", padding=20, border_radius=10, expand=True),
                    ])
                ])
            else:
                content_area.content = ft.Text("⚠️ ACCESS DENIED: LEVEL 5 REQUIRED", color="red", size=20)

        # --- หน้า DISASTER MONITOR (Level 10 Only!) ---
        elif route_name == "disaster":
            if lv == 10:
                content_area.content = ft.Column([
                    ft.Text("TOP SECRET: GLOBAL THREAT MONITOR", size=25, color="red", weight="bold"),
                    ft.Container(content=ft.Text("NUCLEAR SENSORS: ONLINE", color="white"), bgcolor="#440000", padding=20, border_radius=15),
                    ft.ElevatedButton("INITIATE COUNTER-MEASURES", bgcolor="red", color="white")
                ])
            else:
                content_area.content = ft.Column([
                    ft.Icon(ft.icons.LOCK, size=100, color="red"),
                    ft.Text("SECURITY VIOLATION", size=30, color="red", weight="bold"),
                    ft.Text("LEVEL 10 CLEARANCE REQUIRED FOR THIS TERMINAL", color="white")
                ], horizontal_alignment="center")

        # --- หน้า AI CONSOLE (Level 1+) ---
        elif route_name == "ai":
            content_area.content = ft.Column([
                ft.Text("AI NEURAL LINK", size=25, color="cyan"),
                ft.TextField(label="Message J.A.R.V.I.S...", expand=True),
                ft.ElevatedButton("EXECUTE")
            ])
            
        page.update()

    # --- แถบข้างที่เปลี่ยนไปตามสิทธิ์ ---
    def build_sidebar():
        lv = user_session["level"]
        menu = [
            ft.Text("J.A.R.V.I.S.", size=25, weight="bold", color="cyan"),
            ft.Text(f"LOGGED: {user_session['name']}\nLEVEL: {lv}", size=10, color="grey"),
            ft.Divider(color="#003355"),
            ft.TextButton("CORE TERMINAL", on_click=lambda _: route_change("home")),
            ft.TextButton("AI INTERFACE", on_click=lambda _: route_change("ai")),
        ]
        
        # เพิ่มเมนูพิเศษสำหรับ Level 10 เท่านั้น
        if lv == 10:
            menu.append(ft.TextButton("DISASTER MONITOR", on_click=lambda _: route_change("disaster"), font_family="bold"))
            menu.append(ft.TextButton("SECURITY CONFIG", on_click=lambda _: route_change("home")))

        menu.append(ft.VerticalDivider(expand=True))
        menu.append(ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login(), bgcolor="red"))
        
        return ft.Container(
            content=ft.Column(menu, spacing=15),
            width=220, bgcolor="#000d1a", padding=25, border=ft.border.only(right=ft.border.BorderSide(1, "#003355"))
        )

    # --- ระบบ LOGIN ที่ตรวจเช็กสิทธิ์ ---
    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=300, border_color="cyan")
        p_in = ft.TextField(label="PASSCODE", password=True, width=300, border_color="cyan")
        
        def login_process(e):
            username = u_in.value
            password = p_in.value
            
            if username in USERS and USERS[username]["pass"] == password:
                user_session["name"] = username
                user_session["level"] = USERS[username]["level"]
                page.clean()
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("INVALID CREDENTIALS"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        page.add(
            ft.Column([
                ft.Text("SECURITY PROTOCOLS", size=30, weight="bold", color="cyan"),
                u_in, p_in,
                ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=200, bgcolor="cyan", color="black")
            ], horizontal_alignment="center", spacing=20)
        )
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
        
