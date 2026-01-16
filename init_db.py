"""
Initialize database with default admin user
Run this script once to create the admin user
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import hash_password

# Create tables
models.Base.metadata.create_all(bind=engine)

# Create admin user
db = SessionLocal()

try:
    # Check if admin already exists
    existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
    
    if not existing_admin:
        admin_user = models.User(
            username="admin",
            hashed_password=hash_password("admin123"),
            roles=["ROLE_ADMIN", "ROLE_USER"]
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Roles: ROLE_ADMIN, ROLE_USER")
    else:
        print("ℹ️  Admin user already exists")
        
finally:
    db.close()
