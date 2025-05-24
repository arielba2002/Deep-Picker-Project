# Script to create an admin user with password 'admin'
from sqlalchemy.orm import sessionmaker
from config.database import engine
from models import user_model
from services.auth_services import get_password_hash

Session = sessionmaker(bind=engine)
session = Session()

admin_email = "admin@admin.com"
admin_name = "admin"
admin_password = "admin"

existing = session.query(user_model.User).filter(user_model.User.email == admin_email).first()
if existing:
    print("Admin user already exists.")
else:
    hashed = get_password_hash(admin_password)
    admin = user_model.User(name=admin_name, email=admin_email, hashed_password=hashed)
    session.add(admin)
    session.commit()
    print("Admin user created: admin@admin.com / admin")
