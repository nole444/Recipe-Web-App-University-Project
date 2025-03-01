from app import app, db, bcrypt
from app.models import User, Role

with app.app_context():
    #Check if the admin role already exists
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', permissions='view,edit,delete,admin')
        db.session.add(admin_role)
        db.session.commit()

    #Check if the admin user already exists
    admin_user = User.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash('adminpassword').decode('utf-8')
        admin = User(username='admin', email='admin@example.com', password=hashed_password, role=admin_role)
        db.session.add(admin)
    else:
        #Update the role if the user already exists
        admin_user.role = admin_role
    
    db.session.commit()
    print('Admin user setup complete!')
