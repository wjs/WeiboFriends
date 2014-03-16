DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS relation;

CREATE TABLE IF NOT EXISTS user (
	uid varchar(20) PRIMARY KEY,
	nick varchar(30) NOT NULL,
	follows int NOT NULL DEFAULT 0,
	fans int NOT NULL DEFAULT 0,
	db_follows int NOT NULL DEFAULT 0,
	db_fans int NOT NULL DEFAULT 0,
	create_time Timestamp NOT NULL DEFAULT 0,
	update_time Timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS relation (
	source varchar(20),
	target varchar(20),
	PRIMARY KEY(source, target)
) ENGINE=innodb DEFAULT CHARSET=utf8;