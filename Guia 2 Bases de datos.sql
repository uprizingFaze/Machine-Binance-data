CREATE TABLE Tabla1 (
    Código INT PRIMARY KEY,
    Apellido VARCHAR(50),
    Nombre VARCHAR(50),
    Fecha_de_nacimiento DATE,
    Edad INT
);

CREATE TABLE Tabla2 (
    Fecha DATE,
    Cedula VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(50),
    Telefono VARCHAR(15),
    Direccion VARCHAR(100),
    Valor_a_pagar DECIMAL(10, 2)
);

CREATE TABLE Tabla3 (
    Id_producto INT PRIMARY KEY ,
    Nombre_Producto VARCHAR(50),
    Cantidad INT,
    Valor_unidad DECIMAL(10,2),
    Valor_total DECIMAL(10,2),
);

CREATE TABLE Tabla4(
    Id_asignatura INT PRIMARY KEY,
    Nombre_asignatura VARCHAR(50),
    Semestre INT,
    Programa_Profesional VARCHAR(50),
)
-- Tabla1
ALTER TABLE Tabla1
ADD Semestre VARCHAR(10);

EXEC sp_rename 'Tabla1.Código', 'Cedula', 'COLUMN';

ALTER TABLE Tabla1
DROP COLUMN Edad;

-- Tabla 2

ALTER TABLE Tabla2
DROP COLUMN Fecha;

ALTER TABLE Tabla2
ADD Twitter VARCHAR(50);

ALTER TABLE Tabla2
ALTER COLUMN Cedula INT;

-- Tabla 4

ALTER TABLE Tabla4
ADD Id_programa_profesional INT PRIMARY KEY;

ALTER TABLE Tabla4
DROP COLUMN Semestre;

