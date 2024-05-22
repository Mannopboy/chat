from app import *
from backend.models.models import *
from werkzeug.utils import secure_filename
import os


@app.route('/change_info/', methods=['POST'])
def change_info():
    """
    to change user datas
    :return:
    """
    user = online_user()
    username = request.form.get('username')
    name = request.form.get('name')
    img = request.files.get('img')
    chat_id = None
    if 'chat_id' in request.form:
        chat_id = request.form.get('chat_id')
    if img:
        filename = secure_filename(img.filename)
        folder = "static/img/upload"
        if not os.path.exists(folder):
            os.makedirs(folder)
        img_url = "/static/img/upload/" + filename
        app.config['UPLOADED_FOLDER'] = "static/img/upload"
        img.save(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
        user.img = img_url
        db.session.commit()
    user.username = username
    user.name = name
    db.session.commit()
    flash('User datas has successfully changed', 'success')
    return redirect(url_for('chat', chat_id=chat_id))


# extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]
#
# import os
# import sys
#
# sys.path.insert(0, os.path.abspath(".."))
# project = 'Chat App'
