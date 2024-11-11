from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from webapp import db
from webapp.registration.models import Category, Bikes, Parts, Lessons
from webapp.registration.views import login

# Создаем мини-приложение market для управления магазином
market = Blueprint('market', __name__)


# Создаем маршрут к магазину с выводом доступных категорий
@market.route('/market/')
def market_page():
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template('market/market.html',
                           title='Магазин', categories=categories)


# Создаем маршрут согласно выбранной категории
@market.route('/market/<category>/', methods=['GET', 'POST'])
def category_page(category):
    categories = Category.query.order_by(Category.name.asc()).all()
    if not categories:
        abort(404)
    if category == 'bikes':
        return redirect(url_for('market.bikes_page'))
    elif category == 'parts':
        return redirect(url_for('market.parts_page'))
    elif category == 'lessons':
        return redirect(url_for('market.lessons_page'))
    elif category == 'category_create':
        return redirect(url_for('category_create'))
    elif category == 'category_list':
        return redirect(url_for('market.category_list'))
    elif category == 'category_update':
        return redirect(url_for('market.category_update'))
    elif category == 'category_delete':
        return redirect(url_for('market.category_delete'))


# CREATE CATEGORY // Создаем новую категорию в магазине
@market.route('/market/category_create/', methods=['GET', 'POST'])
def category_create():
    if not login:
        flash('Авторизуйся для доступа к этой странице', 'danger')
    if request.method == 'POST':
        name = request.form.get('category_name')
        route = request.form.get('category_route')
        if not name or not route:
            flash('Пожалуйста заполни все поля', 'danger')
        category = Category(name=name, route=route)
        category_count = Category.query.filter_by(name=name).count()
        if category_count > 0:
            flash('Такая категория уже существует. Выбери другое имя', 'danger')
        else:
            db.session.add(category)
            db.session.commit()
            flash('Категория добавлена!', 'success')
    return render_template('market/category_create.html', title='Добавление категории')


# DELETE CATEGORY // Удаляем категорию category_name из базы данных
@market.route('/market/category_delete/', methods=['GET', 'POST'])
def category_delete():
    if request.method == 'POST':
        name = request.form.get('category_name')
        if not name:
            flash('Пожалуйста укажи имя категории для удаления', 'danger')
            return redirect(url_for('category_delete'))
        category = Category.query.filter_by(name=name).first()
        category_count = Category.query.filter_by(name=name).count()
        if category_count == 0:
            flash('Такой категории нет в базе', 'danger')
        else:
            db.session.delete(category)
            db.session.commit()
            flash('Категория удалена!', 'success')
    return render_template('market/category_delete.html', title='Удаление категории')


# LIST CATEGORY // Вывести список существующих категорий
@market.route('/market/category_list/', methods=['GET', 'POST'])
def category_list():
    if request.method == 'POST':
        categories_list = Category.query.order_by(Category.name.asc()).all()
        for category in categories_list:
            flash(f'{category.name}, {category.route}', 'success')
    return render_template('market/category_list.html', title='Список категорий')


# EDIT CATEGORY // Изменение данных категории
@market.route('/market/category_update/', methods=['GET', 'POST'])
def category_update():
    if request.method == 'POST':
        name_old = request.form.get('category_name_old')
        name_new = request.form.get('category_name_new')
        if not all([name_old, name_new]):
            flash('Пожалуйста заполните все поля', 'danger')
            return redirect(url_for('market.category_update'))
        category = Category.query.filter_by(name=name_old).first()
        if not category:
            flash('Такой категории не существует. Укажи другое имя', 'danger')
        else:
            category.name = name_new
        try:
            db.session.commit()
            flash('Категория изменена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении категории: {str(e)}', 'danger')
    return render_template('market/category_update.html', title='Изменение категории')


# Создаем маршрут к категории Велосипеды
@market.route('/market/bikes/')
def bikes_page():
    bikes_ = Bikes.query.order_by(Bikes.id.asc()).all()
    # if not bikes_:
    #     abort(404)
    return render_template('market/market_bikes.html',
                           title='Велосипеды', bikes=bikes_)


# CREATE BIKE // Создание нового экземпляра к категории Bikes
@market.route('/market/bikes_create/', methods=['GET', 'POST'])
def bikes_create_page():
    if request.method == 'POST':
        # Получение данных нового экземпляра Bikes из форм
        bikes_name = request.form.get('bikes_name')
        bikes_about = request.form.get('bikes_about')
        bikes_price = request.form.get('bikes_price')
        # Проверка на заполненность всех полей
        if not all([bikes_name, bikes_about, bikes_price]):
            flash('Пожалуйста заполни все поля', 'danger')
            return redirect(url_for('market.bikes_create_page'))
        try:
            bikes_price = float(bikes_price)
            # Проверка на существование велосипеда с таким же именем
            bike_count = Bikes.query.filter_by(bikes_name=bikes_name).count()
            if bike_count > 0:
                flash('Такой велосипед уже существует. Выбери другое имя', 'danger')
            else:
                # Создание нового экземпляра Bikes
                bike = Bikes(
                    bikes_name=bikes_name,
                    bikes_about=bikes_about,
                    bikes_price=bikes_price,
                    category_id=0
                )
                # Добавление и сохранение в базе данных
                db.session.add(bike)
                db.session.commit()
                flash('Велосипед добавлен!', 'success')
                return redirect(url_for('market.bikes_page'))
        except ValueError:
            flash('Некорректное значение цены', 'danger')
    return render_template('market/bikes_create.html', title='Добавление велосипеда')


