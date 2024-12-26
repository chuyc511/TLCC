chinese_week = {
    1: '一',
    2: '二',
    3: '三',
    4: '四',
    5: '五',
    6: '六',
    7: '日',
}

def get_team_message(team):

    weekday = team.date.isoweekday()

    transfer_date_str = team.date.strftime('%Y-%m-%d') + '(' + chinese_week[weekday] + ')'

    res_str = f'{transfer_date_str} 一條副本\n'

    if weekday <= 5:
        res_str += 'Y寶箱19:30  N寶箱19:43'
    else:
        res_str += 'Y寶箱13:00  N寶箱13:13'
    
    res_str += '\n目前隊員:'

    if team.member_a is not None:
        res_str += f'\n{team.member_a_name}'
    if team.member_b is not None:
        res_str += f'\n{team.member_b_name}'
    if team.member_c is not None:
        res_str += f'\n{team.member_c_name}'
    if team.member_d is not None:
        res_str += f'\n{team.member_d_name}'
    if team.member_e is not None:
        res_str += f'\n{team.member_e_name}'
    if team.member_f is not None:
        res_str += f'\n{team.member_f_name}'

    res_str += f'\n\n目前指令有:\n/Team 查看當天組隊\n/+1 加入\n/-1 退出'

    return res_str