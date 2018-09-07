CREATE DATABASE IF NOT EXISTS SO;
CREATE USER IF NOT EXISTS 'so'@'localhost' IDENTIFIED BY 'adminso';
GRANT ALL PRIVILEGES ON so . * TO 'so'@'localhost';
USE SO;

CREATE TABLE IF NOT EXISTS Algoritmo(
nombre_algoritmo varchar(15) PRIMARY KEY);

CREATE TABLE IF NOT EXISTS CDT(
nombre_cdt varchar(60) PRIMARY KEY,
n_procesos int);

CREATE TABLE IF NOT EXISTS Proceso(
nombre_cdt varchar(60),
id_proceso int,
tiempo_arribo int,
cpu1 int,
entrada int,
cpu2 int,
salida int,
cpu3 int,
PRIMARY KEY (nombre_cdt, id_proceso),
FOREIGN KEY (nombre_cdt) REFERENCES CDT(nombre_cdt));

INSERT INTO Algoritmo VALUES ("FCFS"),("SJF"),("SRTF"),("ROUND ROBIN");