# EDIT BIKE // Изменение данных экземпляра в категории Bikes
@market.route('/market/bikes_update/', methods=['GET', 'POST'])
def bikes_update_page():
    if request.method == 'POST':
        bikes_name_old = request.form.get('bikes_name_old')
        bikes_name_new = request.form.get('bikes_name_new')
        bikes_about_new = request.form.get('bikes_about_new')
        bikes_price_new = request.form.get('bikes_price_new')
        bike = Bikes.query.filter_by(bikes_name=bikes_name_old).first()
        if not bike:
            flash('Такого велосипеда не существует. Укажи другое имя', 'danger')
        else:
            bike.bikes_name = bikes_name_new
            bike.bikes_about = bikes_about_new
            bike.bikes_price = bikes_price_new
            db.session.commit()
            flash('Данные велосипеда изменены!', 'success')
            return redirect(url_for('market.bikes_page'))
    return render_template('market/bikes_update.html', title='Изменение данных велосипеда')


# DELETE BIKE // Удаляем велосипед из категории Bikes
@market.route('/market/bikes_delete/', methods=['GET', 'POST'])
def bikes_delete_page():
    if request.method == 'POST':
        bikes_name = request.form.get('bikes_name')
        if not bikes_name:
            flash('Пожалуйста укажи имя категории для удаления', 'danger')
            return redirect(url_for('market.bikes_delete_page'))
        bike = Bikes.query.filter_by(bikes_name=bikes_name).first()
        bike_count = Bikes.query.filter_by(bikes_name=bikes_name).count()
        if bike_count == 0:
            flash('Такой категории нет в базе', 'danger')
        else:
            db.session.delete(bike)
            db.session.commit()
            flash('Категория удалена!', 'success')
            return redirect(url_for('market.bikes_page'))
    return render_template('market/bikes_delete.html', title='Удаление велосипеда')


# PARTS PAGE // Создаем маршрут к странице ЗАПЧАСТИ
@market.route('/market/parts/')
def parts_page():
    parts_ = Parts.query.order_by(Parts.id.asc()).all()
    if not parts_:
        abort(404)
    return render_template('market/market_parts.html',
                           title='Запчасти', parts=parts_)


# CREATE PART // Создание запчасти в категории ЗАПЧАСТИ
@market.route('/market/parts_create/', methods=['GET', 'POST'])
def parts_create_page():
    if request.method == 'POST':
        # Получение данных нового экземпляра Parts из форм
        parts_name = request.form.get('parts_name')
        parts_about = request.form.get('parts_about')
        parts_price = request.form.get('parts_price')
        # Проверка на заполненность всех полей
        if not all([parts_name, parts_about, parts_price]):
            flash('Пожалуйста заполни все поля', 'danger')
            return redirect(url_for('market.parts_create_page'))
        try:
            parts_price = float(parts_price)
            # Проверка на существование велосипеда с таким же именем
            bike_count = Parts.query.filter_by(parts_name=parts_name).count()
            if bike_count > 0:
                flash('Такая запчасть уже существует. Выбери другое имя', 'danger')
            else:
                # Создание нового экземпляра Parts
                part = Parts(
                    parts_name=parts_name,
                    parts_about=parts_about,
                    parts_price=parts_price,
                    category_id=0
                )
                # Добавление и сохранение в базе данных
                db.session.add(part)
                db.session.commit()
                flash('Запчасть добавлена!', 'success')
                return redirect(url_for('market.parts_page'))
        except ValueError:
            flash('Некорректное значение цены', 'danger')
    return render_template('market/parts_create.html', title='Добавление новой запчасти')


# EDIT PART // Изменение данных экземпляра в категории ЗАПЧАСТИ
@market.route('/market/parts_update/', methods=['GET', 'POST'])
def parts_update_page():
    if request.method == 'POST':
        parts_name_old = request.form.get('parts_name_old')
        parts_name_new = request.form.get('parts_name_new')
        parts_about_new = request.form.get('parts_about_new')
        parts_price_new = request.form.get('parts_price_new')
        part = Parts.query.filter_by(parts_name=parts_name_old).first()
        if not part:
            flash('Такой запчасти не существует. Укажи другое имя', 'danger')
        else:
            part.parts_name = parts_name_new
            part.parts_about = parts_about_new
            part.parts_price = parts_price_new
            db.session.commit()
            flash('Данные запчасти изменены!', 'success')
            return redirect(url_for('market.parts_page'))
    return render_template('market/parts_update.html', title='Изменение данных запчасти')


