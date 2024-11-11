from webapp import db


# Создаем класс User для возможности хранения данных пользователей
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Пароли обычно хранятся в зашифрованном виде

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


# Создаем класс Category для нашего магазина
class Category(db.Model):
    __tablename__ = 'categories_list'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    route = db.Column(db.String(30), nullable=False)
    bikes = db.relationship('Bikes', back_populates='category')
    parts = db.relationship('Parts', back_populates='category')
    lessons = db.relationship('Lessons', back_populates='category')

    def __init__(self, name, route):
        self.name = name
        self.route = route

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


# Создаем подкласс Bikes, указываем связь с классом Category
class Bikes(db.Model):
    __tablename__ = 'bikes_list'
    id = db.Column(db.Integer(), primary_key=True)
    bikes_name = db.Column(db.String(30), nullable=False)
    bikes_about = db.Column(db.String(200), nullable=False)
    bikes_price = db.Column(db.Float())
    category_id = db.Column(db.Integer, db.ForeignKey('categories_list.id'))
    category = db.relationship('Category', back_populates='bikes')

    def __init__(self, bikes_name, bikes_about, bikes_price, category_id):
        self.bikes_name = bikes_name
        self.bikes_about = bikes_about
        self.bikes_price = bikes_price
        self.category_id = category_id

    def __repr__(self):
        return "<{}:{}>".format(
                                self.bikes_name,
                                self.bikes_about,
                                self.bikes_price,
                                self.category_id
                                )


# Создаем подкласс Parts, указываем связь с классом Category
class Parts(db.Model):
    __tablename__ = 'parts_list'
    id = db.Column(db.Integer(), primary_key=True)
    parts_name = db.Column(db.String(30), nullable=False)
    parts_about = db.Column(db.String(200), nullable=False)
    parts_price = db.Column(db.Float())
    category_id = db.Column(db.Integer, db.ForeignKey('categories_list.id'))
    category = db.relationship('Category', back_populates='parts')

    def __init__(self, parts_name, parts_about, parts_price, category_id):
        self.parts_name = parts_name
        self.parts_about = parts_about
        self.parts_price = parts_price
        self.category_id = category_id

    def __repr__(self):
        return "<{}:{}>".format(
                                self.parts_name,
                                self.parts_about,
                                self.parts_price,
                                self.category_id
                                )


# Создаем подкласс Lessons, указываем связь с классом Category
class Lessons(db.Model):
    __tablename__ = 'lessons_list'
    id = db.Column(db.Integer(), primary_key=True)
    lessons_name = db.Column(db.String(30), nullable=False)
    lessons_about = db.Column(db.String(200), nullable=False)
    lessons_price = db.Column(db.Float())
    category_id = db.Column(db.Integer, db.ForeignKey('categories_list.id'))
    category = db.relationship('Category', back_populates='lessons')

    def __init__(self, lessons_name, lessons_about, lessons_price, category_id):
        self.lessons_name = lessons_name
        self.lessons_about = lessons_about
        self.lessons_price = lessons_price
        self.category_id = category_id

    def __repr__(self):
        return "<{}:{}>".format(
                                self.lessons_name,
                                self.lessons_about,
                                self.lessons_price,
                                self.category_id
                                )