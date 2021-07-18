from flask import render_template, session
from app_init import app


@app.route('/', methods=['post', 'get'])  # функция-декоратор отслеживания главной страницы по URL-адресу ('/')
@app.route('/home', methods=['post', 'get'])  # обработка двух URL-адресов
def index():
    message = ''
    is_logged = "email" in session
    return render_template("index.html", message=message, is_logged=is_logged)  # вывод шаблона на экран
