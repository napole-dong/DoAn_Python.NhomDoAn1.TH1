import tkinter as tk
from tkinter import ttk


class AdminMainFrame(ttk.Frame):
    """Giao diện chính cho Quản trị viên với bảng điều khiển hiện đại."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="App.TFrame")

        self.stats_vars = {
            "students": tk.StringVar(value="--"),
            "teachers": tk.StringVar(value="--"),
            "courses": tk.StringVar(value="--"),
            "classes": tk.StringVar(value="--"),
        }

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        wrapper = ttk.Frame(self, style="App.TFrame", padding=(30, 20))
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.grid_columnconfigure(0, weight=1)

        header = ttk.Frame(wrapper, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ttk.Label(
            header,
            text="Bảng điều khiển Quản trị viên",
            style="HeroTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Theo dõi nhanh số liệu cốt lõi và truy cập các tác vụ quan trọng",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w")

        quick_actions = ttk.Frame(header, style="App.TFrame")
        quick_actions.grid(row=0, column=1, rowspan=2, sticky="e", padx=(15, 0))
        ttk.Button(
            quick_actions,
            text="Làm mới dữ liệu",
            style="Outline.TButton",
            command=self.load_data,
        ).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(
            quick_actions,
            text="Đăng xuất",
            style="Accent.TButton",
            command=self.handle_logout,
        ).grid(row=0, column=1)

        stats_frame = ttk.Frame(wrapper, style="App.TFrame")
        stats_frame.grid(row=1, column=0, sticky="ew")
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1, uniform="stat")

        stats_config = [
            ("students", "Sinh viên", "Hồ sơ đang hoạt động"),
            ("teachers", "Giảng viên", "Nhân sự đang giảng dạy"),
            ("courses", "Môn học", "Danh mục môn toàn trường"),
            ("classes", "Lớp học phần", "Lịch giảng dạy mở"),
        ]

        for idx, (key, title, subtitle) in enumerate(stats_config):
            card = ttk.Frame(stats_frame, style="Card.TFrame", padding=20)
            card.grid(row=0, column=idx, padx=8, pady=8, sticky="nsew")
            ttk.Label(card, text=title, style="CardMuted.TLabel").pack(anchor="w")
            ttk.Label(card, textvariable=self.stats_vars[key], style="StatValue.TLabel").pack(
                anchor="w", pady=(8, 4)
            )
            ttk.Label(card, text=subtitle, style="CardMuted.TLabel").pack(anchor="w")

        features_frame = ttk.Frame(wrapper, style="App.TFrame")
        features_frame.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        for col in range(2):
            features_frame.grid_columnconfigure(col, weight=1, uniform="feature")

        feature_cards = [
            (
                "Quản lý Sinh viên",
                "Thêm mới, cập nhật hồ sơ, phân lớp và cấp tài khoản.",
                self.go_to_student_management,
            ),
            (
                "Quản lý Giảng viên",
                "Theo dõi thông tin giảng viên và phân công giảng dạy.",
                self.go_to_teacher_management,
            ),
            (
                "Môn học & Lớp học phần",
                "Cập nhật danh mục môn, lịch học và sĩ số từng lớp.",
                self.go_to_course_management,
            ),
            (
                "Nhập điểm",
                "Nhập nhanh điểm thành phần và tổng kết theo từng lớp.",
                self.go_to_grading_frame,
            ),
            (
                "Sắp thời khóa biểu",
                "Quản lý lịch học, phòng học và tránh trùng lịch giảng viên.",
                self.go_to_schedule_management,
            ),
        ]

        for idx, (title, description, callback) in enumerate(feature_cards):
            row, col = divmod(idx, 2)
            card = ttk.Frame(features_frame, style="Card.TFrame", padding=20)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            ttk.Label(card, text=title, style="SectionTitle.TLabel").pack(anchor="w")
            ttk.Label(
                card,
                text=description,
                style="CardMuted.TLabel",
                wraplength=280,
                padding=(0, 6, 0, 12),
            ).pack(anchor="w")
            ttk.Button(card, text="Mở chức năng", style="Primary.TButton", command=callback).pack(
                fill="x"
            )

        # Khởi tạo dữ liệu ban đầu
        self.load_data()

    def load_data(self):
        """Làm mới dữ liệu thống kê mỗi khi hiển thị frame."""
        counts = self.controller.db.get_dashboard_counts() or {}
        for key, var in self.stats_vars.items():
            value = counts.get(key, 0)
            var.set(f"{value:,}")

    def go_to_student_management(self):
        """Hàm mới: Chuyển đến frame Quản lý Sinh viên"""
        self.controller.show_frame("AdminStudentManagementFrame")

    def go_to_teacher_management(self):
        """Hàm mới: Chuyển đến frame Quản lý Giảng viên"""
        self.controller.show_frame("AdminTeacherManagementFrame")

    def go_to_course_management(self):
        """Hàm mới: Chuyển đến frame Quản lý Môn học & LHP"""
        self.controller.show_frame("AdminCourseManagementFrame")

    def go_to_grading_frame(self):  # <-- HÀM MỚI
        """Hàm mới: Chuyển đến frame Nhập điểm"""
        self.controller.show_frame("AdminGradingFrame")

    def go_to_schedule_management(self):
        """Chuyển đến màn hình sắp xếp thời khóa biểu."""
        self.controller.show_frame("AdminScheduleManagementFrame")

    def handle_logout(self):
        """Xử lý đăng xuất: Quay về màn hình Login"""
        # Gọi hàm show_frame của controller (app.py)
        self.controller.show_frame("LoginFrame")
