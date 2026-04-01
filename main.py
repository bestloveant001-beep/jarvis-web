import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY DATABASE ---
USERS = {
    "ADMIN": {"pass": "159753", "level": 10},
    "TONY": {"pass": "9999", "level": 5},
    "GUEST": {"pass": "0000", "level": 1}
}

# ดึง API Key จาก Environment Variable ของ Railway (เพื่อความปลอดภัย)
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

    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=25)

    def route_change(route_name):
        content_area.content = None
        lv = user_session["level"]

        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("MAIN TERMINAL", size=35, weight=ft.FontWeight.BOLD, color="cyan"),
                ft.Text(f"ACCESS LEVEL: {lv} | SYSTEM STATUS: OPTIMAL", color="green"),
                ft.Divider(color="#003355"),
                ft.Row([
                    ft.Container(content=ft.Text("CPU: 32%", color="white"), bgcolor="#001a33", padding=20, border_radius=10, expand=True),
                    ft.Container(content=ft.Text("SATELLITE: ACTIVE", color="white"), bgcolor="#001a33", padding=20, border_radius=10, expand=True),
                ])
            ], spacing=20)
        
        elif route_name == "disaster":
            if lv == 10:
                content_area.content = ft.Column([
                    ft.Text("THREAT MONITOR", size=30, weight=ft.FontWeight.BOLD, color="red"),
                    ft.Container(content=ft.Text("SCANNING GLOBAL THREATS...", color="white"), bgcolor="#330000", padding=20, border_radius=15),
                    ft.ElevatedButton("INITIATE COUNTER-MEASURES", color="white", bgcolor="red")
                ])
            else:
                content_area.content = ft.Column([
                    ft.Icon(ft.icons.LOCK, size=80, color="red"),
                    ft.Text("ACCESS DENIED", size=30, color="red", weight=ft.FontWeight.BOLD),
                    ft.Text("LEVEL 10 CLEARANCE REQUIRED")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        elif route_name == "ai":
            chat_log = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=350)
            user_input = ft.TextField(hint_text="Command J.A.R.V.I.S...", expand=True)
            
            def send_msg(e):
                if user_input.value:
                    chat_log.controls.append(ft.Text(f"SIR: {user_input.value}", color="white", weight=ft.FontWeight.BOLD))
                    try:
                        resp = model.generate_content(user_input.value)
                        chat_log.controls.append(ft.Text(f"JARVIS: {resp.text}", color="cyan"))
                    except:
                        chat_log.controls.append(ft.Text("ERROR: NEURAL LINK OFFLINE", color="red"))
                    user_input.value = ""
                    page.update()

            content_area.content = ft.Column([
                ft.Text("AI NEURAL INTERFACE", size=25, color="cyan"),
                ft.Container(content=chat_log, bgcolor="#000d1a", padding=15, border_radius=10, expand=True, border=ft.border.all(1, "cyan")),
                ft.Row([user_input, ft.ElevatedButton("SEND", on_click=send_msg)])
            ])
            
        page.update()

    def build_sidebar():
        lv = user_session["level"]
        menu = [
            ft.Text("J.A.R.V.I.S.", size=28, weight=ft.FontWeight.BOLD, color="cyan"),
            ft.Text(f"USER: {user_session['name']}", size=12, color="grey"),
            ft.Divider(color="#003355"),
            ft.TextButton("DASHBOARD", on_click=lambda _: route_change("home")),
            ft.TextButton("AI CONSOLE", on_click=lambda _: route_change("ai")),
        ]
        if lv == 10:
            menu.append(ft.TextButton("THREAT MONITOR", on_click=lambda _: route_change("disaster")))
        
        menu.append(ft.VerticalDivider(expand=True))
        menu.append(ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login(), color="white", bgcolor="red"))
        
        return ft.Container(
            content=ft.Column(menu, spacing=15),
            width=210, bgcolor="#000a14", padding=20, border=ft.border.only(right=ft.border.BorderSide(1, "#003355"))
        )

    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=280)
        p_in = ft.TextField(label="PASSCODE", password=True, width=280)
        
        def login_process(e):
            u = u_in.value
            p = p_in.value
            if u in USERS and USERS[u]["pass"] == p:
                user_session["name"] = u
                user_session["level"] = USERS[u]["level"]
                page.clean()
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("INVALID ACCESS CODE"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("SECURITY PROTOCOL", size=30, weight=ft.FontWeight.BOLD, color="cyan"),
                    u_in, p_in,
                    ft.ElevatedButton("AUTHENTICATE", on_click=login_process, width=200, bgcolor="cyan", color="black")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                alignment=ft.alignment.center, expand=True
            )
        )
        page.update()

    show_login()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
                                             
