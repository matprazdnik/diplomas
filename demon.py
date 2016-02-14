#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cymysql
from flask import Flask, url_for, render_template, request
import cgi
import hashlib
import time
import smtplib
from email.mime.text import MIMEText
from subprocess import call

config = {
    'db': {
        'host': '127.0.0.1',
        'user': 'mf',
        'passwd': '12345',
        'db': 'mf',
        'charset': 'utf8'
    }
}

dbc = config['db']
conn = cymysql.connect(host=dbc['host'], user=dbc['user'], passwd=dbc['passwd'], db=dbc['db'], charset=dbc['charset'])
cur = conn.cursor()
cur.execute ('select id, first_name, last_name, gender, school, grade, degree, state from users where state >= 100 and state < 200 limit 2000')
users = cur.fetchall ()
for e in users:
  user_id = e[0]
  first_name = e[1]
  last_name = e[2]
  gender = e[3]
  if gender == 'м' or gender == 'М':
    gender = 'ученик'
  elif gender == 'ж' or gender == 'Ж':
    gender = 'ученица'
  school = e[4]
  grade = e[5]
  degree = e[6]
  if int (degree) >= 11:
    degree = 'первой степени'
  elif int (degree) >= 5:
    degree = 'второй степени'
  elif int (degree) >= 2:
    degree = 'третьей степени'
  elif int (degree) > 0:
    degree = ''
  else:
    continue
  state = e[7]
  
  cur.execute ('update users set state = 200 where id=%s', [str (user_id)])
  conn.commit ()
  
  file_name = 'u' + str (user_id) + ''
  tex = open (file_name + '.tex', mode = 'w', encoding = 'utf-8')
  tex.write ('\\documentclass[a4paper,landscape]{article}\n\n')
  tex.write ('\\usepackage[utf8]{inputenc}\n')
  tex.write ('\\usepackage[T2A]{fontenc}\n')
  tex.write ('\\usepackage[top=0.69in,bottom=0.69in,left=1in,right=1in]{geometry}\n')
  tex.write ('\\usepackage{graphicx}\n\n')
  tex.write ('\\pagestyle{empty}\n\n')
  tex.write ('\\begin{document}\n')
  tex.write ('{\n')
  tex.write ('\\noindent\n')
  tex.write ('Московское математическое общество\\\\\n')
  tex.write ('Департамент образования города Москвы\\\\\n')
  tex.write ('Московский государственный университет им. М. В. Ломоносова\\\\\n')
  tex.write ('Механико-математический факультет\\\\\n')
  tex.write ('Центр педагогического мастерства\\\\\n')
  tex.write ('Московский центр непрерывного математического образования\\\\\n')
  tex.write ('}\n\n')
  tex.write ('\\vskip 2cm\n\n')
  if degree == '':
    tex.write ('\\vskip 0.5cm\n\n')
  else:
    tex.write ('\\hskip 15cm \\resizebox{!}{0.5cm}{\\textit{\\textbf{' + degree +'}}}\n\n')
  tex.write ('\\vskip 1.5cm\n')
  tex.write ('\\center{\\resizebox{!}{1.2cm}{\\textit{' + first_name + ' ' + last_name + '}}\n')
  tex.write ('\\center{\\huge ' + gender + ' ' + grade + ' класса \\\\\n')
  tex.write ('(' + school + '), \\\\\n')
  tex.write ('за успешное выступление \\\\\n')
  tex.write ('на XXVI Математическом празднике \\\\\n')
  tex.write ('15 февраля 2015 года \\\\\n\n')
  tex.write ('}\n\n')
  tex.write ('\\vskip 0.2cm\n\n')
  tex.write ('\\begin{tabular}{p{6cm}p{6cm}p{6cm}p{6cm}}\n')
  tex.write ('  \\flushleft{\\large Заместитель председателя оргкомитета Математического~праздника, зам.~директора МЦНМО} & & \\flushleft{\\large Председатель~жюри Математического~праздника, директор МЦНМО и ГБОУ~ЦПМ} &  \\\\\n')
  tex.write ('   & \\center{\\large В.~Д.~Арнольд} & & \\center{\\large И.~В.~Ященко} \\\\\n')
  tex.write ('\\end{tabular}\n')
  tex.write ('\\end{document}\n')
  tex.close ()

  call (['pdflatex', file_name + '.tex'])
  call (['pdf2ps', file_name + '.pdf'])

  call (['mv', file_name + '.tex', 'site/static/'])
  call (['mv', file_name + '.pdf', 'site/static/'])
  call (['mv', file_name + '.ps', 'site/static/'])
  
  cur.execute ('update users set state = 300 where id=%s', [str (user_id)])
  conn.commit ()

  if state < 100:
    state_str = 'новый'
  elif state < 200:
    state_str = 'требуется генерация'
  elif state < 300:
    state_str = 'идет генерация'
  elif state < 400:
    state_str = 'готово, TODO: link'
  else:
    state_str = 'ОШИБКА'
cur.close ()
conn.close ()
