CREATE DATABASE "ECCA"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
    
\c ECCA

--Drops previos en caso de existir tablas*/

DROP TABLE IF EXISTS Plan;
DROP TABLE IF EXISTS Asignatura;
DROP TABLE IF EXISTS Plan_Asignatura;
DROP TABLE IF EXISTS Estadistica_Asignatura;
DROP TABLE IF EXISTS Requisito;
DROP TABLE IF EXISTS Analoga;

create table Plan (
	id serial PRIMARY KEY,
	nombre varchar(128) not null,
	version varchar(128) not null,
	duracion_semestres integer not null
);

create table Asignatura (
	codigo integer PRIMARY KEY,
	nombre varchar(128) not null,
	tipo varchar(128) not null
);

create table Estadistica_Asignatura (
	id serial PRIMARY KEY,
	cod_asignatura integer not null,
	ano integer not null,
	semestre integer not null,
	inscritos_teoria integer default 0,
	aprobados_teoria integer default 0,
	reprobados_teoria integer default 0,
	inscritos_laboratorio integer default 0,
	aprobados_laboratorio integer default 0,
	reprobados_laboratorio integer default 0,
	tasa_aprobacion_teoria real default 0,
	tasa_aprobacion_laboratorio real default 0,
	tasa_desinscripcion real default 0
);

create table Requisito (
	id serial PRIMARY KEY,
	cod_asignatura integer not null,
	cod_asignatura_requisito integer not null,
	nivel_requisito integer not null
);

create table Analoga (
	id serial PRIMARY KEY,
	cod_asignatura integer not null,
	cod_asignatura_analoga integer not null
);

create table Plan_Asignatura (
	id serial PRIMARY KEY,
	id_plan integer not null,
	cod_asignatura integer not null,
	nivel integer not null
);

--Referenciacion para las llaves foraneas

ALTER TABLE Plan_Asignatura
	ADD CONSTRAINT FK_Plan_Asignatura_ID_Plan
	FOREIGN KEY (id_plan) REFERENCES Plan(id);

ALTER TABLE Plan_Asignatura
	ADD CONSTRAINT FK_Plan_Asignatura_ID_Asignatura
	FOREIGN KEY (cod_asignatura) REFERENCES Asignatura(codigo);

ALTER TABLE Requisito
	ADD CONSTRAINT FK_Requisito_ID_Asignatura
	FOREIGN KEY (cod_asignatura) REFERENCES Asignatura(codigo);

ALTER TABLE Requisito
	ADD CONSTRAINT FK_Requisito_ID_Asignatura_Requisito
	FOREIGN KEY (cod_asignatura_requisito) REFERENCES Asignatura(codigo);

ALTER TABLE Analoga
	ADD CONSTRAINT FK_Analoga_ID_Asignatura
	FOREIGN KEY (cod_asignatura) REFERENCES Asignatura(codigo);

ALTER TABLE Analoga
	ADD CONSTRAINT FK_Analoga_ID_Asignatura_Analoga
	FOREIGN KEY (cod_asignatura_analoga) REFERENCES Asignatura(codigo);

ALTER TABLE Estadistica_Asignatura
	ADD CONSTRAINT FK_Estadistica_Asignatura_ID_Asignatura
	FOREIGN KEY (cod_asignatura) REFERENCES Asignatura(codigo);