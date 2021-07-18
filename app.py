from app_init import app
import routes

if __name__ == "__main__":  # если программа запускается через этот файл
    app.run(debug=True)  # запуск локального сервера в режиме отладки (вывод инф-ции об ошибках)
