DROP TABLE IF EXISTS test;
CREATE TABLE test(num int);
INSERT INTO test values(1);
INSERT INTO test values(2);
INSERT INTO test values(3);
INSERT INTO test values(4);
INSERT INTO test values(5);


DROP TABLE IF EXISTS USERS;
CREATE TABLE USERS(NAME TEXT, AGE INT, EMAIL CHAR(50), AUTH CHAR);
INSERT INTO USERS values('Emre EROĞLU', 28, 'emreeroglu@itu.edu.tr', 'a');
INSERT INTO USERS values('abcd', 45, 'abcd@itu.edu.tr', 'u');
INSERT INTO USERS values('efgh', 85, 'efgh@itu.edu.tr', 'm');
INSERT INTO USERS values('jklm', 20, 'jklm@itu.edu.tr', 'a');