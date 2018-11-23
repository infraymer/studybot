from pymongo import MongoClient

import util

client = MongoClient()
db = client.bot


class State:
    START = 'start'
    LESSON = 'lesson'
    QUESTION = 'question'
    ANSWER = 'answer'


class User:
    @staticmethod
    def get_state(user):
        return db.users.find_one({'chat_id': user.id})['state']

    @staticmethod
    def get_task(user):
        try:
            task_index = db.users.find_one({'chat_id': user.id})['task']
            task = get_tasks()[task_index]
            return task, task_index
        except:
            return None, None

    @staticmethod
    def next_task(user):
        task_index = db.users.find_one({'chat_id': user.id})['task']
        task_index = task_index + 1
        db.users.update({'chat_id': user.id}, {'$set': {'task': task_index, 'question': 0}})

    @staticmethod
    def next_question(user):
        q_index = db.users.find_one({'chat_id': user.id})['question']
        q_index = q_index + 1
        db.users.update({'chat_id': user.id}, {'$set': {'question': q_index}})

    @staticmethod
    def get_question(user):
        try:
            task_index = db.users.find_one({'chat_id': user.id})['task']
            q_index = db.users.find_one({'chat_id': user.id})['question']
            question = get_tasks()[task_index]['questions'][q_index]
            return question, q_index
        except:
            return None, None

    @staticmethod
    def set_state(user, state):
        post = {'state': state}
        db.users.update({'chat_id': user.id}, {'$set': post})


def get_tasks():
    return db.tasks.find()


def get_users():
    return db.users.find()


def get_first_task():
    try:
        task = db.tasks.find()[0]
        return task
    except:
        return None


def update_video_state(update):
    user = util.get_user_from_callback_query(update)
    post = {'state': {'video': True}}
    db.users.update({'chat_id': user.id}, {'$set': post})


def user_state(update):
    user = util.get_user_from_message(update)
    return db.users.find_one({'chat_id': user.id})['state']


def add_user(user):
    try:
        post = {
            'chat_id': user.id,
            'username': user.username,
            'fullname': user.full_name,
            'state': State.START,
            'task': 0,
            'question': 0
        }
        db.users.update(
            {'chat_id': user.id},
            {'$set': post}, upsert=True)
        # db.users.save(post)
    except Exception as err:
        print(err)
