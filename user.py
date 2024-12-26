class User(object):
    user_id = None
    line_name = None
    tianlong_name = None

    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)