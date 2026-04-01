import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY ---
USERS = {"ADMIN": {"pass": "159753", "level": 10}, "TONY": {"pass": "9999", "level": 5}}
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S."
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"
    page.padding = 0

    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=15)

    def route_change(route_name):
        content_area.content = None
        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("SYSTEM DASHBOARD", size=25, weight="bold", color="cyan"),
                ft.Row([
                    ft.Container(content=ft.Text("CORE: OK"), bgcolor="#0a192f", padding=15, border_radius=10, expand=True),
                    ft.Container(content=ft.Text("SAT: LINKED"), bgcolor="#0a192f", padding=15, border_radius=10, expand=True),
                ])
            ])
        elif route_name == "map":
            content_area.content = ft.Column([
                ft.Text("FLOOR PLAN", size=25, weight="bold", color="cyan"),
                ft.Container(content=ft.Text("PENTHOUSE - SECURE", color="cyan"), bgcolor="#0a192f", padding=15, border_radius=10),
                ft.Container(content=ft.Text("LAB - ACTIVE", color="orange"), bgcolor="#0a192f", padding=15, border_radius=10),
            ], spacing=10)
        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", expand=True)
            user_input = ft.TextField(hint_text="Command...", expand=True, border_color="cyan")
            def send_msg(e):
                if user_input.value:
                    chat_log.controls.append(ft.Text(f"SIR: {user_input.value}", color="white"))
                    try:
                        resp = model.generate_content(user_input.value)
                        chat_log.controls.append(ft.Text(f"JARVIS: {resp.text}", color="cyan"))
                    except: chat_log.controls.append(ft.Text("AI ERROR", color="red"))
                    user_input.value = ""; page.update()
            content_area.content = ft.Column([
                ft.Container(content=chat_log, bgcolor="#050a14", padding=10, border_radius=10, expand=True),
                ft.Row([user_input, ft.ElevatedButton("SEND", on_click=send_msg, bgcolor="cyan", color="black")])
            ])
        page.update()

    def build_sidebar():
        return ft.Container(
            content=ft.Column([
                ft.Text("J.A.R.V.I.S.", size=22, weight="bold", color="cyan"),
                ft.Divider(color="#1e3a8a"),
                ft.IconButton("dashboard", on_click=lambda _: route_change("home")),
                ft.IconButton("layers", on_click=lambda _: route_change("map")),
                ft.IconButton("smart_toy", on_click=lambda _: route_change("ai")),
                ft.VerticalDivider(expand=True),
                ft.IconButton("logout", icon_color="red", on_click=lambda _: show_login())
            ], spacing=10, horizontal_alignment="center"),
            width=60, bgcolor="#020617", padding=10
        )

    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=250, border_color="cyan")
        p_in = ft.TextField(label="CODE", password=True, width=250, border_color="cyan")
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                user_session.update({"name": u_in.value, "level": USERS[u_in.value]["level"]})
                page.clean()
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.add(ft.Text("DENIED", color="red")); page.update()

        page.add(ft.Column([
            ft.Container(height=50),
            ft.Icon("shield_lock", size=60, color="cyan"),
            ft.Text("SECURE LOGIN", size=25, color="cyan", weight="bold"),
            u_in, p_in,
            ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=200, bgcolor="cyan", color="black")
        ], horizontal_alignment="center", spacing=20))
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
                    
