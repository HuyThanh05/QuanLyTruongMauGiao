import sys
import os
from pathlib import Path

# Add project root to Python path
# This allows running the script from any directory
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.Models import Role, User

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

        u1 = User(phone='0123456789', email='admin1@example.com', password_hash=generate_password_hash('123456'))
        u1.roles.append(admin_role)

        u2 = User(phone='0123456788', email='teacher1@example.com', password_hash=generate_password_hash('123456'))
        u2.roles.append(teacher_role)

        u3 = User(phone='0123456787', email='parent1@example.com', password_hash=generate_password_hash('123456'))
        u3.roles.append(parent_role)

        u4 = User(phone='0123456786', email='accountant1@example.com', password_hash=generate_password_hash('123456'))
        u4.roles.append(accountant_role)

        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()
        print("Users created successfully!")

if __name__ == '__main__':
    create_roles(),
    create_users()