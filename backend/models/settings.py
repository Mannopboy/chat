from .models import *


def iterate_models(model, user):
    """
    function receives db model list and returns it with object form
    :param model:
    :param user: to get second user data and number of not received messages

    :return:
    """
    list = []
    for subject in model:
        list.append(subject.convert_json(user=user))
    return list


def filter_chat(chat_id, status=False):
    """
    function that filters messages by day
    :param chat_id: to filter messages by chat id
    :param status: to filter messages by received and not received
    :return: messages in object form
    """
    if status:
        user_messages = UsersMessages.query.filter(UsersMessages.chat_id == chat_id,
                                                   UsersMessages.messages_status != None).order_by(
            UsersMessages.id).all()
    else:
        user_messages = UsersMessages.query.filter(UsersMessages.chat_id == chat_id).order_by(
            UsersMessages.id).all()
    message_list = []
    for msg in user_messages:
        status = False
        seen_num = 0
        if msg.messages_status:
            status = True
            seen_num = len(msg.messages_status)
        info = {
            "day": msg.date.strftime("%Y-%m-%d"),

            "messages": [{
                "id": msg.id,
                "text": msg.text,
                "time": msg.date.strftime("%H:%M"),
                "status": status,
                "seen_num": seen_num,
                "user": {
                    "id": msg.user.id,
                    "username": msg.user.username
                },
            }, ]
        }
        message_list.append(info)

    # to remove duplicated days

    filtered_list = []
    for message in message_list:
        added_to_existing = False
        for merged in filtered_list:
            if merged['day'] == message['day']:
                added_to_existing = True
                for message in message['messages']:
                    merged['messages'].append(message)
                break
            if added_to_existing:
                break
        if not added_to_existing:
            filtered_list.append(message)
    return filtered_list
