import tkinter as tk
from datetime import datetime
from tkinter import ttk


DAY_NAME_MAP = {
    2: "Thứ 2",
    3: "Thứ 3",
    4: "Thứ 4",
    5: "Thứ 5",
    6: "Thứ 6",
    7: "Thứ 7",
    8: "Chủ nhật",
}


class StudentScheduleFrame(ttk.Frame):
    """Giao diện thời khóa biểu với bộ lọc và chế độ xem linh hoạt."""

    def __init__(self, parent, controller):
        super().__init__(parent, style="App.TFrame")
        self.controller = controller
        self.student_id = None
        self.schedule_data = []

        self.search_var = tk.StringVar()
        self.filter_day_var = tk.StringVar(value="Tất cả các ngày")
        self.student_meta_var = tk.StringVar(value="Chưa tải dữ liệu thời khóa biểu.")
        self.summary_var = tk.StringVar(value="")
        self.week_context_var = tk.StringVar(value="")
        self.empty_state_var = tk.StringVar(value="")

        self.search_var.trace_add("write", lambda *_: self.populate_list_view())
        self.filter_day_var.trace_add("write", lambda *_: self.populate_list_view())

        self._build_layout()

    # ------------------------------------------------------------------
    # UI BUILDERS
    # ------------------------------------------------------------------
    def _build_layout(self):
        header = ttk.Frame(self, style="App.TFrame", padding=(20, 15))
        header.pack(fill="x")

        ttk.Label(header, text="Thời khóa biểu", style="HeroTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(header, textvariable=self.student_meta_var, style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 0)
        )

        controls = ttk.Frame(self, style="App.TFrame", padding=(20, 5))
        controls.pack(fill="x")
        controls.grid_columnconfigure(1, weight=1)
        controls.grid_columnconfigure(3, weight=1)

        ttk.Label(controls, text="Tìm kiếm:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(controls, textvariable=self.search_var).grid(
            row=0, column=1, sticky="ew", pady=5, padx=(0, 15)
        )

        ttk.Label(controls, text="Lọc theo ngày:").grid(row=0, column=2, sticky="w", pady=5)
        day_options = ["Tất cả các ngày"] + list(DAY_NAME_MAP.values())
        self.day_filter = ttk.Combobox(
            controls, state="readonly", values=day_options, textvariable=self.filter_day_var
        )
        self.day_filter.grid(row=0, column=3, sticky="ew", pady=5)

        ttk.Button(
            controls,
            text="Làm mới",
            style="Outline.TButton",
            command=self.refresh_data,
        ).grid(row=0, column=4, padx=(15, 0))

        ttk.Label(
            self,
            textvariable=self.summary_var,
            style="Muted.TLabel",
            padding=(20, 0),
        ).pack(fill="x", pady=(0, 5))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.list_tab = ttk.Frame(notebook, style="App.TFrame", padding=10)
        self.week_tab = ttk.Frame(notebook, style="App.TFrame", padding=10)

        notebook.add(self.list_tab, text="Theo danh sách")
        notebook.add(self.week_tab, text="Theo tuần")

        self._build_list_tab()
        self._build_week_tab()

        footer = ttk.Frame(self, style="App.TFrame", padding=(20, 0))
        footer.pack(fill="x", pady=(0, 15))
        ttk.Button(footer, text="Quay lại", command=self.go_back).pack(anchor="e")

    def _build_list_tab(self):
        self.list_tab.grid_rowconfigure(0, weight=1)
        self.list_tab.grid_columnconfigure(0, weight=1)

        columns = ("course", "class", "teacher", "day", "period", "room")
        self.detail_tree = ttk.Treeview(
            self.list_tab,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        headings = [
            ("course", "Môn học", 200, "w"),
            ("class", "Lớp học phần", 170, "w"),
            ("teacher", "Giảng viên", 170, "w"),
            ("day", "Thứ", 100, "center"),
            ("period", "Tiết", 120, "center"),
            ("room", "Phòng", 100, "center"),
        ]
        for col, text, width, anchor in headings:
            self.detail_tree.heading(col, text=text)
            self.detail_tree.column(col, width=width, anchor=anchor, stretch=True)

        scrollbar = ttk.Scrollbar(
            self.list_tab,
            orient="vertical",
            command=self.detail_tree.yview,
        )
        self.detail_tree.configure(yscrollcommand=scrollbar.set)
        self.detail_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.empty_state_label = ttk.Label(
            self.list_tab,
            textvariable=self.empty_state_var,
            style="Muted.TLabel",
        )

    def _build_week_tab(self):
        self.week_tab.grid_rowconfigure(1, weight=1)
        self.week_tab.grid_columnconfigure(0, weight=1)

        ttk.Label(self.week_tab, text="Lịch học theo tuần", style="SectionTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        columns = ("Tiet", "Thu2", "Thu3", "Thu4", "Thu5", "Thu6", "Thu7")
        self.week_tree = ttk.Treeview(
            self.week_tab,
            columns=columns,
            show="headings",
            height=10,
        )
        for col in columns:
            heading = "Tiết" if col == "Tiet" else col.replace("Thu", "Thứ ")
            anchor = "center" if col == "Tiet" else "w"
            width = 80 if col == "Tiet" else 180
            self.week_tree.heading(col, text=heading)
            self.week_tree.column(col, width=width, anchor=anchor, stretch=True)

        self.week_tree.tag_configure("today-row", background="#e0f2fe")

        week_scroll = ttk.Scrollbar(self.week_tab, orient="vertical", command=self.week_tree.yview)
        self.week_tree.configure(yscrollcommand=week_scroll.set)
        self.week_tree.grid(row=1, column=0, sticky="nsew")
        week_scroll.grid(row=1, column=1, sticky="ns")

        ttk.Label(
            self.week_tab,
            textvariable=self.week_context_var,
            style="Muted.TLabel",
        ).grid(row=2, column=0, sticky="w", pady=(8, 0))

    # ------------------------------------------------------------------
    # DATA HANDLERS
    # ------------------------------------------------------------------
    def load_data(self, student_id):
        self.student_id = student_id
        self.refresh_data()

    def refresh_data(self):
        if not self.student_id:
            return

        # Hiển thị meta sinh viên để người dùng nắm ngữ cảnh
        info = self.controller.db.get_student_info(self.student_id)
        if info:
            ho_ten = info[0]
            dob = info[1].strftime("%d/%m/%Y") if info[1] else "N/A"
            gender = info[2] if len(info) > 2 else ""
            meta_parts = [f"MSSV {self.student_id}", ho_ten]
            if gender:
                meta_parts.append(gender)
            meta_parts.append(f"SN {dob}")
            self.student_meta_var.set(" · ".join(meta_parts))
        else:
            self.student_meta_var.set(f"MSSV {self.student_id}")

        raw_data = self.controller.db.get_student_schedule(self.student_id)
        normalized = []
        for row in raw_data:
            normalized.append(
                {
                    "TenMH": row[0],
                    "TenLHP": row[1],
                    "HoTenGV": row[2],
                    "Thu": row[3],
                    "TietBatDau": row[4],
                    "SoTiet": row[5],
                    "PhongHoc": row[6],
                }
            )
        self.schedule_data = normalized

        total_sessions = len(self.schedule_data)
        total_days = len({item["Thu"] for item in self.schedule_data}) or 0
        if total_sessions:
            self.summary_var.set(
                f"{total_sessions} lịch học · diễn ra trong {total_days} ngày mỗi tuần"
            )
        else:
            self.summary_var.set("Chưa có thời khóa biểu để hiển thị.")

        self.populate_list_view()
        self.populate_week_view()

    def _filter_schedule_data(self):
        keyword = (self.search_var.get() or "").strip().lower()
        day_label = self.filter_day_var.get()
        day_number = None
        for number, label in DAY_NAME_MAP.items():
            if label == day_label:
                day_number = number
                break

        filtered = []
        for item in self.schedule_data:
            if day_number and item["Thu"] != day_number:
                continue
            if keyword:
                haystack = " ".join(
                    [item["TenMH"], item["TenLHP"], item["HoTenGV"], item["PhongHoc"]]
                ).lower()
                if keyword not in haystack:
                    continue
            filtered.append(item)
        return filtered

    def populate_list_view(self):
        filtered = self._filter_schedule_data()

        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)

        for schedule in filtered:
            thu_text = DAY_NAME_MAP.get(schedule["Thu"], f"Thứ {schedule['Thu']}")
            start = schedule["TietBatDau"]
            end = start + schedule["SoTiet"] - 1
            tiet_text = f"Tiết {start} - {end}"
            self.detail_tree.insert(
                "",
                "end",
                values=(
                    schedule["TenMH"],
                    schedule["TenLHP"],
                    schedule["HoTenGV"],
                    thu_text,
                    tiet_text,
                    schedule["PhongHoc"],
                ),
            )

        if filtered:
            self.empty_state_label.pack_forget()
            self.empty_state_var.set("")
        else:
            keyword = self.search_var.get().strip()
            day_label = self.filter_day_var.get()
            reason = "Không có lịch học phù hợp"
            if keyword:
                reason += f" với từ khóa '{keyword}'"
            if day_label and day_label != "Tất cả các ngày":
                reason += f" · bộ lọc ngày {day_label}"
            self.empty_state_var.set(reason)
            self.empty_state_label.pack(pady=20)

    def populate_week_view(self):
        grid = {period: {day: "" for day in range(2, 8)} for period in range(1, 11)}
        for item in self.schedule_data:
            thu = item["Thu"]
            start = item["TietBatDau"]
            end = start + item["SoTiet"] - 1
            description = (
                f"{item['TenMH']} ({item['TenLHP']})\n"
                f"GV: {item['HoTenGV']}\n"
                f"{item['PhongHoc']} · Tiết {start}-{end}"
            )
            if thu not in range(2, 8):
                continue
            for offset in range(item["SoTiet"]):
                slot = start + offset
                if 1 <= slot <= 10:
                    grid[slot][thu] = description

        for row in self.week_tree.get_children():
            self.week_tree.delete(row)

        weekday = datetime.today().weekday()
        highlight_day = weekday + 2
        if highlight_day > 7:
            highlight_day = None

        for period in range(1, 11):
            values = [f"Tiết {period}"] + [grid[period].get(day, "") for day in range(2, 8)]
            tags = (
                "today-row",
            ) if highlight_day and grid[period].get(highlight_day) else ()
            self.week_tree.insert("", "end", values=values, tags=tags)

        label_key = highlight_day if highlight_day else 8 if weekday == 6 else None
        today_label = DAY_NAME_MAP.get(label_key, "Không có lịch học hôm nay")
        self.week_context_var.set(
            f"Hôm nay: {today_label}. Tổng số lịch học trong tuần: {len(self.schedule_data)}"
        )

    def go_back(self):
        """Quay về trang Student Main Frame"""
        self.controller.show_frame("StudentMainFrame", self.student_id)
