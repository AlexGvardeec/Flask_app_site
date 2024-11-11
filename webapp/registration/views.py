from webapp import db
from flask import request, redirect, url_for, flash, render_template, session, Blueprint
from webapp.registration.models import User

registration = Blueprint('registration', __name__)


# REGISTRATION // Регистрация пользователя
@registration.route('/registration/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('Пожалуйста заполните все поля', 'danger')
            return redirect(url_for('registration.register'))
        user = User(username=username, email=email, password=password)
        user_count = User.query.filter_by(username=username).count()
        if user_count > 0:
            flash('Такой пользователь уже существует. '
                  'Авторизуйтесь или выберите другое имя','danger')
        else:
            db.session.add(user)
            db.session.commit()
            flash('Пользователь зарегистрирован!', 'success')
            return redirect(url_for('registration.login'))
    return render_template('registration/registration.html', title='Регистрация')


# LOGIN // Вход в аккаунт
@registration.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # В реальных приложениях используйте хеширование!
            session['user_id'] = user.id
            flash('Авторизация успешна!', 'success')
            return redirect(url_for('main_page.home'))
        else:
            flash('Неверные данные! Попробуй ещё раз', 'danger')
    return render_template('login/login.html', title='Авторизация')


# LOGOUT // Выход из аккаунта
@registration.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # В реальных приложениях используйте хеширование!
            session.pop('user_id', None)
            flash('Вы успешно вышли из аккаунта', 'info')
            return redirect(url_for('main_page.home'))
        else:
            flash('Введите верный пароль', 'danger')
    return render_template('logout/logout.html', title='Выход из аккаунта')
