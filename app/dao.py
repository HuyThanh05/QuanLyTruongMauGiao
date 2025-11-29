import sys
import os
from pathlib import Path
from datetime import datetime, date

# Add project root to Python path
# This allows running the script from any directory
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.Models import (
    Role,
    User,
    Classroom,
    Student,
    HealthRecord,
    TuitionFee,
    Invoice,
    GenderEnum,
    PaymentStatusEnum,
)

app = create_app()


def create_roles():
    with app.app_context():
        admin = Role(id=1, name='Admin')
        teacher = Role(id=2, name='Teacher')
        accountant = Role(id=3, name='Accountant')
        parent = Role(id=4, name='Parent')

        db.session.add(admin)
        db.session.add(teacher)
        db.session.add(accountant)
        db.session.add(parent)

        db.session.commit()
        print("Roles created successfully!")

def create_users():
    with app.app_context():
        admin_role = Role.query.filter_by(name='Admin').first()
        teacher_role = Role.query.filter_by(name='Teacher').first()
        parent_role = Role.query.filter_by(name='Parent').first()
        accountant_role = Role.query.filter_by(name='Accountant').first()

        u1 = User(name = "khoideptrai",phone='0123456789', email='admin1@example.com', password_hash=generate_password_hash('123456'))
        u1.roles.append(admin_role)

        u2 = User(name = "khoideptrai",phone='0123456788', email='teacher1@example.com', password_hash=generate_password_hash('123456'))
        u2.roles.append(teacher_role)

        u3 = User(name = "khoideptrai",phone='0123456787', email='parent1@example.com', password_hash=generate_password_hash('123456'))
        u3.roles.append(parent_role)

        u4 = User(name = "khoideptrai",phone='0123456786', email='accountant1@example.com', password_hash=generate_password_hash('123456'))
        u4.roles.append(accountant_role)

        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()
        print("Users created successfully!")

def create_students():
    """Tạo một số học sinh demo, gán vào phụ huynh và lớp học."""
    with app.app_context():
        # Lấy phụ huynh và lớp để gán
        parent_role = Role.query.filter_by(name='Parent').first()
        parent_users = (
            User.query.join(User.roles)
            .filter(Role.id == parent_role.id)
            .all()
            if parent_role
            else []
        )
        classrooms = Classroom.query.all()

        if not parent_users or not classrooms:
            print("Vui lòng tạo Parent user và Classroom trước khi tạo Student.")
            return

        students_data = [
            {"name": "Nguyễn Văn A", "age": 5, "dob": date(2020, 5, 10), "gender": GenderEnum.Nam, "address": "123 Đường ABC, Quận 1, TP.HCM", "entry_date": date(2024, 8, 15)},
            {"name": "Trần Thị B", "age": 4, "dob": date(2021, 3, 22), "gender": GenderEnum.Nu, "address": "456 Đường DEF, Quận 3, TP.HCM", "entry_date": date(2024, 8, 20)},
            {"name": "Lê Văn C", "age": 5, "dob": date(2020, 7, 15), "gender": GenderEnum.Nam, "address": "789 Đường GHI, Quận 5, TP.HCM", "entry_date": date(2024, 8, 18)},
            {"name": "Phạm Thị D", "age": 4, "dob": date(2021, 1, 8), "gender": GenderEnum.Nu, "address": "321 Đường JKL, Quận 7, TP.HCM", "entry_date": date(2024, 8, 22)},
            {"name": "Hoàng Văn E", "age": 6, "dob": date(2019, 9, 25), "gender": GenderEnum.Nam, "address": "654 Đường MNO, Quận 2, TP.HCM", "entry_date": date(2024, 8, 16)},
            {"name": "Vũ Thị F", "age": 4, "dob": date(2021, 4, 12), "gender": GenderEnum.Nu, "address": "987 Đường PQR, Quận 10, TP.HCM", "entry_date": date(2024, 8, 25)},
            {"name": "Đặng Văn G", "age": 5, "dob": date(2020, 6, 30), "gender": GenderEnum.Nam, "address": "147 Đường STU, Quận 4, TP.HCM", "entry_date": date(2024, 8, 19)},
            {"name": "Bùi Thị H", "age": 4, "dob": date(2021, 2, 14), "gender": GenderEnum.Nu, "address": "258 Đường VWX, Quận 6, TP.HCM", "entry_date": date(2024, 8, 21)},
            {"name": "Ngô Văn I", "age": 5, "dob": date(2020, 8, 5), "gender": GenderEnum.Nam, "address": "369 Đường YZ, Quận 8, TP.HCM", "entry_date": date(2024, 8, 17)},
            {"name": "Đỗ Thị K", "age": 4, "dob": date(2021, 5, 18), "gender": GenderEnum.Nu, "address": "741 Đường Main, Quận 11, TP.HCM", "entry_date": date(2024, 8, 23)},
        ]

        students = []
        for idx, data in enumerate(students_data):
            parent_idx = idx % len(parent_users)
            class_idx = idx % len(classrooms)
            student = Student(
                name=data["name"],
                age=data["age"],
                dob=data["dob"],
                gender=data["gender"],
                address=data["address"],
                entry_date=data["entry_date"],
                parent_id=parent_users[parent_idx].id,
                class_id=classrooms[class_idx].id,
            )
            students.append(student)

        db.session.add_all(students)
        db.session.commit()
        print(f"Students created successfully! ({len(students)} students)")

