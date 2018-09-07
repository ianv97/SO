CREATE DATABASE IF NOT EXISTS SO;
CREATE USER IF NOT EXISTS 'so'@'localhost' IDENTIFIED BY 'adminso';
GRANT ALL PRIVILEGES ON so . * TO 'so'@'localhost';
drop database SO;
CREATE DATABASE SO;
USE SO;

CREATE TABLE IF NOT EXISTS Algoritmo(
nombre varchar(15) PRIMARY KEY);

CREATE TABLE IF NOT EXISTS CDT(
id smallint PRIMARY KEY AUTO_INCREMENT,
nombre varchar(60),
n_procesos int);

CREATE TABLE IF NOT EXISTS Proceso(
id_cdt smallint,
id int AUTO_INCREMENT,
tiempo_arribo int,
cpu1 int,
entrada int,
cpu2 int,
salida int,
cpu3 int,
PRIMARY KEY (id_cdt, id),
FOREIGN KEY (id_cdt) REFERENCES CDT(id));

INSERT INTO Algoritmo VALUES ("FCFS"),("SJF"),("SRTF"),("ROUND ROBIN");