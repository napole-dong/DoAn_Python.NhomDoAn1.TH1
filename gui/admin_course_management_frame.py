import tkinter as tk
from tkinter import ttk, messagebox


class AdminCourseManagementFrame(ttk.Frame):
    """
    Khung giao diện cho Admin quản lý Môn học VÀ Lớp học phần.
    Sử dụng Notebook (Tabs) để tách biệt 2 chức năng.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- Dữ liệu cache cho các Combobox ---
        self.khoa_ten_to_ma = {}
        self.mh_ten_to_ma = {}
        self.gv_ten_to_ma = {}

        # --- Cấu hình layout chính ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(
            self, text="Quản lý Môn học & Lớp học phần", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, pady=10)

        # --- Tạo Notebook (Tabs) ---
        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Tạo 2 frame con cho 2 tab
        self.tab_monhoc = ttk.Frame(notebook, padding="10")
        self.tab_lhp = ttk.Frame(notebook, padding="10")

        notebook.add(self.tab_monhoc, text="Quản lý Môn học")
        notebook.add(self.tab_lhp, text="Quản lý Lớp học phần")

        # Nút quay lại
        btn_back = ttk.Button(
            self,
            text="Quay lại Admin",
            command=lambda: controller.show_frame("AdminMainFrame"),
        )
        btn_back.grid(row=2, column=0, pady=10)

        # --- Xây dựng nội dung cho 2 tab ---
        self.create_monhoc_tab()
        self.create_lhp_tab()

    def load_data(self):
        """Tải dữ liệu khi frame được hiển thị"""
        # Tải dữ liệu chung
        self.load_khoa_data()
        self.load_mh_simple_data()
        self.load_gv_simple_data()

        # Tải dữ liệu riêng cho từng tab
        self.refresh_monhoc_list()
        self.refresh_lhp_list()

        self.clear_form_mh()
        self.clear_form_lhp()

    # ===================================================================
    # --- TAB 1: QUẢN LÝ MÔN HỌC ---
    # ===================================================================

    def create_monhoc_tab(self):
        """Hàm xây dựng giao diện cho tab Môn học"""
        self.tab_monhoc.grid_rowconfigure(0, weight=1)
        self.tab_monhoc.grid_columnconfigure(0, weight=1)

        # --- Khung trái (Danh sách MH) ---
        mh_left_frame = ttk.Frame(self.tab_monhoc)
        mh_left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        mh_left_frame.grid_rowconfigure(0, weight=1)
        mh_left_frame.grid_columnconfigure(0, weight=1)

        # Treeview Môn học
        cols_mh = ("ma_mh", "ten_mh", "so_tin_chi", "ten_khoa")
        self.tree_mh = ttk.Treeview(mh_left_frame, columns=cols_mh, show="headings")
        self.tree_mh.heading("ma_mh", text="Mã MH")
        self.tree_mh.heading("ten_mh", text="Tên Môn học")
        self.tree_mh.heading("so_tin_chi", text="Số TC")
        self.tree_mh.heading("ten_khoa", text="Khoa")
        self.tree_mh.column("ma_mh", width=80, anchor="center")
        self.tree_mh.column("ten_mh", width=250)
        self.tree_mh.column("so_tin_chi", width=60, anchor="center")
        self.tree_mh.column("ten_khoa", width=150)

        mh_scroll = ttk.Scrollbar(
            mh_left_frame, orient="vertical", command=self.tree_mh.yview
        )
        self.tree_mh.configure(yscrollcommand=mh_scroll.set)

        self.tree_mh.grid(row=0, column=0, sticky="nsew")
        mh_scroll.grid(row=0, column=1, sticky="ns")
        self.tree_mh.bind("<<TreeviewSelect>>", self.on_monhoc_select)

        # --- Khung phải (Form MH) ---
        mh_right_frame = ttk.LabelFrame(self.tab_monhoc, text="Thông tin Môn học")
        mh_right_frame.grid(row=0, column=1, sticky="ns", padx=(10, 0))

        ttk.Label(mh_right_frame, text="Mã MH:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_ma_mh = ttk.Entry(mh_right_frame, width=30)
        self.entry_ma_mh.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(mh_right_frame, text="Tên Môn học:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_ten_mh = ttk.Entry(mh_right_frame, width=30)
        self.entry_ten_mh.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(mh_right_frame, text="Số Tín Chỉ:").grid(
            row=2, column=0, sticky="w", pady=5, padx=5
        )
        self.spin_so_tc = ttk.Spinbox(mh_right_frame, from_=1, to=15, width=28)
        self.spin_so_tc.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(mh_right_frame, text="Khoa:").grid(
            row=3, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_khoa_mh = ttk.Combobox(mh_right_frame, width=28, state="readonly")
        self.combo_khoa_mh.grid(row=3, column=1, pady=5, padx=5)

        # Nút Môn học
        btn_add_mh = ttk.Button(
            mh_right_frame, text="Thêm Môn học", command=self.add_monhoc
        )
        btn_add_mh.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

        btn_update_mh = ttk.Button(
            mh_right_frame, text="Sửa Môn học", command=self.update_monhoc
        )
        btn_update_mh.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

        btn_delete_mh = ttk.Button(
            mh_right_frame, text="Xóa Môn học", command=self.delete_monhoc
        )
        btn_delete_mh.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

        btn_clear_mh = ttk.Button(
            mh_right_frame, text="Làm mới Form", command=self.clear_form_mh
        )
        btn_clear_mh.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

    def load_khoa_data(self):
        """Tải (MaKhoa, TenKhoa) cho combobox"""
        khoa_list = self.controller.db.get_all_khoa()
        self.khoa_ten_to_ma = {ten: ma for ma, ten in khoa_list}
        self.combo_khoa_mh["values"] = list(self.khoa_ten_to_ma.keys())

    def refresh_monhoc_list(self):
        for item in self.tree_mh.get_children():
            self.tree_mh.delete(item)
        mh_data = self.controller.db.get_all_monhoc_details()
        for row in mh_data:
            # === SỬA LỖI HIỂN THỊ (1/2) ===
            # Chuyển 'row' (kiểu pyodbc.Row) thành 'list'
            # để Treeview hiểu đúng các cột.
            self.tree_mh.insert("", "end", values=list(row), iid=row[0])  # iid=MaMH

    def on_monhoc_select(self, event):
        selected_item_id = self.tree_mh.selection()
        if not selected_item_id:
            return

        ma_mh = selected_item_id[0]
        values = self.tree_mh.item(ma_mh, "values")

        # === SỬA LỖI LOGIC NÚT "SỬA" (3/3) ===
        # Tự dọn dẹp form thủ công thay vì gọi self.clear_form_mh()
        # để tránh việc hủy lựa chọn (deselect) trên Treeview.
        self.entry_ma_mh.config(state="normal")
        self.entry_ma_mh.delete(0, tk.END)
        self.entry_ten_mh.delete(0, tk.END)
        self.spin_so_tc.set("1")
        self.combo_khoa_mh.set("")
        # === KẾT THÚC SỬA LỖI LOGIC NÚT "SỬA" ===

        self.entry_ma_mh.insert(0, values[0])
        self.entry_ma_mh.config(state="readonly")
        self.entry_ten_mh.insert(0, values[1])
        self.spin_so_tc.set(values[2])
        self.combo_khoa_mh.set(values[3])

    def clear_form_mh(self):
        self.entry_ma_mh.config(state="normal")
        self.entry_ma_mh.delete(0, tk.END)
        self.entry_ten_mh.delete(0, tk.END)
        self.spin_so_tc.set("1")
        self.combo_khoa_mh.set("")
        if self.tree_mh.selection():
            self.tree_mh.selection_remove(self.tree_mh.selection()[0])

    def add_monhoc(self):
        ma_mh = self.entry_ma_mh.get().strip()
        ten_mh = self.entry_ten_mh.get().strip()
        so_tc = self.spin_so_tc.get()
        ten_khoa = self.combo_khoa_mh.get()

        if not ma_mh or not ten_mh or not ten_khoa:
            messagebox.showwarning(
                "Thiếu thông tin", "Mã MH, Tên MH và Khoa là bắt buộc."
            )
            return

        ma_khoa = self.khoa_ten_to_ma.get(ten_khoa)
        if not ma_khoa:
            messagebox.showwarning("Lỗi", "Khoa không hợp lệ.")
            return

        if self.controller.db.check_monhoc_exists(ma_mh):
            messagebox.showerror("Lỗi Trùng Lặp", f"Mã MH '{ma_mh}' đã tồn tại.")
            return

        mh_data = (ma_mh, ten_mh, so_tc)
        success = self.controller.db.add_monhoc(mh_data, ma_khoa)
        if success:
            messagebox.showinfo("Thành công", "Thêm Môn học thành công.")
            self.refresh_monhoc_list()
            self.clear_form_mh()
            self.load_mh_simple_data()  # Cập nhật combobox ở Tab 2

    def update_monhoc(self):
        if not self.tree_mh.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Môn học để sửa.")
            return

        ma_mh = self.entry_ma_mh.get().strip()
        ten_mh = self.entry_ten_mh.get().strip()
        so_tc = self.spin_so_tc.get()
        ten_khoa = self.combo_khoa_mh.get()
        ma_khoa = self.khoa_ten_to_ma.get(ten_khoa)

        mh_data = (ma_mh, ten_mh, so_tc)
        success = self.controller.db.update_monhoc(mh_data, ma_khoa)
        if success:
            messagebox.showinfo("Thành công", "Cập nhật Môn học thành công.")
            self.refresh_monhoc_list()
            self.clear_form_mh()
            self.load_mh_simple_data()  # Cập nhật combobox ở Tab 2

    def delete_monhoc(self):
        if not self.tree_mh.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Môn học để xóa.")
            return

        ma_mh = self.tree_mh.selection()[0]
        ten_mh = self.tree_mh.item(ma_mh, "values")[1]

        if not messagebox.askyesno(
            "Xác nhận Xóa",
            f"Bạn có chắc chắn muốn xóa Môn học:\n{ma_mh} - {ten_mh}\n"
            "Nếu môn học này đã có Lớp học phần, việc xóa sẽ thất bại.",
        ):
            return

        success = self.controller.db.delete_monhoc(ma_mh)
        if success:
            messagebox.showinfo("Thành công", "Đã xóa Môn học.")
            self.refresh_monhoc_list()
            self.clear_form_mh()
            self.load_mh_simple_data()  # Cập nhật combobox ở Tab 2

    # ===================================================================
    # --- TAB 2: QUẢN LÝ LỚP HỌC PHẦN (LHP) ---
    # ===================================================================

    def create_lhp_tab(self):
        """Hàm xây dựng giao diện cho tab Lớp học phần"""
        self.tab_lhp.grid_rowconfigure(0, weight=1)
        self.tab_lhp.grid_columnconfigure(0, weight=1)

        # --- Khung trái (Danh sách LHP) ---
        lhp_left_frame = ttk.Frame(self.tab_lhp)
        lhp_left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        lhp_left_frame.grid_rowconfigure(0, weight=1)
        lhp_left_frame.grid_columnconfigure(0, weight=1)

        # Treeview LHP
        cols_lhp = ("ma_lhp", "ten_lhp", "ten_mh", "ten_gv", "hoc_ky", "nam_hoc")
        self.tree_lhp = ttk.Treeview(lhp_left_frame, columns=cols_lhp, show="headings")
        self.tree_lhp.heading("ma_lhp", text="Mã LHP")
        self.tree_lhp.heading("ten_lhp", text="Tên LHP")
        self.tree_lhp.heading("ten_mh", text="Tên Môn học")
        self.tree_lhp.heading("ten_gv", text="Giảng viên")
        self.tree_lhp.heading("hoc_ky", text="Học Kỳ")
        self.tree_lhp.heading("nam_hoc", text="Năm Học")

        self.tree_lhp.column("ma_lhp", width=60, anchor="center")
        self.tree_lhp.column("ten_lhp", width=150)
        self.tree_lhp.column("ten_mh", width=200)
        self.tree_lhp.column("ten_gv", width=150)
        self.tree_lhp.column("hoc_ky", width=60, anchor="center")
        self.tree_lhp.column("nam_hoc", width=80, anchor="center")

        lhp_scroll = ttk.Scrollbar(
            lhp_left_frame, orient="vertical", command=self.tree_lhp.yview
        )
        self.tree_lhp.configure(yscrollcommand=lhp_scroll.set)

        self.tree_lhp.grid(row=0, column=0, sticky="nsew")
        lhp_scroll.grid(row=0, column=1, sticky="ns")
        self.tree_lhp.bind("<<TreeviewSelect>>", self.on_lhp_select)

        # --- Khung phải (Form LHP) ---
        lhp_right_frame = ttk.LabelFrame(self.tab_lhp, text="Thông tin Lớp học phần")
        lhp_right_frame.grid(row=0, column=1, sticky="ns", padx=(10, 0))

        ttk.Label(lhp_right_frame, text="Tên LHP:").grid(
            row=0, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_ten_lhp = ttk.Entry(lhp_right_frame, width=30)
        self.entry_ten_lhp.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(lhp_right_frame, text="Môn học:").grid(
            row=1, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_monhoc_lhp = ttk.Combobox(
            lhp_right_frame, width=28, state="readonly"
        )
        self.combo_monhoc_lhp.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(lhp_right_frame, text="Giảng viên:").grid(
            row=2, column=0, sticky="w", pady=5, padx=5
        )
        self.combo_gv_lhp = ttk.Combobox(lhp_right_frame, width=28, state="readonly")
        self.combo_gv_lhp.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(lhp_right_frame, text="Học kỳ:").grid(
            row=3, column=0, sticky="w", pady=5, padx=5
        )
        self.spin_hoc_ky_lhp = ttk.Spinbox(lhp_right_frame, from_=1, to=3, width=28)
        self.spin_hoc_ky_lhp.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(lhp_right_frame, text="Năm học (VD: 2024-2025):").grid(
            row=4, column=0, sticky="w", pady=5, padx=5
        )
        self.entry_nam_hoc_lhp = ttk.Entry(lhp_right_frame, width=30)
        self.entry_nam_hoc_lhp.grid(row=4, column=1, pady=5, padx=5)

        # Nút LHP
        btn_add_lhp = ttk.Button(
            lhp_right_frame, text="Mở Lớp học phần", command=self.add_lhp
        )
        btn_add_lhp.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

        btn_delete_lhp = ttk.Button(
            lhp_right_frame, text="Xóa Lớp học phần", command=self.delete_lhp
        )
        btn_delete_lhp.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

        btn_clear_lhp = ttk.Button(
            lhp_right_frame, text="Làm mới Form", command=self.clear_form_lhp
        )
        btn_clear_lhp.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

    def load_mh_simple_data(self):
        """Tải (MaMH, TenMH) cho combobox"""
        mh_list = self.controller.db.get_simple_list_monhoc()
        self.mh_ten_to_ma = {ten: ma for ma, ten in mh_list}
        self.combo_monhoc_lhp["values"] = list(self.mh_ten_to_ma.keys())

    def load_gv_simple_data(self):
        """Tải (MaGV, HoTenGV) cho combobox"""
        gv_list = self.controller.db.get_simple_list_giangvien()
        self.gv_ten_to_ma = {ten: ma for ma, ten in gv_list}
        self.combo_gv_lhp["values"] = list(self.gv_ten_to_ma.keys())

    def refresh_lhp_list(self):
        for item in self.tree_lhp.get_children():
            self.tree_lhp.delete(item)
        lhp_data = self.controller.db.get_all_lophocphan_details()
        for row in lhp_data:
            # === SỬA LỖI HIỂN THỊ (2/2) ===
            # Chuyển 'row' (kiểu pyodbc.Row) thành 'list'
            self.tree_lhp.insert("", "end", values=list(row), iid=row[0])  # iid=MaLHP

    def on_lhp_select(self, event):
        """Khi click vào 1 dòng LHP, chỉ xóa form, không điền"""
        # (Việc sửa LHP thường phức tạp, ở đây ta chỉ Thêm/Xóa)
        if self.tree_lhp.selection():
            self.clear_form_lhp()

    def clear_form_lhp(self):
        self.entry_ten_lhp.delete(0, tk.END)
        self.combo_monhoc_lhp.set("")
        self.combo_gv_lhp.set("")
        self.spin_hoc_ky_lhp.set("1")
        self.entry_nam_hoc_lhp.delete(0, tk.END)
        if self.tree_lhp.selection():
            self.tree_lhp.selection_remove(self.tree_lhp.selection()[0])

    def add_lhp(self):
        ten_lhp = self.entry_ten_lhp.get().strip() or None  # Cho phép NULL
        ten_mh = self.combo_monhoc_lhp.get()
        ten_gv = self.combo_gv_lhp.get()
        hoc_ky = self.spin_hoc_ky_lhp.get()
        nam_hoc = self.entry_nam_hoc_lhp.get().strip()

        if not ten_mh or not ten_gv or not hoc_ky or not nam_hoc:
            messagebox.showwarning(
                "Thiếu thông tin", "Môn học, Giảng viên, Học kỳ và Năm học là bắt buộc."
            )
            return

        ma_mh = self.mh_ten_to_ma.get(ten_mh)
        ma_gv = self.gv_ten_to_ma.get(ten_gv)

        if not ma_mh or not ma_gv:
            messagebox.showerror("Lỗi", "Môn học hoặc Giảng viên không hợp lệ.")
            return

        lhp_data = (ten_lhp, hoc_ky, nam_hoc)
        success = self.controller.db.add_lophocphan(lhp_data, ma_mh, ma_gv)
        if success:
            messagebox.showinfo("Thành công", "Đã mở Lớp học phần mới.")
            self.refresh_lhp_list()
            self.clear_form_lhp()

    def delete_lhp(self):
        if not self.tree_lhp.selection():
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Lớp học phần để xóa.")
            return

        ma_lhp = self.tree_lhp.selection()[0]
        ten_lhp = self.tree_lhp.item(ma_lhp, "values")[1]

        if not messagebox.askyesno(
            "Xác nhận Xóa",
            f"Bạn có chắc chắn muốn xóa Lớp học phần:\n{ma_lhp} - {ten_lhp}\n\n"
            "Hành động này sẽ xóa LỊCH HỌC và ĐIỂM của sinh viên đã đăng ký lớp này.\n"
            "KHÔNG THỂ HOÀN TÁC!",
        ):
            return

        success = self.controller.db.delete_lophocphan(ma_lhp)
        if success:
            messagebox.showinfo("Thành công", "Đã xóa Lớp học phần.")
            self.refresh_lhp_list()
            self.clear_form_lhp()