# DELETE PART // Удаляем экземпляр из категории ЗАПЧАСТИ
@market.route('/market/parts_delete/', methods=['GET', 'POST'])
def parts_delete_page():
    if request.method == 'POST':
        parts_name = request.form.get('parts_name')
        if not parts_name:
            flash('Укажи наименование запчасти для удаления', 'danger')
            return redirect(url_for('market.parts_delete_page'))
        part = Parts.query.filter_by(parts_name=parts_name).first()
        part_count = Parts.query.filter_by(parts_name=parts_name).count()
        if part_count == 0:
            flash('Такой запчасти нет в базе', 'danger')
            return redirect(url_for('market.parts_delete_page'))
        else:
            db.session.delete(part)
            db.session.commit()
            flash('Запчасть удалена из списка!', 'success')
            return redirect(url_for('market.parts_page'))
    return render_template('market/parts_delete.html', title='Удаление запчасти')


# LESSONS PAGE // Создание маршрута к странице ЗАНЯТИЯ
@market.route('/market/lessons/')
def lessons_page():
    lessons_ = Lessons.query.order_by(Lessons.id.asc()).all()
    if not lessons_:
        abort(404)
    return render_template('market/market_lessons.html', title='Занятия', lessons=lessons_)


# CREATE LESSON // Создание занятия в категории ЗАНЯТИЯ
@market.route('/market/lessons_create/', methods=['GET', 'POST'])
def lessons_create_page():
    if request.method == 'POST':
        # Получение данных нового экземпляра Lessons из форм
        lessons_name = request.form.get('lessons_name')
        lessons_about = request.form.get('lessons_about')
        lessons_price = request.form.get('lessons_price')
        # Проверка на заполненность всех полей
        if not all([lessons_name, lessons_about, lessons_price]):
            flash('Пожалуйста заполни все поля', 'danger')
            return redirect(url_for('market.lessons_create_page'))
        try:
            lessons_price = float(lessons_price)
            # Проверка на существование велосипеда с таким же именем
            lessons_count = Lessons.query.filter_by(lessons_name=lessons_name).count()
            if lessons_count > 0:
                flash('Такое занятие уже существует. Выбери другое имя', 'danger')
            else:
                # Создание нового экземпляра Lessons
                lesson = Lessons(
                    lessons_name=lessons_name,
                    lessons_about=lessons_about,
                    lessons_price=lessons_price,
                    category_id=0
                )
                # Добавление и сохранение в базе данных
                db.session.add(lesson)
                db.session.commit()
                flash('Занятие добавлено!', 'success')
                return redirect(url_for('market.lessons_page'))
        except ValueError:
            flash('Некорректное значение цены', 'danger')
    return render_template('market/lessons_create.html', title='Добавление нового занятия')


# EDIT LESSON // Изменение данных экземпляра в категории ЗАНЯТИЯ
@market.route('/market/lessons_update/', methods=['GET', 'POST'])
def lessons_update_page():
    if request.method == 'POST':
        lessons_name_old = request.form.get('lessons_name_old')
        lessons_name_new = request.form.get('lessons_name_new')
        lessons_about_new = request.form.get('lessons_about_new')
        lessons_price_new = request.form.get('lessons_price_new')
        lesson = Lessons.query.filter_by(lessons_name=lessons_name_old).first()
        if not lesson:
            flash('Такого занятия не существует. Укажи другое имя', 'danger')
        else:
            lesson.lessons_name = lessons_name_new
            lesson.lessons_about = lessons_about_new
            lesson.lessons_price = lessons_price_new
            db.session.commit()
            flash('Данные занятия изменены!', 'success')
            return redirect(url_for('market.lessons_page'))
    return render_template('market/lessons_update.html', title='Изменение данных занятия')


# DELETE LESSON // Удаляем экземпляр из категории ЗАНЯТИЯ
@market.route('/market/lessons_delete/', methods=['GET', 'POST'])
def lessons_delete_page():
    if request.method == 'POST':
        lessons_name = request.form.get('lessons_name')
        if not lessons_name:
            flash('Укажи наименование занятия для удаления', 'danger')
            return redirect(url_for('market.lessons_delete_page'))
        lesson = Lessons.query.filter_by(lessons_name=lessons_name).first()
        lesson_count = Lessons.query.filter_by(lessons_name=lessons_name).count()
        if lesson_count == 0:
            flash('Такого занятия нет в базе', 'danger')
            return redirect(url_for('market.lessons_delete_page'))
        else:
            db.session.delete(lesson)
            db.session.commit()
            flash('Занятие удалено из списка!', 'success')
            return redirect(url_for('market.lessons_page'))
    return render_template('market/lessons_delete.html', title='Удаление занятия')
