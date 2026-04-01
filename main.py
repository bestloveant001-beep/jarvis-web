import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY CONFIG ---
USERS = {
    "ADMIN": {"pass": "159753", "level": 10},
    "TONY": {"pass": "9999", "level": 5}
}

# ดึง API Key จาก Environment Variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. COMMAND CENTER"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#00050a"
    page.padding = 0
    page.window_width = 1100
    page.window_height = 800

    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=30)

    # --- 🏢 UI NAVIGATION & CONTENT ---
    def route_change(route_name):
        content_area.content = None
        lv = user_session["level"]

        # 1. DASHBOARD
        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("SYSTEM OVERVIEW", size=40, weight="bold", color="cyan"),
                ft.Row([
                    ft.Container(content=ft.Column([ft.Icon("memory", color="cyan"), ft.Text("CPU: 32%", size=20)], horizontal_alignment="center"), bgcolor="#0a192f", padding=20, border_radius=15, expand=True, border=ft.border.all(1, "#1e3a8a")),
                    ft.Container(content=ft.Column([ft.Icon("satellite_alt", color="orange"), ft.Text("NET: SECURE", size=20)], horizontal_alignment="center"), bgcolor="#0a192f", padding=20, border_radius=15, expand=True, border=ft.border.all(1, "#1e3a8a")),
                ], spacing=20),
                ft.Container(content=ft.Column([ft.Text("ENERGY CORE", size=12, color="grey"), ft.ProgressBar(value=0.85, color="cyan", height=10)]), bgcolor="#001122", padding=20, border_radius=15)
            ], spacing=30)

        # 2. FLOOR MAP (NEW!)
        elif route_name == "map":
            floors = [
                {"n": "PENTHOUSE", "s": "SECURE", "t": "24°C", "c": "cyan"},
                {"n": "R&D LAB", "s": "ACTIVE", "t": "21°C", "c": "orange"},
                {"n": "ARMORY", "s": "LOCKED", "t": "20°C", "c": "red"},
                {"n": "GARAGE", "s": "EMPTY", "t": "28°C", "c": "green"},
            ]
            floor_list = ft.Column(spacing=10, scroll="always")
            for f in floors:
                floor_list.controls.append(
                    ft.Container(
                        content=ft.Row([ft.Icon("layers", color=f["c"]), ft.Column([ft.Text(f["n"], weight="bold"), ft.Text(f"STATUS: {f['s']} | {f['t']}", size=12, color="grey")], expand=True), ft.ElevatedButton("GO")], spacing=15),
                        bgcolor="#0a192f", padding=15, border_radius=12, border=ft.border.all(1, "#1e3a8a")
                    )
                )
            content_area.content = ft.Column([
                ft.Text("FACILITY BLUEPRINT", size=30, weight="bold", color="cyan"),
                ft.Row([
                    ft.Container(content=ft.Column([ft.Container(height=40, width=150, bgcolor="#1e3a8a" if i==0 else "#0a192f", border=ft.border.all(1, "cyan"), border_radius=5) for i in range(4)], horizontal_alignment="center"), bgcolor="#050a14", padding=20, border_radius=15),
                    ft.Container(content=floor_list, expand=True)
                ], spacing=20, vertical_alignment="start")
            ])

        # 3. AI CONSOLE
        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", expand=True, spacing=10)
            user_input = ft.TextField(hint_text="Message J.A.R.V.I.S...", expand=True, border_color="cyan")
            def send_msg(e):
                if user_input.value:
                    chat_log.controls.append(ft.Container(content=ft.Text(f"SIR: {user_input.value}"), bgcolor="#1e293b", padding=10, border_radius=10))
                    try:
                        resp = model.generate_content(user_input.value)
                        chat_log.controls.append(ft.Container(content=ft.Text(f"JARVIS: {resp.text}", color="cyan"), bgcolor="#0f172a", padding=10, border_radius=10, border=ft.border.all(1, "cyan")))
                    except: chat_log.controls.append(ft.Text("SYSTEM ERROR", color="red"))
                    user_input.value = ""; page.update()
            
            content_area.content = ft.Column([
                ft.Text("NEURAL INTERFACE", size=25, color="cyan", weight="bold"),
                ft.Container(content=chat_log, bgcolor="#050a14", padding=20, border_radius=15, expand=True, border=ft.border.all(1, "#1e3a8a")),
                ft.Row([user_input, ft.ElevatedButton("SEND", on_click=send_msg, bgcolor="cyan", color="black")])
            ])
        page.update()

    # --- 📟 SIDEBAR COMPONENT ---
    def build_sidebar():
        return ft.Container(
            content=ft.Column([
                ft.Text("J.A.R.V.I.S.", size=30, weight="bold", color="cyan"),
                ft.Text("OS v6.0 ONLINE", size=10, color="grey"),
                ft.Divider(color="#1e3a8a", height=30),
                ft.TextButton("DASHBOARD", icon="dashboard", on_click=lambda _: route_change("home")),
                ft.TextButton("FLOOR MAP", icon="layers", on_click=lambda _: route_change("map")),
                ft.TextButton("AI CONSOLE", icon="smart_toy", on_click=lambda _: route_change("ai")),
                ft.VerticalDivider(expand=True),
                ft.ElevatedButton("LOGOUT", icon="logout", on_click=lambda _: show_login(), bgcolor="red", color="white")
            ], spacing=15),
            width=210, bgcolor="#020617", padding=25, border=ft.border.only(right=ft.border.BorderSide(1, "#1e3a8a"))
        )

    # --- 🔐 COOL LOGIN SCREEN ---
    def show_login():
        page.clean()
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        
        u_in = ft.TextField(label="IDENTITY", width=300, border_color="cyan", prefix_icon="person")
        p_in = ft.TextField(label="ACCESS CODE", password=True, width=300, border_color="cyan", prefix_icon="key")
        
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                user_session["name"] = u_in.value
                user_session["level"] = USERS[u_in.value]["level"]
                page.clean()
                page.horizontal_alignment = "start"; page.vertical_alignment = "start"
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("INVALID ACCESS CODE"), bgcolor="red")
                page.snack_bar.open = True; page.update()

        login_box = ft.Container(
            content=ft.Column([
                ft.Icon("shield_lock", size=70, color="cyan"),
                ft.Text("SECURE LOGIN", size=28, weight="bold", color="cyan"),
                ft.Text("LEVEL 10 CLEARANCE REQUIRED", size=10, color="grey"),
                ft.Divider(height=10, color="transparent"),
                u_in, p_in,
                ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=220, bgcolor="cyan", color="black", height=45)
            ], horizontal_alignment="center", spacing=20),
            padding=40, bgcolor="#050a14", border_radius=25, border=ft.border.all(1, "cyan"),
            shadow=ft.BoxShadow(blur_radius=20, color="#001122")
        )
        page.add(login_box)
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
                
