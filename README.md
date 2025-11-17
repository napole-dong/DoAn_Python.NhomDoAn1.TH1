# He thong Quan ly Sinh Vien

Ung dung Tkinter ho tro quan tri vien va sinh vien quan ly thong tin hoc tap tren CSDL SQL Server.

## Chuc nang chinh
- **Dang nhap 2 vai tro**: Admin va Sinh vien, kiem tra qua bang `TaiKhoan`.
- **Sinh vien**: xem/cap nhat thong tin ca nhan, theo doi lich hoc da dang ky, xem bang diem tong hop.
- **Admin**: quan ly sinh vien, giang vien, mon hoc, lop hoc phan; nhap diem va sap xep thoi khoa bieu.
- **Giao dien hien dai**: xu ly bang `ttk.Notebook`, `Treeview`, form CRUD, va dashboard thong ke.

## Cau truc thu muc
```
DoAn_Python.NhomDoAn1.TH1/
├─ app.py                # Controller Tkinter khoi tao cac Frame
├─ database.py           # Lop Database truy van SQL Server bang pyodbc
├─ main.py               # Entry point chay ung dung
├─ gui/                  # Tap hop cac Frame (Admin/SV/Login/Theme)
├─ QuanLiSinhVien_sql.sql# Script tao CSDL va du lieu mau
└─ README.md
```

## Yeu cau moi truong
- Python 3.10 tro len (chuong trinh da kiem tra voi Windows).
- Thu vien `pyodbc` va Tkinter (mac dinh tren Windows Python).
- SQL Server Express/LocalDB + `ODBC Driver 17 for SQL Server` da cai san.

Cai thu vien Python:
```bash
pip install pyodbc
```

## Cai dat CSDL
1. Mo SQL Server Management Studio (hoac sqlcmd) ket noi toi instance (mac dinh trong ma nguon: `dyspi\SQLEXPRESS`).
2. Chay toan bo script `QuanLiSinhVien_sql.sql` de tao DB `QuanLiSinhVien`, bang va du lieu mau.
3. Neu su dung instance khac, sua chuoi ket noi trong `database.py` (thuoc tinh `conn_string`).

## Chay ung dung
```bash
cd d:/DoAn_Python.NhomDoAn1.TH1
py main.py
```
- `MainApplication` trong `app.py` se khoi tao theme, ket noi DB va hien `LoginFrame`.
- Dang nhap bang tai khoan da tao trong bang `TaiKhoan` (tu script SQL). Vi du: `TenDangNhap = admin`, `MatKhau = 123`.

## Luong su dung
- **Sinh vien**: sau khi dang nhap, dung cac nut tren `StudentMainFrame` de chuyen sang xem thong tin ca nhan, thoi khoa bieu, bang diem. Nut "Quay lai" tro ve trang chu.
- **Admin**: tu `AdminMainFrame`, truy cap cac module quan ly (Sinh vien/Giang vien/Mon hoc/LHP/Nhap diem/Sap xep TKB). Moi module tuong tac voi `database.py` de thuc hien CRUD va refresh danh sach.

## Ghi chu phat trien
- File `.gitignore` loai bo `__pycache__` va file `.pyc` khi lam viec.
- Khi thay doi cau truc CSDL, cap nhat lai `database.py` va script SQL tuong ung.
- Co the chay `py main.py` trong khi phat trien de kiem tra UI; Tkinter ho tro hot reload mot phan khi restart ung dung.

## Dong gop
1. Tao nhanh moi tu `main`.
2. Thuc hien thay doi, chay lai ung dung de kiem thu.
3. Commit + push va tao Pull Request mo ta ro thay doi, cac buoc kiem thu.
