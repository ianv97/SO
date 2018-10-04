CREATE DATABASE IF NOT EXISTS SO;
CREATE USER IF NOT EXISTS 'so'@'localhost' IDENTIFIED BY 'adminso';
GRANT ALL PRIVILEGES ON so . * TO 'so'@'localhost';
USE SO;

CREATE TABLE IF NOT EXISTS CDT(
id MEDIUMINT PRIMARY KEY AUTO_INCREMENT,
nombre varchar(60),
n_procesos INT,
t_memoria INT);

CREATE TABLE IF NOT EXISTS Proceso(
id_cdt MEDIUMINT,
id INT,
tiempo_arribo INT,
cpu1 INT,
entrada INT,
cpu2 INT,
salida INT,
cpu3 INT,
memoria INT,
PRIMARY KEY (id_cdt, id),
FOREIGN KEY (id_cdt) REFERENCES CDT(id));

CREATE TABLE Particiones(
id_cdt MEDIUMINT,
id INT,
tamano INT,
PRIMARY KEY (id_cdt, id),
FOREIGN KEY (id_cdt) REFERENCES CDT(id));