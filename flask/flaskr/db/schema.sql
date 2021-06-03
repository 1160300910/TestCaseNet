DROP TABLE IF EXISTS TestCase

CREATE TABLE TestCase (
         caseId INT PRIMARY KEY AUTO_INCREMENT,
         peoType INT NOT NULL,
         name  CHAR(50) NOT NULL,
         level INT NOT NULL,
         entry CHAR(50) NOT NULL,
         conditionInfo CHAR(50) NOT NULL,
         executeInfo CHAR(50) NOT NULL,
         ps CHAR(50) NOT NULL,
         changeDate DATETIME NOT NULL,
         changePeo INT NOT NULL,
         actionPeo INT NOT NULL,
         actionedPeo INT NOT NULL,
         actionDate DATETIME NOT NULL,
         definedType INT NOT NULL,
         tag  CHAR(20) NOT NULL,
         caseType INT NOT NULL,
         fatherFile  CHAR(50) NOT NULL,
         state INT NOT NULL
);


DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);




CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);