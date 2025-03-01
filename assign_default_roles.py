from app import app, db
from app.models import User, Role

with app.app_context():
    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user', permissions='view,edit')
        db.session.add(user_role)
        db.session.commit()

    users_without_role = User.query.filter_by(role=None).all()
    for user in users_without_role:
        user.role = user_role
        db.session.commit()

    print('All users have been assigned a role!')
