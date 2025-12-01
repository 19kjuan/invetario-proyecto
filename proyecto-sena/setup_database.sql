-- Crear base de datos
DROP DATABASE IF EXISTS inventario_tenis_padel;
CREATE DATABASE inventario_tenis_padel;
USE inventario_tenis_padel;

-- ================================
-- TABLA DE PRODUCTOS
-- ================================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria ENUM('Tenis','Pádel','Accesorios') DEFAULT 'Accesorios',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


ALTER TABLE productos
  ADD COLUMN stock_minimo INT NULL DEFAULT 5 AFTER stock;

-- ================================
-- TABLA DE VENTAS
-- ================================
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL
);

-- ================================
-- DETALLE DE VENTAS (relación muchos a muchos)
-- ================================
CREATE TABLE detalle_ventas (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE RESTRICT
);

-- ================================
-- TRIGGER PARA ACTUALIZAR STOCK
-- ================================
DELIMITER $$
CREATE TRIGGER descontar_stock
AFTER INSERT ON detalle_ventas
FOR EACH ROW
BEGIN
    UPDATE productos
    SET stock = stock - NEW.cantidad
    WHERE id_producto = NEW.id_producto;
END$$
DELIMITER ;

-- ================================
-- DATOS DE EJEMPLO (INVENTARIO INICIAL)
-- ================================
INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
('Raqueta Tenis Wilson Pro Staff', 'Raqueta profesional para tenis avanzado', 350.00, 10, 'Tenis'),
('Raqueta Pádel Bullpadel Vertex', 'Raqueta de pádel de alta gama', 280.00, 15, 'Pádel'),
('Pelotas Tenis Head (tubo x3)', 'Tubo con 3 pelotas presurizadas', 8.50, 100, 'Tenis'),
('Pelotas Pádel Dunlop (pack x3)', 'Pack de 3 pelotas de pádel', 7.00, 80, 'Pádel'),
('Grip Antideslizante', 'Grip universal para raquetas', 4.00, 50, 'Accesorios'),
('Bolso Wilson Super Tour', 'Bolso grande para raquetas y accesorios', 120.00, 20, 'Accesorios');

-- ================================
-- EJEMPLO DE VENTA
-- ================================
-- Crear una venta (se guarda el total luego de sumar los subtotales)
INSERT INTO ventas (total) VALUES (367.00);

-- Insertar detalle (3 pelotas de tenis y 1 grip)
INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal)
VALUES 
(1, 3, 3, 8.50, 25.50),
(1, 5, 1, 4.00, 4.00),
(1, 1, 1, 350.00, 350.00);

-- Actualización automática de stock ya aplicada con trigger