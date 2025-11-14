from app import MainApplication

if __name__ == "__main__":
    """
    Đây là điểm vào (entry point) chính của ứng dụng.
    """
    try:
        # Khởi tạo đối tượng ứng dụng chính
        app = MainApplication()

        # Chạy vòng lặp chính của Tkinter (để cửa sổ hiển thị)
        app.mainloop()

    except Exception as e:
        print(f"Đã xảy ra lỗi không xác định: {e}")
        # (Trong ứng dụng thực tế, bạn nên ghi lỗi này vào file log)
