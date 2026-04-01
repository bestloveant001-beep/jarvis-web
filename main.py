import flet as ft
import os

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. RECOVERY"
    page.bgcolor = "#00050a"
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def on_login(e):
        if u.value == "ADMIN" and p.value == "159753":
            page.clean()
            page.add(
                ft.Text("ACCESS GRANTED", size=30, color="cyan", weight="bold"),
                ft.Text("SYSTEM ONLINE / DASHBOARD READY", color="white"),
                ft.ElevatedButton("LOGOUT", on_click=lambda _: main(page))
            )
        else:
            page.add(ft.Text("DENIED", color="red"))
            page.update()

    u = ft.TextField(label="USER", width=250, border_color="cyan")
    p = ft.TextField(label="PASS", password=True, width=250, border_color="cyan")
    
    page.clean()
    page.add(
        ft.Icon("shield_lock", size=50, color="cyan"),
        ft.Text("J.A.R.V.I.S. RECOVERY", size=20, color="cyan"),
        u, p,
        ft.ElevatedButton("ENTER", on_click=on_login, bgcolor="cyan", color="black")
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view="web_browser", port=port)