def create_classrooms():
    """Tạo một số lớp học demo, gán giáo viên chủ nhiệm nếu có."""
    with app.app_context():
        teacher_role = Role.query.filter_by(name='Teacher').first()
        teacher_users = (
            User.query.join(User.roles)
            .filter(Role.id == teacher_role.id)
            .all()
            if teacher_role
            else []
        )

        teacher_id_1 = teacher_users[0].id if len(teacher_users) > 0 else None
        teacher_id_2 = teacher_users[1].id if len(teacher_users) > 1 else teacher_id_1

        c1 = Classroom(
            name="Lớp Mầm 1",
            term="2024-2025",
            max_slots=30,
            teacher_id=teacher_id_1,
        )

        c2 = Classroom(
            name="Lớp Chồi 1",
            term="2024-2025",
            max_slots=30,
            teacher_id=teacher_id_2,
        )

        c3 = Classroom(
            name = "Lớp Lá 1",
            term = "2024-2025",
            max_slots = 30,
            teacher_id = 1
        )

        db.session.add_all([c1, c2,c3])
        db.session.commit()
        print("Classrooms created successfully!")

def create_healthRecords():
    """Tạo một số phiếu sức khỏe demo cho học sinh."""
    with app.app_context():
        students = Student.query.all()
        teacher_role = Role.query.filter_by(name='Teacher').first()
        teacher_users = (
            User.query.join(User.roles)
            .filter(Role.id == teacher_role.id)
            .all()
            if teacher_role
            else []
        )

        if not students or not teacher_users:
            print("Vui lòng tạo Student và Teacher user trước khi tạo HealthRecord.")
            return

        # Tạo 10 phiếu sức khỏe với dữ liệu đa dạng
        health_records_data = [
            {"weight": 18.5, "height": 105.0, "temperature": 36.8, "note": "Khỏe mạnh, không có dấu hiệu bất thường.", "date": datetime(2024, 9, 1)},
            {"weight": 19.2, "height": 107.5, "temperature": 36.9, "note": "Tình trạng sức khỏe tốt, ăn uống bình thường.", "date": datetime(2024, 9, 5)},
            {"weight": 17.8, "height": 103.0, "temperature": 36.7, "note": "Cần bổ sung dinh dưỡng, hơi nhẹ cân so với tuổi.", "date": datetime(2024, 9, 8)},
            {"weight": 20.1, "height": 109.0, "temperature": 37.0, "note": "Phát triển tốt, cân nặng và chiều cao phù hợp.", "date": datetime(2024, 9, 12)},
            {"weight": 18.9, "height": 106.2, "temperature": 36.6, "note": "Sức khỏe ổn định, vui vẻ, hoạt động bình thường.", "date": datetime(2024, 9, 15)},
            {"weight": 19.5, "height": 108.0, "temperature": 36.8, "note": "Khỏe mạnh, tham gia các hoạt động tích cực.", "date": datetime(2024, 9, 18)},
            {"weight": 17.5, "height": 102.5, "temperature": 36.9, "note": "Cần theo dõi thêm về dinh dưỡng.", "date": datetime(2024, 9, 20)},
            {"weight": 20.3, "height": 110.0, "temperature": 36.7, "note": "Phát triển tốt, không có vấn đề sức khỏe.", "date": datetime(2024, 9, 22)},
            {"weight": 19.0, "height": 107.0, "temperature": 36.8, "note": "Tình trạng sức khỏe ổn định, ăn ngủ tốt.", "date": datetime(2024, 9, 25)},
            {"weight": 18.7, "height": 105.5, "temperature": 36.9, "note": "Khỏe mạnh, năng động, hòa đồng với bạn bè.", "date": datetime(2024, 9, 28)},
        ]

        records = []
        for idx, data in enumerate(health_records_data):
            # Phân bổ đều cho các học sinh và giáo viên
            student_idx = idx % len(students) if students else 0
            teacher_idx = idx % len(teacher_users) if teacher_users else 0
            
            r = HealthRecord(
                weight=data["weight"],
                height=data["height"],
                temperature=data["temperature"],
                date_created=data["date"],
                note=data["note"],
                student_id=students[student_idx].id,
                teacher_id=teacher_users[teacher_idx].id,
            )
            records.append(r)

        db.session.add_all(records)
        db.session.commit()
        print(f"Health records created successfully! ({len(records)} records)")

