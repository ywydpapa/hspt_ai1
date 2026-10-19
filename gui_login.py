import tkinter as tk
from tkinter import ttk
from datetime import datetime
import db


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HSPT 로그인 시스템")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(bg="#0F172A")

        self.center_window(420, 520)

        self.container = tk.Frame(self, bg="#0F172A")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_login_screen()

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_container()

        card = tk.Frame(self.container, bg="#FFFFFF", padx=30, pady=30)
        card.pack(fill="both", expand=True)

        badge = tk.Label(
            card,
            text="HSPT AI SYSTEM",
            font=("Segoe UI", 9, "bold"),
            fg="#2563EB",
            bg="#EFF6FF",
            padx=12,
            pady=4,
        )
        badge.pack(pady=(0, 10))

        title_label = tk.Label(
            card,
            text="HSPT 로그인",
            font=("Segoe UI", 18, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
        )
        title_label.pack(pady=(0, 4))

        subtitle_label = tk.Label(
            card,
            text="아이디와 비밀번호를 입력해주세요",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#FFFFFF",
        )
        subtitle_label.pack(pady=(0, 14))

        self.err_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9),
            fg="#DC2626",
            bg="#FEF2F2",
            padx=10,
            pady=6,
        )

        id_lbl = tk.Label(
            card,
            text="아이디",
            font=("Segoe UI", 9, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            anchor="w",
        )
        id_lbl.pack(fill="x", pady=(0, 4))

        self.id_entry = ttk.Entry(card, font=("Segoe UI", 11))
        self.id_entry.insert(0, "djkim")
        self.id_entry.pack(fill="x", ipady=4, pady=(0, 14))

        pw_lbl = tk.Label(
            card,
            text="비밀번호",
            font=("Segoe UI", 9, "bold"),
            fg="#334155",
            bg="#FFFFFF",
            anchor="w",
        )
        pw_lbl.pack(fill="x", pady=(0, 4))

        pw_frame = tk.Frame(card, bg="#FFFFFF")
        pw_frame.pack(fill="x", pady=(0, 18))

        self.pw_entry = ttk.Entry(pw_frame, font=("Segoe UI", 11), show="*")
        self.pw_entry.insert(0, "core2020")
        self.pw_entry.pack(side="left", fill="x", expand=True, ipady=4)

        self.show_pw = False

        def toggle_pw():
            if self.show_pw:
                self.pw_entry.config(show="*")
                self.show_pw = False
                toggle_btn.config(text="표시")
            else:
                self.pw_entry.config(show="")
                self.show_pw = True
                toggle_btn.config(text="숨김")

        toggle_btn = tk.Button(
            pw_frame,
            text="표시",
            font=("Segoe UI", 8),
            command=toggle_pw,
            relief="flat",
            bg="#F1F5F9",
            fg="#475569",
            padx=6,
        )
        toggle_btn.pack(side="right", padx=(6, 0), ipady=2)

        login_btn = tk.Button(
            card,
            text="로그인",
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.handle_login,
        )
        login_btn.pack(fill="x", ipady=8, pady=(0, 14))

        hint_lbl = tk.Label(
            card,
            text="💡 [테스트 샘플 계정]\n아이디: djkim  |  비밀번호: core2020",
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#F1F5F9",
            pady=8,
            bd=0,
        )
        hint_lbl.pack(fill="x", pady=(8, 0))

        self.id_entry.bind("<Return>", lambda e: self.handle_login())
        self.pw_entry.bind("<Return>", lambda e: self.handle_login())
        self.pw_entry.focus_set()

    def handle_login(self):
        user_id = self.id_entry.get().strip()
        user_pw = self.pw_entry.get()

        if not user_id:
            self.show_error("아이디를 입력해주세요.")
            return
        if not user_pw:
            self.show_error("비밀번호를 입력해주세요.")
            return

        try:
            user = db.authenticate_user(user_id, user_pw)
            if user:
                self.show_success_screen(user)
            else:
                self.show_error("아이디 또는 비밀번호가 올바르지 않습니다.")
        except Exception as e:
            self.show_error(f"DB 접속 에러: {str(e)}")

    def show_error(self, message):
        self.err_label.config(text=message)
        self.err_label.pack(fill="x", pady=(0, 12), before=self.id_entry)

    def show_success_screen(self, user):
        self.clear_container()

        card = tk.Frame(self.container, bg="#FFFFFF", padx=30, pady=30)
        card.pack(fill="both", expand=True)

        icon_label = tk.Label(
            card, text="🎉", font=("Segoe UI", 36), bg="#FFFFFF"
        )
        icon_label.pack(pady=(6, 4))

        title_label = tk.Label(
            card,
            text="로그인 성공!",
            font=("Segoe UI", 18, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
        )
        title_label.pack(pady=(0, 6))

        user_name = user.get("userName") or "회원"
        welcome_lbl = tk.Label(
            card,
            text=f"{user_name} 님, 환영합니다.",
            font=("Segoe UI", 11, "bold"),
            fg="#2563EB",
            bg="#FFFFFF",
        )
        welcome_lbl.pack(pady=(0, 20))

        info_frame = tk.Frame(
            card, bg="#F8FAFC", bd=1, relief="solid", padx=16, pady=12
        )
        info_frame.pack(fill="x", pady=(0, 20))

        rows = [
            ("회원 번호", str(user.get("userNo") or "-")),
            ("사용자 이름", str(user.get("userName") or "-")),
            ("아이디", str(user.get("userId") or "-")),
            ("인증 상태", "인증 완료 (MySQL)"),
            ("접속 일시", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]

        for k, v in rows:
            row_frame = tk.Frame(info_frame, bg="#F8FAFC")
            row_frame.pack(fill="x", pady=3)
            k_lbl = tk.Label(
                row_frame,
                text=k,
                font=("Segoe UI", 9),
                fg="#64748B",
                bg="#F8FAFC",
            )
            k_lbl.pack(side="left")
            v_lbl = tk.Label(
                row_frame,
                text=v,
                font=("Segoe UI", 9, "bold"),
                fg="#0F172A",
                bg="#F8FAFC",
            )
            v_lbl.pack(side="right")

        logout_btn = tk.Button(
            card,
            text="로그아웃 (로그인 화면으로)",
            font=("Segoe UI", 10, "bold"),
            bg="#F1F5F9",
            fg="#475569",
            activebackground="#E2E8F0",
            relief="flat",
            cursor="hand2",
            command=self.show_login_screen,
        )
        logout_btn.pack(fill="x", ipady=8)


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()

