Name: Harshada Prabhakar Bhangale
Project Name: MICROBLOG

PROJECT DESCRIPTION:

MICROBLOG has two services namely:

1. User Microservice has activities related to particular user like add new user to table, add/remove a follower to a user,authenticate user by checking
  if the users password and hashed table password for that user matches.

  Different functions are as follows:

  createUser(username, email, password)-Registers a new user account.
  authenticateUser(username, password)- Returns true if the supplied password matches the hashed password stored for that username in the database.
  addFollower(username, usernameToFollow)- Start following a new user.
  removeFollower(username, usernameToRemove)- Stop following a user.


2. Timeline Microservice has all the activites related to viewing follower, users tweet and post new tweet by user

  Different functions are as follows:

  getUserTimeline(username) - Returns recent tweets from a user.
  getPublicTimeline() - Returns recent tweets from all users.
  getHomeTimeline(username) -Returns recent tweets from all users that this user follows.
  postTweet(username, text) - Post a new tweet.



  Installations:

  Ubuntu
  Flask
  Python 3.8
  Sqlite3
  Foreman


 Commands:
pip install python-dotenv
$ flask init
$ foreman start

