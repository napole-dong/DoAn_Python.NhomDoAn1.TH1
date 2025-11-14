import tkinter as tk
from tkinter import ttk, messagebox


class AdminTeacherManagementFrame(ttk.Frame):
    """
    Khung giao diện cho Admin quản lý Giảng viên (Thêm, Sửa, Xóa).
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Biến để lưu trữ danh sách Khoa (MaKhoa, TenKhoa)
        self.khoa_list = []
        # Dictionary để tra cứu nhanh MaKhoa <-> TenKhoa
        self.khoa_ma_to_ten = {}
        self.khoa_ten_to_ma = {}

        # --- Cấu hình layout chính ---
        self.grid_rowconfigure(1, weight=1)  # Cho Treeview co giãn
        self.grid_columnconfigure(0, weight=1)  # Cho Treeview co giãn
        self.grid_columnconfigure(1, weight=0)  # Form bên phải

        # --- Khung bên trái (Hiển thị danh sách) ---
        left_frame = ttk.Frame(self, padding="10")
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(
            left_frame, text="Danh sách Giảng viên", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, pady=10)

        # Bảng Treeview
        columns = ("ma_gv", "ho_ten_gv", "email", "dien_thoai", "ten_khoa")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings")

        # Tiêu đề cột
        self.tree.heading("ma_gv", text="Mã GV")
        self.tree.heading("ho_ten_gv", text="Họ Tên")
        self.tree.heading("email", text="Email")
        self.tree.heading("dien_thoai", text="Điện thoại")
        self.tree.heading("ten_khoa", text="Tên Khoa")

        # Độ rộng cột
        self.tree.column("ma_gv", width=80, anchor="center")
        self.tree.column("ho_ten_gv", width=150)
        self.tree.column("email", width=150)
        self.tree.column("dien_thoai", width=100)
        self.tree.column("ten_khoa", width=120)

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
        right_frame = ttk.LabelFrame(self, text="Thông tin chi tiết", padding="10")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Form fields
        ttk.Label(right_frame, text="Mã GV:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_ma_gv = ttk.Entry(right_frame, width=30)
        self.entry_ma_gv.grid(row=0, column=1, pady=5)

        ttk.Label(right_frame, text="Họ Tên:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_ho_ten_gv = ttk.Entry(right_frame, width=30)
        self.entry_ho_ten_gv.grid(row=1, column=1, pady=5)

        ttk.Label(right_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(right_frame, width=30)
        self.entry_email.grid(row=2, column=1, pady=5)

        ttk.Label(right_frame, text="Điện thoại:").grid(
            row=3, column=0, sticky="w", pady=5
        )
        self.entry_dien_thoai = ttk.Entry(right_frame, width=30)
        self.entry_dien_thoai.grid(row=3, column=1, pady=5)

        ttk.Label(right_frame, text="Khoa:").grid(row=4, column=0, sticky="w", pady=5)
        self.combo_khoa = ttk.Combobox(right_frame, width=28, state="readonly")
        self.combo_khoa.grid(row=4, column=1, pady=5)

        # --- Khung Nút chức năng (dưới form) ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        btn_add = ttk.Button(button_frame, text="Thêm", command=self.add_teacher)
        btn_add.pack(fill="x", pady=5)

        btn_update = ttk.Button(button_frame, text="Sửa", command=self.update_teacher)
        btn_update.pack(fill="x", pady=5)

        btn_delete = ttk.Button(button_frame, text="Xóa", command=self.delete_teacher)
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
        # 1. Tải danh sách Khoa cho Combobox
        self.load_khoa_data()

        # 2. Tải danh sách Giảng viên cho Treeview
        self.refresh_teacher_list()

        # 3. Xóa form
        self.clear_form()

    def load_khoa_data(self):
        """Tải dữ liệu cho Combobox Khoa"""
        self.khoa_list = self.controller.db.get_all_khoa()  # [(MaKhoa, TenKhoa), ...]
        self.khoa_ma_to_ten = {ma: ten for ma, ten in self.khoa_list}
        self.khoa_ten_to_ma = {ten: ma for ma, ten in self.khoa_list}
        self.combo_khoa["values"] = list(self.khoa_ten_to_ma.keys())

    def refresh_teacher_list(self):
        """Tải lại dữ liệu cho bảng Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu mới
        teacher_data = self.controller.db.get_all_teachers()
        for row in teacher_data:
            # row = (MaGV, HoTenGV, Email, DienThoai, MaKhoa, TenKhoa)
            display_row = (row[0], row[1], row[2], row[3], row[5])  # Bỏ MaKhoa
            self.tree.insert("", "end", values=display_row, iid=row[0])  # iid=MaGV

    def on_item_select(self, event):
        """Khi Admin click vào một dòng trong bảng"""
        selected_item_id = self.tree.selection()
        if not selected_item_id:
            return

        ma_gv = selected_item_id[0]
        item_values = self.tree.item(ma_gv, "values")

        # --- SỬA LỖI ---
        # Tự dọn dẹp form thủ công thay vì gọi self.clear_form()
        # để tránh việc hủy lựa chọn (deselect) trên Treeview.

        self.entry_ma_gv.config(state="normal")
        self.entry_ma_gv.delete(0, tk.END)
        self.entry_ho_ten_gv.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_dien_thoai.delete(0, tk.END)
        self.combo_khoa.set("")

        # --- KẾT THÚC SỬA LỖI ---

        # Điền dữ liệu vào form
        self.entry_ma_gv.insert(0, item_values[0])
        self.entry_ma_gv.config(state="readonly")  # Khóa ô Mã GV

        self.entry_ho_ten_gv.insert(0, item_values[1])
        self.entry_email.insert(0, item_values[2] or "")
        self.entry_dien_thoai.insert(0, item_values[3] or "")
        self.combo_khoa.set(item_values[4] or "")  # Set TenKhoa

    def clear_form(self):
        """Xóa trắng các ô trong form"""
        self.entry_ma_gv.config(state="normal")
        self.entry_ma_gv.delete(0, tk.END)
        self.entry_ho_ten_gv.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_dien_thoai.delete(0, tk.END)
        self.combo_khoa.set("")

        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def get_data_from_form(self):
        """Lấy và kiểm tra dữ liệu từ form"""
        ma_gv = self.entry_ma_gv.get().strip()
        ho_ten = self.entry_ho_ten_gv.get().strip()
        email = self.entry_email.get().strip() or None
        dien_thoai = self.entry_dien_thoai.get().strip() or None
        ten_khoa = self.combo_khoa.get()

        if not ma_gv or not ho_ten or not ten_khoa:
            messagebox.showwarning(
                "Thiếu thông tin", "Mã GV, Họ Tên và Khoa là bắt buộc."
            )
            return None, None

        ma_khoa = self.khoa_ten_to_ma.get(ten_khoa)
        if not ma_khoa:
            messagebox.showwarning("Lỗi", "Khoa không hợp lệ.")
            return None, None

        gv_data = (ma_gv, ho_ten, email, dien_thoai)
        return gv_data, ma_khoa

    def add_teacher(self):
        """Xử lý nút Thêm"""
        gv_data, ma_khoa = self.get_data_from_form()
        if not gv_data:
            return

        ma_gv = gv_data[0]

        if self.controller.db.check_teacher_exists(ma_gv):
            messagebox.showerror("Lỗi Trùng Lặp", f"Mã GV '{ma_gv}' đã tồn tại.")
            return

        success = self.controller.db.add_teacher(gv_data, ma_khoa)
        if success:
            messagebox.showinfo("Thành công", "Thêm giảng viên thành công.")
            self.refresh_teacher_list()
            self.clear_form()

    def update_teacher(self):
        """Xử lý nút Sửa"""
        if not self.tree.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một giảng viên để sửa.")
            return

        gv_data, ma_khoa = self.get_data_from_form()
        if not gv_data:
            return

        success = self.controller.db.update_teacher(gv_data, ma_khoa)
        if success:
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công.")
            self.refresh_teacher_list()
            self.clear_form()

    def delete_teacher(self):
        """Xử lý nút Xóa"""
        if not self.tree.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một giảng viên để xóa.")
            return

        ma_gv = self.tree.selection()[0]
        ho_ten = self.tree.item(ma_gv, "values")[1]

        if not messagebox.askyesno(
            "Xác nhận Xóa",
            f"Bạn có chắc chắn muốn xóa giảng viên:\n\n{ma_gv} - {ho_ten}\n\n"
            "Nếu giảng viên này đang phụ trách lớp học phần, việc xóa sẽ thất bại.",
        ):
            return

        success = self.controller.db.delete_teacher(ma_gv)
        if success:
            messagebox.showinfo("Thành công", "Đã xóa giảng viên.")
            self.refresh_teacher_list()
            self.clear_form()
