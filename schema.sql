-- $ sqlite3 users.db < users.sql

PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username VARCHAR primary key,
    email VARCHAR,
    hashedPassword VARCHAR
  );
  COMMIT;


  BEGIN TRANSACTION;
  DROP TABLE IF EXISTS usersFollower;
  CREATE TABLE usersFollower (
      usernameToFollow VARCHAR,
      username VARCHAR,
      FOREIGN KEY(username) REFERENCES users(username)
    );
  COMMIT;


  BEGIN TRANSACTION;
  DROP TABLE IF EXISTS tweets;
  CREATE TABLE tweets (
      tweet VARCHAR,
      username VARCHAR,
      createDate VARCHAR,
      FOREIGN KEY(username) REFERENCES users(username)
    );
  COMMIT;
