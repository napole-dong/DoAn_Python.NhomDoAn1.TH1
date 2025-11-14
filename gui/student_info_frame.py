import tkinter as tk
from tkinter import ttk, messagebox


class StudentInfoFrame(ttk.Frame):
    """
    Khung giao diện cho phép sinh viên xem và cập nhật
    thông tin cá nhân (Địa chỉ, Email).
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.student_id = None

        # --- Biến lưu trữ (StringVars) để liên kết với các Entry ---
        # Dùng StringVar giúp giao diện tự động cập nhật
        self.ho_ten_var = tk.StringVar()
        self.ngay_sinh_var = tk.StringVar()
        self.gioi_tinh_var = tk.StringVar()
        self.dia_chi_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # --- Tiêu đề ---
        lbl_title = ttk.Label(
            self, text="THÔNG TIN CÁ NHÂN", font=("Arial", 16, "bold")
        )
        lbl_title.pack(pady=20)

        # --- Form chứa thông tin ---
        form_frame = ttk.Frame(self, padding="10")
        form_frame.pack(padx=20, fill="x", expand=True)

        # Cấu hình grid cho form
        form_frame.columnconfigure(1, weight=1)  # Cho phép cột 1 (Entry) co giãn

        # Các trường thông tin
        # Họ tên (Chỉ đọc)
        ttk.Label(form_frame, text="Họ tên:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(form_frame, textvariable=self.ho_ten_var, state="readonly").grid(
            row=0, column=1, sticky="ew", pady=5, padx=5
        )

        # Ngày sinh (Chỉ đọc)
        ttk.Label(form_frame, text="Ngày sinh:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        ttk.Entry(form_frame, textvariable=self.ngay_sinh_var, state="readonly").grid(
            row=1, column=1, sticky="ew", pady=5, padx=5
        )

        # Giới tính (Chỉ đọc)
        ttk.Label(form_frame, text="Giới tính:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        ttk.Entry(form_frame, textvariable=self.gioi_tinh_var, state="readonly").grid(
            row=2, column=1, sticky="ew", pady=5, padx=5
        )

        # Địa chỉ (CHO SỬA)
        ttk.Label(form_frame, text="Địa chỉ:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_dia_chi = ttk.Entry(form_frame, textvariable=self.dia_chi_var)
        self.entry_dia_chi.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        # Email (CHO SỬA)
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(form_frame, textvariable=self.email_var)
        self.entry_email.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

        # --- Khung chứa các nút ---
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        # Nút "Lưu thay đổi"
        btn_save = ttk.Button(button_frame, text="Lưu thay đổi", command=self.save_info)
        btn_save.pack(side="left", padx=10)

        # Nút "Quay lại"
        btn_back = ttk.Button(button_frame, text="Quay lại", command=self.go_back)
        btn_back.pack(side="left", padx=10)

    def load_data(self, student_id):
        """
        Hàm này được controller (app.py) gọi để tải dữ liệu SV.
        """
        self.student_id = student_id
        # Gọi hàm từ database.py
        info = self.controller.db.get_student_info(student_id)

        if info:
            # info[0] = HoTen, info[1] = NgaySinh, info[2] = GioiTinh
            # info[3] = DiaChi, info[4] = Email
            self.ho_ten_var.set(info[0] or "")  # or "" để tránh lỗi nếu CSDL là NULL
            self.ngay_sinh_var.set(info[1] or "")
            self.gioi_tinh_var.set(info[2] or "")
            self.dia_chi_var.set(info[3] or "")
            self.email_var.set(info[4] or "")

    def save_info(self):
        """
        Gọi khi nhấn nút "Lưu thay đổi".
        """
        # Lấy dữ liệu mới từ các ô Entry (thông qua StringVar)
        new_dia_chi = self.dia_chi_var.get()
        new_email = self.email_var.get()

        # Gọi hàm update của database.py
        success = self.controller.db.update_student_info(
            self.student_id, new_dia_chi, new_email
        )

        if success:
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
            self.go_back()  # Quay về trang chính sau khi lưu
        else:
            messagebox.showerror(
                "Thất bại", "Cập nhật thông tin thất bại.\n" "Vui lòng kiểm tra lại."
            )

    def go_back(self):
        """Quay về trang Student Main Frame"""
        self.controller.show_frame("StudentMainFrame", self.student_id)
