class User(object):

    @staticmethod
    def get_name():
        return "Daniil"

    @staticmethod
    def get_age():
        return 24 - 2


print(User.get_name())
