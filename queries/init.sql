CREATE DATABASE permissions;
USE permissions;
CREATE TABLE permission_records(name VARCHAR(255), email VARCHAR(255), team VARCHAR(255), explorer VARCHAR(255), sensors VARCHAR(255), PRIMARY KEY(email, team)) ;
CREATE TABLE permission_records_temp(name VARCHAR(255), email VARCHAR(255), team VARCHAR(255), explorer VARCHAR(255), sensors VARCHAR(255), PRIMARY KEY(email, team));
INSERT INTO permission_records VALUES ('Joe','joe@domain.com','Support','reader','reader'), ('Don','stefano@domain.com','Support','reader','reader');