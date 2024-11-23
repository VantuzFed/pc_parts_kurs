-- kursach-new
drop schema if exists pc_parts;
create schema if not exists pc_parts;
use pc_parts; 

CREATE TABLE `Users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `login` varchar(20) UNIQUE NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `e_mail` varchar(30) UNIQUE NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `password_` varchar(20) NOT NULL,
  `account_type` enum('User', 'Admin') DEFAULT 'User',
  `profile_image` varchar(20)
);

CREATE TABLE `Warehouses` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `address` text NOT NULL,
  `capacity` int NOT NULL,
  `creation_date` timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Components` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `vendor` varchar(40) NOT NULL,
  `model` varchar(90) NOT NULL,
  `type` varchar(50) NOT NULL,
  `price` decimal NOT NULL,
  `creation_date` timestamp DEFAULT CURRENT_TIMESTAMP,
  `update_date` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comp_image` varchar(20)
);

CREATE TABLE `Warehouse_stock` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `warehouse_id` int unique,
  `component_id` int unique,
  `quantity` int NOT NULL,
  `last_updated` timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Suppliers` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `e_mail` varchar(30),
  `phone_number` varchar(15),
  `address` text
);

CREATE TABLE `Supplier_components` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `supplier_id` int unique,
  `component_id` int unique,
  `supply_price` numeric(10,2) NOT NULL,
  `supply_date` timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Orders` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int unique,
  `order_date` timestamp DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(50) DEFAULT 'В обработке',
  `total_price` numeric(10,2) DEFAULT 0
);

CREATE TABLE `Order_details` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `order_id` int unique,
  `component_id` int unique,
  `quantity` int,
  `unit_price` numeric(10,2)
);

ALTER TABLE `Warehouses` ADD FOREIGN KEY (`id`) REFERENCES `Warehouse_stock` (`warehouse_id`) ON DELETE CASCADE;

ALTER TABLE `Components` ADD FOREIGN KEY (`id`) REFERENCES `Warehouse_stock` (`component_id`) ON DELETE CASCADE;

ALTER TABLE `Supplier_components` ADD FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`);

ALTER TABLE `Suppliers` ADD FOREIGN KEY (`id`) REFERENCES `Supplier_components` (`supplier_id`) ON DELETE CASCADE;

ALTER TABLE `Users` ADD FOREIGN KEY (`id`) REFERENCES `Orders` (`user_id`) ON DELETE CASCADE;

ALTER TABLE `Order_details` ADD FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`);

ALTER TABLE `Order_details` ADD FOREIGN KEY (`order_id`) REFERENCES `Orders` (`id`) ON DELETE CASCADE;
