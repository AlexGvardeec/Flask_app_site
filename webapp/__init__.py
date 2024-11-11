from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Создаем приложение app с помощью Flask
app = Flask(__name__, static_folder='static', static_url_path='/res', )

# Добавляем конфигурации в приложение
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Используем SQLite для простоты
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Необходим для flash-сообщений

# Создаем для приложения базу данных db с помощью модуля flask-SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Импортируем мини-приложения для управления отдельными частями app
from webapp.main_page.views import main_page
from webapp.market.views import market
from webapp.about_us.views import about_us
from webapp.contacts.views import contacts
from webapp.registration.views import registration

# Регистрируем мини-приложения в приложении app
app.register_blueprint(main_page)
app.register_blueprint(market)
app.register_blueprint(about_us)
app.register_blueprint(contacts)
app.register_blueprint(registration)

# Дополнительно импортируем модули для исключения циклических связей
import webapp.main_page.views
import webapp.market.views
import webapp.about_us.views
import webapp.contacts.views
import webapp.registration.views
