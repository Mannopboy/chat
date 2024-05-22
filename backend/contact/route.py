from app import *
from backend.models.models import *


@app.route('/add_contact', methods=['POST'])
def add_contact():
    """
    :return:to add a new contact
    """
    user = online_user()
    name = request.form['name']
    username = request.form['username'].capitalize()
    chat_id = None
    if 'chat_id' in request.form:
        chat_id = request.form['chat_id']

    get_user = User.query.filter(User.username == username).first()
    if get_user:
        add = UserContacts(first_person=user.id, second_person=get_user.id, name=name)
        add.add()
        user_chat = UsersChat(first_person=user.id, second_person=get_user.id)
        user_chat.add()
        flash('Contact successfully saved!', 'success')
        return redirect(url_for('chat', chat_id=user_chat.id))
    else:
        flash('User did not join to app!', 'error')
        return redirect(url_for('chat', chat_id=chat_id))
