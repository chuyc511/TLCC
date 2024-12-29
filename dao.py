import os

from dotenv import load_dotenv

import psycopg2
import psycopg2.extras

from user import User
from team import Team

load_dotenv()

def execute_script(script, parameters = None):

    res = []

    try:
        conn = psycopg2.connect(
            database = os.getenv('DATABASE_NAME', ''), 
            user = os.getenv('DATABASE_USER', ''),
            password = os.getenv('DATABASE_PASSWORD', ''), 
            host = os.getenv('DATABASE_HOST', ''), 
            port = int(os.getenv('DATABASE_PORT', '5432'))
        )

        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:

            cur.execute(script, parameters)

            if 'update' not in script and 'insert into' not in script:
                res = cur.fetchall()

        conn.commit()
    except Exception as error:
        print(f'connect error: {error}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

        return res

def query_users():
    query_user_script = '''select * from tlcc_user;'''
            
    result_list = []

    for record in execute_script(query_user_script):
        result_list.append(User(record))

    return result_list

def create_user(user_id, line_name, tianlong_name):
    create_user_script = '''
        insert into tlcc_user
        values (
            %(user_id)s,
            %(line_name)s,
            %(tianlong_name)s
        );
    '''
    execute_script(create_user_script, {
        'user_id': user_id,
        'line_name': line_name,
        'tianlong_name': tianlong_name
    })

def update_user(user_id, line_name, tianlong_name):
    update_user_script = '''
        update tlcc_user 
        set line_name = %(line_name)s,
            tianlong_name = %(tianlong_name)s
        where user_id = %(user_id)s;
    '''
    execute_script(update_user_script, {
        'user_id': user_id,
        'line_name': line_name,
        'tianlong_name': tianlong_name
    })

def query_team(date):
    query_team_script = '''
        select 
            date,
            member_a,
            tca.tianlong_name as member_a_name,
            member_b,
            tcb.tianlong_name as member_b_name,
            member_c,
            tcc.tianlong_name as member_c_name,
            member_d,
            tcd.tianlong_name as member_d_name,
            member_e,
            tce.tianlong_name as member_e_name,
            member_f,
            tcf.tianlong_name as member_f_name
        from tlcc_team as tt
            left join tlcc_user as tca
                on tca.user_id = tt.member_a
            left join tlcc_user as tcb
                on tcb.user_id = tt.member_b
            left join tlcc_user as tcc
                on tcc.user_id = tt.member_c
            left join tlcc_user as tcd
                on tcd.user_id = tt.member_d
            left join tlcc_user as tce
                on tce.user_id = tt.member_e
            left join tlcc_user as tcf
                on tcf.user_id = tt.member_f 
        where date = %(date)s;
    '''
    result_list = execute_script(query_team_script, { 'date': date })

    if len(result_list) > 0:
        return Team(result_list[0])

    return Team({})

def create_team(date, member_a):
    create_team_script = '''
        insert into tlcc_team (
            date,
            member_a
        )
        values (
            %(date)s,
            %(member_a)s
        );
    '''
    execute_script(create_team_script, {
        'date': date,
        'member_a': member_a
    })

def update_team_member_a(date, member_a):
    update_team_script = '''
        update tlcc_team 
        set member_a = %(member_a)s
        where date = %(date)s;
    '''
    execute_script(update_team_script, {
        'date': date,
        'member_a': member_a
    })

def update_team_member_b(date, member_b):
    update_team_script = '''
        update tlcc_team 
        set member_b = %(member_b)s
        where date = %(date)s;
    '''
    execute_script(update_team_script, {
        'date': date,
        'member_b': member_b
    })

def update_team_member_c(date, member_c):
    update_team_script = '''
        update tlcc_team 
        set member_c = %(member_c)s
        where date = %(date)s;
    '''
    execute_script(update_team_script, {
        'date': date,
        'member_c': member_c
    })

def update_team_member_d(date, member_d):
    update_team_script = '''
        update tlcc_team 
        set member_d = %(member_d)s
        where date = %(date)s;
    '''
    execute_script(update_team_script, {
        'date': date,
        'member_d': member_d
    })

def update_team_member_e(date, member_e):
    update_team_script = '''
        update tlcc_team 
        set member_e = %(member_e)s
        where date = %(date)s;
    '''
    execute_script(update_team_script, {
        'date': date,
        'member_e': member_e
    })

def update_team_member_f(date, member_f):
    update_team_script = '''
        update tlcc_team 
        set member_f = %(member_f)s
        where date = %(date)s;
    '''
    execute_script(update_team_script, {
        'date': date,
        'member_f': member_f
    })