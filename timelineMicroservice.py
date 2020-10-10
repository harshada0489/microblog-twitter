# Name::: Harshada Prabhakar Bhangale
# Project Name:::- MICROBLOG

import flask
import click
from flask import request, jsonify, g
import sqlite3
import datetime


app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')


@app.route('/user/<username>/userTimeline', methods=['GET'])
# gets user timeline
def getUserTimeline(username):
# gets users recent <=25 tweets
        userTweetList = query_db('SELECT * from tweets where username = ? order by createDate desc limit 25;',(username,))
        if(userTweetList):
            return jsonify(userTweetList)
        else:
            statusCode = '404 -Not Found'
            message = "User does not EXIST"
            return jsonMessage(message, statusCode)


@app.route('/user/publicTimeline', methods=['GET'])
# gets publllic timeline
def getPublicTimeline():
    # shows all users recent tweet till 25 records
    tweetList = query_db('SELECT * from tweets order by createDate desc limit 25;')
    if(tweetList):
        return jsonify(tweetList)
    else:
        statusCode = '404 -Not Found'
        message = "User does not EXIST"
        return jsonMessage(message, statusCode)


@app.route('/user/<username>/homeTimeline', methods=['GET'])
# gets Home time tiiile oof user
def getHomeTimeline(username):
        # gets the list of followers tweet of a particular user
        tweetList = query_db('SELECT * from tweets WHERE username IN(SELECT usernameToFollow FROM usersFollower WHERE username =?)order by createDate desc limit 25;',(username,))
        if(tweetList):
            return jsonify(tweetList)
        else:
            statusCode = '404 -Not Found'
            message = "User does not EXIST"
            return jsonMessage(message, statusCode)


@app.route('/user/tweet', methods=['POST'])
#  posts users new tweet
def postTweet():
    # retrieves json daaata into variables
    username = request.json.get('username')
    postTweet = request.json.get('tweet')
    # checks if user exists
    userResult = query_db('SELECT username FROM users where username= ?;', (username,))
    if userResult:
        #  generates current time into variable createDate
        createDate=datetime.datetime.now()
        print(createDate)

        db = get_db()
        # inserts new tweet posted by user tweets table
        followerResult = query_db('INSERT INTO tweets VALUES(?, ?, ?);', (postTweet,username,createDate,))
        db.commit()
        message = 'Tweet created succesfully'
        statusCode = '201 - Created'
        return jsonMessage(message,statusCode)
    else:
        statusCode = '404 -Not Found'
        message = "User does not EXIST"
        return jsonMessage(message, statusCode)



# common method response in json format
def jsonMessage(message, statusCode):
    # returns json format as response
    return jsonify({
            'content-type': 'application/json',
            'status code': statusCode,
            'Message': message
            });


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# gets database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
        db.commit()
    return db


@app.teardown_appcontext
# closes connection to database
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#common method for retriving query from database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#creates all new tables and all other queries in schema.sql file
# @app.cli.command('init')
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()
