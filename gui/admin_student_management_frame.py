import tkinter as tk
from tkinter import ttk, messagebox


class AdminStudentManagementFrame(ttk.Frame):
    """
    Khung giao diện cho Admin quản lý Sinh viên (Thêm, Sửa, Xóa).
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="App.TFrame")

        # Biến để lưu trữ danh sách Lớp (MaLop, TenLop)
        self.lop_list = []
        # Dictionary để tra cứu nhanh MaLop -> TenLop và ngược lại
        self.lop_ma_to_ten = {}
        self.lop_ten_to_ma = {}

        # --- Cấu hình layout chính ---
        self.grid_rowconfigure(1, weight=1)  # Cho phép Treeview co giãn
        self.grid_columnconfigure(0, weight=1)  # Cho phép Treeview co giãn
        self.grid_columnconfigure(1, weight=0)  # Form bên phải

        # --- Khung bên trái (Hiển thị danh sách) ---
        left_frame = ttk.Frame(self, style="Card.TFrame", padding=10)
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(
            left_frame, text="Danh sách Sinh viên", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, pady=10)

        # Bảng Treeview
        columns = (
            "ma_sv",
            "ho_ten",
            "ngay_sinh",
            "gioi_tinh",
            "dia_chi",
            "email",
            "ten_lop",
        )
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings")

        # Tiêu đề cột
        self.tree.heading("ma_sv", text="Mã SV")
        self.tree.heading("ho_ten", text="Họ Tên")
        self.tree.heading("ngay_sinh", text="Ngày Sinh")
        self.tree.heading("gioi_tinh", text="Giới Tính")
        self.tree.heading("dia_chi", text="Địa Chỉ")
        self.tree.heading("email", text="Email")
        self.tree.heading("ten_lop", text="Tên Lớp")

        # Độ rộng cột
        self.tree.column("ma_sv", width=80, anchor="center")
        self.tree.column("ho_ten", width=150)
        self.tree.column("ngay_sinh", width=80, anchor="center")
        self.tree.column("gioi_tinh", width=60, anchor="center")
        self.tree.column("dia_chi", width=120)
        self.tree.column("email", width=150)
        self.tree.column("ten_lop", width=100)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(
            left_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Gán sự kiện: Khi click vào 1 dòng trên bảng
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # --- Khung bên phải (Form Thêm/Sửa) ---
        right_frame = ttk.LabelFrame(
            self, text="Thông tin chi tiết", padding="10", style="Card.TLabelframe"
        )
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Form fields
        ttk.Label(right_frame, text="Mã SV:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_ma_sv = ttk.Entry(right_frame, width=30)
        self.entry_ma_sv.grid(row=0, column=1, pady=5)

        ttk.Label(right_frame, text="Họ Tên:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_ho_ten = ttk.Entry(right_frame, width=30)
        self.entry_ho_ten.grid(row=1, column=1, pady=5)

        ttk.Label(right_frame, text="Ngày Sinh (YYYY-MM-DD):").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_ngay_sinh = ttk.Entry(right_frame, width=30)
        self.entry_ngay_sinh.grid(row=2, column=1, pady=5)

        ttk.Label(right_frame, text="Giới Tính:").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.combo_gioi_tinh = ttk.Combobox(
            right_frame, values=["Nam", "Nữ", "Khác"], width=28, state="readonly"
        )
        self.combo_gioi_tinh.grid(row=3, column=1, pady=5)

        ttk.Label(right_frame, text="Địa Chỉ:").grid(
            row=4, column=0, sticky="w", pady=5
        )
        self.entry_dia_chi = ttk.Entry(right_frame, width=30)
        self.entry_dia_chi.grid(row=4, column=1, pady=5)

        ttk.Label(right_frame, text="Email:").grid(row=5, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(right_frame, width=30)
        self.entry_email.grid(row=5, column=1, pady=5)

        ttk.Label(right_frame, text="Lớp:").grid(row=6, column=0, sticky="w", pady=5)
        self.combo_lop = ttk.Combobox(right_frame, width=28, state="readonly")
        self.combo_lop.grid(row=6, column=1, pady=5)

        # --- Khung Nút chức năng (dưới form) ---
        button_frame = ttk.Frame(self, style="App.TFrame")
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        btn_add = ttk.Button(button_frame, text="Thêm", command=self.add_student)
        btn_add.pack(fill="x", pady=5)

        btn_update = ttk.Button(button_frame, text="Sửa", command=self.update_student)
        btn_update.pack(fill="x", pady=5)

        btn_delete = ttk.Button(button_frame, text="Xóa", command=self.delete_student)
        btn_delete.pack(fill="x", pady=5)

        btn_clear = ttk.Button(
            button_frame, text="Làm mới (Clear)", command=self.clear_form
        )
        btn_clear.pack(fill="x", pady=5)

        btn_back = ttk.Button(
            button_frame,
            text="Quay lại Admin",
            command=lambda: controller.show_frame("AdminMainFrame"),
        )
        btn_back.pack(fill="x", pady=20)

    def load_data(self):
        """
        Tải hoặc tải lại toàn bộ dữ liệu khi frame được hiển thị.
        """
        # 1. Tải danh sách Lớp cho Combobox
        self.load_lop_data()

        # 2. Tải danh sách Sinh viên cho Treeview
        self.refresh_student_list()

        # 3. Xóa form
        self.clear_form()

    def load_lop_data(self):
        """Tải dữ liệu cho Combobox Lớp"""
        self.lop_list = self.controller.db.get_all_lop()  # [(MaLop, TenLop), ...]
        self.lop_ma_to_ten = {ma: ten for ma, ten in self.lop_list}
        self.lop_ten_to_ma = {ten: ma for ma, ten in self.lop_list}
        self.combo_lop["values"] = list(self.lop_ten_to_ma.keys())

    def refresh_student_list(self):
        """Tải lại dữ liệu cho bảng Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu mới
        student_data = self.controller.db.get_all_students_details()
        for row in student_data:
            # row = (MaSV, HoTen, NgaySinh, GioiTinh, DiaChi, Email, MaLop, TenLop)
            # Chỉ hiển thị TenLop, không hiển thị MaLop
            display_row = (row[0], row[1], row[2], row[3], row[4], row[5], row[7])
            self.tree.insert("", "end", values=display_row, iid=row[0])  # iid=MaSV

    def on_item_select(self, event):
        """Khi Admin click vào một dòng trong bảng"""
        selected_item_id = self.tree.selection()
        if not selected_item_id:
            return

        ma_sv = selected_item_id[0]
        # Lấy dữ liệu của dòng được chọn từ Treeview
        item_values = self.tree.item(ma_sv, "values")

        # --- SỬA LỖI ---
        # Tự dọn dẹp form thủ công thay vì gọi self.clear_form()
        # Vì self.clear_form() sẽ hủy lựa chọn (deselect) trên Treeview

        self.entry_ma_sv.config(state="normal")
        self.entry_ma_sv.delete(0, tk.END)
        self.entry_ho_ten.delete(0, tk.END)
        self.entry_ngay_sinh.delete(0, tk.END)
        self.combo_gioi_tinh.set("")
        self.entry_dia_chi.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.combo_lop.set("")

        # --- KẾT THÚC SỬA LỖI ---

        # Điền dữ liệu vào form
        self.entry_ma_sv.insert(0, item_values[0])
        self.entry_ma_sv.config(state="readonly")  # Khóa ô Mã SV

        self.entry_ho_ten.insert(0, item_values[1])
        self.entry_ngay_sinh.insert(
            0, item_values[2] or ""
        )  # Xử lý nếu NgaySinh là None
        self.combo_gioi_tinh.set(item_values[3] or "")
        self.entry_dia_chi.insert(0, item_values[4] or "")
        self.entry_email.insert(0, item_values[5] or "")
        self.combo_lop.set(item_values[6] or "")  # Set TenLop

    def clear_form(self):
        """Xóa trắng các ô trong form"""
        self.entry_ma_sv.config(state="normal")
        self.entry_ma_sv.delete(0, tk.END)
        self.entry_ho_ten.delete(0, tk.END)
        self.entry_ngay_sinh.delete(0, tk.END)
        self.combo_gioi_tinh.set("")
        self.entry_dia_chi.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.combo_lop.set("")

        # Bỏ chọn trên Treeview
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def get_data_from_form(self):
        """Lấy và kiểm tra dữ liệu từ form"""
        ma_sv = self.entry_ma_sv.get().strip()
        ho_ten = self.entry_ho_ten.get().strip()
        ngay_sinh = self.entry_ngay_sinh.get().strip() or None  # Cho phép NULL
        gioi_tinh = self.combo_gioi_tinh.get() or None
        dia_chi = self.entry_dia_chi.get().strip() or None
        email = self.entry_email.get().strip() or None
        ten_lop = self.combo_lop.get()

        if not ma_sv or not ho_ten or not ten_lop:
            messagebox.showwarning(
                "Thiếu thông tin", "Mã SV, Họ Tên và Lớp là bắt buộc."
            )
            return None, None

        ma_lop = self.lop_ten_to_ma.get(ten_lop)
        if not ma_lop:
            messagebox.showwarning("Lỗi", "Lớp không hợp lệ.")
            return None, None

        sv_data = (ma_sv, ho_ten, ngay_sinh, gioi_tinh, dia_chi, email)
        return sv_data, ma_lop

    def add_student(self):
        """Xử lý nút Thêm"""
        sv_data, ma_lop = self.get_data_from_form()
        if not sv_data:
            return

        ma_sv = sv_data[0]

        # Kiểm tra xem MaSV đã tồn tại chưa
        if self.controller.db.check_student_exists(ma_sv):
            messagebox.showerror("Lỗi Trùng Lặp", f"Mã SV '{ma_sv}' đã tồn tại.")
            return

        # Gọi hàm add_student (transaction) từ database.py
        success = self.controller.db.add_student(sv_data, ma_lop)
        if success:
            messagebox.showinfo(
                "Thành công", "Thêm sinh viên thành công.\nMật khẩu mặc định là '123'."
            )
            self.refresh_student_list()
            self.clear_form()
        # (Nếu thất bại, database.py đã hiển thị lỗi)

    def update_student(self):
        """Xử lý nút Sửa"""
        # Kiểm tra xem có chọn dòng nào không
        if not self.tree.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để sửa.")
            return

        sv_data, ma_lop = self.get_data_from_form()
        if not sv_data:
            return

        # Gọi hàm update từ database.py
        success = self.controller.db.update_student_admin(sv_data, ma_lop)
        if success:
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
            self.refresh_student_list()
            self.clear_form()

    def delete_student(self):
        """Xử lý nút Xóa"""
        if not self.tree.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để xóa.")
            return

        ma_sv = self.tree.selection()[0]
        ho_ten = self.tree.item(ma_sv, "values")[1]

        if not messagebox.askyesno(
            "Xác nhận Xóa",
            f"Bạn có chắc chắn muốn xóa sinh viên:\n\n{ma_sv} - {ho_ten}\n\n"
            "Hành động này sẽ xóa TÀI KHOẢN và toàn bộ ĐIỂM của sinh viên này.\n"
            "KHÔNG THỂ HOÀN TÁC!",
        ):
            return

        # Gọi hàm delete (transaction) từ database.py
        success = self.controller.db.delete_student(ma_sv)
        if success:
            messagebox.showinfo("Thành công", "Đã xóa sinh viên.")
            self.refresh_student_list()
            self.clear_form()
