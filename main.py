import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY CONFIG ---
USERS = {
    "ADMIN": {"pass": "159753", "level": 10},
    "TONY": {"pass": "9999", "level": 5}
}

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
    content_area = ft.Container(expand=True, padding=20)

    def route_change(route_name):
        content_area.content = None
        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("SYSTEM STATUS", size=30, weight="bold", color="cyan"),
                ft.Row([
                    ft.Container(content=ft.Text("CORE: ONLINE"), bgcolor="#0a192f", padding=20, border_radius=15, expand=True),
                    ft.Container(content=ft.Text("NET: SECURE"), bgcolor="#0a192f", padding=20, border_radius=15, expand=True),
                ])
            ])
        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", expand=True)
            user_input = ft.TextField(hint_text="Command...", expand=True, border_color="cyan")
            def send_msg(e):
                if user_input.value:
                    chat_log.controls.append(ft.Container(content=ft.Text(f"SIR: {user_input.value}"), bgcolor="#1e293b", padding=10, border_radius=10))
                    try:
                        resp = model.generate_content(user_input.value)
                        chat_log.controls.append(ft.Container(content=ft.Text(f"JARVIS: {resp.text}", color="cyan"), bgcolor="#0f172a", padding=10, border_radius=10))
                    except: chat_log.controls.append(ft.Text("ERROR", color="red"))
                    user_input.value = ""; page.update()

            content_area.content = ft.Column([
                ft.Text("AI CONSOLE", size=25, color="cyan"),
                ft.Container(content=chat_log, bgcolor="#050a14", padding=15, border_radius=15, expand=True),
                ft.Row([user_input, ft.IconButton(icon="send", on_click=send_msg, icon_color="cyan")])
            ])
        page.update()

    def build_sidebar():
        return ft.Container(
            content=ft.Column([
                ft.Text("J.A.R.V.I.S.", size=28, weight="bold", color="cyan"),
                ft.Divider(color="#1e3a8a"),
                ft.TextButton("DASHBOARD", on_click=lambda _: route_change("home")),
                ft.TextButton("AI CONSOLE", on_click=lambda _: route_change("ai")),
                ft.VerticalDivider(expand=True),
                ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login(), bgcolor="red", color="white")
            ], spacing=15),
            width=200, bgcolor="#020617", padding=20
        )

    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=280)
        p_in = ft.TextField(label="CODE", password=True, width=280)
        
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                user_session["name"] = u_in.value
                user_session["level"] = USERS[u_in.value]["level"]
                page.clean()
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.add(ft.Text("DENIED", color="red")); page.update()

        # แก้ไขจุดพัง: ใช้ Column ครอบแทนการใช้ Container alignment
        page.add(
            ft.Column([
                ft.Container(height=100), # เว้นระยะข้างบนแทน alignment
                ft.Row([
                    ft.Column([
                        ft.Text("SECURE ACCESS", size=30, color="cyan", weight="bold"),
                        u_in, p_in,
                        ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=200)
                    ], horizontal_alignment="center")
                ], alignment="center")
            ], expand=True)
        )
        page.update()

    show_login()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
