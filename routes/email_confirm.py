from flask import render_template, request, redirect, session, url_for
from flask_mail import Mail, Message
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
import os
from app_init import app

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@app.route('/email_check', methods=['GET', 'POST'])
def email_check():
    if request.method == 'GET':
        # return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
        message = 'Email verification'
        return render_template('email_check.html', message=message)

    email = request.form['email']
    token = serializer.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = f'Your link is {link}'
    mail.send(msg)

    # return f'<h1>The email you entered is {email}. The token is {token}</h1>'
    message = f'A link has been sent to email {email}.'
    is_logged = "email" in session
    return render_template("index.html", message=message, is_logged=is_logged)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email_val = serializer.loads(token, salt='email-confirm', max_age=600)
        session["email"] = email_val
    except SignatureExpired:
        message = 'The link is expired.'
        is_logged = "email" in session
        return render_template("index.html", message=message, is_logged=is_logged)

    return redirect(url_for("logged_in"))
