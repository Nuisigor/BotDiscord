CREATE TABLE IF NOT EXISTS Aulas(
    AulaID char(10) PRIMARY KEY,
    AulaLink1 varchar(40),
    AulaLink2 varchar(40)
);

CREATE TABLE IF NOT EXISTS HorarioAulas(
    Aula char(10),
    DiaSemana varchar(15),
    DiaSemanaIndex integer,
    Hora integer,
    Minuto integer,
    FOREIGN KEY (Aula) REFERENCES Aulas(AulaID),
    CONSTRAINT pk_Horario PRIMARY KEY (Aula,DiaSemana)
);

CREATE TABLE IF NOT EXISTS Professor(
    Nome varchar(50) PRIMARY KEY,
    email varchar(50)
);

CREATE TABLE IF NOT EXISTS Monitor(
    Nome varchar(50) PRIMARY KEY,
    email varchar(50)
);

CREATE TABLE IF NOT EXISTS Materia(
    ID integer PRIMARY KEY,
    Professor varchar(50),
    Materia varchar(50),
    Canal varchar(100),
    Cargo varchar(100),
    Aula char(10),
    FOREIGN KEY (Aula) REFERENCES Aulas(AulaID),
    FOREIGN KEY (Professor) REFERENCES Professor(Nome)
);