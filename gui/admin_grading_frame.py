import tkinter as tk
from tkinter import ttk, messagebox


class AdminGradingFrame(ttk.Frame):
    """
    Khung giao diện cho Admin Nhập điểm cho sinh viên
    theo từng Lớp học phần.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Dữ liệu cache
        # Key: Tên hiển thị (display_name), Value: MaLHP
        self.lhp_display_to_ma = {}
        # MaLHP của lớp đang được chọn
        self.selected_ma_lhp = None

        # --- Cấu hình layout chính ---
        self.grid_rowconfigure(2, weight=1)  # Cho Treeview co giãn
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Nhập điểm Sinh viên", font=("Arial", 16, "bold")).grid(
            row=0, column=0, pady=10
        )

        # --- Khung 1: Chọn Lớp học phần ---
        select_frame = ttk.LabelFrame(self, text="1. Chọn Lớp học phần", padding="10")
        select_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        select_frame.columnconfigure(1, weight=1)

        ttk.Label(select_frame, text="Chọn LHP:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_lhp = ttk.Combobox(select_frame, state="readonly")
        self.combo_lhp.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Gán sự kiện: Khi Admin chọn 1 lớp
        self.combo_lhp.bind("<<ComboboxSelected>>", self.on_lhp_select)

        # --- Khung 2: Danh sách SV & Nhập điểm ---
        grading_frame = ttk.LabelFrame(self, text="2. Nhập điểm", padding="10")
        grading_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        grading_frame.columnconfigure(0, weight=1)
        grading_frame.rowconfigure(0, weight=1)

        # Bảng (Treeview) danh sách SV
        cols_sv = ("ma_sv", "ho_ten", "diem")
        self.tree_sv = ttk.Treeview(grading_frame, columns=cols_sv, show="headings")
        self.tree_sv.heading("ma_sv", text="Mã SV")
        self.tree_sv.heading("ho_ten", text="Họ Tên")
        self.tree_sv.heading("diem", text="Điểm Tổng Kết")
        self.tree_sv.column("ma_sv", width=100, anchor="center")
        self.tree_sv.column("ho_ten", width=250)
        self.tree_sv.column("diem", width=100, anchor="center")

        self.tree_sv.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Gán sự kiện: Khi click vào 1 SV
        self.tree_sv.bind("<<TreeviewSelect>>", self.on_student_select)

        # --- Form nhập điểm (nằm bên dưới bảng) ---
        entry_frame = ttk.Frame(grading_frame, padding="10")
        entry_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        entry_frame.columnconfigure(1, weight=1)

        ttk.Label(entry_frame, text="Mã SV:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.lbl_ma_sv = ttk.Label(entry_frame, text="...", font=("Arial", 10, "bold"))
        self.lbl_ma_sv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(entry_frame, text="Họ Tên:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.lbl_ho_ten = ttk.Label(entry_frame, text="...")
        self.lbl_ho_ten.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(entry_frame, text="Điểm (0-10):").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_diem = ttk.Entry(entry_frame)
        self.entry_diem.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_save = ttk.Button(entry_frame, text="Lưu Điểm", command=self.save_grade)
        btn_save.grid(row=3, column=1, padx=5, pady=10, sticky="e")

        # Nút quay lại
        btn_back = ttk.Button(
            self,
            text="Quay lại Admin",
            command=lambda: controller.show_frame("AdminMainFrame"),
        )
        btn_back.grid(row=3, column=0, padx=20, pady=10)

    def load_data(self):
        """Tải dữ liệu khi frame được hiển thị (chỉ tải danh sách LHP)"""
        self.load_lhp_list()
        self.clear_all()

    def clear_all(self):
        """Xóa trắng toàn bộ frame"""
        self.combo_lhp.set("")
        self.selected_ma_lhp = None
        self.clear_student_list()

    def clear_student_list(self):
        """Xóa danh sách SV và form nhập điểm"""
        for item in self.tree_sv.get_children():
            self.tree_sv.delete(item)
        self.clear_grade_form()

    def clear_grade_form(self):
        """Xóa trắng form nhập điểm"""
        self.lbl_ma_sv.config(text="...")
        self.lbl_ho_ten.config(text="...")
        self.entry_diem.delete(0, tk.END)
        if self.tree_sv.selection():
            self.tree_sv.selection_remove(self.tree_sv.selection()[0])

    def load_lhp_list(self):
        """Tải danh sách LHP cho Combobox"""
        lhp_data = self.controller.db.get_all_lophocphan_details()
        # lhp_data = [(MaLHP, TenLHP, TenMH, TenGV, HocKy, NamHoc), ...]

        self.lhp_display_to_ma.clear()
        display_list = []

        for row in lhp_data:
            ma_lhp = row[0]
            # Tạo tên hiển thị (VD: "CSDL - Nhóm 1 (Cơ sở dữ liệu) - GV. Dũng - HK1 2024-2025")
            display_name = (
                f"{row[1] or row[2]} ({row[2]}) - GV: {row[3]} - "
                f"HK{row[4]} {row[5]}"
            )
            self.lhp_display_to_ma[display_name] = ma_lhp
            display_list.append(display_name)

        self.combo_lhp["values"] = display_list

    def on_lhp_select(self, event):
        """Khi Admin chọn một LHP từ Combobox"""
        self.clear_student_list()

        display_name = self.combo_lhp.get()
        ma_lhp = self.lhp_display_to_ma.get(display_name)

        if not ma_lhp:
            return

        self.selected_ma_lhp = ma_lhp

        # Lấy danh sách SV của lớp này
        student_list = self.controller.db.get_students_for_grading(ma_lhp)
        # student_list = [(MaSV, HoTen, DiemTongKet), ...]

        for row in student_list:
            diem = row[2] if row[2] is not None else "Chưa có"
            display_row = (row[0], row[1], diem)
            self.tree_sv.insert("", "end", values=display_row, iid=row[0])  # iid=MaSV

    def on_student_select(self, event):
        """Khi Admin click vào 1 SV trong bảng"""
        selected_item_id = self.tree_sv.selection()
        if not selected_item_id:
            return

        ma_sv = selected_item_id[0]
        values = self.tree_sv.item(ma_sv, "values")
        # values = (MaSV, HoTen, Diem)

        self.lbl_ma_sv.config(text=values[0])
        self.lbl_ho_ten.config(text=values[1])

        diem_value = values[2] if values[2] != "Chưa có" else ""
        self.entry_diem.delete(0, tk.END)
        self.entry_diem.insert(0, diem_value)

    def save_grade(self):
        """Xử lý nút Lưu Điểm"""
        ma_sv = self.lbl_ma_sv.cget("text")
        diem_str = self.entry_diem.get().strip()

        if ma_sv == "..." or self.selected_ma_lhp is None:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn Lớp và Sinh viên trước.")
            return

        # Kiểm tra điểm hợp lệ
        diem_val = None
        if diem_str == "":
            diem_val = ""  # Cho phép xóa điểm (gửi chuỗi rỗng)
        else:
            try:
                diem_val = float(diem_str)
                if not (0.0 <= diem_val <= 10.0):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Điểm không hợp lệ",
                    "Điểm phải là một số từ 0.0 đến 10.0 (hoặc để trống).",
                )
                return

        # Gọi hàm update
        success = self.controller.db.update_student_grade(
            ma_sv, self.selected_ma_lhp, diem_val
        )

        if success:
            messagebox.showinfo("Thành công", f"Đã cập nhật điểm cho {ma_sv}.")
            # Tải lại danh sách SV trong bảng
            self.on_lhp_select(None)  # Gọi lại hàm on_lhp_select để refresh
            self.clear_grade_form()
