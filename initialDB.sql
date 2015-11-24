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

DROP TABLE IF EXISTS POOL;
CREATE TABLE POOL(NAME TEXT, CITY TEXT, CAPACITY INT, BUILT INT);
INSERT INTO POOL values('Colesium','Rome', 25000, 1985);
INSERT INTO POOL values('Itu','Istanbul', 27500, 2010);
INSERT INTO POOL values('Yanky','London', 19000, 2004);
INSERT INTO POOL values('Surioc','Sao Paolo', 35000, 1995);
INSERT INTO POOL values('Haka','New Zealand', 7000, 2001);

DROP TABLE IF EXISTS PLAYERS;
CREATE TABLE PLAYERS(ID INT, NAME TEXT, AGE INT, NATION TEXT, TEAM TEXT, FIELD TEXT);
INSERT INTO PLAYERS values(1, 'DENEME',55, 'FRA', 'PSG', 'MIDFIELDER');

DROP TABLE IF EXISTS COUNTRIES;
CREATE TABLE COUNTRIES(ID SERIAL PRIMARY KEY, NAME VARCHAR(50) NOT NULL, POPULATION FLOAT NOT NULL, COORDINATES FLOAT SET DEFAULT 0);
INSERT INTO COUNTRIES values('Türkiye',3000000,1);
INSERT INTO COUNTRIES values('Amerika',7000000,3);
INSERT INTO COUNTRIES values('Gine',800000,5);

DROP TABLE IF EXISTS LEAGUES;
CREATE TABLE LEAGUES(ID SERIAL PRIMARY KEY, NAME VARCHAR(75) NOT NULL, NATION VARCHAR(50) NOT NULL, CLASSIFICATION INT NOT NULL);
INSERT INTO LEAGUES values('Süper Lig','Türkiye',1);
INSERT INTO LEAGUES values('Bank Asya','Türkiye',2);

DROP TABLE IF EXISTS STATS;
CREATE TABLE STATS(NAME TEXT,SURNAME TEXT,TEAM TEXT,LEAGUE TEXT, GOAL INT, ASSIST INT,SAVE INT);
INSERT INTO STATS values('Can','Eren','Detroit','Super',30,12,0);
INSERT INTO STATS values('Kaan','Orhan','Detroit','Super',23,11,0);
INSERT INTO STATS values('Peter','Yankee','Miami','Super',0,7,10);
INSERT INTO STATS values('Xavi','Xennon','Miami','Super',11,24,0);
INSERT INTO STATS values('Berk','Aygun','Bristol','Super',5,7,0);
INSERT INTO STATS values('Ali','Alie','Reds','Second',43,15,0);
INSERT INTO STATS values('Mike','Mucho','Reds','Second',12,6,0);
INSERT INTO STATS values('Jean','Tella','Coco','Second',15,3,0);
INSERT INTO STATS values('David','Sanchez','Tacho','Second',12,16,0);
INSERT INTO STATS values('Damien','Rilly','Blues','Amateur',2,8,6);
INSERT INTO STATS values('Steve','Hudson','Kirks Team','Amateur',4,12,0);
INSERT INTO STATS values('Gerald','Patty','Eagles','Amateur',1,3,0);
INSERT INTO STATS values('George','Suffo','Attackers','Amateur',0,6,3);
