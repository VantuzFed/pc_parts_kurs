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
  `account_type` enum('User','Admin') DEFAULT 'User',
  `profile_image` varchar(20)
);

CREATE TABLE `Sessions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int UNIQUE,
  `token` varchar(40) UNIQUE,
  `ip_address` varchar(12),
  `start_time` timestamp DEFAULT CURRENT_TIMESTAMP,
  `expiration_date` timestamp
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
  `warehouse_id` int UNIQUE,
  `component_id` int UNIQUE,
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
  `supplier_id` int UNIQUE,
  `component_id` int UNIQUE,
  `supply_price` numeric(10,2) NOT NULL,
  `supply_date` timestamp DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE `Orders` (
--   `id` int PRIMARY KEY AUTO_INCREMENT,
--   `user_id` int UNIQUE,
--   `order_date` timestamp DEFAULT CURRENT_TIMESTAMP,
--   `status` varchar(50) DEFAULT 'В обработке',
--   `total_price` numeric(10,2) DEFAULT 0
-- );

-- CREATE TABLE `Order_details` (
--   `id` int PRIMARY KEY AUTO_INCREMENT,
--   `order_id` int UNIQUE,
--   `component_id` int UNIQUE,
--   `quantity` int,
--   `unit_price` numeric(10,2)
-- );

ALTER TABLE `Sessions` ADD FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE;

ALTER TABLE `Warehouse_stock` ADD FOREIGN KEY (`warehouse_id`) REFERENCES `Warehouses` (`id`) ON DELETE CASCADE;

ALTER TABLE `Warehouse_stock` ADD FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`) ON DELETE CASCADE;

ALTER TABLE `Supplier_components` ADD FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`);

ALTER TABLE `Supplier_components` ADD FOREIGN KEY (`supplier_id`) REFERENCES `Suppliers` (`id`) ON DELETE CASCADE;

-- ALTER TABLE `Orders` ADD FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE CASCADE;

-- ALTER TABLE `Order_details` ADD FOREIGN KEY (`component_id`) REFERENCES `Components` (`id`);

-- ALTER TABLE `Order_details` ADD FOREIGN KEY (`order_id`) REFERENCES `Orders` (`id`) ON DELETE CASCADE;