def create_invoices():
    """Tạo một số hóa đơn học phí demo cho phụ huynh."""
    with app.app_context():
        # Chọn accountant
        accountant_role = Role.query.filter_by(name='Accountant').first()
        accountant_user = (
            User.query.join(User.roles)
            .filter(Role.id == accountant_role.id)
            .first()
            if accountant_role
            else None
        )

        if not accountant_user:
            print("Vui lòng tạo user Accountant trước khi tạo Invoice.")
            return

        classrooms = Classroom.query.all()
        
        # Tạo 10 hóa đơn với dữ liệu đa dạng
        invoices_data = [
            {"date": datetime(2024, 9, 1), "amount": 2500000, "content": "Học phí tháng 9/2024 - lớp Mầm 1"},
            {"date": datetime(2024, 9, 1), "amount": 2600000, "content": "Học phí tháng 9/2024 - lớp Chồi 1"},
            {"date": datetime(2024, 10, 1), "amount": 2500000, "content": "Học phí tháng 10/2024 - lớp Mầm 1"},
            {"date": datetime(2024, 10, 1), "amount": 2600000, "content": "Học phí tháng 10/2024 - lớp Chồi 1"},
            {"date": datetime(2024, 11, 1), "amount": 2550000, "content": "Học phí tháng 11/2024 - lớp Mầm 1"},
            {"date": datetime(2024, 11, 1), "amount": 2650000, "content": "Học phí tháng 11/2024 - lớp Chồi 1"},
            {"date": datetime(2024, 12, 1), "amount": 2500000, "content": "Học phí tháng 12/2024 - lớp Mầm 1"},
            {"date": datetime(2024, 12, 1), "amount": 2600000, "content": "Học phí tháng 12/2024 - lớp Chồi 1"},
            {"date": datetime(2025, 1, 1), "amount": 2700000, "content": "Học phí tháng 1/2025 - lớp Mầm 1"},
            {"date": datetime(2025, 1, 1), "amount": 2800000, "content": "Học phí tháng 1/2025 - lớp Chồi 1"},
        ]

        invoices = []
        for data in invoices_data:
            inv = Invoice(
                date_created=data["date"],
                amount=data["amount"],
                content=data["content"],
                accountant_id=accountant_user.id,
            )
            invoices.append(inv)

        db.session.add_all(invoices)
        db.session.commit()
        print(f"Invoices created successfully! ({len(invoices)} invoices)")

def create_tuitionfees():
    """Tạo dữ liệu học phí chi tiết cho từng học sinh, gắn với Invoice."""
    with app.app_context():
        students = Student.query.all()
        invoices = Invoice.query.all()

        if not students or not invoices:
            print("Vui lòng tạo Student và Invoice trước khi tạo TuitionFee.")
            return

        # Tạo 10 học phí với dữ liệu đa dạng
        fees_data = [
            {"month": 9, "year": 2024, "fee_base": 2000000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2024, 9, 5), "status": PaymentStatusEnum.Paid},
            {"month": 9, "year": 2024, "fee_base": 2100000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2024, 9, 6), "status": PaymentStatusEnum.Paid},
            {"month": 10, "year": 2024, "fee_base": 2000000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2024, 10, 5), "status": PaymentStatusEnum.Paid},
            {"month": 10, "year": 2024, "fee_base": 2100000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2024, 10, 7), "status": PaymentStatusEnum.Paid},
            {"month": 11, "year": 2024, "fee_base": 2050000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2024, 11, 5), "status": PaymentStatusEnum.Paid},
            {"month": 11, "year": 2024, "fee_base": 2150000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": None, "status": PaymentStatusEnum.Unpaid},
            {"month": 12, "year": 2024, "fee_base": 2000000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2024, 12, 5), "status": PaymentStatusEnum.Paid},
            {"month": 12, "year": 2024, "fee_base": 2100000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": None, "status": PaymentStatusEnum.Unpaid},
            {"month": 1, "year": 2025, "fee_base": 2200000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": datetime(2025, 1, 5), "status": PaymentStatusEnum.Paid},
            {"month": 1, "year": 2025, "fee_base": 2300000, "meal_fee": 300000, "extra_fee": 200000, "payment_date": None, "status": PaymentStatusEnum.Unpaid},
        ]

        fees = []
        for idx, data in enumerate(fees_data):
            # Phân bổ đều cho các học sinh và hóa đơn
            student_idx = idx % len(students) if students else 0
            invoice_idx = idx % len(invoices) if invoices else None

            fee = TuitionFee(
                month=data["month"],
                year=data["year"],
                fee_base=data["fee_base"],
                meal_fee=data["meal_fee"],
                extra_fee=data["extra_fee"],
                payment_date=data["payment_date"],
                status=data["status"],
                invoice_id=invoices[invoice_idx].id if invoice_idx is not None and invoice_idx < len(invoices) else None,
                student_id=students[student_idx].id,
            )
            fees.append(fee)

        db.session.add_all(fees)
        db.session.commit()
        print(f"Tuition fees created successfully! ({len(fees)} fees)")

if __name__ == '__main__':
    create_roles()
    create_users()
    create_classrooms()
    create_students()
    create_healthRecords()
    create_invoices()
    create_tuitionfees()