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
    page.title = "J.A.R.V.I.S. MOBILE"
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"
    page.padding = 10

    # --- 🧭 NAVIGATION BAR ---
    def nav():
        return ft.Container(
            content=ft.Row([
                ft.IconButton("dashboard", on_click=lambda _: show_dashboard()),
                ft.IconButton("layers", on_click=lambda _: show_map()),
                ft.IconButton("smart_toy", on_click=lambda _: show_ai()),
                ft.IconButton("logout", icon_color="red", on_click=lambda _: show_login())
            ], alignment="center", spacing=20),
            bgcolor="#050a14", padding=5, border_radius=10
        )

    # --- 📊 PAGE: DASHBOARD ---
    def show_dashboard():
        page.clean()
        page.add(
            nav(),
            ft.Text("SYSTEM STATUS", size=25, weight="bold", color="cyan"),
            ft.Container(
                content=ft.Column([
                    ft.Text("CPU: 32% ONLINE", color="cyan"),
                    ft.Text("NET: SECURE", color="orange"),
                    ft.ProgressBar(value=0.85, color="cyan")
                ]),
                bgcolor="#0a192f", padding=20, border_radius=15
            )
        )

    # --- 🏢 PAGE: MAP ---
    def show_map():
        page.clean()
        floors = [["PENTHOUSE", "cyan"], ["LAB", "orange"], ["ARMORY", "red"], ["GARAGE", "green"]]
        cards = ft.Column(scroll="always", height=400)
        for f in floors:
            cards.controls.append(
                ft.Container(
                    content=ft.Row([ft.Icon("layers", color=f[1]), ft.Text(f[0], weight="bold", expand=True), ft.Icon("chevron_right")]),
                    bgcolor="#0a192f", padding=15, border_radius=10
                )
            )
        page.add(nav(), ft.Text("FACILITY MAP", size=25, weight="bold", color="cyan"), cards)

    # --- 🤖 PAGE: AI ---
    def show_ai():
        page.clean()
        chat_log = ft.Column(scroll="always", height=350)
        user_input = ft.TextField(hint_text="Command...", expand=True)
        def send(e):
            if user_input.value:
                chat_log.controls.append(ft.Text(f"SIR: {user_input.value}"))
                try:
                    resp = model.generate_content(user_input.value)
                    chat_log.controls.append(ft.Text(f"JARVIS: {resp.text}", color="cyan"))
                except: chat_log.controls.append(ft.Text("ERROR: NO API KEY", color="red"))
                user_input.value = ""; page.update()
        page.add(
            nav(),
            ft.Text("AI CONSOLE", size=25, weight="bold", color="cyan"),
            ft.Container(content=chat_log, bgcolor="#050a14", padding=10, border_radius=10, expand=True),
            ft.Row([user_input, ft.ElevatedButton("SEND", on_click=send)])
        )

    # --- 🔐 PAGE: LOGIN ---
    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=250)
        p_in = ft.TextField(label="CODE", password=True, width=250)
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                show_dashboard()
            else:
                page.add(ft.Text("ACCESS DENIED", color="red")); page.update()

        page.add(
            ft.Column([
                ft.Container(height=50),
                ft.Icon("shield_lock", size=60, color="cyan"),
                ft.Text("SECURE LOGIN", size=25, weight="bold", color="cyan"),
                u_in, p_in,
                ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=200, bgcolor="cyan", color="black")
            ], horizontal_alignment="center", spacing=20)
        )
        page.update()

    show_login()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
        
