class Team(object):
    date = None
    member_a = None
    member_b = None
    member_c = None
    member_d = None
    member_e = None
    member_f = None
    member_a_name = None
    member_b_name = None
    member_c_name = None
    member_d_name = None
    member_e_name = None
    member_f_name = None

    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)