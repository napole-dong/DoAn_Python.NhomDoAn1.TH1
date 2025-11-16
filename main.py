"""Entry point for launching the Tkinter application."""

from app import MainApplication


if __name__ == "__main__":
    try:
        app = MainApplication()
        app.mainloop()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Đã xảy ra lỗi không xác định: {exc}")
