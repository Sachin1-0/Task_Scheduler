from app import create_app, db
from app.models import User, Category, Task
from datetime import date, timedelta

app = create_app()

with app.app_context():
    db.create_all()
    
    if User.query.first():
        print("Database already initialized.")
    else:
        user1 = User(username='johndoe', email='john@example.com')
        user1.set_password('Password123!')
        db.session.add(user1)
        db.session.commit()
        
        cat1 = Category(name='Work', user_id=user1.id, is_default=True)
        cat2 = Category(name='Personal', user_id=user1.id, is_default=True)
        cat3 = Category(name='Study', user_id=user1.id, is_default=True)
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()
        
        today = date.today()
        task1 = Task(title='Complete Task Scheduler', description='Finish the Flask project.', due_date=today, priority='High', status='In Progress', user_id=user1.id, category_id=cat1.id)
        task2 = Task(title='Buy Groceries', description='Milk, Bread, Coffee', due_date=today + timedelta(days=2), priority='Medium', status='Pending', user_id=user1.id, category_id=cat2.id)
        task3 = Task(title='Read Flask Docs', description='Review SQLAlchemy relationships.', due_date=today - timedelta(days=1), priority='Low', status='Completed', user_id=user1.id, category_id=cat3.id)
        db.session.add_all([task1, task2, task3])
        db.session.commit()
        print("Database initialized with dummy data.")
