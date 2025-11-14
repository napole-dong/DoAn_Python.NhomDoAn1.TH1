import tkinter as tk
from tkinter import ttk


class StudentGradesFrame(ttk.Frame):
    """
    Khung giao diện hiển thị Bảng điểm của sinh viên.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.student_id = None

        # --- Tiêu đề ---
        lbl_title = ttk.Label(
            self, text="BẢNG ĐIỂM CÁ NHÂN", font=("Arial", 16, "bold")
        )
        lbl_title.pack(pady=20)

        # --- Khung cho Bảng (Treeview) ---
        tree_frame = ttk.Frame(self)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Tạo Bảng (Treeview) ---
        columns = ("ma_mh", "ten_mh", "so_tin_chi", "diem_tong_ket")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Đặt tên tiêu đề
        self.tree.heading("ma_mh", text="Mã Môn Học")
        self.tree.heading("ten_mh", text="Tên Môn Học")
        self.tree.heading("so_tin_chi", text="Số Tín Chỉ")
        self.tree.heading("diem_tong_ket", text="Điểm Tổng Kết")

        # Đặt độ rộng cột
        self.tree.column("ma_mh", width=100, anchor="center")
        self.tree.column("ten_mh", width=300)
        self.tree.column("so_tin_chi", width=80, anchor="center")
        self.tree.column("diem_tong_ket", width=100, anchor="center")

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # --- Nút Quay lại ---
        btn_back = ttk.Button(self, text="Quay lại", command=self.go_back)
        btn_back.pack(pady=10)

    def load_data(self, student_id):
        """
        Tải bảng điểm khi frame được hiển thị.
        """
        self.student_id = student_id

        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu điểm từ CSDL
        grades_data = self.controller.db.get_student_grades(student_id)

        # Kiểm tra nếu chưa có điểm
        if not grades_data:
            self.tree.insert("", "end", values=("", "Chưa có dữ liệu điểm", "", ""))
            return

        # Chèn dữ liệu vào bảng
        for row in grades_data:
            # row[0]=MaMH, row[1]=TenMH, row[2]=SoTinChi, row[3]=DiemTongKet
            diem = row[3]

            # Xử lý điểm (hiển thị "Chưa có" nếu CSDL là NULL)
            diem_display = diem if diem is not None else "Chưa có"

            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],  # Mã MH
                    row[1],  # Tên MH
                    row[2],  # Số tín chỉ
                    diem_display,  # Điểm
                ),
            )

    def go_back(self):
        """Quay về trang Student Main Frame"""
        self.controller.show_frame("StudentMainFrame", self.student_id)
