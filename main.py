import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY DATABASE ---
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

    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=25)

    def route_change(route_name):
        content_area.content = None
        lv = user_session["level"]

        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("SYSTEM OVERVIEW", size=30, weight="bold", color="cyan"),
                ft.Text(f"CURRENT CLEARANCE: LEVEL {lv}", color="green"),
                ft.Divider(color="#003355"),
                ft.Row([
                    ft.Container(content=ft.Text("NETWORK: SECURE"), bgcolor="#001529", padding=20, border_radius=10, expand=True),
                    ft.Container(content=ft.Text("SATELLITE: ACTIVE"), bgcolor="#001529", padding=20, border_radius=10, expand=True),
                ])
            ])
        
        elif route_name == "disaster":
            if lv == 10:
                content_area.content = ft.Column([
                    ft.Text("DISASTER MONITOR", size=30, weight="bold", color="red"),
                    ft.Container(content=ft.Text("NO THREATS DETECTED", color="white"), bgcolor="#440000", padding=20, border_radius=15),
                    ft.ElevatedButton("SYSTEM SCAN", bgcolor="red", color="white")
                ])
            else:
                content_area.content = ft.Column([
                    ft.Text("ACCESS DENIED", size=40, color="red", weight="bold"),
                    ft.Text("LEVEL 10 REQUIRED", size=20)
                ], horizontal_alignment="center")

        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", height=300)
            content_area.content = ft.Column([
                ft.Text("AI INTERFACE", size=25, color="cyan"),
                chat_log,
                ft.Row([ft.TextField(hint_text="Message...", expand=True), ft.ElevatedButton("SEND")])
            ])
            
        page.update()

    def build_sidebar():
        lv = user_session["level"]
        menu_items = [
            ft.Text("J.A.R.V.I.S.", size=25, weight="bold", color="cyan"),
            ft.Text(f"USER: {user_session['name']}", size=12, color="grey"),
            ft.Divider(color="#003355"),
            ft.TextButton("DASHBOARD", on_click=lambda _: route_change("home")),
            ft.TextButton("AI CONSOLE", on_click=lambda _: route_change("ai")),
        ]
        
        if lv == 10:
            menu_items.append(ft.TextButton("THREAT MONITOR", on_click=lambda _: route_change("disaster")))

        menu_items.append(ft.VerticalDivider(expand=True))
        menu_items.append(ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login(), bgcolor="red", color="white"))
        
        return ft.Container(
            content=ft.Column(menu_items, spacing=15),
            width=220, bgcolor="#000d1a", padding=25, border=ft.border.only(right=ft.border.BorderSide(1, "#003355"))
        )

    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=300)
        p_in = ft.TextField(label="PASSCODE", password=True, width=300)
        
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                user_session["name"] = u_in.value
                user_session["level"] = USERS[u_in.value]["level"]
                page.clean()
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.add(ft.Text("INVALID CREDENTIALS", color="red"))
                page.update()

        page.add(ft.Column([ft.Text("SECURITY LOGIN", size=30, color="cyan"), u_in, p_in, ft.ElevatedButton("ACCESS", on_click=login_process)], horizontal_alignment="center", spacing=20))
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
        
