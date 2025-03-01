# Group Members

1. Joel Brown
2. Kobe Myers
3. Erik Princi
4. Brian Morales

# Project Description

We created a recipe browser that allows users to upload recipes, and view recipes from others. Administrators can edit or delete posts created by any user.

# Running App in Terminal Commands

1. **Activate the Virtual Environment**:

    ```sh
    source venv/bin/activate
    ```

2. **Install Required Packages**:

    Make sure you have the following Flask packages installed. You can check by using the command `pip list`. If they are not installed, use the following command to install them:

    ```sh
    pip install Flask psycopg2-binary flask_sqlalchemy flask_bcrypt flask_login flask_migrate flask_wtf
    ```

3. **Start PostgreSQL Server**:

    ```sh
    sudo systemctl start postgresql
    ```

4. **Check PostgreSQL Status**:

    Make sure PostgreSQL is running:

    ```sh
    sudo systemctl status postgresql
    ```

5. **Set Up the Database**:

    Run the setup script to create initial database tables:

    ```sh
    python setup.py
    ```

6. **Set Flask App Environment Variable**:

    ```sh
    export FLASK_APP=app.py
    ```

7. **Initialize Flask-Migrate**:

    Initialize the migration repository (only needed the first time):

    ```sh
    flask db init
    ```

8. **Generate an Initial Migration**:

    ```sh
    flask db migrate -m "Initial migration."
    ```

9. **Apply the Migration**:

    ```sh
    flask db upgrade
    ```

10. **Run the Flask Application**:

    ```sh
    flask run
    ```

### Notes

- Running `create_admin.py` will create an admin user with the following credentials:
    - email: admin@example.com
    - password: adminpassword
- Ensure PostgreSQL is installed and running before attempting to connect your Flask application to the database.
- Use `pip list` to verify the installation of required packages.
- Adjust the database URI in your `app/__init__.py` file if needed.

# Separation of Work

1. Joel Brown: Worked on RBA and viewing, delete option in CRUD functionality, helped with HTML templates, and debugging with login code
2. Kobe Myers: intial setup of database, flask app, and front end web structure
3. Erik Princi: Fixing bugs related to the database, worked on front-end pages along with the addition of the background image, helped with some of the routes for the html pages. Helped with debugging and testing as well.
4. Brian Morales: fixing bugs related to remembering login, fixing the recipe table foreign key access to acurately use the reference `user_id`, adding the search feature to look up specific recipes, `search.html`, post date and created by markers for recipes, preserving whitespace when adding content to a recipe to allow for proper structuring of instructions.

