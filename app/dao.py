import sys
import os
from pathlib import Path
from datetime import datetime

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
    PaymentMethodEnum,
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
        # Lấy 1–2 phụ huynh và 1–2 lớp để gán
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

        s1 = Student(
            name="Nguyễn Văn A",
            age=5,
            dob=datetime(2020, 5, 10),
            gender=GenderEnum.Male,
            address="123 Đường ABC, Quận 1, TP.HCM",
            entry_date=datetime(2024, 8, 15),
            parent_id=parent_users[0].id,
            class_id=classrooms[0].id,
        )

        s2 = Student(
            name="Trần Thị B",
            age=4,
            dob=datetime(2021, 3, 22),
            gender=GenderEnum.Female,
            address="456 Đường DEF, Quận 3, TP.HCM",
            entry_date=datetime(2024, 8, 20),
            parent_id=parent_users[-1].id,
            class_id=classrooms[-1].id,
        )

        db.session.add_all([s1, s2])
        db.session.commit()
        print("Students created successfully!")

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

        db.session.add_all([c1, c2])
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

        t_id = teacher_users[0].id

        records = []
        for s in students:
            r = HealthRecord(
                weight=18.5,
                height=105.0,
                temperature=36.8,
                date_created=datetime.utcnow(),
                note="Khỏe mạnh, không có dấu hiệu bất thường.",
                student_id=s.id,
                teacher_id=t_id,
            )
            records.append(r)

        db.session.add_all(records)
        db.session.commit()
        print("Health records created successfully!")


def create_invoices():
    """Tạo một số hóa đơn học phí demo cho phụ huynh."""
    with app.app_context():
        # Chọn 1 accountant và một vài phụ huynh
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

        invoices = []

        inv1 = Invoice(
            date_created=datetime(2024, 9, 1),
            amount=2500000,
            payment_method_id=PaymentMethodEnum.Offline,
            content="Học phí tháng 9/2024 - lớp Mầm 1",
            accountant_id=accountant_user.id,
        )

        inv2 = Invoice(
            date_created=datetime(2024, 10, 1),
            amount=2600000,
            payment_method_id=PaymentMethodEnum.Online,
            content="Học phí tháng 10/2024 - lớp Chồi 1",
            accountant_id=accountant_user.id,
        )

        invoices.extend([inv1, inv2])
        db.session.add_all(invoices)
        db.session.commit()
        print("Invoices created successfully!")


def create_tuitionfees():
    """Tạo dữ liệu học phí chi tiết cho từng học sinh, gắn với Invoice."""
    with app.app_context():
        students = Student.query.all()
        invoices = Invoice.query.all()

        if not students or not invoices:
            print("Vui lòng tạo Student và Invoice trước khi tạo TuitionFee.")
            return

        fees = []

        # Gán 2 học sinh đầu cho 2 invoice đầu (nếu đủ)
        for idx, s in enumerate(students[:2]):
            inv = invoices[idx] if idx < len(invoices) else None

            fee_base = 2000000
            meal_fee = 300000
            extra_fee = 200000

            fee = TuitionFee(
                month=9 + idx,
                year=2024,
                fee_base=fee_base,
                meal_fee=meal_fee,
                extra_fee=extra_fee,
                payment_date=datetime(2024, 9 + idx, 5),
                status=PaymentStatusEnum.Paid,
                invoice_id=inv.id if inv else None,
                student_id=s.id,
            )
            fees.append(fee)

        db.session.add_all(fees)
        db.session.commit()
        print("Tuition fees created successfully!")

if __name__ == '__main__':
    create_roles()
    create_users()
    create_classrooms()
    create_students()
    create_healthRecords()
    create_invoices()
    create_tuitionfees()