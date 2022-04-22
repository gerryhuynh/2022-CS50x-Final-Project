from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, Markup, redirect, render_template, request, session, url_for
from flask_session import Session
from urllib.parse import urlparse
from werkzeug.security import check_password_hash, generate_password_hash
import re

from additional import login_required


# Configure Flask application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
# Resource: https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blogs.db")


def validate_new_email(email):
    email_regex = r"[\w_.+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}"

    if not re.search(email_regex, email):
        # Resources:
        # https://docs.python.org/3/howto/regex.html
        # https://www.w3schools.com/python/python_regex.asp
        flash("Invalid email.", "error")
        return False
    elif db.execute("SELECT * FROM users WHERE email = ?", email):
        flash("Email already taken.", "error")
        return False

    return True


def validate_new_password(password, confirmation):
    password_regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^a-zA-Z0-9]).{8,}$"
    # Resource: https://ihateregex.io/expr/password/

    if not re.search(password_regex, password):
        flash("Password must meet all requirements.", "error")
        return False
    elif confirmation != password:
        flash("Passwords do not match.", "error")
        return False

    return True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Handle error 404
@app.errorhandler(404)
def not_found(e):
    flash("Error 404: Page not found.", "error")
    print(urlparse(request.url).path)
    return redirect(url_for("index"))
    # Resources:
    # - https://www.geeksforgeeks.org/python-404-error-handling-in-flask/
    # - https://flask.palletsprojects.com/en/2.1.x/api/#flask.Flask.errorhandler

# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (i.e. submitted form)
    if request.method == "POST":

        # Request content from submitted form
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not all([name, email, password, confirmation]):
            # Resources:
            # https://stackoverflow.com/questions/69544373/how-to-check-if-multiple-string-variables-are-empty
            # https://www.w3schools.com/python/ref_func_all.asp
            flash("Please fill in every field.", "error")
            return redirect(url_for("register"))
        elif not validate_new_email(email):
            return redirect(url_for("register"))
        elif not validate_new_password(password, confirmation):
            return redirect(url_for("register"))

        db.execute("INSERT INTO users (name, email, hash) VALUES(?, ?, ?)", name, email, generate_password_hash(password))

        flash("You have successfully registered!", "success")
        # Resource: https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/

        return redirect(url_for("login"))

    return render_template("register.html")


