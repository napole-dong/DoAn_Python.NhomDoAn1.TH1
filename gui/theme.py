"""Custom ttk theme helpers for the student management application."""

from tkinter import ttk

PRIMARY_COLOR = "#2563eb"
PRIMARY_DARK = "#1d4ed8"
PRIMARY_LIGHT = "#3b82f6"
ACCENT_COLOR = "#f97316"
BACKGROUND = "#f8fafc"
CARD_BACKGROUND = "#ffffff"
BORDER_COLOR = "#e2e8f0"
TEXT_MUTED = "#64748b"
SUCCESS_COLOR = "#16a34a"
WARNING_COLOR = "#f59e0b"
ERROR_COLOR = "#dc2626"


def configure_theme(root):
    """Apply a modernized visual style across all ttk widgets."""

    style = ttk.Style(root)

    # Force a known theme so style colors render consistently on Windows.
    if "clam" in style.theme_names():
        style.theme_use("clam")

    default_font = ("Segoe UI", 10)
    heading_font = ("Segoe UI", 12, "bold")

    style.configure(".", font=default_font)

    style.configure("TFrame", background=BACKGROUND)
    style.configure("App.TFrame", background=BACKGROUND)
    style.configure(
        "Card.TFrame",
        background=CARD_BACKGROUND,
        bordercolor=BORDER_COLOR,
        relief="ridge",
        padding=15,
    )

    style.configure("Hero.TFrame", background=BACKGROUND)

    style.configure(
        "Card.TLabelframe",
        background=CARD_BACKGROUND,
        bordercolor=BORDER_COLOR,
        relief="ridge",
        padding=15,
    )
    style.configure(
        "Card.TLabelframe.Label",
        font=heading_font,
        foreground=PRIMARY_COLOR,
        background=CARD_BACKGROUND,
    )

    style.configure(
        "HeroTitle.TLabel",
        font=("Segoe UI", 20, "bold"),
        foreground=PRIMARY_COLOR,
        background=BACKGROUND,
    )
    style.configure(
        "SectionTitle.TLabel",
        font=heading_font,
        foreground="#0f172a",
        background=BACKGROUND,
    )
    style.configure(
        "Muted.TLabel",
        foreground=TEXT_MUTED,
        background=BACKGROUND,
    )
    style.configure(
        "CardMuted.TLabel",
        foreground=TEXT_MUTED,
        background=CARD_BACKGROUND,
    )
    style.configure(
        "StatValue.TLabel",
        font=("Segoe UI", 24, "bold"),
        foreground=PRIMARY_COLOR,
        background=CARD_BACKGROUND,
    )
    style.configure(
        "StatLabel.TLabel",
        foreground=TEXT_MUTED,
        background=CARD_BACKGROUND,
    )
    style.configure(
        "Tag.TLabel",
        background=PRIMARY_LIGHT,
        foreground="white",
        font=("Segoe UI", 9, "bold"),
        padding=(10, 3),
    )
    style.configure(
        "Error.TLabel",
        foreground=ERROR_COLOR,
        background=CARD_BACKGROUND,
    )

    style.configure(
        "Primary.TButton",
        background=PRIMARY_COLOR,
        foreground="white",
        padding=(18, 10),
        bordercolor=PRIMARY_COLOR,
        focusthickness=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", PRIMARY_LIGHT), ("pressed", PRIMARY_DARK)],
        foreground=[("disabled", "#cbd5f5"), ("!disabled", "white")],
    )

    style.configure(
        "Accent.TButton",
        background=ACCENT_COLOR,
        foreground="white",
        padding=(18, 10),
        bordercolor=ACCENT_COLOR,
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#fb923c"), ("pressed", "#ea580c")],
        foreground=[("disabled", "#fed7aa"), ("!disabled", "white")],
    )

    style.configure(
        "Outline.TButton",
        background=CARD_BACKGROUND,
        foreground=PRIMARY_COLOR,
        bordercolor=PRIMARY_COLOR,
        padding=(18, 10),
    )
    style.map(
        "Outline.TButton",
        background=[("active", "#dbeafe")],
        foreground=[("disabled", TEXT_MUTED), ("!disabled", PRIMARY_COLOR)],
    )

    style.configure("TEntry", padding=8)
    style.configure("TCombobox", padding=6)
    style.configure("TCheckbutton", background=CARD_BACKGROUND)
    style.configure("TNotebook", background=BACKGROUND, tabmargins=(6, 6, 0, 0))
    style.configure("TNotebook.Tab", padding=(14, 8))

    style.configure(
        "Treeview",
        background=CARD_BACKGROUND,
        fieldbackground=CARD_BACKGROUND,
        bordercolor=BORDER_COLOR,
        rowheight=28,
        font=default_font,
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#e2e8f0",
        foreground="#0f172a",
        padding=6,
    )
    style.map(
        "Treeview",
        background=[("selected", "#dbeafe")],
        foreground=[("selected", "#0f172a")],
    )

    style.configure("Horizontal.TSeparator", background=BORDER_COLOR)

    # Give notebook panes and label frames a consistent background.
    style.configure("TLabel", background=BACKGROUND)
    style.configure("Card.TLabel", background=CARD_BACKGROUND)

    # Sidebar styling for admin schedule module
    sidebar_bg = "#111827"
    style.configure(
        "SidebarHeading.TLabel",
        background=sidebar_bg,
        foreground="#f8fafc",
        font=("Segoe UI", 13, "bold"),
    )
    style.configure(
        "Sidebar.TButton",
        background="#1f2937",
        foreground="#f8fafc",
        padding=(14, 10),
        bordercolor="#1f2937",
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", "#374151"), ("pressed", "#0f172a")],
        foreground=[("disabled", "#94a3b8"), ("!disabled", "#f8fafc")],
    )

    return style
