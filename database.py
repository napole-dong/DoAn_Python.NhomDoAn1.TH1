import pyodbc
from tkinter import messagebox


class Database:
    """
    Lớp này chịu trách nhiệm cho tất cả các tương tác với CSDL SQL Server.
    """

    def __init__(self):
        """
        Khởi tạo và cố gắng kết nối CSDL ngay lập tức.
        """
        self.connection = None
        try:
            conn_string = (
                r"DRIVER={ODBC Driver 17 for SQL Server};"
                r"SERVER=dyspi\SQLEXPRESS;"
                r"DATABASE=QuanLiSinhVien;"
                r"Trusted_Connection=yes;"
            )
            self.connection = pyodbc.connect(conn_string)
            print("Kết nối CSDL (database.py) thành công!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == "IM002":
                messagebox.showerror(
                    "Lỗi Driver",
                    "Không tìm thấy 'ODBC Driver 17 for SQL Server'.\n"
                    "Hãy tải và cài đặt driver này từ Microsoft.",
                )
            else:
                messagebox.showerror(
                    "Lỗi Kết Nối CSDL", f"Không thể kết nối.\nLỗi: {ex}"
                )

    def check_login(self, username, password):
        """
        Kiểm tra thông tin đăng nhập trong bảng TaiKhoan.
        """
        if not self.connection:
            messagebox.showerror("Lỗi", "Mất kết nối CSDL.")
            return None
        try:
            cursor = self.connection.cursor()
            # Mặc định dùng mật khẩu chữ rõ (plain text)
            sql = "SELECT MaQuyen FROM TaiKhoan WHERE TenDangNhap = ? AND MatKhau = ?"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]  # Trả về MaQuyen
            else:
                return None
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi kiểm tra đăng nhập:\n{ex}")
            return None

    # ===================================================================
    # --- CÁC HÀM CHO SINH VIÊN (TỰ XEM) ---
    # ===================================================================

    def get_student_info(self, student_id):
        """
        (SV) Lấy thông tin của một sinh viên dựa trên MaSV.
        """
        if not self.connection:
            return None
        sql = "SELECT HoTen, NgaySinh, GioiTinh, DiaChi, Email FROM SinhVien WHERE MaSV = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy thông tin SV: {ex}")
            return None

    def update_student_info(self, student_id, dia_chi, email):
        """
        (SV) Cập nhật địa chỉ và email cho sinh viên.
        """
        if not self.connection:
            return False
        sql = "UPDATE SinhVien SET DiaChi = ?, Email = ? WHERE MaSV = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (dia_chi, email, student_id))
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Cập Nhật", f"Lỗi khi cập nhật thông tin: {ex}")
            return False

    def get_student_schedule(self, student_id):
        """
        (SV) Lấy thời khóa biểu chi tiết của sinh viên.
        """
        if not self.connection:
            return []
        sql = """
            SELECT 
                mh.TenMH, lhp.TenLHP, gv.HoTenGV, 
                lh.Thu, lh.TietBatDau, lh.SoTiet, lh.PhongHoc
            FROM DangKyHoc AS dkh
            JOIN LopHocPhan AS lhp ON dkh.MaLHP = lhp.MaLHP
            JOIN LichHoc AS lh ON lhp.MaLHP = lh.MaLHP
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            JOIN GiangVien AS gv ON lhp.MaGV = gv.MaGV
            WHERE dkh.MaSV = ?
            ORDER BY lh.Thu, lh.TietBatDau
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (student_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy TKB: {ex}")
            return []

    def get_student_grades(self, student_id):
        """
        (SV) Lấy bảng điểm của sinh viên.
        """
        if not self.connection:
            return []
        sql = """
            SELECT 
                mh.MaMH, mh.TenMH, mh.SoTinChi, dkh.DiemTongKet
            FROM DangKyHoc AS dkh
            JOIN LopHocPhan AS lhp ON dkh.MaLHP = lhp.MaLHP
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            WHERE dkh.MaSV = ?
            ORDER BY mh.TenMH
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (student_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy bảng điểm: {ex}")
            return []

    # ===================================================================
    # --- CÁC HÀM CHO ADMIN - QUẢN LÝ SINH VIÊN (PHẦN BỊ THIẾU) ---
    # ===================================================================

    def get_all_students_details(self):
        """
        (Admin) Lấy thông tin chi tiết của TẤT CẢ sinh viên.
        """
        if not self.connection:
            return []
        sql = """
            SELECT sv.MaSV, sv.HoTen, sv.NgaySinh, sv.GioiTinh, 
                   sv.DiaChi, sv.Email, sv.MaLop, l.TenLop
            FROM SinhVien AS sv
            JOIN Lop AS l ON sv.MaLop = l.MaLop
            ORDER BY sv.MaLop, sv.HoTen
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy danh sách SV: {ex}")
            return []

    def get_all_lop(self):
        """
        (Admin) Lấy danh sách Lớp (MaLop, TenLop) cho combobox.
        """
        if not self.connection:
            return []
        sql = "SELECT MaLop, TenLop FROM Lop ORDER BY TenLop"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy danh sách Lớp: {ex}")
            return []

    def check_student_exists(self, student_id):
        """
        (Admin) Kiểm tra xem MaSV đã tồn tại chưa.
        """
        if not self.connection:
            return None
        sql = "SELECT COUNT(1) FROM SinhVien WHERE MaSV = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (student_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except pyodbc.Error:
            return None

    def add_student(self, sv_data, lop_id):
        """
        (Admin) Thêm sinh viên mới (Transaction).
        """
        if not self.connection:
            return False
        ma_sv = sv_data[0]
        mat_khau_mac_dinh = "123"
        sql_taikhoan = (
            "INSERT INTO TaiKhoan (TenDangNhap, MatKhau, MaQuyen) VALUES (?, ?, 'SV')"
        )
        sql_sinhvien = """
            INSERT INTO SinhVien (MaSV, HoTen, NgaySinh, GioiTinh, DiaChi, Email, MaLop, TenDangNhap)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_taikhoan, (ma_sv, mat_khau_mac_dinh))
            cursor.execute(sql_sinhvien, (*sv_data, lop_id, ma_sv))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm sinh viên: {ex}")
            return False
        finally:
            cursor.close()

    def update_student_admin(self, sv_data, lop_id):
        """
        (Admin) Cập nhật thông tin sinh viên.
        """
        if not self.connection:
            return False
        sql = """
            UPDATE SinhVien 
            SET HoTen = ?, NgaySinh = ?, GioiTinh = ?, 
                DiaChi = ?, Email = ?, MaLop = ?
            WHERE MaSV = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                sql,
                (
                    sv_data[1],
                    sv_data[2],
                    sv_data[3],
                    sv_data[4],
                    sv_data[5],
                    lop_id,
                    sv_data[0],
                ),
            )
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật sinh viên: {ex}")
            return False

    def delete_student(self, student_id):
        """
        (Admin) Xóa sinh viên (Transaction).
        """
        if not self.connection:
            return False
        sql_dangky = "DELETE FROM DangKyHoc WHERE MaSV = ?"
        sql_sinhvien = "DELETE FROM SinhVien WHERE MaSV = ?"
        sql_taikhoan = "DELETE FROM TaiKhoan WHERE TenDangNhap = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_dangky, (student_id,))
            cursor.execute(sql_sinhvien, (student_id,))
            cursor.execute(sql_taikhoan, (student_id,))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa sinh viên: {ex}")
            return False
        finally:
            cursor.close()

    def get_dashboard_counts(self):
        """(Admin) Lấy số liệu tổng quan cho màn hình chính."""
        if not self.connection:
            return {}

        queries = {
            "students": "SELECT COUNT(1) FROM SinhVien",
            "teachers": "SELECT COUNT(1) FROM GiangVien",
            "courses": "SELECT COUNT(1) FROM MonHoc",
            "classes": "SELECT COUNT(1) FROM LopHocPhan",
        }

        counts = {key: 0 for key in queries}
        cursor = self.connection.cursor()
        try:
            for key, sql in queries.items():
                cursor.execute(sql)
                result = cursor.fetchone()
                counts[key] = result[0] if result else 0
            return counts
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn", f"Không thể lấy số liệu tổng quan: {ex}"
            )
            return {}
        finally:
            cursor.close()

    # ===================================================================
    # --- CÁC HÀM CHO ADMIN - QUẢN LÝ GIẢNG VIÊN ---
    # ===================================================================

    def get_all_khoa(self):
        """(Admin) Lấy danh sách Khoa (MaKhoa, TenKhoa)."""
        if not self.connection:
            return []
        sql = "SELECT MaKhoa, TenKhoa FROM Khoa ORDER BY TenKhoa"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy danh sách Khoa: {ex}")
            return []

    def get_all_teachers(self):
        """(Admin) Lấy thông tin chi tiết TẤT CẢ giảng viên."""
        if not self.connection:
            return []
        sql = """
            SELECT gv.MaGV, gv.HoTenGV, gv.Email, gv.DienThoai, gv.MaKhoa, k.TenKhoa
            FROM GiangVien AS gv
            JOIN Khoa AS k ON gv.MaKhoa = k.MaKhoa
            ORDER BY gv.MaKhoa, gv.HoTenGV
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy danh sách GV: {ex}")
            return []

    def check_teacher_exists(self, teacher_id):
        """(Admin) Kiểm tra xem MaGV đã tồn tại chưa."""
        if not self.connection:
            return None
        sql = "SELECT COUNT(1) FROM GiangVien WHERE MaGV = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (teacher_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except pyodbc.Error:
            return None

    def add_teacher(self, gv_data, khoa_id):
        """(Admin) Thêm giảng viên mới."""
        if not self.connection:
            return False
        sql = """
            INSERT INTO GiangVien (MaGV, HoTenGV, Email, DienThoai, MaKhoa)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (*gv_data, khoa_id))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm giảng viên: {ex}")
            return False
        finally:
            cursor.close()

    def update_teacher(self, gv_data, khoa_id):
        """(Admin) Cập nhật thông tin giảng viên."""
        if not self.connection:
            return False
        sql = """
            UPDATE GiangVien 
            SET HoTenGV = ?, Email = ?, DienThoai = ?, MaKhoa = ?
            WHERE MaGV = ?
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                sql, (gv_data[1], gv_data[2], gv_data[3], khoa_id, gv_data[0])
            )
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật giảng viên: {ex}")
            return False

    def delete_teacher(self, teacher_id):
        """(Admin) Xóa giảng viên."""
        if not self.connection:
            return False
        sql_check = "SELECT COUNT(1) FROM LopHocPhan WHERE MaGV = ?"
        sql_delete = "DELETE FROM GiangVien WHERE MaGV = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_check, (teacher_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror(
                    "Lỗi Xóa",
                    "Không thể xóa giảng viên này.\n"
                    "Giảng viên đang được gán cho một (hoặc nhiều) Lớp Học Phần.",
                )
                return False
            cursor.execute(sql_delete, (teacher_id,))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa giảng viên: {ex}")
            return False
        finally:
            cursor.close()

    # ===================================================================
    # --- CÁC HÀM CHO ADMIN - QUẢN LÝ MÔN HỌC & LHP ---
    # ===================================================================

    def get_all_monhoc_details(self):
        """(Admin) Lấy thông tin chi tiết TẤT CẢ môn học."""
        if not self.connection:
            return []
        sql = """
            SELECT mh.MaMH, mh.TenMH, mh.SoTinChi, k.TenKhoa
            FROM MonHoc AS mh
            JOIN Khoa AS k ON mh.MaKhoa = k.MaKhoa
            ORDER BY k.TenKhoa, mh.TenMH
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy danh sách Môn học: {ex}")
            return []

    def check_monhoc_exists(self, ma_mh):
        """(Admin) Kiểm tra MaMH đã tồn tại chưa."""
        if not self.connection:
            return None
        sql = "SELECT COUNT(1) FROM MonHoc WHERE MaMH = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (ma_mh,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except pyodbc.Error:
            return None

    def add_monhoc(self, mh_data, khoa_id):
        """(Admin) Thêm Môn học mới."""
        if not self.connection:
            return False
        sql = "INSERT INTO MonHoc (MaMH, TenMH, SoTinChi, MaKhoa) VALUES (?, ?, ?, ?)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (*mh_data, khoa_id))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm Môn học: {ex}")
            return False
        finally:
            cursor.close()

    def update_monhoc(self, mh_data, khoa_id):
        """(Admin) Cập nhật Môn học."""
        if not self.connection:
            return False
        sql = "UPDATE MonHoc SET TenMH = ?, SoTinChi = ?, MaKhoa = ? WHERE MaMH = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (mh_data[1], mh_data[2], khoa_id, mh_data[0]))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật Môn học: {ex}")
            return False
        finally:
            cursor.close()

    def delete_monhoc(self, ma_mh):
        """(Admin) Xóa Môn học (Sẽ thất bại nếu MH đã có LHP)."""
        if not self.connection:
            return False
        sql_check = "SELECT COUNT(1) FROM LopHocPhan WHERE MaMH = ?"
        sql_delete = "DELETE FROM MonHoc WHERE MaMH = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_check, (ma_mh,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror(
                    "Lỗi Xóa",
                    "Không thể xóa Môn học này.\n"
                    "Đã có Lớp Học Phần thuộc môn học này.",
                )
                return False
            cursor.execute(sql_delete, (ma_mh,))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa Môn học: {ex}")
            return False
        finally:
            cursor.close()

    def get_all_lophocphan_details(self):
        """(Admin) Lấy thông tin chi tiết TẤT CẢ Lớp Học Phần."""
        if not self.connection:
            return []
        sql = """
            SELECT lhp.MaLHP, lhp.TenLHP, mh.TenMH, gv.HoTenGV, lhp.HocKy, lhp.NamHoc
            FROM LopHocPhan AS lhp
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            JOIN GiangVien AS gv ON lhp.MaGV = gv.MaGV
            ORDER BY lhp.NamHoc DESC, lhp.HocKy, mh.TenMH
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi lấy danh sách LHP: {ex}")
            return []

    def get_simple_list_monhoc(self):
        """(Admin) Lấy (MaMH, TenMH) cho Combobox."""
        if not self.connection:
            return []
        sql = "SELECT MaMH, TenMH FROM MonHoc ORDER BY TenMH"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except pyodbc.Error:
            return []

    def get_simple_list_giangvien(self):
        """(Admin) Lấy (MaGV, HoTenGV) cho Combobox."""
        if not self.connection:
            return []
        sql = "SELECT MaGV, HoTenGV FROM GiangVien ORDER BY HoTenGV"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except pyodbc.Error:
            return []

    def add_lophocphan(self, lhp_data, ma_mh, ma_gv):
        """(Admin) Thêm Lớp Học Phần mới."""
        if not self.connection:
            return False
        sql = """
            INSERT INTO LopHocPhan (TenLHP, HocKy, NamHoc, MaMH, MaGV)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (*lhp_data, ma_mh, ma_gv))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm LHP: {ex}")
            return False
        finally:
            cursor.close()

    def delete_lophocphan(self, ma_lhp):
        """(Admin) Xóa Lớp Học Phần (Transaction)."""
        if not self.connection:
            return False
        sql_lichhoc = "DELETE FROM LichHoc WHERE MaLHP = ?"
        sql_dangky = "DELETE FROM DangKyHoc WHERE MaLHP = ?"
        sql_lhp = "DELETE FROM LopHocPhan WHERE MaLHP = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_lichhoc, (ma_lhp,))
            cursor.execute(sql_dangky, (ma_lhp,))
            cursor.execute(sql_lhp, (ma_lhp,))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror(
                "Lỗi Xóa", f"Không thể xóa Lớp Học Phần này.\n" f"Lỗi: {ex}"
            )
            return False
        finally:
            cursor.close()

    # ===================================================================
    # --- CÁC HÀM CHO ADMIN - SẮP XẾP THỜI KHÓA BIỂU ---
    # ===================================================================

    def get_students_for_schedule_assignment(self):
        """(Admin) Lấy danh sách SV để cấp thời khóa biểu."""
        if not self.connection:
            return []
        sql = """
            SELECT sv.MaSV, sv.HoTen, sv.MaLop, l.TenLop
            FROM SinhVien AS sv
            JOIN Lop AS l ON sv.MaLop = l.MaLop
            ORDER BY l.TenLop, sv.HoTen
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = ["MaSV", "HoTen", "MaLop", "TenLop"]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn",
                f"Không thể lấy danh sách sinh viên cho chức năng cấp thời khóa biểu: {ex}",
            )
            return []
        finally:
            cursor.close()

    def get_student_enrollments(self, ma_sv):
        """(Admin) Lấy danh sách LHP mà SV đã được cấp."""
        if not self.connection:
            return []
        sql = """
            SELECT dkh.MaLHP, mh.TenMH, lhp.TenLHP, lhp.HocKy, lhp.NamHoc
            FROM DangKyHoc AS dkh
            JOIN LopHocPhan AS lhp ON dkh.MaLHP = lhp.MaLHP
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            WHERE dkh.MaSV = ?
            ORDER BY lhp.NamHoc DESC, lhp.HocKy, mh.TenMH
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_sv,))
            rows = cursor.fetchall()
            columns = ["MaLHP", "TenMH", "TenLHP", "HocKy", "NamHoc"]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn",
                f"Không thể lấy danh sách lớp học phần của sinh viên {ma_sv}: {ex}",
            )
            return []
        finally:
            cursor.close()

    def assign_student_to_lhp(self, ma_sv, ma_lhp):
        """(Admin) Gán một LHP vào thời khóa biểu của SV."""
        if not self.connection:
            return False, "Mất kết nối CSDL."

        conflict_message = self._check_student_assignment_conflicts(ma_sv, ma_lhp)
        if conflict_message:
            return False, conflict_message

        sql = "INSERT INTO DangKyHoc (MaSV, MaLHP) VALUES (?, ?)"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_sv, ma_lhp))
            self.connection.commit()
            return True, "Đã cấp thời khóa biểu cho sinh viên."
        except pyodbc.IntegrityError as ex:
            self.connection.rollback()
            err_text = str(ex)
            if "PRIMARY KEY" in err_text:
                return False, "Sinh viên đã học lớp học phần này."
            return False, f"Không thể cấp thời khóa biểu: {ex}"
        except pyodbc.Error as ex:
            self.connection.rollback()
            return False, f"Không thể cấp thời khóa biểu: {ex}"
        finally:
            cursor.close()

    def remove_student_from_lhp(self, ma_sv, ma_lhp):
        """(Admin) Gỡ một LHP khỏi thời khóa biểu SV."""
        if not self.connection:
            return False, "Mất kết nối CSDL."

        sql = "DELETE FROM DangKyHoc WHERE MaSV = ? AND MaLHP = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_sv, ma_lhp))
            if cursor.rowcount == 0:
                return False, "Không tìm thấy bản ghi phù hợp để gỡ."
            self.connection.commit()
            return True, "Đã gỡ lớp học phần khỏi thời khóa biểu sinh viên."
        except pyodbc.Error as ex:
            self.connection.rollback()
            return False, f"Không thể gỡ lớp học phần: {ex}"
        finally:
            cursor.close()

    def get_lophocphan_for_schedule(self):
        """(Admin) Lấy danh sách LHP kèm thông tin phục vụ sắp lịch."""
        if not self.connection:
            return []
        sql = """
            SELECT 
                lhp.MaLHP, lhp.TenLHP, mh.TenMH, gv.HoTenGV, 
                lhp.HocKy, lhp.NamHoc, lhp.MaGV, lhp.MaMH
            FROM LopHocPhan AS lhp
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            JOIN GiangVien AS gv ON lhp.MaGV = gv.MaGV
            ORDER BY lhp.NamHoc DESC, lhp.HocKy, mh.TenMH
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [
                "MaLHP",
                "TenLHP",
                "TenMH",
                "HoTenGV",
                "HocKy",
                "NamHoc",
                "MaGV",
                "MaMH",
            ]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn",
                f"Không thể lấy danh sách Lớp học phần cho chức năng sắp lịch: {ex}",
            )
            return []
        finally:
            cursor.close()

    def _check_student_assignment_conflicts(self, ma_sv, ma_lhp):
        """Kiểm tra trùng lịch giữa LHP mới và lịch hiện tại của SV."""
        if not self.connection:
            return "Mất kết nối CSDL."

        sql = """
            SELECT COUNT(1)
            FROM DangKyHoc AS dk
            JOIN LichHoc AS lh_existing ON dk.MaLHP = lh_existing.MaLHP
            JOIN LichHoc AS lh_new ON lh_new.MaLHP = ?
            WHERE dk.MaSV = ?
              AND lh_existing.Thu = lh_new.Thu
              AND NOT ((lh_existing.TietBatDau + lh_existing.SoTiet) <= lh_new.TietBatDau
                       OR (lh_new.TietBatDau + lh_new.SoTiet) <= lh_existing.TietBatDau)
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_lhp, ma_sv))
            if cursor.fetchone()[0] > 0:
                return "Lớp học phần này trùng lịch với môn khác của sinh viên."
            return None
        except pyodbc.Error as ex:
            return f"Lỗi kiểm tra trùng lịch sinh viên: {ex}"
        finally:
            cursor.close()

    def get_schedule_for_lhp(self, ma_lhp):
        """Lấy lịch học của một LHP."""
        if not self.connection:
            return []
        sql = """
            SELECT MaLich, Thu, TietBatDau, SoTiet, PhongHoc
            FROM LichHoc
            WHERE MaLHP = ?
            ORDER BY Thu, TietBatDau
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_lhp,))
            rows = cursor.fetchall()
            columns = ["MaLich", "Thu", "TietBatDau", "SoTiet", "PhongHoc"]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn", f"Không thể lấy lịch học của lớp {ma_lhp}: {ex}"
            )
            return []
        finally:
            cursor.close()

    def create_schedule_entry(self, ma_lhp, thu, tiet_bat_dau, so_tiet, phong_hoc):
        """Thêm lịch học mới sau khi kiểm tra trùng lịch."""
        if not self.connection:
            return False, "Mất kết nối CSDL."

        conflict_message = self._check_schedule_conflicts(
            ma_lhp, thu, tiet_bat_dau, so_tiet, phong_hoc
        )
        if conflict_message:
            return False, conflict_message

        sql = """
            INSERT INTO LichHoc (MaLHP, Thu, TietBatDau, SoTiet, PhongHoc)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_lhp, thu, tiet_bat_dau, so_tiet, phong_hoc))
            self.connection.commit()
            return True, "Đã thêm lịch học thành công."
        except pyodbc.Error as ex:
            self.connection.rollback()
            return False, f"Không thể thêm lịch học: {ex}"
        finally:
            cursor.close()

    def delete_schedule_entry(self, ma_lich):
        """Xóa một lịch học cụ thể."""
        if not self.connection:
            return False
        sql = "DELETE FROM LichHoc WHERE MaLich = ?"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_lich,))
            if cursor.rowcount == 0:
                return False
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa lịch học: {ex}")
            return False
        finally:
            cursor.close()

    def get_timetable_for_class(self, ma_lop):
        """Lấy thời khóa biểu tổng hợp của một Lớp sinh viên."""
        if not self.connection:
            return []
        sql = """
            SELECT DISTINCT
                lh.MaLich,
                lh.Thu,
                lh.TietBatDau,
                lh.SoTiet,
                lh.PhongHoc,
                mh.TenMH,
                lhp.TenLHP,
                lhp.MaLHP,
                gv.HoTenGV
            FROM SinhVien AS sv
            JOIN DangKyHoc AS dk ON sv.MaSV = dk.MaSV
            JOIN LopHocPhan AS lhp ON dk.MaLHP = lhp.MaLHP
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            JOIN GiangVien AS gv ON lhp.MaGV = gv.MaGV
            JOIN LichHoc AS lh ON lh.MaLHP = lhp.MaLHP
            WHERE sv.MaLop = ?
            ORDER BY lh.Thu, lh.TietBatDau
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_lop,))
            rows = cursor.fetchall()
            columns = [
                "MaLich",
                "Thu",
                "TietBatDau",
                "SoTiet",
                "PhongHoc",
                "TenMH",
                "TenLHP",
                "MaLHP",
                "HoTenGV",
            ]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn",
                f"Không thể lấy thời khóa biểu cho lớp {ma_lop}: {ex}",
            )
            return []
        finally:
            cursor.close()

    def get_timetable_for_teacher(self, ma_gv):
        """Lấy thời khóa biểu của một giảng viên."""
        if not self.connection:
            return []
        sql = """
            SELECT
                lh.MaLich,
                lh.Thu,
                lh.TietBatDau,
                lh.SoTiet,
                lh.PhongHoc,
                mh.TenMH,
                lhp.TenLHP,
                lhp.MaLHP,
                gv.HoTenGV
            FROM LopHocPhan AS lhp
            JOIN MonHoc AS mh ON lhp.MaMH = mh.MaMH
            JOIN GiangVien AS gv ON lhp.MaGV = gv.MaGV
            JOIN LichHoc AS lh ON lh.MaLHP = lhp.MaLHP
            WHERE lhp.MaGV = ?
            ORDER BY lh.Thu, lh.TietBatDau
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (ma_gv,))
            rows = cursor.fetchall()
            columns = [
                "MaLich",
                "Thu",
                "TietBatDau",
                "SoTiet",
                "PhongHoc",
                "TenMH",
                "TenLHP",
                "MaLHP",
                "HoTenGV",
            ]
            return [dict(zip(columns, row)) for row in rows]
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn",
                f"Không thể lấy thời khóa biểu cho giảng viên {ma_gv}: {ex}",
            )
            return []
        finally:
            cursor.close()

    def _check_schedule_conflicts(self, ma_lhp, thu, tiet_bat_dau, so_tiet, phong_hoc):
        """Kiểm tra trùng lịch cho giảng viên, phòng học và sinh viên."""
        if not self.connection:
            return "Mất kết nối CSDL."

        new_end = tiet_bat_dau + so_tiet
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT MaGV FROM LopHocPhan WHERE MaLHP = ?",
                (ma_lhp,),
            )
            row = cursor.fetchone()
            if not row:
                return "Không tìm thấy Lớp học phần được chọn."
            ma_gv = row[0]

            teacher_sql = """
                SELECT COUNT(1)
                FROM LichHoc AS lh
                JOIN LopHocPhan AS lhp ON lh.MaLHP = lhp.MaLHP
                WHERE lhp.MaGV = ?
                  AND lh.Thu = ?
                  AND NOT ((lh.TietBatDau + lh.SoTiet) <= ? OR ? <= lh.TietBatDau)
            """
            cursor.execute(teacher_sql, (ma_gv, thu, tiet_bat_dau, new_end))
            if cursor.fetchone()[0] > 0:
                return "Giảng viên đã có lịch dạy trùng thời gian này."

            room_sql = """
                SELECT COUNT(1)
                FROM LichHoc
                WHERE Thu = ? AND PhongHoc = ?
                  AND NOT ((TietBatDau + SoTiet) <= ? OR ? <= TietBatDau)
            """
            cursor.execute(room_sql, (thu, phong_hoc, tiet_bat_dau, new_end))
            if cursor.fetchone()[0] > 0:
                return "Phòng học đang được sử dụng ở khung giờ này."

            student_sql = """
                SELECT COUNT(1)
                FROM DangKyHoc AS dk_cur
                JOIN DangKyHoc AS dk_other ON dk_cur.MaSV = dk_other.MaSV
                JOIN LichHoc AS lh ON dk_other.MaLHP = lh.MaLHP
                WHERE dk_cur.MaLHP = ?
                  AND dk_other.MaLHP <> dk_cur.MaLHP
                  AND lh.Thu = ?
                  AND NOT ((lh.TietBatDau + lh.SoTiet) <= ? OR ? <= lh.TietBatDau)
            """
            cursor.execute(student_sql, (ma_lhp, thu, tiet_bat_dau, new_end))
            if cursor.fetchone()[0] > 0:
                return "Sinh viên của lớp đang học môn khác trong khung giờ này."

            return None
        except pyodbc.Error as ex:
            return f"Lỗi kiểm tra trùng lịch: {ex}"
        finally:
            cursor.close()

    # ===================================================================
    # --- CÁC HÀM CHO ADMIN - QUẢN LÝ ĐIỂM ---
    # ===================================================================

    def get_students_for_grading(self, ma_lhp):
        """
        (Admin) Lấy danh sách SV (MaSV, HoTen, DiemTongKet)
        từ một Lớp học phần cụ thể để chấm điểm.
        """
        if not self.connection:
            return []
        sql = """
            SELECT sv.MaSV, sv.HoTen, dkh.DiemTongKet
            FROM DangKyHoc AS dkh
            JOIN SinhVien AS sv ON dkh.MaSV = sv.MaSV
            WHERE dkh.MaLHP = ?
            ORDER BY sv.HoTen
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (ma_lhp,))
            return cursor.fetchall()
        except pyodbc.Error as ex:
            messagebox.showerror(
                "Lỗi Truy Vấn", f"Lỗi khi lấy danh sách SV của lớp: {ex}"
            )
            return []

    def update_student_grade(self, ma_sv, ma_lhp, diem):
        """
        (Admin) Cập nhật DiemTongKet cho 1 SV trong 1 LHP.
        """
        if not self.connection:
            return False
        sql = "UPDATE DangKyHoc SET DiemTongKet = ? WHERE MaSV = ? AND MaLHP = ?"
        diem_to_save = diem if diem != "" else None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (diem_to_save, ma_sv, ma_lhp))
            self.connection.commit()
            return True
        except pyodbc.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật điểm: {ex}")
            return False
        finally:
            cursor.close()

    def close(self):
        """
        Đóng kết nối CSDL khi ứng dụng tắt.
        """
        if self.connection:
            self.connection.close()
            print("Đã đóng kết nối CSDL.")
