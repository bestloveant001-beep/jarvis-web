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
    page.title = "J.A.R.V.I.S. INTERFACE"
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"  # Deep Space Blue
    page.window_width = 1000
    page.window_height = 800
    page.padding = 0

    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=30)

    # --- UI Functions ---
    def route_change(route_name):
        content_area.content = None
        
        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("SYSTEM STATUS", size=40, weight="bold", color="cyan"),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.MEMORY, color="cyan", size=30),
                            ft.Text("NEURAL LINK", size=12, color="grey"),
                            ft.Text("STABLE", size=20, weight="bold", color="cyan"),
                        ]),
                        bgcolor="#0a192f", padding=20, border_radius=15, expand=True, border=ft.border.all(1, "#1e3a8a")
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.SATELLITE_ALT, color="orange", size=30),
                            ft.Text("UPLINK", size=12, color="grey"),
                            ft.Text("ENCRYPTED", size=20, weight="bold", color="orange"),
                        ]),
                        bgcolor="#1a1c2c", padding=20, border_radius=15, expand=True, border=ft.border.all(1, "#334155")
                    ),
                ], spacing=20),
                ft.Container(
                    content=ft.Column([
                        ft.Text("CORE ENERGY", size=14, color="grey"),
                        ft.ProgressBar(value=0.85, color="cyan", bgcolor="#001a33", height=10),
                    ]),
                    padding=20, bgcolor="#001122", border_radius=15
                )
            ], spacing=30)

        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", expand=True, spacing=10)
            user_input = ft.TextField(
                hint_text="Command J.A.R.V.I.S...",
                expand=True,
                border_color="cyan",
                cursor_color="cyan",
                focused_border_color="white",
                text_style=ft.TextStyle(color="white"),
                on_submit=lambda e: send_msg(e)
            )

            def send_msg(e):
                if user_input.value:
                    # User Bubble
                    chat_log.controls.append(
                        ft.Container(
                            content=ft.Text(f"SIR: {user_input.value}", color="white"),
                            alignment=ft.alignment.center_right,
                            padding=10, bgcolor="#1e293b", border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15)
                        )
                    )
                    page.update()
                    
                    # AI Response
                    try:
                        resp = model.generate_content(user_input.value)
                        chat_log.controls.append(
                            ft.Container(
                                content=ft.Text(f"JARVIS: {resp.text}", color="cyan"),
                                alignment=ft.alignment.center_left,
                                padding=10, bgcolor="#0f172a", border=ft.border.all(1, "cyan"),
                                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15)
                            )
                        )
                    except:
                        chat_log.controls.append(ft.Text("SYSTEM ERROR: NEURAL LINK FAILED", color="red"))
                    
                    user_input.value = ""
                    page.update()

            content_area.content = ft.Column([
                ft.Text("NEURAL INTERFACE", size=25, weight="bold", color="cyan"),
                ft.Container(
                    content=chat_log,
                    bgcolor="#050a14", padding=20, border_radius=20, expand=True,
                    border=ft.border.all(1, "#1e3a8a"), shadow=ft.BoxShadow(blur_radius=10, color="#001122")
                ),
                ft.Row([
                    user_input,
                    ft.IconButton(icon=ft.icons.SEND_ROUNDED, icon_color="cyan", icon_size=30, on_click=send_msg)
                ], spacing=10)
            ])
            
        page.update()

    # --- Sidebar ---
    def build_sidebar():
        return ft.Container(
            content=ft.Column([
                ft.Text("J.A.R.V.I.S.", size=30, weight="bold", color="cyan"),
                ft.Text("OS VERSION 5.2", size=10, color="grey"),
                ft.Divider(color="#1e3a8a", height=40),
                ft.TextButton("DASHBOARD", icon=ft.icons.DASHBOARD, on_click=lambda _: route_change("home")),
                ft.TextButton("AI CONSOLE", icon=ft.icons.SMART_TOY, on_click=lambda _: route_change("ai")),
                ft.VerticalDivider(expand=True),
                ft.ElevatedButton(
                    "LOGOUT", icon=ft.icons.LOGOUT, on_click=lambda _: show_login(),
                    style=ft.ButtonStyle(color="white", bgcolor="red", shape=ft.RoundedRectangleBorder(radius=10))
                )
            ], spacing=20),
            width=220, bgcolor="#020617", padding=25,
            border=ft.border.only(right=ft.border.BorderSide(1, "#1e3a8a"))
        )

    # --- Login ---
    def show_login():
        page.clean()
        u_in = ft.TextField(label="USER IDENTITY", border_color="cyan", width=300)
        p_in = ft.TextField(label="ACCESS CODE", password=True, border_color="cyan", width=300)
        
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                user_session["name"] = u_in.value
                user_session["level"] = USERS[u_in.value]["level"]
                page.clean()
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("IDENTITY UNKNOWN"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.FINGERPRINT, size=80, color="cyan"),
                    ft.Text("BIOMETRIC LOGIN", size=30, weight="bold", color="cyan"),
                    u_in, p_in,
                    ft.ElevatedButton("AUTHORIZE", on_click=login_process, width=200, bgcolor="cyan", color="black")
                ], horizontal_alignment="center", spacing=25),
                alignment=ft.alignment.center, expand=True
            )
        )
        page.update()

    show_login()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
            
