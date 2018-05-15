#! /usr/bin/python3
# -*- coding:utf-8 -*-
import tinydb as d
import os
import time
from . import CURRENT_DIR, random_selector, users_db
import uuid

db = d.TinyDB(os.path.join(CURRENT_DIR, "lottery.db"))
t_users = db.table('users')
t_awards = db.table('awards')


def current_ms():
    return int(round(time.time() * 1000))


def server_resp(status, msg, data=None):
    return {"status": status, "msg": msg, "data": data}


def reset():
    db.purge_tables()

    add_users(users_db.load())
    return server_resp(200, "success")


def users():
    t_users.clear_cache()
    return server_resp(200, "success", t_users.all())


def luckless_users():
    t_users.clear_cache()
    user = d.Query()
    return server_resp(200, "success", t_users.search(
        user['award_id'] == None))


def lucky_users(award_id=None):
    t_users.clear_cache()
    user = d.Query()
    if award_id is None:
        return server_resp(200, "success", t_users.search(
            user.award_id != None))
    else:
        return server_resp(200, "success", t_users.search(
            user.award_id == award_id))


def awards():
    t_awards.clear_cache()
    return server_resp(200, "success", t_awards.all())


def award(id):
    t_awards.clear_cache()
    award = t_awards.get(d.where('award_id') == id)
    return server_resp(200, "success", award) if award else server_resp(500, "不存在此奖品")


def update(uid, award_id):
    if not t_awards.get(d.Query().award_id == award_id):
        return server_resp(500, "不存在此奖品")
    if len(t_users.update({'award_id': award_id}, d.Query().uid == uid)) == 0:
        return server_resp(501, "不存在此用户")
    else:
        return server_resp(200, "success")


def revoke(uid):
    t_users.clear_cache()
    t_awards.clear_cache()

    user = t_users.get(d.where('uid') == uid)
    if not user:
        return server_resp(501, "不存在此用户")
    if user['award_id']:
        # award = t_awards.get(d.where('award_id') == user['award_id'])
        # if award:
        #     t_awards.update({'award_size': max(award['award_size']-1, 0)}, doc_ids=[award.doc_id])
        t_users.update({'award_id': None}, doc_ids=[user.doc_id])
    return server_resp(200, "success")


def add_awards(awards):
    t_awards.clear_cache()
    for award in awards:
        t_awards.insert({'award_id': uuid.uuid4().hex,
                         'award_name': award['award_name'],
                         'award_size': int(award['award_capacity']),
                         'award_capacity': int(award['award_capacity'])})
    return server_resp(200, "success")


def remove_awards(awards):
    t_awards.clear_cache()
    for award_id in awards:
        if len(lucky_users(award_id)['data']) == 0:
            t_awards.remove(d.where('award_id') == award_id)
        else:
            return server_resp(502, "不允许删除此奖品", {'award_id': award_id})
    return server_resp(200, "success")


def add_users(users):
    t_users.clear_cache()
    for user in users:
        t_users.insert({'uid': user['uid'].upper(),
                        'name': user['name'],
                        'award_id': None,
                        'role': user['role']})


def run():
    global start_time
    start_time = current_ms()
    return server_resp(200, "success")


def draw_lottery(award_id):
    if not start_time:
        return server_resp(503, "尚未开始抽奖")

    award = t_awards.get(d.where('award_id') == award_id)
    if not award:
        return server_resp(500, "不存在此奖项")

    if award['award_size'] <= 0:
        return server_resp(504, "该奖项已经抽完")

    luckies = random_selector.randomselect(current_ms() - start_time,
                                           luckless_users()['data'], award['award_capacity'])
    for lucky in luckies:
        update(lucky['uid'], award_id)
        lucky.update({'award_id': award_id})
    t_awards.update({'award_size': award['award_capacity'] - len(luckies)},
                    doc_ids=[award.doc_id])
    return server_resp(200, "success", luckies)

