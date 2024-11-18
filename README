This is server side for project. You can make an account, log in, read other users's post and write your own post, that will appear in common feed. Also there is a possibility to change your account data (name/email and etc.)
React.js react-router-dom are used for client side. Flask is used for server development.

# Requirement database is PostgresSQL with tables
1. users: CREATE TABLE users (
id INT GENERATED AS IDENTITY BY DEFAULT,
nickname VARCHAR(40),
age INT,
email VARCHAR(40),
password TEXT,
avatar BYTEA -- BTW isn't implemented ((
);

2. posts: CREATE TABLE posts (
    post_id INT GENERATED AS IDENTITY BY DEFAULT,
    post_text TEXT,
    creator_id INT,
    date_and_time TIMESTAMP
);

# Requirements for server:
﻿async-timeout==4.0.2
blinker==1.6.2
cachelib==0.10.2
click==8.1.3
colorama==0.4.6
Flask==2.3.2
Flask-Cors==3.0.10
Flask-JWT-Extended==4.4.4
Flask-Session==0.5.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.2
psycopg2==2.9.6
PyJWT==2.7.0
redis==4.5.5
six==1.16.0
Werkzeug==2.3.4
