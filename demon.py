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
import re 

school_log = open("schools.log", "w");

def process_school_name(school):
  if school[0:6] == 'школа ':
    school = 'школы ' + school[6:]
  elif school[0:6] == 'Школа ':
    school = 'Школы ' + school[6:]
  elif school[0:6] == 'школа,':
    school = 'школы,' + school[6:]
  elif school[0:14] == 'частная школа ':
    school = 'частной школы ' + school[14:]
  elif school[0:6] == 'лицей ':
    school = 'лицея ' + school[6:]
  elif school[0:6] == 'Лицей ':
    school = 'Лицея ' + school[6:]
  elif school[0:9] == 'гимназия ':
    school = 'гимназии ' + school[9:]
  elif school[0:12] == 'прогимназия ':
    school = 'прогимназии ' + school[12:]
  elif school[0:22] == 'классическая гимназия ':
    school = 'классической гимназии ' + school[22:]
  elif school[0:9] == 'Гимназия ':
    school = 'Гимназии ' + school[9:]
  elif school[0:6] == 'центр ':
    school = 'центра ' + school[6:]
  elif school[0:14] == 'учебный центр ':
    school = 'учебного центра ' + school[14:]
  elif school == 'Пятьдесят седьмая школа':
    school = 'Пятьдесят седьмой школы'
  elif school[0:15] == 'школа-интернат ':
    school = 'школы-интерната ' + school[15:]
  elif school == 'sch500469':
    school = 'гимназии г. Видное'
  elif school == 'sch503445':
    school = 'школы № 6 г. Мытищи'
  elif school == 'sch121200':
    school = 'школы № 108'
  elif school == 'Государственная cтоличная гимназия':
    school = 'Государственной cтоличной гимназии'
  elif school == 'Свято-Петровская Школа':
    school = 'Свято-Петровской Школы'
  elif school == 'МЦНМО г. ХЗ':
    school = 'МЦНМО г. ХЗ'
  elif school == 'Филипповская школа':
    school = 'Филипповской школы'
  elif school == 'Захаровская школа пос. Летний отдых':
    school = 'Захаровской школы пос. Летний отдых'
  elif school == 'Елизаветинская гимназия':
    school = 'Елизаветинской гимназии'
  elif school == 'Британская международная школа':
    school = 'Британской международной школы'
  elif school == 'Троицкая Православная школа':
    school = 'Троицкой Православной школы'
  elif school == 'Кадетская школа-интернат № 11':
    school = 'Кадетской школы-интерната № 11'
  elif school == 'Московская международная гимназия':
    school = 'Московской международной гимназии'
  elif school == 'православная школа-пансион <<Плесково>>':
    school = 'православной школы-пансиона <<Плесково>>'
  elif school == 'образовательный центр <<Солнечный ветер>>':
    school = 'образовательного центра <<Солнечный ветер>>'
  #elif school == 'лицей №2 им. М.В. Ломоносова г. Брянск':
  #  school = 'лицея №2 им. М.В. Ломоносова г. Брянск'
  elif school == 'Ломоносовская школа':
    school = 'Ломоносовской школы'
  elif school == 'Физтех-лицей имени П.Л. Капицы г. Долгопрудный':
    school = 'Физтех-лицея имени П.Л. Капицы г. Долгопрудный'
  elif school == 'Хибинская гимназия г. Кировск':
    school = 'Хибинской гимназии г. Кировск'
  elif school == 'еврейская школа <<Мир интеллекта>>':
    school = 'еврейской школы <<Мир интеллекта>>'
  elif school == 'Московский государственный техникум технологий и права':
    school = 'Московского государственного техникума технологий и права'
  elif school == 'Пироговская школа':
    school = 'Пироговской школы'
  elif school == 'Костромской кадетский корпус':
    school = 'Костромского кадетского корпуса'
  elif school == 'семейное образование':
    school = 'семейного образования'
  elif school == 'Раменская № 2 г. Раменское':
    school = 'Раменской № 2 г. Раменское'
  elif school == 'Славяно-англо-американская <<Марина>> школа':
    school = 'Славяно-англо-американской школы <<Марина>>'
  elif school == 'Многопрофильный № 1799':
    school = 'многопрофильного лицея № 1799'
  elif school == 'средняя общеобразовательная школа, д. Кузмищи, Костромская обл.':
    school = 'СОШ, д. Кузмищи, Костромская обл.'
  elif school == 'Университетская школа МГПУ':
    school = 'Университетской школы МГПУ'
  elif school == 'лесная школа, г. Лесная Чаща':
    school = 'лесной школы, г. Лесная Чаща'
  elif school == 'sch333333':
    school = 'школы Юного Песца'    
  elif school == 'православная школа-пансион "Плесково"':
    school = 'православной школы-пансиона "Плесково"'
  elif school == 'Костромской кадетский корпус г. Кострома':
    school = 'Костромского кадетского корпуса г. Кострома'
  elif school == 'Государственная столичная гимназия':
    school = 'Государственной столичной гимназии'
  elif school == 'Газпром школа':
    school = 'Газпром школы'
  elif school == 'Лесная Школа':
    school = 'Лесной Школы'
  elif school == 'образовательный центр им С.Н. Олехника':
    school = 'образовательного центра им С.Н. Олехника'
  elif school == 'Православная классическая гимназия "Ковчег", Московская обл.':
    school = 'Православной классической гимназии "Ковчег", Московская обл.'
  elif school == 'Курчатовская школа':
    school = 'Курчатовской школы'
  elif school == 'лицейско-гимназический комплекс на Юго-Востоке':
    school = 'лицейско-гимназического комплекса на Юго-Востоке'
  elif school == 'Солоницевский учебно-воспитательный комплекс  <<Жемчужина>> пос. Солоницевка':
    school = 'Солоницевского учебно-воспитательного комплекса  <<Жемчужина>> пос. Солоницевка'
  elif school == 'Инженерно-техническая школа':
    school = 'Инженерно-технической школы'
  elif school == 'Славянско-англо-американская школа "Марина"':
    school = 'Славянско-англо-американской школы "Марина"'
  elif school == 'Государственная столичная гимназия':
    school = 'Государственной столичной гимназии'
  elif school == 'Международная английская школа, д. Грибаново, Московская обл.':
    school = 'Международной английской школы, д. Грибаново, Московская обл.'
  elif school == 'Мехельтинская средняя школа, Республика Дагестан':
    school = 'Мехельтинской средней школы, Республика Дагестан'
  elif school == 'Государственная столичная гимназия':
    school = 'Государственной столичной гимназии'
  elif school == 'Инженерно-техническая школа':
    school = 'Инженерно-технической школы'
  elif school == 'Российская международная школа г. Домодедово, Московская обл.':
    school = 'Российской международной школы г. Домодедово, Московская обл.'
  elif school == 'Мехельтинская средняя школа, Республика Дагестан':
    school = 'Мехельтинской средней школы, Республика Дагестан'
  elif school == 'Государственная столичная гимназия':
    school = 'Государственной столичной гимназии'  
  else:
    print (' school: ' + school, file=school_log)
  
  return school


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
  if int (degree) >= 28:
    degree = 'первой степени'
  elif int (degree) >= 20:
    degree = 'второй степени'
  elif int (degree) >= 16:
    degree = 'третьей степени'
  elif int (degree) >= 11:
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
  school = process_school_name(school);
  school = re.sub ('"(.*)"', '<<\\1>>', school)
  school = re.sub ('«', '<<', school)
  school = re.sub ('“', '<<', school)
  school = re.sub ('»', '>>', school)
  school = re.sub ('”', '>>', school)
  school = re.sub (' ', ' ', school)
  school = re.sub (' ', ' ', school)
  tex.write (school + ', \\\\\n')
  tex.write ('за успешное выступление \\\\\n')
  tex.write ('на XXVII Математическом празднике \\\\\n')
  tex.write ('21 февраля 2016 года \\\\\n\n')
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

school_log.close()