CREATE DATABASE SO;
USE SO;

CREATE TABLE Algoritmo(
Id_algoritmo int PRIMARY KEY,
Nombre varchar(15));

algoritmoCREATE TABLE Carga_de_trabajo(
Id_carga int PRIMARY KEY AUTO_INCREMENT,
Nombre varchar(60),
N_procesos int,
Algoritmo int,
FOREIGN KEY (Algoritmo) REFERENCES Algoritmo(Id_Algoritmo));

CREATE TABLE Proceso(
Id_carga int,
Id_proceso int,
Tiempo_arribo int,
Cpu1 int,
Entrada int,
Cpu2 int,
Salida int,
Cpu3 int,
PRIMARY KEY (Id_carga, Id_proceso),
FOREIGN KEY (Id_carga) REFERENCES Carga_de_trabajo(Id_carga));

INSERT INTO Algoritmo VALUES (1,"FCFS"),(2,"SJF"),(3,"SRTF"),(4,"ROUND ROBIN");