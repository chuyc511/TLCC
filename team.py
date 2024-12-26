class Team(object):
    date = None
    member_a = None
    member_b = None
    member_c = None
    member_d = None
    member_e = None
    member_f = None

    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)