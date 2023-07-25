# sistema-venta-

framework django

1.- Crear base de datos MySQL con nombre "bazar" con Xampp o wampserver.

2.- Abrir CMD con ruta del la carpeta "AppBazar"

3.- Ejecutar el comando "py manage.py migrate"

4.- Ingresar estos datos a la base de datos "bazar"
INSERT INTO app_categoria (nombre) VALUES("TERROR");
INSERT INTO app_categoria (nombre) VALUES("AVENTURA");
INSERT INTO app_categoria (nombre) VALUES("FICCIÓN");
INSERT INTO app_categoria (nombre) VALUES("FICCIÓN INFANTIL");
INSERT INTO app_categoria (nombre) VALUES("FANTASÍA");
INSERT INTO app_categoria (nombre) VALUES("INFANTIL");
INSERT INTO app_categoria (nombre) VALUES("SUSPENSO");
INSERT INTO app_categoria (nombre) VALUES("RELATOS");
INSERT INTO app_categoria (nombre) VALUES("EPICA");
INSERT INTO app_categoria (nombre) VALUES("LITERATURA");

INSERT INTO app_producto (nombre, cantidad, precio, cod_categoria)
SELECT 
    CONCAT('Producto ', LPAD(@row := @row + 1, 2, '0')) AS nombre,
    100 AS cantidad,
    FLOOR(RAND() * 100) + 1 AS precio,
    FLOOR(RAND() * 10) + 1 AS cod_categoria_id
FROM
    (SELECT @row := 0) AS r
CROSS JOIN
    information_schema.tables
LIMIT 30;

INSERT INTO app_tipo_venta (nombre) VALUES("Boleta");
INSERT INTO app_tipo_venta (nombre) VALUES("Factura");

5.- Abrir CMD con ruta del la carpeta "AppBazar" y ejecutar este comando "py manage.py runserver"

6.- Copiar el URL y ingresar a /login
