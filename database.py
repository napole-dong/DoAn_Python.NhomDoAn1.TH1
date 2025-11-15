import sqlite3
import os
from tkinter import messagebox


class Database:
    """
    Lớp này chịu trách nhiệm cho tất cả các tương tác với CSDL nhưng
    sử dụng SQLite làm backend local (file-based).
    """

    def __init__(self, db_path=None):
        """
        Khởi tạo kết nối SQLite. Nếu chưa có file DB, sẽ tạo file và khởi tạo schema
        mặc định.
        """
        self.connection = None
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if db_path is None:
                db_path = os.path.join(base_dir, "quanli.db")
            # Kết nối tới SQLite (tạo file nếu chưa tồn tại)
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            # Trả về row dưới dạng tuple (các method hiện tại dùng tuple indexing)
            self.connection.row_factory = sqlite3.Row
            # Bật ràng buộc khóa ngoại
            self.connection.execute("PRAGMA foreign_keys = ON;")
            print(f"Kết nối SQLite: {db_path}")
            # Khởi tạo schema nếu cần
            self.init_db()
        except sqlite3.Error as ex:
            messagebox.showerror("Lỗi Kết Nối CSDL", f"Không thể kết nối SQLite.\nLỗi: {ex}")

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
        except sqlite3.Error as ex:
            messagebox.showerror("Lỗi Truy Vấn", f"Lỗi khi kiểm tra đăng nhập:\n{ex}")
            return None

    def init_db(self):
        """
        Tạo các bảng cơ bản nếu chưa tồn tại. Điều này là tối giản dựa trên các
        truy vấn được sử dụng trong ứng dụng.
        """
        try:
            cur = self.connection.cursor()
            # Bảng TaiKhoan
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS TaiKhoan (
                    TenDangNhap TEXT PRIMARY KEY,
                    MatKhau TEXT,
                    MaQuyen TEXT
                )
                """
            )
            # Bảng Lop
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS Lop (
                    MaLop TEXT PRIMARY KEY,
                    TenLop TEXT
                )
                """
            )
            # SinhVien
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS SinhVien (
                    MaSV TEXT PRIMARY KEY,
                    HoTen TEXT,
                    NgaySinh TEXT,
                    GioiTinh TEXT,
                    DiaChi TEXT,
                    Email TEXT,
                    MaLop TEXT,
                    TenDangNhap TEXT,
                    FOREIGN KEY (MaLop) REFERENCES Lop(MaLop),
                    FOREIGN KEY (TenDangNhap) REFERENCES TaiKhoan(TenDangNhap)
                )
                """
            )
            # Khoa
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS Khoa (
                    MaKhoa TEXT PRIMARY KEY,
                    TenKhoa TEXT
                )
                """
            )
            # GiangVien
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS GiangVien (
                    MaGV TEXT PRIMARY KEY,
                    HoTenGV TEXT,
                    Email TEXT,
                    DienThoai TEXT,
                    MaKhoa TEXT,
                    FOREIGN KEY (MaKhoa) REFERENCES Khoa(MaKhoa)
                )
                """
            )
            # MonHoc
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS MonHoc (
                    MaMH TEXT PRIMARY KEY,
                    TenMH TEXT,
                    SoTinChi INTEGER,
                    MaKhoa TEXT,
                    FOREIGN KEY (MaKhoa) REFERENCES Khoa(MaKhoa)
                )
                """
            )
            # LopHocPhan
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS LopHocPhan (
                    MaLHP INTEGER PRIMARY KEY AUTOINCREMENT,
                    TenLHP TEXT,
                    HocKy INTEGER,
                    NamHoc INTEGER,
                    MaMH TEXT,
                    MaGV TEXT,
                    FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH),
                    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
                )
                """
            )
            # LichHoc
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS LichHoc (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    MaLHP INTEGER,
                    Thu INTEGER,
                    TietBatDau INTEGER,
                    SoTiet INTEGER,
                    PhongHoc TEXT,
                    FOREIGN KEY (MaLHP) REFERENCES LopHocPhan(MaLHP)
                )
                """
            )
            # DangKyHoc
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS DangKyHoc (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    MaSV TEXT,
                    MaLHP INTEGER,
                    DiemTongKet REAL,
                    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV),
                    FOREIGN KEY (MaLHP) REFERENCES LopHocPhan(MaLHP)
                )
                """
            )
            self.connection.commit()
            # Seed a default admin account if none exists
            try:
                cur.execute("SELECT COUNT(1) FROM TaiKhoan WHERE TenDangNhap = ?", ("admin",))
                exists = cur.fetchone()[0]
                if not exists:
                    # Note: storing plaintext password (keep as-is to match original app behavior)
                    cur.execute(
                        "INSERT INTO TaiKhoan (TenDangNhap, MatKhau, MaQuyen) VALUES (?, ?, ?)",
                        ("admin", "admin123", "Admin"),
                    )
                    self.connection.commit()
            except sqlite3.Error:
                # non-fatal: ignore seeding errors here
                pass
            cur.close()
        except sqlite3.Error as ex:
            messagebox.showerror("Lỗi Khởi Tạo CSDL", f"Không thể khởi tạo DB: {ex}")

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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
            self.connection.rollback()
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa sinh viên: {ex}")
            return False
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error:
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
        except sqlite3.Error:
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
            self.connection.rollback()
            messagebox.showerror(
                "Lỗi Xóa", f"Không thể xóa Lớp Học Phần này.\n" f"Lỗi: {ex}"
            )
            return False
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
        except sqlite3.Error as ex:
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
        except sqlite3.Error as ex:
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
