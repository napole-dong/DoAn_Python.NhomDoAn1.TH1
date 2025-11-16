import tkinter as tk
from tkinter import ttk


class StudentMainFrame(ttk.Frame):
    """Trang chính cho sinh viên với bố cục thẻ chức năng hiện đại."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="App.TFrame")

        self.student_id = None
        self.welcome_message = tk.StringVar(value="Chào mừng Sinh viên!")
        self.tagline_message = tk.StringVar(value="Cùng theo dõi tiến độ học tập của bạn.")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        wrapper = ttk.Frame(self, style="App.TFrame", padding=(30, 25))
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.grid_columnconfigure(0, weight=1)

        hero = ttk.Frame(wrapper, style="App.TFrame")
        hero.grid(row=0, column=0, sticky="ew")
        hero.grid_columnconfigure(1, weight=0)

        ttk.Label(hero, text="Cổng thông tin Sinh viên", style="HeroTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(hero, textvariable=self.welcome_message, style="SectionTitle.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 0)
        )
        ttk.Label(hero, textvariable=self.tagline_message, style="Muted.TLabel").grid(
            row=2, column=0, sticky="w", pady=(2, 0)
        )

        ttk.Button(
            hero,
            text="Đăng xuất",
            style="Outline.TButton",
            command=self.handle_logout,
        ).grid(row=0, column=1, rowspan=3, padx=(20, 0))

        cards_frame = ttk.Frame(wrapper, style="App.TFrame")
        cards_frame.grid(row=1, column=0, sticky="nsew", pady=(25, 0))
        for col in range(3):
            cards_frame.grid_columnconfigure(col, weight=1, uniform="student-cards")

        card_specs = [
            (
                "Thông tin cá nhân",
                "Cập nhật địa chỉ, email và các dữ liệu hồ sơ quan trọng.",
                self.go_to_info_frame,
            ),
            (
                "Thời khóa biểu",
                "Xem lịch học từng tuần, giảng viên phụ trách và phòng học.",
                self.go_to_schedule_frame,
            ),
            (
                "Bảng điểm",
                "Theo dõi điểm thành phần, tổng kết và số tín chỉ tích lũy.",
                self.go_to_grades_frame,
            ),
        ]

        for idx, (title, desc, callback) in enumerate(card_specs):
            card = ttk.Frame(cards_frame, style="Card.TFrame", padding=22)
            card.grid(row=0, column=idx, padx=10, sticky="nsew")
            ttk.Label(card, text=title, style="SectionTitle.TLabel").pack(anchor="w")
            ttk.Label(
                card,
                text=desc,
                style="CardMuted.TLabel",
                wraplength=220,
                padding=(0, 6, 0, 16),
            ).pack(anchor="w")
            ttk.Button(card, text="Truy cập", style="Primary.TButton", command=callback).pack(
                fill="x"
            )

    def set_student_info(self, student_id):
        """
        Hàm này được controller (app.py) gọi khi hiển thị frame.
        Nó nhận MaSV và cập nhật lời chào.
        """
        self.student_id = student_id

        # Gọi database để lấy tên sinh viên
        info = self.controller.db.get_student_info(self.student_id)
        if info:
            # info[0] là HoTen
            self.welcome_message.set(f"Chào mừng, {info[0]}!")
        else:
            self.welcome_message.set(f"Chào mừng, {self.student_id}!")
        self.tagline_message.set(f"Mã sinh viên: {self.student_id}")

    def go_to_info_frame(self):
        """Chuyển sang frame Sửa thông tin"""
        # Khi chuyển frame, ta truyền theo student_id
        self.controller.show_frame("StudentInfoFrame", self.student_id)

    def go_to_schedule_frame(self):
        """Chuyển sang frame Xem TKB"""
        # Khi chuyển frame, ta truyền theo student_id
        self.controller.show_frame("StudentScheduleFrame", self.student_id)

    # --- HÀM MỚI ĐƯỢC THÊM VÀO ---
    def go_to_grades_frame(self):
        """Chuyển sang frame Xem Điểm"""
        # Khi chuyển frame, ta truyền theo student_id
        self.controller.show_frame("StudentGradesFrame", self.student_id)

    # --- KẾT THÚC HÀM MỚI ---

    def handle_logout(self):
        """Xử lý đăng xuất: Quay về màn hình Login"""
        self.student_id = None  # Xóa ID sinh viên hiện tại
        self.welcome_message.set("Chào mừng Sinh viên!")  # Reset lời chào
        self.controller.show_frame("LoginFrame")
