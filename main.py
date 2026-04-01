import flet as ft
import os
import time
import google.generativeai as genai

# --- 🔐 CONFIG ---
ADMIN_USER = "ADMIN"
ADMIN_CODE = "159753"
GEMINI_API_KEY = "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4" 

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. NEXT-GEN"
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"
    page.padding = 0 # เต็มจอ

    # ส่วนแสดงเนื้อหาหลัก
    content_area = ft.Container(expand=True, padding=20)

    # --- ฟังก์ชันสลับหน้าจอ ---
    def route_change(route_name):
        content_area.content = None
        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("SYSTEM OVERVIEW", size=30, weight="bold", color="cyan"),
                ft.Row([
                    ft.Container(content=ft.Text("CPU: 42%", color="white"), bgcolor="#1a3355", padding=20, border_radius=10, expand=True),
                    ft.Container(content=ft.Text("NET: ACTIVE", color="white"), bgcolor="#1a3355", padding=20, border_radius=10, expand=True),
                ]),
                ft.Container(
                    content=ft.Column([
                        ft.Text("SATELLITE UPLINK STATUS", size=15, color="cyan"),
                        ft.ProgressBar(value=0.7, color="cyan", bgcolor="#002233"),
                    ]),
                    padding=20, bgcolor="#001a33", border_radius=15
                )
            ], spacing=20)
        
        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", height=400)
            user_in = ft.TextField(label="Command...", expand=True, border_color="cyan")
            def send_msg(e):
                if user_in.value:
                    chat_log.controls.append(ft.Text("YOU: " + user_in.value, color="white"))
                    try:
                        resp = model.generate_content(user_in.value)
                        chat_log.controls.append(ft.Text("DOLA: " + resp.text, color="cyan"))
                    except: chat_log.controls.append(ft.Text("AI ERROR", color="red"))
                    user_in.value = ""
                    page.update()

            content_area.content = ft.Column([
                ft.Text("AI NEURAL LINK", size=25, color="cyan", weight="bold"),
                ft.Container(content=chat_log, bgcolor="#001122", padding=15, border_radius=10, expand=True),
                ft.Row([user_in, ft.ElevatedButton("SEND", on_click=send_msg)])
            ], expand=True)

        elif route_name == "settings":
            content_area.content = ft.Column([
                ft.Text("CORE SETTINGS", size=25, color="cyan"),
                ft.Switch(label="NIGHT PROTOCOL", value=True),
                ft.Switch(label="STEALTH MODE", value=False),
                ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login(), color="red")
            ])
        page.update()

    # --- แถบเมนูข้าง (Sidebar) ---
    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("J.A.R.V.I.S.", size=22, weight="bold", color="cyan"),
            ft.Divider(color="cyan"),
            ft.TextButton("DASHBOARD", on_click=lambda _: route_change("home")),
            ft.TextButton("AI CONSOLE", on_click=lambda _: route_change("ai")),
            ft.TextButton("SETTINGS", on_click=lambda _: route_change("settings")),
        ], spacing=20),
        width=200, bgcolor="#001122", padding=20
    )

    # --- หน้า LOGIN ---
    def show_login():
        page.clean()
        u = ft.TextField(label="IDENTITY", width=250)
        p = ft.TextField(label="PASSCODE", password=True, width=250)
        def do_login(e):
            if u.value == ADMIN_USER and p.value == ADMIN_CODE:
                page.clean()
                page.add(ft.Row([sidebar, content_area], expand=True))
                route_change("home")
            else:
                page.add(ft.Text("ACCESS DENIED", color="red"))
                page.update()
        
        page.add(
            ft.Column([
                ft.Text("BIOMETRIC SCAN", size=35, weight="bold", color="cyan"),
                u, p,
                ft.ElevatedButton("AUTHORIZE", on_click=do_login, width=200)
            ], horizontal_alignment="center")
        )
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
            
