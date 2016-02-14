#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cymysql
from flask import Flask, url_for, render_template, request, redirect
import cgi

mf = Flask(__name__)

config = {
    'db': {
        'host': '127.0.0.1',
        'user': 'mf',
        'passwd': '12345',
        'db': 'mf',
        'charset': 'utf8'
    }
}

def get_state_str(user_id, state):
    if state < 100:
        return 'новый'
    elif state < 200:
        return 'требуется генерация'
    elif state < 300:
        return 'идет генерация'
    elif state < 400:
        return 'готово, <a href="/static/u' + str(user_id) + '.tex">TeX</a>, ' + \
            '<a href="/static/u' + str(user_id) + '.pdf">PDF</a>, ' + \
            '<a href="/static/u' + str(user_id) + '.ps">PS</a>'
    else:
        return 'ОШИБКА'

@mf.route('/')
def index():
    dbc = config['db']
    conn = cymysql.connect(host=dbc['host'], user=dbc['user'], passwd=dbc['passwd'], db=dbc['db'], charset=dbc['charset'])
    cur = conn.cursor()
    cur.execute('select id, first_name, last_name, gender, school, grade, degree, state from users')
    users = []
    for r in cur.fetchall():
        users.append(r)
    content = ''
    content += '<table>\n'
    content += '<tr>' + ''.join(['<th>' + cgi.escape(x) + '</th>' for x in ['#', 'Имя', 'Пол', 'Школа', 'Класс', 'Степень', 'Состояние']]) + '</tr>\n'
    for e in users:
        user_id = e[0]
        first_name = e[1]
        last_name = e[2]
        gender = e[3]
        school = e[4]
        grade = e[5]
        degree = e[6]
        state = e[7]
        state_str = get_state_str(user_id, state)
        user_link = '<a href="/mf/user' + str(user_id) + '">' + first_name + ' ' + last_name + '</a>'
        content += '<tr><td>' + str(user_id) + '</td><td>' + user_link + '</td><td>' + gender + '</td><td>' + school + \
            '</td><td>' + grade + '</td><td>' + degree + '</td><td>' + state_str + '</td></tr>\n'
    content += '</table>\n'
    cur.close()
    conn.close()
    return render_template('template.html', title = 'Матпраздник', content = content)

@mf.route('/user<int:user_id>')
def user(user_id):
    dbc = config['db']
    conn = cymysql.connect(host=dbc['host'], user=dbc['user'], passwd=dbc['passwd'], db=dbc['db'], charset=dbc['charset'])
    cur = conn.cursor()
    cur.execute('select id, first_name, last_name, gender, school, grade, degree, state from users where id=%s', [user_id])
    e = False
    for r in cur.fetchall():
        e = r
    if e == False:
        return render_template('template.html', title = 'Ошибка', content = 'Такого пользователя нет')
    content = ''
    user_id = e[0]
    first_name = e[1]
    last_name = e[2]
    gender = e[3]
    school = e[4]
    grade = e[5]
    degree = e[6]
    state = e[7]
    state_str = get_state_str(user_id, state)
    content += '<form action="/mf/edit_user" method="POST">\n'
    content += '    <table>\n'
    content += '        <input type="hidden" name="id" value="' + str(user_id) + '" />\n'
    content += '        <tr><td>Имя</td><td><input type="text" name="first_name" value="' + cgi.escape(first_name) + '" /></td></tr>\n'
    content += '        <tr><td>Фамилия</td><td><input type="text" name="last_name" value="' + cgi.escape(last_name) + '" /></td></tr>\n'
    content += '        <tr><td>Пол</td><td><input type="text" name="gender" value="' + cgi.escape(gender) + '" /></td></tr>\n'
    content += '        <tr><td>Школа</td><td><input type="text" name="school" value="' + cgi.escape(school) + '" /></td></tr>\n'
    content += '        <tr><td>Класс</td><td><input type="text" name="grade" value="' + cgi.escape(grade) + '" /></td></tr>\n'
    content += '        <tr><td>Степень диплома</td><td><input type="text" name="degree" value="' + cgi.escape(degree) + '" /></td></tr>\n'
    content += '        <tr><td>Состояние</td><td>' + cgi.escape(state_str) + '</td></tr>\n'
    content += '        <tr><td><input type="submit" value="Обновить информацию" /></td><td></td></tr>\n'
    content += '    </table>\n'
    content += '</form>\n'
    cur.close()
    conn.close()
    return render_template('template.html', title = 'Матпраздник', content = content)

@mf.route('/edit_user', methods = ['POST'])
def edit_user():
    dbc = config['db']
    conn = cymysql.connect(host=dbc['host'], user=dbc['user'], passwd=dbc['passwd'], db=dbc['db'], charset=dbc['charset'])
    cur = conn.cursor()
    user_id = request.form['id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    school = request.form['school']
    grade = request.form['grade']
    degree = request.form['degree']
    state = 100
    cur.execute('update users set first_name=%s, last_name=%s, gender=%s, school=%s, grade=%s, degree=%s, state=%s where id=%s', \
        [first_name, last_name, gender, school, grade, degree, str(state), str(user_id)])
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/user' + str(user_id), code = 302)
    
if __name__ == '__main__':
    mf.debug = True
    mf.run(host='0.0.0.0',port=5200)
