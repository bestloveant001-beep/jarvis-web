import flet as ft
import os
import google.generativeai as genai

# --- 🔐 SECURITY ---
USERS = {"ADMIN": {"pass": "159753", "level": 10}}
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

def main(page: ft.Page):
    # ปิดการคำนวณขนาดหน้าต่างเพื่อให้มือถือโหลดเร็วขึ้น
    page.title = "J.A.R.V.I.S."
    page.theme_mode = "dark"
    page.bgcolor = "#00050a"

    def login_process(e):
        if u_in.value == "ADMIN" and p_in.value == "159753":
            page.clean()
            show_dashboard()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("DENIED"))
            page.snack_bar.open = True
            page.update()

    # --- 📟 แดชบอร์ดแบบง่ายที่สุด ---
    def show_dashboard():
        chat_log = ft.Column(scroll="always", height=300)
        user_input = ft.TextField(hint_text="Type...", expand=True)

        def send(e):
            if user_input.value:
                chat_log.controls.append(ft.Text(f"SIR: {user_input.value}"))
                try:
                    resp = model.generate_content(user_input.value)
                    chat_log.controls.append(ft.Text(f"JARVIS: {resp.text}", color="cyan"))
                except: chat_log.controls.append(ft.Text("ERROR", color="red"))
                user_input.value = ""; page.update()

        page.add(
            ft.Column([
                ft.Text("J.A.R.V.I.S. ONLINE", size=25, weight="bold", color="cyan"),
                ft.Divider(),
                ft.Container(content=chat_log, bgcolor="#050a14", padding=10, border_radius=10),
                ft.Row([user_input, ft.ElevatedButton("SEND", on_click=send)])
            ])
        )

    # --- 🔐 หน้า LOGIN แบบเบาหวิว ---
    u_in = ft.TextField(label="USER", width=250)
    p_in = ft.TextField(label="PASS", password=True, width=250)
    
    page.add(
        ft.Column([
            ft.Container(height=50),
            ft.Text("SECURE LOGIN", size=25, weight="bold", color="cyan"),
            u_in, p_in,
            ft.ElevatedButton("ACCESS", on_click=login_process, width=200)
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
    
