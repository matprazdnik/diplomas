# Setup

```
pip3 install -r requirements.txt
```

```
# apt-get install texlive-latex-base texlive-lang-cyrillic texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra mysql-server
# /usr/bin/mysql_secure_installation
# mysql -u root -p

create database mf character set utf8;
create user 'mf'@'localhost' identified by '12345';
grant all on mf.* to 'mf';
flush privileges;

use mf;
create table users
(
id int not null auto_increment,
first_name text,
last_name text,
gender text,
school text,
grade text,
degree text,
state int,
primary key (id)
);

exit
```

```
python3 import-csv.py diplomas.csv

# mysql -u root -p
use mf;
update users set state=100  where degree > 10;
```

```
# mysql -u root -p
use mf;
update users set state=100  where degree > 1;
```
