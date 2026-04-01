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
    page.title = "J.A.R.V.I.S. ULTIMATE"
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"
    page.padding = 10

    # --- 📟 ฟังก์ชันสลับหน้า (แบบ Clean Page เพื่อความเสถียรบนมือถือ) ---
    def show_dashboard(e=None):
        page.clean()
        page.add(
            navigation_bar(),
            ft.Column([
                ft.Text("SYSTEM STATUS", size=28, weight="bold", color="cyan"),
                ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Icon("memory", color="cyan"), ft.Text("CPU: 32% ONLINE")]),
                        ft.Row([ft.Icon("satellite_alt", color="orange"), ft.Text("UPLINK: SECURE")]),
                        ft.ProgressBar(value=0.85, color="cyan")
                    ]),
                    bgcolor="#0a192f", padding=20, border_radius=15, border=ft.border.all(1, "#1e3a8a")
                ),
                ft.Text("ACTIVE RELEASES: MARK 85", size=12, color="grey")
            ], spacing=20)
        )

    def show_map(e=None):
        page.clean()
        floors = [
            {"n": "PENTHOUSE", "s": "SECURE", "c": "cyan"},
            {"n": "R&D LAB", "s": "ACTIVE", "c": "orange"},
            {"n": "ARMORY", "s": "LOCKED", "c": "red"},
            {"n": "GARAGE", "s": "EMPTY", "c": "green"},
        ]
        floor_cards = ft.Column(scroll="always", height=450)
        for f in floors:
            floor_cards.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("layers", color=f["c"]),
                        ft.Column([ft.Text(f["n"], weight="bold"), ft.Text(f"STATUS: {f['s']}", size=12, color="grey")], expand=True),
                        ft.IconButton("open_in_new", icon_color=f["c"])
                    ]),
                    bgcolor="#0a192f", padding=15, border_radius=12, border=ft.border.all(1, "#1e3a8a")
                )
            )
        page.add(
            navigation_bar(),
            ft.Text("FACILITY MAP", size=28, weight="bold", color="cyan"),
            floor_cards
        )

    def show_ai(e=None):
        page.clean()
        chat_log = ft.Column(scroll="always", height=400, spacing=10)
        user_input = ft.TextField(hint_text="Command J.A.R.V.I.S...", expand=True, border_color="cyan")
        
        def send(e):
            if user_input.value:
                chat_log.controls.append(ft.Container(content=ft.Text(f"SIR: {user_input.value}"), bgcolor="#1e293b", padding=10, border_radius=10))
                try:
                    resp = model.generate_content(user_input.value)
                    chat_log.controls.append(ft.Container(content=ft.Text(f"JARVIS: {resp.text}", color="cyan"), bgcolor="#0f172a", padding=10, border_radius=10, border=ft.border.all(1, "cyan")))
                except: chat_log.controls.append(ft.Text("ERROR: NO API KEY", color="red"))
                user_input.value = ""; page.update()

        page.add(
            navigation_bar(),
            ft.Text("NEURAL INTERFACE", size=28, weight="bold", color="cyan"),
            ft.Container(content=chat_log, bgcolor="#050a14", padding=15, border_radius=15, expand=True, border=ft.border.all(1, "#1e3a8a")),
            ft.Row([user_input, ft.IconButton("send", on_click=send, icon_color="cyan")])
        )

    # --- 🧭 แถบเมนูเปลี่ยนหน้า (อยู่ด้านบนเพื่อให้กดง่ายบนมือถือ) ---
    def navigation_bar():
        return ft.Container(
            content=ft.Row([
                ft.IconButton("dashboard", on_click=show_dashboard, tooltip="Dashboard"),
                ft.IconButton("layers", on_click=show_map, tooltip="Floor Map"),
                ft.IconButton("smart_toy", on_click=show_ai, tooltip="AI Console"),
                ft.VerticalDivider(),
                ft.IconButton("logout", icon_color="red", on_click=lambda _: show_login())
            ], alignment="center"),
            bgcolor="#020617", padding=5, border_radius=10, margin=ft.margin.only(bottom=20)
        )

    # --- 🔐 หน้า LOGIN (THE NEW TECH LOOK) ---
    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=280, border_color="cyan", prefix_icon="person")
        p_in = ft.TextField(label="ACCESS CODE", password=True, width=280, border_color="cyan", prefix_icon="key")
        
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                show_dashboard()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("INVALID ACCESS"), bgcolor="red")
                page.snack_bar.open = True; page.update()

        page.add(
            ft.Column([
                ft.Container(height=60),
                ft.Icon("shield_lock", size=80, color="cyan"),
                ft.Text("SECURE ACCESS", size=30, weight="bold", color="cyan"),
                ft.Text("SYSTEM ENCRYPTED", size=10, color="grey"),
                u_in, p_in,
                ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=220, bgcolor="cyan", color="black", height=50)
            ], horizontal_alignment="center", spacing=20)
        )
        page.update()

    show_login()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
        
