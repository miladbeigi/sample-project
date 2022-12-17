CREATE DATABASE permissions;
USE permissions;
CREATE TABLE permission_records(name VARCHAR(255), email VARCHAR(255), team VARCHAR(255), explorer VARCHAR(255), sensors VARCHAR(255));
INSERT INTO permission_records VALUES ('Joe','joe@domain.com','Support','reader','reader'), ('Don','stefano@domain.com','Support','reader','reader');