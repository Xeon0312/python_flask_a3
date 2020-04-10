BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "marks" (
	"assignment1"	INTEGER,
	"assignment2"	INTEGER,
	"assignment3"	INTEGER,
	"lab"	INTEGER,
	"midtermexam"	INTEGER,
	"finalexam"	INTEGER,
	"studentname"	INTEGER
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER AUTOINCREMENT,
	"username"	TEXT,
	"password"	TEXT,
	"role" 	INTEGER,
	PRIMARY KEY("id")
);

INSERT INTO "marks" VALUES (9,4,30,NULL,40,100,'ok1');
INSERT INTO "marks" VALUES (10,5,10,NULL,50,80,'ok2');
INSERT INTO "marks" VALUES (NULL,20,10,NULL,10,10,'ok3');
INSERT INTO "marks" VALUES (NULL,NULL,NULL,NULL,NULL,NULL,'ok4');
INSERT INTO "marks" VALUES (0,0,0,NULL,0,0,'ok5');
INSERT INTO "marks" VALUES (10,10,10,NULL,10,10,'ok6');
INSERT INTO "marks" VALUES (10,10,10,NULL,20,20,'ok7');
INSERT INTO "marks" VALUES (NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO "users" VALUES (1,NULL,NULL);
INSERT INTO "users" VALUES (2,'ok2','ok2');
INSERT INTO "users" VALUES (3,'ok1','ok1');
INSERT INTO "users" VALUES (4,'ok2','ok2');
INSERT INTO "users" VALUES (5,'ok3','ok3');
INSERT INTO "users" VALUES (6,'ok4','ok4');
INSERT INTO "users" VALUES (7,'ok1','ok1');
INSERT INTO "users" VALUES (8,'ok2','ok2');
INSERT INTO "users" VALUES (9,'ok3','ok3');
INSERT INTO "users" VALUES (10,'ok4','ok4');
INSERT INTO "users" VALUES (11,'ok5','ok5');
INSERT INTO "users" VALUES (12,'ok6','ok6');
INSERT INTO "users" VALUES (13,'abbas123','abbas123');
INSERT INTO "users" VALUES (14,NULL,NULL);

CREATE TABLE IF NOT EXISTS "remarking" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"studentname"	TEXT,
	"item"	TEXT,
	"desc" 	TEXT
);


CREATE TABLE IF NOT EXISTS "feedback" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"instructorname"	TEXT,
	"item1"	TEXT,
	"item2" 	TEXT,
	"item3" 	TEXT,
	"item4" 	TEXT
);
COMMIT;
