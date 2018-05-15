#! /usr/bin/python3
# -*- coding:utf-8 -*-
import bottle as b
import os
from . import CURRENT_DIR, lottery

app = b.Bottle()


@app.route('/')
def index():
    return b.static_file('welcome.html', os.path.join(CURRENT_DIR, "templates"))


@app.route('/update', method='POST')
def update():
    b.abort(403)


@app.route('/revoke')
def revoke():
    uid = b.request.params.get('uid')
    if not uid:
        b.abort(403)
    return lottery.revoke(id)


@app.route('/users')
def users():
    return lottery.users()


@app.route('/lucky_users')
def lucky_users():
    award_id = b.request.params.get('award_id')
    return lottery.lucky_users(award_id)


@app.route('/luckless_users')
def luckless_users():
    return lottery.luckless_users()


@app.route('/awards')
def awards():
    return lottery.awards()


@app.route('/award')
def award():
    award_id = b.request.params.get('award_id')
    if award_id is None:
        b.abort(403)
    return lottery.award(award_id)


@app.route('/add_awards', method='POST')
def add_awards():
    return lottery.add_awards(b.request.json['awards'])


@app.route('/add_award')
def add_award():
    name = b.request.params.getunicode('award_name')
    award_capacity = b.request.params.get('award_capacity')
    if None in (name, award_capacity):
        b.abort(403)
    return lottery.add_awards([{'award_name': name, 'award_capacity': award_capacity}])


@app.route('/remove_award')
def remove_award():
    award_id = b.request.params.get('award_id')
    if award_id is None:
        b.abort(403)
    return lottery.remove_awards([award_id])


@app.route('/reset')
def reset():
    return lottery.reset()


@app.route('/run')
def run():
    return lottery.run()


@app.route('/draw_lottery')
def draw_lottery():
    award_id = b.request.params.get('award_id')
    if award_id is None:
        b.abort(403)
    return lottery.draw_lottery(award_id)


@app.route('/static/<filepath:path>')
def callback(filepath):
    return b.static_file(filepath, os.path.join(CURRENT_DIR, "static"))


@app.route('/templates/<filepath:path>')
def callback(filepath):
    return b.static_file(filepath, os.path.join(CURRENT_DIR, "templates"))


@b.error
def error403(error):
    return "非法访问 " + error


def run(host, port, debug):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run('0.0.0.0', 8080, True)
