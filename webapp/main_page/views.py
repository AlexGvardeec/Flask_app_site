from flask import Blueprint, render_template

# Создаю мини-приложение main_page для управления главной страницей
main_page = Blueprint('main page', __name__)


# Определяю маршрут для главной страницы
@main_page.route('/')
def home():
    return render_template('main_page.html')
