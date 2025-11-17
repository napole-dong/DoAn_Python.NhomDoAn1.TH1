import tkinter as tk
from tkinter import ttk, messagebox

# Import lớp Database
from database import Database

# Import tất cả các Frame giao diện từ thư mục 'gui'
# from gui.login_frame import LoginFrame # <- Đảm bảo file này là file đã sửa
from gui.login_frame import LoginFrame  # <- Tạm thời đổi tên import để chắc chắn

from gui.admin_main_frame import AdminMainFrame
from gui.student_main_frame import StudentMainFrame
from gui.student_info_frame import StudentInfoFrame
from gui.student_schedule_frame import StudentScheduleFrame
from gui.student_grades_frame import StudentGradesFrame
from gui.admin_student_management_frame import AdminStudentManagementFrame
from gui.admin_teacher_management_frame import AdminTeacherManagementFrame
from gui.admin_course_management_frame import AdminCourseManagementFrame
from gui.admin_grading_frame import AdminGradingFrame
from gui.admin_schedule_management_frame import AdminScheduleManagementFrame
from gui.theme import configure_theme


class MainApplication(tk.Tk):
    """
    Lớp ứng dụng chính, kế thừa từ tk.Tk (cửa sổ gốc).
    Đây là "Controller" quản lý tất cả các Frame (Views).
    """

    def __init__(self):
        super().__init__()

        # --- 0. Thiết lập giao diện hiện đại ---
        configure_theme(self)

        # --- 1. Khởi tạo CSDL ---
        self.db = Database()
        # Nếu kết nối CSDL thất bại ngay từ đầu, dừng ứng dụng
        if not self.db.connection:
            messagebox.showerror(
                "Lỗi CSDL", "Không thể kết nối CSDL. Ứng dụng sẽ thoát."
            )
            self.destroy()  # Đóng cửa sổ
            return

        # --- 2. Cấu hình cửa sổ chính ---
        self.title("Hệ thống Quản lý Sinh viên")
        # Kích thước lớn để chứa form Admin
        self.geometry("1100x700")

        # --- 3. Tạo 1 container (khung) chính ---
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --- 4. Dictionary để lưu trữ các frame ---
        self.frames = {}

        # --- 5. Khởi tạo tất cả các frame (các trang) ---
        # Vòng lặp này chứa TẤT CẢ 10 frame đã tạo
        # (Đây là phần code bị thiếu trong file của bạn)
        for F in (
            LoginFrame,  # Đảm bảo đây là LoginFrame (fixed)
            AdminMainFrame,
            StudentMainFrame,
            StudentInfoFrame,
            StudentScheduleFrame,
            StudentGradesFrame,
            AdminStudentManagementFrame,
            AdminTeacherManagementFrame,
            AdminCourseManagementFrame,
            AdminGradingFrame,
            AdminScheduleManagementFrame,
        ):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # --- 6. Hiển thị frame Đăng nhập đầu tiên ---
        # Sửa tên frame nếu bạn đổi tên file import
        if "LoginFrame" in self.frames:
            self.show_frame("LoginFrame")
        elif "LoginFrameFixed" in self.frames:
            self.show_frame("LoginFrameFixed")
        else:
            self.show_frame(LoginFrame.__name__)

        # --- 7. Xử lý khi người dùng nhấn nút X (đóng cửa sổ) ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_frame(self, frame_name, *args):
        """
        Hiển thị 1 frame (dựa theo tên) lên trên cùng.
        *args cho phép truyền tham số (vd: student_id)
        """

        # --- THÊM KHỐI TRY...EXCEPT ĐỂ BẮT LỖI ---
        try:
            frame = self.frames[frame_name]
        except KeyError:
            print(
                f"LỖI: Không tìm thấy frame '{frame_name}'. "
                f"Bạn đã import và thêm nó vào vòng lặp __init__ chưa?"
            )
            messagebox.showerror(
                "Lỗi Lập Trình", f"Không tìm thấy frame '{frame_name}'"
            )
            return

        # --- Xử lý logic ĐẶC BIỆT khi chuyển frame ---
        # Đảm bảo tên frame này khớp với tên lớp
        if frame_name == "LoginFrame" or frame_name == "LoginFrameFixed":
            self.title("Đăng nhập")
            self.geometry("800x600")  # Thu nhỏ lại
            frame.clear_entries()

        elif frame_name == "StudentMainFrame":
            self.title("Cổng thông tin Sinh viên")
            self.geometry("800x600")
            student_id = args[0]
            frame.set_student_info(student_id)

        elif frame_name == "AdminMainFrame":
            self.title("Trang Quản trị")
            self.geometry("800x600")
            if hasattr(frame, "load_data"):
                frame.load_data()

        elif frame_name == "StudentInfoFrame":
            self.title("Thông tin cá nhân")
            self.geometry("800x600")
            student_id = args[0]
            frame.load_data(student_id)

        elif frame_name == "StudentScheduleFrame":
            self.title("Thời khóa biểu")
            self.geometry("900x600")  # Tăng kích thước
            student_id = args[0]
            frame.load_data(student_id)

        elif frame_name == "StudentGradesFrame":
            self.title("Bảng điểm")
            self.geometry("800x600")
            student_id = args[0]
            frame.load_data(student_id)

        # --- Các frame Admin (Phần này bị thiếu trong file của bạn) ---
        elif frame_name == "AdminStudentManagementFrame":
            self.title("Quản lý Sinh viên")
            self.geometry("1100x700")  # Kích thước lớn
            frame.load_data()  # Tải dữ liệu Lớp và SV

        elif frame_name == "AdminTeacherManagementFrame":
            self.title("Quản lý Giảng viên")
            self.geometry("1100x700")
            frame.load_data()  # Tải dữ liệu Khoa và GV

        elif frame_name == "AdminCourseManagementFrame":
            self.title("Quản lý Môn học & Lớp học phần")
            self.geometry("1100x700")
            frame.load_data()  # Tải dữ liệu cho cả 2 tab

        elif frame_name == "AdminGradingFrame":
            self.title("Nhập điểm")
            self.geometry("900x700")
            frame.load_data()  # Tải danh sách LHP

        elif frame_name == "AdminScheduleManagementFrame":
            self.title("Sắp xếp thời khóa biểu")
            self.geometry("1200x720")
            frame.load_data()

        # Đưa frame được yêu cầu lên trên cùng
        frame.tkraise()

    def login(self, username, password):
        """
        Hàm xử lý logic đăng nhập (được gọi từ LoginFrame).
        """

        # ----- THÊM CODE DEBUG Ở ĐÂY -----
        print("--- DEBUG TRONG app.py: hàm login ---")
        print(f"Controller nhận TenDangNhap: '[{username}]'")
        print(f"Controller nhận MatKhau:      '[{password}]'")
        # Thêm [] để chúng ta thấy rõ nếu có dấu cách
        # ----- HẾT CODE DEBUG -----

        ma_quyen = self.db.check_login(username, password)

        if ma_quyen:
            # Sửa logic: Bảng CSDL (ảnh) trả về MaQuyen có dấu cách
            # Ví dụ: 'SV        ' và 'Admin     '
            ma_quyen = ma_quyen.strip()  # Làm sạch MaQuyen trả về từ CSDL

        if ma_quyen == "SV":
            self.show_frame("StudentMainFrame", username)
        elif ma_quyen == "Admin":
            self.show_frame("AdminMainFrame")
        else:
            messagebox.showerror(
                "Đăng nhập thất bại", "Sai Tên đăng nhập hoặc Mật khẩu."
            )

    def on_closing(self):
        """
        Xử lý khi nhấn nút X (đóng cửa sổ).
        Đảm bảo đóng kết nối CSDL an toàn.
        """
        if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát?"):
            self.db.close()  # Đóng kết nối CSDL
            self.destroy()  # Phá hủy cửa sổ
