from webapp import app, db

# Создаем базу данных db (или подключаемся к ней)
# и запускаем приложение с циклом обработки событий
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
