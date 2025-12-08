# Hệ Thống Quản Lý Trường Mẫu Giáo

Hệ thống quản lý toàn diện cho trường mẫu giáo, được xây dựng bằng Python Flask với mô hình MVC.

## Tính Năng

- Quản lý thông tin trường học
- Quản lý học sinh
- Quản lý giáo viên
- Quản lý lớp học
- Quản lý thời khóa biểu
- Quản lý hoạt động hàng ngày
- Quản lý học phí
- Quản lý bữa ăn
- Báo cáo và thống kê

## Cấu Trúc Dự Án

```
QuanLyTruongMauGiao/
├── app/
│   ├── controllers/      # route/view layer (pages, auth_routes, user_api)
│   ├── services/         # nghiệp vụ (auth_service, user_service)
│   ├── models/           # Models, DTO, enums
│   └── static/, templates/ (được Flask cấu hình ở ngoài)
├── static/               # File tĩnh (Css, Js)
├── templates/            # Templates HTML
├── migrations/           # Alembic migration
├── instance/database.sqlite3
├── requirements.txt      # Thư viện
└── run.py                # Khởi chạy ứng dụng
```

## Yêu Cầu Hệ Thống

- Python 3.11+
- Cài đặt qua `pip install -r requirements.txt`

## Hướng Dẫn Cài Đặt

1. Clone repository về máy:

   ```bash
   git clone https://github.com/rifujin123/QuanLyTruongMauGiao.git
   cd QuanLyTruongMauGiao
   ```

2. Tạo môi trường ảo Python:

   ```bash
   python -m venv venv
   ```

3. Kích hoạt môi trường ảo:

   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Cài đặt các thư viện cần thiết:

   ```bash
   pip install -r requirements.txt
   ```

5. Khởi chạy ứng dụng:

   ```bash
   python run.py
   ```

6. Truy cập ứng dụng tại địa chỉ: `http://127.0.0.1:5000`

## Công Nghệ Sử Dụng

- Python Flask - Web Framework
- Bootstrap 5 - Frontend Framework
- Jinja2 - Template Engine
- Werkzeug - WSGI Utility Library
- SQLAlchemy (coming soon) - ORM và Database

## Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork dự án
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## Ghi chú nhanh

- Blueprint: `pages` (UI), `auth` (signup/login/logout), `user_api` (REST, prefix `/api/users`).
- Đăng ký người dùng luôn gán role `Parent`; role khác cấp qua admin.
- Seeder `app/dao.py` tạo 4 user mẫu (Admin/Teacher/Parent/Accountant) mật khẩu `123456`.
- Chạy: `python run.py` (Flask debug). DB mặc định `instance/database.sqlite3`. Config DB/SECRET_KEY nên tách ENV khi deploy.

## Giấy Phép

Dự án này được phân phối dưới giấy phép MIT License.

## Liên Hệ

- GitHub: [@rifujin123](https://github.com/rifujin123)
- Email: [2351050085khoi@ou.edu.vn]

---

From [rifujin123](https://github.com/rifujin123)
