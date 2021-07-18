from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from app_init import app, collection


@app.route('/docs')  # все документы на сайте
def docs():
    results = collection.find()  # создаем объект, кот. обращается к коллекции
    docs_col = [result for result in results]  # создаем список документов из коллекции
    print(docs_col)  # выводим список в консоль
    is_logged = "email" in session
    return render_template("docs.html", docs_col=docs_col, is_logged=is_logged)  # передаем список в шаблон (доступ по имени docs)


@app.route('/docs/<_id>/delete')  # удаление документа
def delete(_id):
    if "email" not in session:  # если не вошел в систему, доступа нет
        return redirect(url_for("login"))   # нужно войти в систему

    id_ = ObjectId(_id)  # для корректного доступа к _id документа

    try:
        collection.delete_one({'_id': id_})
        print('Document with _id: ' + _id + ' has been deleted successfully.')
        # удаляем документ с заданным _id в коллекцию
        # и выводим в консоль его _id
        return redirect('/docs')  # переадресовываем на вывод коллекции документов
    except:
        print('An error occurred while deleting the document')
        return 'An error occurred while deleting the document'


@app.route('/docs/<_id>/update', methods=['POST', 'GET'])  # редактирование документа
def update_doc(_id):
    if "email" not in session:  # если не вошел в систему, доступа нет
        return redirect(url_for("login"))   # нужно войти в систему

    id_ = ObjectId(_id)  # для корректного доступа к _id документа
    doc = collection.find_one({'_id': id_})  # находим документ с заденным _id
    print(doc)
    if request.method == 'POST':
        title = request.form['title']  # присваиваем переменным значения из формы
        author = request.form['author']
        year = request.form['year']

        updating_doc = {  # создаем новый документ
            "title": title,
            "author": author,
            "year": year
        }

        try:
            collection.update_one({'_id': id_}, {'$set': updating_doc})
            print('Document with _id: ' + str(id_) + ' has been updated successfully.')
            # изменяем значение полей документа в коллекции
            # и выводим в консоль его _id
            return redirect('/docs')  # переадресовываем на вывод коллекции документов
        except:
            print('An error occurred while updating the document.')
            return 'An error occurred while updating the document.'
    else:
        return render_template("update_doc.html", doc=doc, is_logged=True)  # передать документ в шаблон


@app.route('/create_doc', methods=['POST', 'GET'])  # создание документа
# добавляем метод POST обработки запоса (по умолчанию только GET)
def create_doc():
    if "email" not in session:  # если не вошел в систему, доступа нет
        return redirect(url_for("login"))   # нужно войти в систему

    if request.method == 'POST':
        title = request.form['title']  # присваиваем переменным значения из формы
        author = request.form['author']
        year = request.form['year']

        new_doc = {  # создаем новый документ
            "title": title,
            "author": author,
            "year": year
        }

        try:
            result = collection.insert_one(new_doc).inserted_id
            print('Document with _id: ' + str(result) + ' has been created successfully.')
            # добавляем новый документ в коллекцию
            # и выводим в консоль его _id
            return redirect('/docs')  # переадресовываем на вывод коллекции документов
        except:
            print('An error occurred while creating the document.')
            return 'An error occurred while creating the document.'
    else:
        return render_template("create_doc.html", is_logged=True)  # будет обрабатывать как данные из формы,
        # так и прямой заход на страницу
