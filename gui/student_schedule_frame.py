import tkinter as tk
from tkinter import ttk


class StudentScheduleFrame(ttk.Frame):
    """
    Khung giao diện hiển thị Thời Khóa Biểu của sinh viên
    dưới dạng bảng (Treeview).
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.student_id = None

        # --- Tiêu đề ---
        lbl_title = ttk.Label(self, text="THỜI KHÓA BIỂU", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=20)

        # --- Tạo Khung cho Bảng (Treeview) ---
        tree_frame = ttk.Frame(self)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Tạo Bảng (Treeview) ---
        # Định nghĩa các cột
        columns = ("mon_hoc", "lop_hp", "giang_vien", "thu", "tiet_hoc", "phong")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Định nghĩa tiêu đề cho các cột
        self.tree.heading("mon_hoc", text="Môn học")
        self.tree.heading("lop_hp", text="Lớp học phần")
        self.tree.heading("giang_vien", text="Giảng viên")
        self.tree.heading("thu", text="Thứ")
        self.tree.heading("tiet_hoc", text="Tiết học")
        self.tree.heading("phong", text="Phòng học")

        # Set độ rộng cột
        self.tree.column("mon_hoc", width=200, minwidth=150)
        self.tree.column("lop_hp", width=150, minwidth=100)
        self.tree.column("giang_vien", width=150, minwidth=100)
        self.tree.column("thu", width=60, anchor="center")
        self.tree.column("tiet_hoc", width=80, anchor="center")
        self.tree.column("phong", width=80, anchor="center")

        # Thêm thanh cuộn (Scrollbar)
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
        Hàm này được controller (app.py) gọi để tải TKB.
        """
        self.student_id = student_id

        # Xóa dữ liệu cũ trong bảng (nếu có)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Gọi hàm từ database.py để lấy TKB
        schedule_data = self.controller.db.get_student_schedule(student_id)

        # Định dạng và chèn dữ liệu vào bảng
        for row in schedule_data:
            # row[0]=TenMH, row[1]=TenLHP, row[2]=HoTenGV
            # row[3]=Thu, row[4]=TietBatDau, row[5]=SoTiet, row[6]=PhongHoc

            # Đổi số Thứ (2, 3, 4...) thành chữ
            thu_dict = {
                2: "Thứ Hai",
                3: "Thứ Ba",
                4: "Thứ Tư",
                5: "Thứ Năm",
                6: "Thứ Sáu",
                7: "Thứ Bảy",
                8: "Chủ nhật",
            }
            thu_text = thu_dict.get(
                row[3], str(row[3])
            )  # Lấy chữ, nếu không có thì trả về số

            # Gộp tiết học (vd: Tiết 1, 3 tiết -> 1-3)
            tiet_bat_dau = row[4]
            so_tiet = row[5]
            tiet_ket_thuc = tiet_bat_dau + so_tiet - 1
            tiet_text = f"{tiet_bat_dau} - {tiet_ket_thuc}"

            # Chèn dòng mới vào bảng
            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],  # Môn học
                    row[1],  # Tên LHP
                    row[2],  # Giảng viên
                    thu_text,  # Thứ
                    tiet_text,  # Tiết
                    row[6],  # Phòng
                ),
            )

    def go_back(self):
        """Quay về trang Student Main Frame"""
        self.controller.show_frame("StudentMainFrame", self.student_id)
