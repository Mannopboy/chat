from app import *
from backend.models.models import *
from backend.models.settings import *
from werkzeug.security import generate_password_hash, check_password_hash


def online_user():
    """
    to filter User model by session
    :return:
    """
    user = None
    if 'username' in session:
        user = User.query.filter(User.username == session['username']).first()
    return user


@app.route('/', defaults={'chat_id': 0}, methods=['POST', 'GET'])
@app.route('/<int:chat_id>', methods=['POST', 'GET'])
def chat(chat_id):  # put application's code here
    """

    :param chat_id: to filter UsersChat model
    :return: user's chat list and contact list
    """
    user = online_user()
    if not user:
        return redirect(url_for('sign'))
    user_chat = None
    username = ''
    user_status = ''
    if chat_id:
        user_chat = UsersChat.query.filter(UsersChat.id == chat_id).first()
        session['chat_id'] = user_chat.id
        if user_chat.first and user_chat.first.id != user.id:
            username = user_chat.first.username
            user_status = user_chat.first.status.strftime("%H:%M")
        else:
            username = user_chat.second.username
            if user_chat.second.status:
                user_status = user_chat.second.status.strftime("%H:%M")
            else:
                user_status = None
    user_chats = UsersChat.query.filter(
        or_(UsersChat.first_person == user.id, UsersChat.second_person == user.id)).order_by(desc(UsersChat.id)).all()

    filtered_list = filter_chat(chat_id)
    user_contacts = UserContacts.query.filter(UserContacts.first_person == user.id).order_by(UserContacts.id).all()
    return render_template('basic.html', user_chats=iterate_models(user_chats, user), user_messages=filtered_list,
                           user=user, chat_id=chat_id, user_chat=user_chat, user_contacts=user_contacts,
                           now=datetime.now(), user_status=user_status, username=username)


@app.route('/sign', defaults={'type_request': "sign_in"}, methods=['POST', 'GET'])
@app.route('/sign/<type_request>', methods=['POST', 'GET'])
def sign(type_request):
    """
    this function is for both register and login
    :param type_request: to separate functions
    :return:
    """
    if request.method == "POST":
        username = request.form.get('username').capitalize()
        password = request.form.get('password')
        if type_request == "sign_in":
            user = User.query.filter(User.username == username).first()
            if user:
                if check_password_hash(user.password, password=password):
                    session['username'] = username
                    flash('Welcome to Chat App', 'success')
                    return redirect(url_for('chat'))
                else:
                    flash('Username or password is incorrect !', 'error')
                    return redirect(url_for('sign', type_request=type_request))

            else:
                flash('Username does not exist !', 'error')
                return redirect(url_for('sign', type_request=type_request))

        else:
            exist_user = User.query.filter(User.username == username).first()
            if not exist_user:
                exist_user = User(username=username, password=generate_password_hash(password, method="sha256"))
                exist_user.add()
            session['username'] = username

            return redirect(url_for('chat'))
    return render_template('sign-in_up.html', type_request=type_request)


@socketio.on("connect")
def connect():
    """
    to connect room of package flask-socketio
    :return:
    """
    chat_id = session.get('chat_id')
    user = online_user()
    if not chat_id or not user:
        return
    if not chat_id:
        leave_room(chat_id)
        return
    join_room(chat_id)
    print('connect')

    send({"username": user.username, "type": "connect"}, to=chat_id)


@socketio.on('message')
def message(data):
    """
    User can send message and another user can view it
    :param data: infos to create msg and update status msg
    :return: created msg and updated msg
    """
    user = online_user()
    chat_id = data['data']['chat_id']
    get_chat = UsersChat.query.filter(UsersChat.id == chat_id).first()
    get_chat = UsersChat.query.filter(UsersChat.id == chat_id).first()
    if data['data']['type'] == "create_msg":

        message_get = UsersMessages(user_id=user.id, text=data['data']['msg'], chat_id=get_chat.id, date=datetime.now())
        message_get.add()

        exist_day = UsersMessages.query.filter(
            extract('day', UsersMessages.date) == int(message_get.date.strftime("%d")),
            extract('month', UsersMessages.date) == int(message_get.date.strftime("%m")),
            extract('year', UsersMessages.date) == int(message_get.date.strftime("%Y")),
            UsersMessages.id != message_get.id).first()

        if exist_day:
            info = {
                "id": message_get.id,
                "text": message_get.text,
                "time": message_get.date.strftime("%H:%M"),

                "user": {
                    "id": message_get.user.id,
                    "username": message_get.user.username
                },
                "day": None,

            }
        else:
            info = {

                "id": message_get.id,
                "text": message_get.text,
                "time": message_get.date.strftime("%H:%M"),

                "user": {
                    "id": message_get.user.id,
                    "username": message_get.user.username
                },
                "day": message_get.date.strftime("%Y-%m-%d"),

            }
        send({"info": info, "type": data['data']['type']}, to=get_chat.id)
    else:
        print(data)
        msg_id = data['data']['msg_id']
        username = data['data']['username']
        user = User.query.filter(User.username == username).first()
        msg_get = UsersMessages.query.filter(UsersMessages.id == msg_id).first()
        exist_seen = SeenMessages.query.filter(SeenMessages.user_id == user.id, SeenMessages.msg_id == msg_id).first()
        if not exist_seen:
            exist_seen = SeenMessages(user_id=user.id, msg_id=msg_id)
            exist_seen.add()
            filter_msg = filter_chat(msg_get.chat_id, status=True)
            send({"msg_id": msg_get.id, "user": username, "type": data['data']['type']}, to=get_chat.id)


@app.route('/logout')
def logout():
    """
    log out function
    :return:
    """
    session.clear()
    return redirect(url_for('sign'))


@socketio.on('disconnect')
def disconnect():
    """
    when user leaves chat this funtion updates user's status
    :return:
    """
    chat_id = session.get('chat_id')
    user = online_user()
    if user:
        user.status = datetime.now()
        db.session.commit()

    send({"username": user.username, "time": user.status.strftime("%H:%M"), "type": "disconnect"}, to=chat_id)
