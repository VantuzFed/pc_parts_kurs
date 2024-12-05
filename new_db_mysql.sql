-- Удаление старой схемы и создание новой
DROP SCHEMA IF EXISTS pc_parts;
CREATE SCHEMA IF NOT EXISTS pc_parts;
USE pc_parts;

-- Таблица пользователей
CREATE TABLE `Users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `login` VARCHAR(20) UNIQUE NOT NULL,
  `first_name` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(20) NOT NULL,
  `e_mail` VARCHAR(30) UNIQUE NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  `password_` VARCHAR(20) NOT NULL,
  `account_type` ENUM('User', 'Admin') DEFAULT 'User',
  `profile_image` VARCHAR(20)
);

-- Таблица складов
CREATE TABLE `Warehouses` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `address` TEXT NOT NULL,
  `capacity` INT NOT NULL,
  `image` VARCHAR(20),
  `creation_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица комплектующих
CREATE TABLE `Components` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `vendor` VARCHAR(40) NOT NULL,
  `model` VARCHAR(90) NOT NULL,
  `type` VARCHAR(50) NOT NULL,
  `creation_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` INT,
  `image` VARCHAR(20),
  FOREIGN KEY (`created_by`) REFERENCES `Users` (`id`) ON DELETE SET NULL
);

-- Таблица остатков на складах
CREATE TABLE `Warehouse_stock` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `warehouse_id` INT NOT NULL,
  `component_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`warehouse_id`) REFERENCES `Warehouses` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`) ON DELETE CASCADE
);

-- Таблица поставщиков
CREATE TABLE `Suppliers` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `e_mail` VARCHAR(30),
  `phone_number` VARCHAR(15),
  `image` VARCHAR(20),
  `address` TEXT
);

-- Связь поставщиков с комплектующими
CREATE TABLE `Supplier_components` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `supplier_id` INT NOT NULL,
  `component_id` INT NOT NULL,
  `price` DECIMAL(10, 2) NOT NULL,
  `supply_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`supplier_id`) REFERENCES `Suppliers` (`id`) ON DELETE CASCADE,
  FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`)
);
