from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.Models import Role, User

app = create_app()


def create_roles():
    with app.app_context():
        admin = Role(id=1, name='Admin')
        teacher = Role(id=2, name='Teacher')
        accountant = Role(id=3, name='Accountant')
        student = Role(id=4, name='Student')

        db.session.add(admin)
        db.session.add(teacher)
        db.session.add(accountant)
        db.session.add(student)

        db.session.commit()
        print("Roles created successfully!")

def create_users():
    with app.app_context():
        admin_role = Role.query.filter_by(name='Admin').first()
        teacher_role = Role.query.filter_by(name='Teacher').first()
        student_role = Role.query.filter_by(name='Student').first()

        u1 = User(phone='0123456789', email='admin1@example.com', password_hash=generate_password_hash('123456'))
        u1.roles.append(admin_role)

        u2 = User(phone='0123456788', email='teacher1@example.com', password_hash=generate_password_hash('123456'))
        u2.roles.append(teacher_role)

        u3 = User(phone='0123456787', email='student1@example.com', password_hash=generate_password_hash('123456'))
        u3.roles.append(student_role)

        u4 = User(phone='0123456786', email='teacher2@example.com', password_hash=generate_password_hash('123456'))
        u4.roles.append(teacher_role)

        u5 = User(phone='0123456785', email='admin2@example.com', password_hash=generate_password_hash('123456'))
        u5.roles.append(admin_role)

        db.session.add_all([u1, u2, u3, u4, u5])
        db.session.commit()
        print("Users created successfully!")

if __name__ == '__main__':
    create_roles(),
    create_users()