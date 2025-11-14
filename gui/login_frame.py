import tkinter as tk
from tkinter import ttk, messagebox


class LoginFrame(ttk.Frame):
    """
    Khung (Frame) giao diện cho màn hình đăng nhập.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # --- Cấu hình layout (grid) ---
        # Đặt 2 hàng (0, 4) và 2 cột (0, 2) làm "vùng đệm" co giãn
        # Giúp đẩy nội dung vào giữa
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # --- Tiêu đề ---
        lbl_title = ttk.Label(
            self, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 16, "bold")
        )
        lbl_title.grid(
            row=0, column=1, pady=20, sticky="s"
        )  # sticky="s" -> bám sát đáy ô

        # --- Tên đăng nhập ---
        lbl_username = ttk.Label(self, text="Tên đăng nhập:")
        lbl_username.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="e")

        self.entry_username = ttk.Entry(self, width=30)
        self.entry_username.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ew")

        # --- Mật khẩu ---
        lbl_password = ttk.Label(self, text="Mật khẩu:")
        lbl_password.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="e")

        self.entry_password = ttk.Entry(self, show="*")  # show="*" để ẩn mật khẩu
        self.entry_password.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="ew")

        # Gán sự kiện: Nhấn phím Enter trên ô mật khẩu cũng sẽ đăng nhập
        self.entry_password.bind("<Return>", self.on_login_button_press)

        # --- Nút Đăng nhập ---
        btn_login = ttk.Button(self, text="Đăng nhập", command=self.handle_login)
        btn_login.grid(
            row=3, column=1, pady=20, sticky="ew"
        )  # sticky="ew" -> co giãn ngang

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
            messagebox.showwarning(
                "Thiếu thông tin", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu."
            )
            return

        # Gọi hàm login của controller (sẽ được tạo trong file app.py)
        # Controller sẽ chịu trách nhiệm gọi database.py
        self.controller.login(username, password)

    def clear_entries(self):
        """
        Xóa nội dung trong các ô entry.
        Hàm này sẽ được controller gọi khi người dùng đăng xuất.
        """
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
