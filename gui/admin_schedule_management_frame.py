import tkinter as tk
from tkinter import ttk, messagebox


class AdminScheduleManagementFrame(ttk.Frame):
    """Màn hình quản trị dùng để sắp thời khóa biểu cho các lớp học phần."""

    def __init__(self, parent, controller):
        super().__init__(parent, style="App.TFrame")
        self.controller = controller

        self.selected_lhp_id = None
        self.lhp_cache = {}
        self.class_label_to_id = {}
        self.teacher_label_to_id = {}
        self.sidebar_buttons = {}

        self.var_ma_lhp = tk.StringVar()
        self.var_ten_lhp = tk.StringVar()
        self.var_ten_mh = tk.StringVar()
        self.var_ten_gv = tk.StringVar()
        self.timetable_context_var = tk.StringVar(value="Chưa có dữ liệu được hiển thị.")

        self._build_layout()

    # ------------------------------------------------------------------
    # UI BUILDERS
    # ------------------------------------------------------------------
    def _build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()

        content = ttk.Frame(self, style="App.TFrame", padding=(20, 15))
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        header = ttk.Frame(content, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Sắp xếp thời khóa biểu",
            style="HeroTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Quản lý lịch học chi tiết cho từng lớp học phần",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w")

        self.main_notebook = ttk.Notebook(content)
        self.main_notebook.grid(row=1, column=0, sticky="nsew")

        self.schedule_tab = ttk.Frame(self.main_notebook, style="App.TFrame", padding=10)
        self.timetable_tab = ttk.Frame(self.main_notebook, style="App.TFrame", padding=10)

        self.main_notebook.add(self.schedule_tab, text="Sắp lịch học")
        self.main_notebook.add(self.timetable_tab, text="Xem thời khóa biểu")

        self._build_schedule_tab()
        self._build_timetable_tab()

    def _build_sidebar(self):
        sidebar_bg = "#111827"
        sidebar = tk.Frame(self, bg=sidebar_bg, width=220)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        ttk.Label(
            sidebar,
            text="Điều hướng",
            style="SidebarHeading.TLabel",
            anchor="w",
        ).pack(fill="x", padx=18, pady=(20, 10))

        nav_items = [
            ("Danh sách lớp học phần", self.focus_lhp_list),
            ("Sắp lịch học", self.focus_schedule_form),
            ("Xem TKB theo lớp", self.open_timetable_for_class),
            ("Xem TKB theo giảng viên", self.open_timetable_for_teacher),
        ]

        for text, command in nav_items:
            btn = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=command)
            btn.pack(fill="x", padx=18, pady=6)
            self.sidebar_buttons[text] = btn

        ttk.Button(
            sidebar,
            text="Quay lại Trang Admin",
            style="Accent.TButton",
            command=lambda: self.controller.show_frame("AdminMainFrame"),
        ).pack(fill="x", padx=18, pady=(30, 10))

    def _build_schedule_tab(self):
        self.schedule_tab.grid_rowconfigure(1, weight=1)
        self.schedule_tab.grid_columnconfigure(0, weight=1)

        intro = ttk.Label(
            self.schedule_tab,
            text="1. Chọn lớp học phần → 2. Cài đặt lịch → 3. Theo dõi lịch đã tạo",
            style="Muted.TLabel",
        )
        intro.grid(row=0, column=0, sticky="w", pady=(0, 8), padx=5)

        body = ttk.Frame(self.schedule_tab, style="App.TFrame")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Panel B: Danh sách LHP
        classes_card = ttk.Frame(body, style="Card.TFrame", padding=15)
        classes_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        classes_card.grid_rowconfigure(1, weight=1)

        ttk.Label(classes_card, text="Danh sách Lớp học phần", style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )

        columns = ("MaLHP", "TenLHP", "TenMH", "HoTenGV", "HocKy", "NamHoc")
        self.lhp_tree = ttk.Treeview(
            classes_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        for col, heading, width in [
            ("MaLHP", "Mã LHP", 70),
            ("TenLHP", "Tên LHP", 180),
            ("TenMH", "Môn học", 160),
            ("HoTenGV", "Giảng viên", 150),
            ("HocKy", "Học kỳ", 70),
            ("NamHoc", "Năm học", 90),
        ]:
            self.lhp_tree.heading(col, text=heading)
            self.lhp_tree.column(col, width=width, anchor="w")
        self.lhp_tree.column("MaLHP", anchor="center")
        self.lhp_tree.column("HocKy", anchor="center")
        self.lhp_tree.column("NamHoc", anchor="center")

        lhp_scroll = ttk.Scrollbar(classes_card, orient="vertical", command=self.lhp_tree.yview)
        self.lhp_tree.configure(yscrollcommand=lhp_scroll.set)
        self.lhp_tree.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        lhp_scroll.grid(row=1, column=1, sticky="ns", pady=(10, 0))
        self.lhp_tree.bind("<<TreeviewSelect>>", self.on_lhp_select)

        # Panel C: Form sắp lịch
        form_card = ttk.Frame(body, style="Card.TFrame", padding=15)
        form_card.grid(row=0, column=1, sticky="nsew")
        form_card.grid_columnconfigure(0, weight=1)
        form_card.grid_columnconfigure(1, weight=1)

        ttk.Label(form_card, text="Thông tin lớp học phần", style="SectionTitle.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        ttk.Label(form_card, text="Mã LHP:").grid(row=1, column=0, sticky="w", pady=(10, 4))
        ttk.Entry(form_card, textvariable=self.var_ma_lhp, state="readonly").grid(
            row=1, column=1, sticky="ew", pady=(10, 4)
        )

        ttk.Label(form_card, text="Tên LHP:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(form_card, textvariable=self.var_ten_lhp, state="readonly").grid(
            row=2, column=1, sticky="ew", pady=4
        )

        ttk.Label(form_card, text="Môn học:").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(form_card, textvariable=self.var_ten_mh, state="readonly").grid(
            row=3, column=1, sticky="ew", pady=4
        )

        ttk.Label(form_card, text="Giảng viên:").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(form_card, textvariable=self.var_ten_gv, state="readonly").grid(
            row=4, column=1, sticky="ew", pady=4
        )

        ttk.Separator(form_card, orient="horizontal").grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=12
        )

        ttk.Label(form_card, text="Thứ (2-7):").grid(row=6, column=0, sticky="w", pady=4)
        self.combo_thu = ttk.Combobox(
            form_card,
            state="readonly",
            values=[str(i) for i in range(2, 8)],
        )
        self.combo_thu.grid(row=6, column=1, sticky="ew", pady=4)

        ttk.Label(form_card, text="Tiết bắt đầu (1-10):").grid(row=7, column=0, sticky="w", pady=4)
        self.combo_tiet = ttk.Combobox(
            form_card,
            state="readonly",
            values=[str(i) for i in range(1, 11)],
        )
        self.combo_tiet.grid(row=7, column=1, sticky="ew", pady=4)

        ttk.Label(form_card, text="Số tiết:").grid(row=8, column=0, sticky="w", pady=4)
        self.spin_so_tiet = ttk.Spinbox(form_card, from_=1, to=10)
        self.spin_so_tiet.grid(row=8, column=1, sticky="ew", pady=4)
        self.spin_so_tiet.set("1")

        ttk.Label(form_card, text="Phòng học:").grid(row=9, column=0, sticky="w", pady=4)
        self.entry_phong = ttk.Entry(form_card)
        self.entry_phong.grid(row=9, column=1, sticky="ew", pady=4)

        btn_frame = ttk.Frame(form_card, style="Card.TFrame")
        btn_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 5))
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(
            btn_frame,
            text="Thêm lịch học",
            style="Primary.TButton",
            command=self.add_schedule_entry,
        ).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(
            btn_frame,
            text="Xóa lịch học",
            style="Accent.TButton",
            command=self.delete_schedule_entry,
        ).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(
            btn_frame,
            text="Làm mới",
            style="Outline.TButton",
            command=self.reset_form,
        ).grid(row=0, column=2, sticky="ew", padx=4)

        ttk.Label(form_card, text="Lịch học đã lên", style="SectionTitle.TLabel").grid(
            row=11, column=0, columnspan=2, sticky="w", pady=(15, 6)
        )

        schedule_cols = ("MaLich", "Thu", "TietBatDau", "SoTiet", "PhongHoc")
        self.schedule_tree = ttk.Treeview(
            form_card,
            columns=schedule_cols,
            show="headings",
            height=8,
        )
        for col, heading, width in [
            ("MaLich", "Mã lịch", 70),
            ("Thu", "Thứ", 60),
            ("TietBatDau", "Tiết bắt đầu", 100),
            ("SoTiet", "Số tiết", 80),
            ("PhongHoc", "Phòng học", 100),
        ]:
            self.schedule_tree.heading(col, text=heading)
            anchor = "center" if col in {"MaLich", "Thu", "TietBatDau", "SoTiet"} else "w"
            self.schedule_tree.column(col, width=width, anchor=anchor)

        form_card.grid_columnconfigure(2, weight=0)
        schedule_scroll = ttk.Scrollbar(
            form_card, orient="vertical", command=self.schedule_tree.yview
        )
        self.schedule_tree.configure(yscrollcommand=schedule_scroll.set)
        self.schedule_tree.grid(row=12, column=0, columnspan=2, sticky="nsew")
        schedule_scroll.grid(row=12, column=2, sticky="ns")

        form_card.grid_rowconfigure(12, weight=1)

    def _build_timetable_tab(self):
        self.timetable_tab.grid_rowconfigure(1, weight=1)
        self.timetable_tab.grid_columnconfigure(0, weight=1)

        filter_card = ttk.Frame(self.timetable_tab, style="Card.TFrame", padding=15)
        filter_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filter_card.grid_columnconfigure(1, weight=1)
        filter_card.grid_columnconfigure(3, weight=1)

        ttk.Label(filter_card, text="Bộ lọc thời khóa biểu", style="SectionTitle.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w"
        )

        ttk.Label(filter_card, text="Chọn lớp:").grid(row=1, column=0, sticky="w", pady=(12, 4))
        self.combo_lop = ttk.Combobox(filter_card, state="readonly", width=35)
        self.combo_lop.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=(12, 4))

        ttk.Label(filter_card, text="Chọn giảng viên:").grid(row=1, column=2, sticky="w", pady=(12, 4))
        self.combo_gv = ttk.Combobox(filter_card, state="readonly", width=35)
        self.combo_gv.grid(row=1, column=3, sticky="ew", pady=(12, 4))

        ttk.Button(
            filter_card,
            text="Hiển thị",
            style="Primary.TButton",
            command=self.show_timetable,
        ).grid(row=2, column=3, sticky="e", pady=(10, 0))

        ttk.Label(
            self.timetable_tab,
            textvariable=self.timetable_context_var,
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, 6), padx=5)

        grid_card = ttk.Frame(self.timetable_tab, style="Card.TFrame", padding=15)
        grid_card.grid(row=2, column=0, sticky="nsew")
        grid_card.grid_rowconfigure(0, weight=1)
        grid_card.grid_columnconfigure(0, weight=1)

        columns = ("Tiet", "Thu2", "Thu3", "Thu4", "Thu5", "Thu6", "Thu7")
        self.timetable_tree = ttk.Treeview(
            grid_card,
            columns=columns,
            show="headings",
            height=10,
        )
        headings = [
            ("Tiet", "Tiết"),
            ("Thu2", "Thứ 2"),
            ("Thu3", "Thứ 3"),
            ("Thu4", "Thứ 4"),
            ("Thu5", "Thứ 5"),
            ("Thu6", "Thứ 6"),
            ("Thu7", "Thứ 7"),
        ]
        for col, heading in headings:
            self.timetable_tree.heading(col, text=heading)
            anchor = "center" if col == "Tiet" else "w"
            width = 70 if col == "Tiet" else 180
            self.timetable_tree.column(col, width=width, anchor=anchor)

        timetable_scroll = ttk.Scrollbar(
            grid_card, orient="vertical", command=self.timetable_tree.yview
        )
        self.timetable_tree.configure(yscrollcommand=timetable_scroll.set)
        self.timetable_tree.grid(row=0, column=0, sticky="nsew")
        timetable_scroll.grid(row=0, column=1, sticky="ns")

    # ------------------------------------------------------------------
    # DATA LOADING
    # ------------------------------------------------------------------
    def load_data(self):
        self.load_lhp_data()
        self.load_filter_sources()
        self.selected_lhp_id = None
        self.var_ma_lhp.set("")
        self.var_ten_lhp.set("")
        self.var_ten_mh.set("")
        self.var_ten_gv.set("")
        self.reset_form()
        self.refresh_schedule_tree()
        self.clear_timetable_grid("Chưa có dữ liệu được hiển thị.")

    def load_lhp_data(self):
        dataset = self.controller.db.get_lophocphan_for_schedule()
        self.lhp_cache = {int(row["MaLHP"]): row for row in dataset}

        for item in self.lhp_tree.get_children():
            self.lhp_tree.delete(item)

        for row in dataset:
            values = (
                row["MaLHP"],
                row["TenLHP"],
                row["TenMH"],
                row["HoTenGV"],
                row["HocKy"],
                row["NamHoc"],
            )
            self.lhp_tree.insert("", "end", iid=str(row["MaLHP"]), values=values)

        if self.lhp_tree.selection():
            self.lhp_tree.selection_remove(self.lhp_tree.selection()[0])

    def load_filter_sources(self):
        lop_data = self.controller.db.get_all_lop()
        teacher_data = self.controller.db.get_simple_list_giangvien()

        class_options = ["-- Không chọn --"]
        self.class_label_to_id = {class_options[0]: None}
        for lop in lop_data:
            label = f"{lop[0].strip()} - {lop[1]}"
            class_options.append(label)
            self.class_label_to_id[label] = lop[0].strip()
        self.combo_lop["values"] = class_options
        self.combo_lop.set(class_options[0])

        teacher_options = ["-- Không chọn --"]
        self.teacher_label_to_id = {teacher_options[0]: None}
        for gv in teacher_data:
            label = f"{gv[0].strip()} - {gv[1]}"
            teacher_options.append(label)
            self.teacher_label_to_id[label] = gv[0].strip()
        self.combo_gv["values"] = teacher_options
        self.combo_gv.set(teacher_options[0])

    # ------------------------------------------------------------------
    # EVENT HANDLERS
    # ------------------------------------------------------------------
    def on_lhp_select(self, _event=None):
        selected = self.lhp_tree.selection()
        if not selected:
            return
        ma_lhp = int(selected[0])
        info = self.lhp_cache.get(ma_lhp)
        if not info:
            return

        self.selected_lhp_id = ma_lhp
        self.var_ma_lhp.set(info["MaLHP"])
        self.var_ten_lhp.set(info["TenLHP"] or "")
        self.var_ten_mh.set(info["TenMH"] or "")
        self.var_ten_gv.set(info["HoTenGV"] or "")

        self.refresh_schedule_tree()

    def refresh_schedule_tree(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        if not self.selected_lhp_id:
            return

        dataset = self.controller.db.get_schedule_for_lhp(self.selected_lhp_id)
        for row in dataset:
            values = (
                row["MaLich"],
                row["Thu"],
                row["TietBatDau"],
                row["SoTiet"],
                row["PhongHoc"],
            )
            self.schedule_tree.insert("", "end", iid=str(row["MaLich"]), values=values)

    def add_schedule_entry(self):
        if not self.selected_lhp_id:
            messagebox.showwarning("Thiếu lựa chọn", "Hãy chọn một lớp học phần trước.")
            return

        thu_value = self.combo_thu.get().strip()
        tiet_value = self.combo_tiet.get().strip()
        phong = self.entry_phong.get().strip()
        so_tiet_str = self.spin_so_tiet.get().strip()

        if not thu_value or not tiet_value or not phong:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ Thứ, Tiết bắt đầu và Phòng học.")
            return

        try:
            thu = int(thu_value)
            tiet_bat_dau = int(tiet_value)
            so_tiet = max(1, int(so_tiet_str))
        except ValueError:
            messagebox.showerror("Sai định dạng", "Thứ, Tiết và Số tiết phải là số hợp lệ.")
            return

        success, message = self.controller.db.create_schedule_entry(
            self.selected_lhp_id,
            thu,
            tiet_bat_dau,
            so_tiet,
            phong,
        )

        if success:
            messagebox.showinfo("Thành công", message)
            self.refresh_schedule_tree()
        else:
            messagebox.showerror("Không thể thêm", message)

    def delete_schedule_entry(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một lịch học để xóa.")
            return

        ma_lich = int(self.schedule_tree.item(selected[0], "values")[0])
        if not messagebox.askyesno("Xác nhận", "Xóa lịch học đã chọn?"):
            return

        if self.controller.db.delete_schedule_entry(ma_lich):
            messagebox.showinfo("Đã xóa", "Đã xóa lịch học khỏi hệ thống.")
            self.schedule_tree.delete(selected[0])
        else:
            messagebox.showerror("Thất bại", "Không thể xóa lịch học. Hãy thử lại.")

    def reset_form(self):
        self.combo_thu.set("")
        self.combo_tiet.set("")
        self.spin_so_tiet.set("1")
        self.entry_phong.delete(0, tk.END)
        # Không xóa thông tin lớp để người dùng tiếp tục thao tác

    # Sidebar button helpers
    def focus_lhp_list(self):
        self.main_notebook.select(self.schedule_tab)
        self.lhp_tree.focus_set()

    def focus_schedule_form(self):
        self.main_notebook.select(self.schedule_tab)
        self.entry_phong.focus_set()

    def open_timetable_for_class(self):
        self.main_notebook.select(self.timetable_tab)
        self.combo_lop.focus_set()

    def open_timetable_for_teacher(self):
        self.main_notebook.select(self.timetable_tab)
        self.combo_gv.focus_set()

    # ------------------------------------------------------------------
    # TIMETABLE VIEW
    # ------------------------------------------------------------------
    def show_timetable(self):
        class_label = self.combo_lop.get()
        teacher_label = self.combo_gv.get()
        ma_lop = self.class_label_to_id.get(class_label)
        ma_gv = self.teacher_label_to_id.get(teacher_label)

        if not ma_lop and not ma_gv:
            messagebox.showwarning(
                "Thiếu lựa chọn",
                "Vui lòng chọn ít nhất một Lớp hoặc một Giảng viên.",
            )
            return

        entries = []
        context_parts = []

        if ma_lop:
            entries = self.controller.db.get_timetable_for_class(ma_lop)
            context_parts.append(f"Lớp {class_label}")

        if ma_gv:
            teacher_entries = self.controller.db.get_timetable_for_teacher(ma_gv)
            if entries:
                lhp_ids = {item["MaLHP"] for item in entries}
                entries = [item for item in teacher_entries if item["MaLHP"] in lhp_ids]
            else:
                entries = teacher_entries
            context_parts.append(f"Giảng viên {teacher_label}")

        if not entries:
            context = ", ".join(context_parts) or "Bộ lọc hiện tại"
            self.clear_timetable_grid(f"{context}: không có dữ liệu phù hợp.")
            return

        context = ", ".join(context_parts)
        self.render_timetable_grid(entries, f"Đang hiển thị cho: {context}")

    def clear_timetable_grid(self, message=""):
        for item in self.timetable_tree.get_children():
            self.timetable_tree.delete(item)
        for period in range(1, 11):
            values = [f"Tiết {period}"] + ["" for _ in range(6)]
            self.timetable_tree.insert("", "end", values=values)
        if message:
            self.timetable_context_var.set(message)

    def render_timetable_grid(self, entries, message):
        grid = {
            period: {day: "" for day in range(2, 8)} for period in range(1, 11)
        }
        for item in entries:
            thu = item["Thu"]
            period = item["TietBatDau"]
            end_period = item["TietBatDau"] + item["SoTiet"] - 1
            description = (
                f"{item['TenMH']} ({item['TenLHP']})\n"
                f"{item['PhongHoc']} | Tiết {period}-{end_period}"
            )
            if 2 <= thu <= 7:
                for offset in range(item["SoTiet"]):
                    slot = period + offset
                    if 1 <= slot <= 10:
                        grid[slot][thu] = description

        for item in self.timetable_tree.get_children():
            self.timetable_tree.delete(item)

        for period in range(1, 11):
            row_values = [f"Tiết {period}"] + [grid[period].get(day, "") for day in range(2, 8)]
            self.timetable_tree.insert("", "end", values=row_values)

        self.timetable_context_var.set(message)