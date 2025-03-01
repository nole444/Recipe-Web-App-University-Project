from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, RecipeForm
from app.models import User, Recipe, Role
from flask_login import login_user, current_user, logout_user, login_required
from app.decorators import role_required
from sqlalchemy import func

@app.route("/")
@app.route("/home")
def home():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('recipe.html', title='New Recipe', form=form)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)

@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user and not current_user.has_permission('admin'):
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.content = form.content.data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.content.data = recipe.content
    return render_template('recipe.html', title='Update Recipe', form=form)

@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user and not current_user.has_permission('admin'):
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('The recipe has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_role = Role.query.filter_by(name='user').first()  # Assign 'user' role by default
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=user_role)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/search")
def search():
    query = request.args.get('query')
    recipes = Recipe.query.filter(func.lower(Recipe.title).contains(func.lower(query))).all()
    return render_template('search.html', recipes=recipes, query=query)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
@login_required
@role_required('admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)