# Log user in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        """
        - Validate form entered properly
        - Validate email exists in database
        - Validate correct password
        - Store user id in session to record as logged in
        """

        email = request.form.get("email")
        password = request.form.get("password")

        # Validate form input
        if not all([email, password]):
            flash("Missing email and password", "error")
            return redirect(url_for("login"))

        # Query database for email
        db_user = db.execute("SELECT * FROM users WHERE email = ?", email)

        # Validate user email & password
        if len(db_user) != 1:
            flash("User does not exist", "error")
            return redirect(url_for("login"))

        if not check_password_hash(db_user[0]["hash"], password):
            flash("Incorrect password", "error")
            return redirect(url_for("login"))

        # Keep user_id in session
        keys = ['id', 'email', 'name']
        session["user"] = {key:db_user[0][key] for key in keys}
        # Resource: https://stackoverflow.com/questions/12117080/how-do-i-create-dictionary-from-another-dictionary

        return redirect(url_for("index"))

    return render_template("login.html")


# Log user out
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    flash("Successfully logged out.", "success")

    return redirect(url_for("index"))


# Home page; shows list of blogs
@app.route("/")
def index():
    posts = db.execute("""
    SELECT posts.slug, users.name, posts.title, posts.summary, posts.created_at
    FROM users
    JOIN users_posts ON users.id = users_posts.user_id
    JOIN posts ON posts.id = users_posts.post_id
    """)

    for post in posts:
        post["created_at"] = datetime.strptime(post["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")
        # Resources:
        # - https://docs.python.org/3/library/datetime.html
        # - https://stackoverflow.com/questions/33834727/how-do-you-extract-only-the-date-from-a-python-datetime
        # - https://www.tutorialsteacher.com/articles/convert-string-to-datetime-in-python

    return render_template("index.html", posts=posts)


# View account information
@app.route("/account")
@login_required
def account():
    return render_template("account.html")


# Change account settings
@app.route("/change-settings", methods=["GET", "POST"])
@login_required
def change_settings():
    change_type = request.args.get("type")
    new_setting = request.form.get("new")

    # User reached route via POST (i.e. user updated their account information)
    if request.method == "POST":
        # Validate entry for new setting
        if not new_setting:
            flash("Missing entry", "error")
            return redirect(url_for("change_settings", type=change_type))

        # Validate current password confirmation when updating email/password
        if change_type == 'email' or change_type == 'password':
            confirm_password = request.form.get("current_password")
            current_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user"]["id"])[0]["hash"]

            if not confirm_password:
                flash("Please confirm current password", "error")
                return redirect(url_for("change_settings", type=change_type))
            elif not check_password_hash(current_password, confirm_password):
                flash("Incorrect current password", "error")
                return redirect(url_for("change_settings", type=change_type))

        # Validate new email
        if change_type == 'email':
            if new_setting == session["user"]["email"]:
                flash("Please enter a new email", "error")
                return redirect(url_for("change_settings", type=change_type))
            elif not validate_new_email(new_setting):
                return redirect(url_for("change_settings", type=change_type))

        # Validate new password
        if change_type == 'password':
            current_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user"]["id"])[0]["hash"]
            confirmation = request.form.get("confirmation")

            if check_password_hash(current_password, new_setting):
                flash("New password must be a different password", "error")
                return redirect(url_for("change_settings", type=change_type))
            elif not validate_new_password(new_setting, confirmation):
                return redirect(url_for("change_settings", type=change_type))


        # Update new account information
        if change_type == 'name' or change_type == 'email':
            session["user"][change_type] = new_setting
            db.execute("UPDATE users SET ? = ? WHERE id = ?", change_type, new_setting, session["user"]["id"])
        elif change_type == 'password':
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_setting), session["user"]["id"])

        return redirect(url_for("account"))


    # User reached route via GET (i.e. clicking one of the links on /account page)
    else:
        valid_change_types = ['name', 'email', 'password']

        if change_type in valid_change_types:
            return render_template("change-settings.html", type=change_type)
        else:
            return redirect(url_for("account"))

# Delete account
@app.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    """
    - Confirm email + password -- use similar page as login
    - Validate information -- similar to login, but make sure login is specific to current user
    - Have option to cancel -- redirect to /account (or try to redirect back to previous page using request.referrer)
    - Possibly try to have the page only accessible if the referring page was /account -- wouldn't need above redirecting feature
    - Delete user row from users using user's id
    - Redirect to /logout
    """

    # User confirms email & password to delete account
    if request.method == "POST":
        """
        - Validate form entered properly
        - Validate email exists in database
        - Validate correct password
        - Store user id in session to record as logged in
        """

        email = request.form.get("email")
        password = request.form.get("password")

        # Check for empty form inputs
        if not all([email, password]):
            flash("Missing email and password", "error")
            return redirect(url_for("delete_account"))

        # Validate email
        if email != session["user"]["email"]:
            flash("Incorrect email", "error")
            return redirect(url_for("delete_account"))

        # Validate password
        correct_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user"]["id"])[0]["hash"]

        if not check_password_hash(correct_password, password):
            flash("Incorrect password", "error")
            return redirect(url_for("delete_account"))

        # Delete user account from table and logout user
        db.execute("DELETE FROM users WHERE id = ?", session["user"]["id"])

        return redirect(url_for("logout"))

    # User confirmed intent to delete account
    elif urlparse(request.referrer).path == url_for("account") or urlparse(request.referrer).path == url_for("delete_account"):
        # Resources:
        # - https://stackoverflow.com/questions/28593235/get-referring-url-for-flask-request
        # - https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request.referrer
        # - https://programtalk.com/python-examples/flask.request.referrer/ (example 8)
        # - https://docs.python.org/3/library/urllib.parse.html
        return render_template("delete-account.html")

    # User can only go to page from /account
    else:
        return redirect(url_for("account"))


# Make new post
@app.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():

    # Display post
    if request.method == "POST":
        title = request.form.get("title")
        tldr = request.form.get("tldr")
        content = request.form.get("content")

        """
        Checks:
        - Title and content filled
        - Valid title length
        - Unique slug
        """
        if not all([title, content]):
            flash("Missing post title and content.", "error")
            return redirect(url_for("new_post"))
        elif len(title) > 255:
            flash("Title too long.", "error")
            return render_template("new_post.html", content=content)

        slug = title.lower().replace(" ", "-")
        # Resource: https://www.w3schools.com/python/ref_string_replace.asp

        if db.execute("SELECT * FROM posts WHERE slug = ?", slug):
            flash("Similar post title already exists.", "error")
            return render_template("new_post.html", content=content)

        # Passed all checks; Insert post into database
        db.execute("INSERT INTO posts (title, slug, summary, content) VALUES(?, ?, ?, ?)", title, slug, tldr, content)

        db.execute("INSERT INTO users_posts (user_id, post_id) VALUES(?, ?)", session["user"]["id"], db.execute("SELECT id FROM posts WHERE slug = ?", slug)[0]["id"])

        return redirect(url_for("index"))

    # print(db.execute("""
    # SELECT users.name, posts.title FROM users
    # JOIN users_posts ON users.id = users_posts.user_id
    # JOIN posts ON posts.id = users_posts.post_id
    # """))

    return render_template("new_post.html")


# Display individual posts
@app.route("/post/<slug>")
def post(slug):
    # Resource: https://flask.palletsprojects.com/en/2.1.x/quickstart/#variable-rules

    if not db.execute("SELECT slug FROM posts WHERE slug = ?", slug):
        flash("Post does not exist.", "error")
        return redirect(url_for("index"))

    post = db.execute("""
    SELECT user_id, posts.slug, users.name, posts.title, posts.summary, posts.created_at, posts.content
    FROM users
    JOIN users_posts ON users.id = users_posts.user_id
    JOIN posts ON posts.id = users_posts.post_id
    WHERE slug = ?
    """, slug)[0]

    post["created_at"] = datetime.strptime(post["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")

    post["content"] = Markup(post["content"].replace("\r\n", "<br />"))
    # Resources:
    # - https://stackoverflow.com/questions/12244057/any-way-to-add-a-new-line-from-a-string-with-the-n-character-in-flask
    # - https://flask.palletsprojects.com/en/2.1.x/templating/#controlling-autoescaping

    return render_template("post.html", post=post)