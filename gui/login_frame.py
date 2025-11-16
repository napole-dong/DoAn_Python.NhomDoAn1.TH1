import tkinter as tk
from tkinter import ttk, messagebox


class LoginFrame(ttk.Frame):
    """Khung (Frame) giao diện cho màn hình đăng nhập."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(style="App.TFrame")

        # Biến trạng thái UI
        self.error_message = tk.StringVar(value="")
        self.remember_account = tk.BooleanVar(value=False)

        # Bố cục chính: canh giữa thẻ đăng nhập
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        outer = ttk.Frame(self, style="App.TFrame", padding=(30, 20, 30, 30))
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)

        card = ttk.Frame(outer, style="Card.TFrame", padding=30)
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=3)
        card.grid_columnconfigure(1, weight=2)

        # --- Panel giới thiệu (trái) ---
        hero_frame = ttk.Frame(card, style="Hero.TFrame")
        hero_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 25))
        hero_frame.grid_rowconfigure(3, weight=1)

        ttk.Label(
            hero_frame,
            text="Hệ thống Quản lý Sinh viên",
            style="HeroTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            hero_frame,
            text="Theo dõi tình trạng học tập, nhập điểm và quản trị chỉ với một lần đăng nhập duy nhất.",
            style="Muted.TLabel",
            wraplength=320,
            padding=(0, 10, 0, 10),
        ).grid(row=1, column=0, sticky="w")

        ttk.Label(hero_frame, text="TRUY CẬP HIỆN ĐẠI", style="Tag.TLabel").grid(
            row=2, column=0, sticky="w", pady=(0, 15)
        )

        bullet_text = (
            "• Cập nhật dữ liệu sinh viên tức thì\n"
            "• Đồng bộ điểm và thời khóa biểu\n"
            "• Hỗ trợ đăng nhập nhanh cho Admin & SV"
        )
        ttk.Label(
            hero_frame,
            text=bullet_text,
            style="Muted.TLabel",
            justify="left",
        ).grid(row=3, column=0, sticky="nw")

        # --- Panel form đăng nhập (phải) ---
        form_frame = ttk.Frame(card, style="Card.TFrame")
        form_frame.grid(row=0, column=1, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(form_frame, text="Xin chào!", style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            form_frame,
            text="Vui lòng đăng nhập để tiếp tục",
            style="CardMuted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        ttk.Separator(form_frame, orient="horizontal").grid(
            row=2, column=0, sticky="ew", pady=(0, 15)
        )

        username_container = ttk.Frame(form_frame, style="Card.TFrame")
        username_container.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        username_container.grid_columnconfigure(0, weight=1)
        ttk.Label(username_container, text="Tên đăng nhập", style="CardMuted.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.entry_username = ttk.Entry(username_container, width=35)
        self.entry_username.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        password_container = ttk.Frame(form_frame, style="Card.TFrame")
        password_container.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        password_container.grid_columnconfigure(0, weight=1)
        ttk.Label(password_container, text="Mật khẩu", style="CardMuted.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.entry_password = ttk.Entry(password_container, show="*")
        self.entry_password.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        self.entry_password.bind("<Return>", self.on_login_button_press)

        options_frame = ttk.Frame(form_frame, style="Card.TFrame")
        options_frame.grid(row=5, column=0, sticky="ew")
        ttk.Checkbutton(
            options_frame,
            text="Ghi nhớ đăng nhập",
            variable=self.remember_account,
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            options_frame,
            textvariable=self.error_message,
            style="Error.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        btn_login = ttk.Button(
            form_frame,
            text="Đăng nhập",
            style="Primary.TButton",
            command=self.handle_login,
        )
        btn_login.grid(row=6, column=0, sticky="ew", pady=(18, 6))

        ttk.Button(
            form_frame,
            text="Liên hệ hỗ trợ",
            style="Outline.TButton",
            command=lambda: messagebox.showinfo(
                "Hỗ trợ",
                "Liên hệ Phòng CNTT để được cấp/khôi phục tài khoản.",
            ),
        ).grid(row=7, column=0, sticky="ew")

        ttk.Label(
            form_frame,
            text="© Trung tâm Quản lý Đào tạo",
            style="CardMuted.TLabel",
        ).grid(row=8, column=0, sticky="w", pady=(15, 0))

        # Tự động focus vào ô tên đăng nhập
        self.after(100, self.entry_username.focus_set)

    def on_login_button_press(self, event):
        """Hàm xử lý sự kiện khi nhấn phím Enter"""
        self.handle_login()

    def handle_login(self):
        """
        Hàm được gọi khi người dùng nhấn nút 'Đăng nhập'.
        Nó sẽ lấy dữ liệu và gọi hàm 'login' từ controller (app.py).
        """

        # ----- SỬA LỖI Ở ĐÂY -----
        # Thêm .strip() để xóa các dấu cách thừa ở đầu và cuối
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        # ----- HẾT SỬA -----

        if not username or not password:
            self.error_message.set("Vui lòng nhập đầy đủ thông tin.")
            return

        # Gọi hàm login của controller (sẽ được tạo trong file app.py)
        # Controller sẽ chịu trách nhiệm gọi database.py
        self.error_message.set("")
        self.controller.login(username, password)

    def clear_entries(self):
        """
        Xóa nội dung trong các ô entry.
        Hàm này sẽ được controller gọi khi người dùng đăng xuất.
        """
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.error_message.set("")
        self.remember_account.set(False)
