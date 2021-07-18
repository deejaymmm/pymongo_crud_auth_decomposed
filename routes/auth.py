from flask import render_template, request, redirect, session, url_for
import bcrypt
from app_init import app, user_coll


@app.route('/register', methods=['post', 'get'])
def register():
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("user")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if not user or not email or not password1 or not password2:
            message = 'All fields must be filled in! '
            return render_template('register.html', message=message)

        user_found = user_coll.find_one({"user": user})
        email_found = user_coll.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'user': user, 'email': email, 'password': hashed}
            user_coll.insert_one(user_input)

            user_data = user_coll.find_one({"email": email})
            new_email = user_data['email']

            # return render_template('logged_in.html', email=new_email)
            return redirect(url_for("login"))
    message = ''
    return render_template("register.html", message=message)


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email, is_logged=True)
    else:
        return redirect(url_for("login", is_logged=False))


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            message = 'All fields must be filled in! '
            return render_template('login.html', message=message)

        email_found = user_coll.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            password_check = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), password_check):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        # session.pop("email", None)
        session.clear()
        return render_template("logout.html")
    else:
        return render_template('index.html')
