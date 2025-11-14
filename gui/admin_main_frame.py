import tkinter as tk
from tkinter import ttk


class AdminMainFrame(ttk.Frame):
    """
    Khung giao diện chính cho Quản trị viên (Admin).
    Nơi chứa các chức năng quản lý.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Cấu hình layout (grid) ---
        self.grid_columnconfigure(0, weight=1)

        # --- Tiêu đề ---
        lbl_title = ttk.Label(
            self, text="TRANG QUẢN TRỊ VIÊN", font=("Arial", 16, "bold")
        )
        lbl_title.grid(row=0, column=0, pady=20, padx=20)

        # --- KHUNG CHỨA CÁC NÚT CHỨC NĂNG ---
        functions_frame = ttk.Frame(self)
        functions_frame.grid(row=1, column=0, padx=50, pady=10, sticky="ew")
        functions_frame.columnconfigure(0, weight=1)

        # --- NÚT QUẢN LÝ SINH VIÊN (ĐÃ KÍCH HOẠT) ---
        btn_manage_students = ttk.Button(
            functions_frame,
            text="1. Quản lý Sinh viên",
            command=self.go_to_student_management,
        )
        btn_manage_students.grid(row=0, column=0, pady=10, sticky="ew")

        # --- NÚT QUẢN LÝ GIẢNG VIÊN (ĐÃ KÍCH HOẠT) ---
        btn_manage_teachers = ttk.Button(
            functions_frame,
            text="2. Quản lý Giảng viên",
            command=self.go_to_teacher_management,
        )
        btn_manage_teachers.grid(row=1, column=0, pady=10, sticky="ew")

        # --- NÚT QUẢN LÝ MÔN HỌC (ĐÃ KÍCH HOẠT) ---
        btn_manage_courses = ttk.Button(
            functions_frame,
            text="3. Quản lý Môn học & Lớp",
            command=self.go_to_course_management,
        )
        btn_manage_courses.grid(row=2, column=0, pady=10, sticky="ew")

        # --- NÚT NHẬP ĐIỂM (ĐÃ KÍCH HOẠT) ---
        btn_manage_grades = ttk.Button(
            functions_frame,
            text="4. Nhập điểm",
            command=self.go_to_grading_frame,  # <-- ĐÃ THAY ĐỔI
        )
        btn_manage_grades.grid(row=3, column=0, pady=10, sticky="ew")  # <-- ĐÃ THAY ĐỔI

        # --- Nút Đăng xuất ---
        btn_logout = ttk.Button(self, text="Đăng xuất", command=self.handle_logout)
        btn_logout.grid(row=2, column=0, pady=30, padx=50, sticky="ew")

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

    def handle_logout(self):
        """Xử lý đăng xuất: Quay về màn hình Login"""
        # Gọi hàm show_frame của controller (app.py)
        self.controller.show_frame("LoginFrame")
