import tkinter as tk
from tkinter import ttk


class StudentMainFrame(ttk.Frame):
    """
    Khung giao diện chính cho Sinh viên.
    Hiển thị các nút chức năng chính.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Biến này sẽ lưu MaSV của sinh viên đang đăng nhập
        self.student_id = None

        # Biến (StringVar) để tự động cập nhật lời chào
        self.welcome_message = tk.StringVar(value="Chào mừng Sinh viên!")

        # --- Cấu hình layout (grid) ---
        self.grid_columnconfigure(0, weight=1)  # Cho cột 0 co giãn

        # --- Tiêu đề ---
        lbl_title = ttk.Label(
            self, text="CỔNG THÔNG TIN SINH VIÊN", font=("Arial", 16, "bold")
        )
        lbl_title.grid(row=0, column=0, pady=20, padx=20)

        # --- Lời chào ---
        lbl_welcome = ttk.Label(
            self, textvariable=self.welcome_message, font=("Arial", 12, "italic")
        )
        lbl_welcome.grid(row=1, column=0, pady=(0, 20), padx=20)

        # --- Các nút chức năng ---
        # Nút "Cập nhật thông tin"
        btn_info = ttk.Button(
            self, text="Cập nhật thông tin cá nhân", command=self.go_to_info_frame
        )
        btn_info.grid(row=2, column=0, pady=10, padx=50, sticky="ew")

        # Nút "Xem Thời Khóa Biểu"
        btn_schedule = ttk.Button(
            self, text="Xem Thời Khóa Biểu", command=self.go_to_schedule_frame
        )
        btn_schedule.grid(row=3, column=0, pady=10, padx=50, sticky="ew")

        # --- SỬA ĐỔI Ở ĐÂY ---
        # Nút "Xem Điểm" (Kích hoạt)
        btn_grades = ttk.Button(
            self,
            text="Xem Điểm",  # Đổi tên text
            command=self.go_to_grades_frame,  # Thêm command
            # state="disabled" # Xóa bỏ dòng này
        )
        btn_grades.grid(row=4, column=0, pady=10, padx=50, sticky="ew")
        # --- KẾT THÚC SỬA ĐỔI ---

        # --- Nút Đăng xuất ---
        btn_logout = ttk.Button(self, text="Đăng xuất", command=self.handle_logout)
        btn_logout.grid(row=5, column=0, pady=30, padx=50, sticky="ew")

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
