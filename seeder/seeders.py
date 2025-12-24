from model.models import User, Category
from werkzeug.security import generate_password_hash

CATEGORIES_SEED = [
    {"name": "Work"},
    {"name": "Sport"},
    {"name": "Study"},
    {"name": "Shopping"},
    {"name": "Others"},
]

def seed_data(db):
    new_user = User(
        name="User123",
        email="user123@gmail.com",
        password=generate_password_hash("user123pass")
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    for category_data in CATEGORIES_SEED:
        category = db.query(Category).filter_by(name=category_data["name"], user_id=new_user.id).first()
        if not category:
            category = Category(name=category_data["name"], user_id=new_user.id)
            db.add(category)
    db.commit()
    print("Seeding completed.")