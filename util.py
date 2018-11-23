def get_user_from_message(update):
    return update.message.from_user


def get_user_from_callback_query(update):
    return update.callback_query.from_user