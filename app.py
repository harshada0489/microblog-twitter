# Name::: Harshada Prabhakar Bhangale
# Project Name:::- MICROBLOG

import flask
import click
from flask import request, jsonify, g
import sqlite3
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')


 #  New user create
@app.route('/user/create', methods=['POST'])
def createUser():
    # Takes values in variables from json
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # uses werkzeug.security for generating hashed password
    hashedPassword = generate_password_hash(password,method = 'pbkdf2:sha256', salt_length = 8)

    # checks  if user exists or not
    result = query_db('SELECT username FROM users where username= ?;', (username,))
    if result:
        message = 'User already EXISTS'
        statusCode = '409 -Confict'
        # if user exists return json message
        return jsonMessage(message, statusCode)
    else:
        # If user is not present insert new user in the table
        db = get_db()
        query_db('INSERT INTO users VALUES (?, ?, ?);', (username, email, hashedPassword,))
        db.commit()
        message = 'User created succesfully'
        statusCode = '201 - Created'
        # Returns json message
        return jsonMessage(message, statusCode)



@app.route('/user/authenticateUser', methods=['POST'])
# authenticates user
def authenticateUser():
    # Takes values in variables from json
    username = request.json.get('username')
    password = request.json.get('password')
    # checks  if user exists or not
    result = query_db('SELECT username, hashedPassword FROM users where username= ?;', (username,))
    if result:
        # if user exists get the hashed password from database
        value2 = [d['hashedPassword'] for d in result]
        hashedPasword = value2[0]
        # compares password given by user and the hashed password retrieved from users table
        value = check_password_hash(hashedPasword,password)

        if(value == True):
            statusCode = '200 - OK'
            message = 'User authenticated successfully'
            return jsonMessage(message, statusCode)


        else:
            statusCode = '404 -Not Found'
            message = 'User authentication failed'
            return jsonMessage(message, statusCode)
    else:
        statusCode = '404 -Not Found'
        message = "User does not EXIST"
        return jsonMessage(message, statusCode)



@app.route('/user/addFollower', methods=['POST'])
# adds new follower to the user
def addFollower():
    # takes values in variables from json format
        username = request.json.get('username')
        usernameToFollow = request.json.get('usernameToFollow')
        # checks if user exists
        userResult = query_db('SELECT username FROM users where username= ?;', (username,))
        if userResult:
            # checks if the follower is existing
            followerResult = query_db('SELECT username FROM users where username= ?;', (usernameToFollow,))

            if followerResult:
                # checks if user is already following
                userAndFollowerCheck = query_db('SELECT * FROM usersFollower where username= ? and usernameToFollow=?;', (username,usernameToFollow,))
                if (userAndFollowerCheck):
                    message = 'User is already following'
                    statusCode = '409'
                    return jsonMessage(message, statusCode)
                else:
                    # if follower exists in users table
                    db = get_db()
                    # if follower exists, assign new follower to the user
                    query_db('INSERT INTO usersFollower VALUES (?, ?);', (usernameToFollow, username,))
                    db.commit()

                    message = 'User follower created succesfully'
                    statusCode = '201 - Created'
                    return jsonMessage(message, statusCode)
            else:
                message = "followUser does not exist"
                statusCode = '404 -Not Found'
                return jsonMessage(message, statusCode)

        else:
            message = "User does not EXIST"
            statusCode = '404 -Not Found'
            return jsonMessage(message, statusCode)


@app.route('/user/removeFollower', methods=['DELETE'])
# removes follower
def removeFollower():
    # gets data to variable name from json
        username = request.json.get('username')
        usernameToUnfollow = request.json.get('usernameToUnfollow')
        # checks if user is following the another user
        userResult = query_db('SELECT * FROM usersFollower where username= ? and usernameToFollow= ?;', (username,usernameToUnfollow,))
        if userResult:
            db = get_db()
            #  if user is having follower, remove that follower by deleting record from userfollower table
            followerResult = query_db('DELETE FROM usersFollower where username= ? and usernameToFollow= ?;', (username,usernameToUnfollow,))
            db.commit()
            message = 'Follower removed succesfully'
            statusCode = '200 - OK'
            return jsonMessage(message, statusCode)
        else:
            statusCode = '404 -Not Found'
            message = "User does not EXIST"
            return jsonMessage(message, statusCode)


# common method response in json format
def jsonMessage(message, statusCode):
    # returns json format as response
    return jsonify({
            'content-type': 'application/json',
            'content-language': 'en-US',
            'status code': statusCode,
            'Message': message
            });


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# connects with database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
        db.commit()
    return db


@app.teardown_appcontext
# used to close the database connection
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# common method for any query retrival
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#creates all new tables and all other queries in schema.sql file
@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
