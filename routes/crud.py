from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from app_init import app, collection, mongo


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


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/qqq/<_id>')
def qqq(_id):
    id_ = ObjectId(_id)
    doc1 = mongo.db.docs.find_one_or_404({'_id' : id_})
    # print(url_for('file', filename=doc1['picture_name']))
    return f'''
        <h1>{doc1['picture_name']}</h1>
        <img src="{url_for('file', filename=doc1['picture_name'])}">
    '''


@app.route('/docs/<_id>/update', methods=['POST', 'GET'])  # редактирование документа
def update_doc(_id):
    if "email" not in session:  # если не вошел в систему, доступа нет
        return redirect(url_for("login"))   # нужно войти в систему

    id_ = ObjectId(_id)  # для корректного доступа к _id документа
    doc = collection.find_one({'_id': id_})  # находим документ с заденным _id

    doc1 = mongo.db.docs.find_one_or_404({'_id' : id_})
    url_pic = url_for('file', filename=doc1['picture_name'])
    if url_pic == '/file/':
        url_pic = '/static/default.jpg'

    if request.method == 'POST':
        title = request.form['title']  # присваиваем переменным значения из формы
        author = request.form['author']
        year = request.form['year']
        picture = request.files['picture']

        updating_doc = {  # создаем новый документ
            "title": title,
            "author": author,
            "year": year,
            "picture_name": picture.filename
        }

        try:
            if picture.filename:
                mongo.save_file(picture.filename, picture)
            else:
                doc1 = collection.find_one({'_id': id_})
                updating_doc['picture_name'] = doc1['picture_name']
            collection.update_one({'_id': id_}, {'$set': updating_doc})

            print('Document with _id: ' + str(id_) + ' has been updated successfully.')
            # изменяем значение полей документа в коллекции
            # и выводим в консоль его _id
            return redirect('/docs')  # переадресовываем на вывод коллекции документов
        except:
            print('An error occurred while updating the document.')
            return 'An error occurred while updating the document.'
    else:
        return render_template("update_doc.html", doc=doc, is_logged=True, url_pic=url_pic)  # передать документ в шаблон


@app.route('/create_doc', methods=['POST', 'GET'])  # создание документа
# добавляем метод POST обработки запоса (по умолчанию только GET)
def create_doc():
    if "email" not in session:  # если не вошел в систему, доступа нет
        return redirect(url_for("login"))   # нужно войти в систему

    if request.method == 'POST':
        title = request.form['title']  # присваиваем переменным значения из формы
        author = request.form['author']
        year = request.form['year']
        picture = request.files['picture']
        # print(picture)

        new_doc = {  # создаем новый документ
            "title": title,
            "author": author,
            "year": year,
            "picture_name": picture.filename
        }

        try:
            mongo.save_file(picture.filename, picture)
            result = collection.insert_one(new_doc).inserted_id
            print('Document with _id: ' + str(result) + ' has been created successfully.')
            # добавляем новый документ в коллекцию
            # и выводим в консоль его _id

            if 'profile_image' in request.files:
                profile_image = request.files['profile_image']
                mongo.save_file(profile_image.filename, profile_image)
                mongo.db.users.insert(
                    {'username': request.form.get('username'), 'profile_image_name': profile_image.filename})

            return redirect('/docs')  # переадресовываем на вывод коллекции документов
        except:
            print('An error occurred while creating the document.')
            return 'An error occurred while creating the document.'
    else:
        return render_template("create_doc.html", is_logged=True)  # будет обрабатывать как данные из формы,
        # так и прямой заход на страницу
