import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY DATABASE ---
USERS = {
    "ADMIN": {"pass": "159753", "level": 10},
    "TONY": {"pass": "9999", "level": 5},
    "GUEST": {"pass": "0000", "level": 1}
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. COMMAND CENTER"
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"
    
    # ใช้การตั้งค่าหน้ากระดาษแบบมาตรฐานที่สุด
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"

    user_session = {"name": "", "level": 0}
    content_area = ft.Container(expand=True, padding=20)

    def route_change(route_name):
        content_area.content = None
        lv = user_session["level"]

        if route_name == "home":
            content_area.content = ft.Column([
                ft.Text("MAIN TERMINAL", size=30, weight="bold", color="cyan"),
                ft.Text(f"ACCESS LEVEL: {lv}", color="green"),
                ft.Divider(color="#003355"),
                ft.Row([
                    ft.Container(content=ft.Text("CPU: ACTIVE"), bgcolor="#001a33", padding=20, border_radius=10, expand=True),
                    ft.Container(content=ft.Text("SAT: LOCKED"), bgcolor="#001a33", padding=20, border_radius=10, expand=True),
                ])
            ], spacing=20)
        
        elif route_name == "ai":
            chat_log = ft.Column(scroll="always", height=300)
            user_input = ft.TextField(hint_text="Type command...", expand=True)
            def send_msg(e):
                if user_input.value:
                    chat_log.controls.append(ft.Text(f"SIR: {user_input.value}"))
                    try:
                        resp = model.generate_content(user_input.value)
                        chat_log.controls.append(ft.Text(f"JARVIS: {resp.text}", color="cyan"))
                    except: chat_log.controls.append(ft.Text("AI ERROR", color="red"))
                    user_input.value = ""; page.update()

            content_area.content = ft.Column([
                ft.Text("AI INTERFACE", size=25, color="cyan"),
                ft.Container(content=chat_log, bgcolor="#000d1a", padding=15, border_radius=10, expand=True),
                ft.Row([user_input, ft.ElevatedButton("SEND", on_click=send_msg)])
            ])
        page.update()

    def build_sidebar():
        menu = [
            ft.Text("J.A.R.V.I.S.", size=25, weight="bold", color="cyan"),
            ft.Divider(color="#003355"),
            ft.TextButton("DASHBOARD", on_click=lambda _: route_change("home")),
            ft.TextButton("AI CONSOLE", on_click=lambda _: route_change("ai")),
            ft.VerticalDivider(expand=True),
            ft.ElevatedButton("LOGOUT", on_click=lambda _: show_login(), bgcolor="red", color="white")
        ]
        return ft.Container(content=ft.Column(menu, spacing=15), width=180, bgcolor="#000a14", padding=15)

    def show_login():
        page.clean()
        u_in = ft.TextField(label="IDENTITY", width=250)
        p_in = ft.TextField(label="PASSCODE", password=True, width=250)
        
        def login_process(e):
            if u_in.value in USERS and USERS[u_in.value]["pass"] == p_in.value:
                user_session["name"] = u_in.value
                user_session["level"] = USERS[u_in.value]["level"]
                page.clean()
                # สร้าง Layout แบบง่ายที่สุด
                page.add(ft.Row([build_sidebar(), content_area], expand=True))
                route_change("home")
            else:
                page.add(ft.Text("INVALID", color="red")); page.update()

        # วาง Login ไว้กลางจอแบบเบสิก
        page.add(
            ft.Column([
                ft.Text("SECURITY LOGIN", size=25, weight="bold", color="cyan"),
                u_in, p_in,
                ft.ElevatedButton("ACCESS", on_click=login_process, width=150)
            ], horizontal_alignment="center", spacing=20)
        )
        page.update()

    show_login()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
        
