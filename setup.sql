-- Sample Database Setup Script
-- Creates sample tables for demonstration

-- Create database
CREATE DATABASE IF NOT EXISTS analytics_db;
USE analytics_db;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    state VARCHAR(2),
    country VARCHAR(50) DEFAULT 'USA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lifetime_value DECIMAL(10, 2) DEFAULT 0,
    INDEX idx_state (state),
    INDEX idx_created (created_at)
) ENGINE=InnoDB;

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2),
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_price (price)
) ENGINE=InnoDB;

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    INDEX idx_customer (customer_id),
    INDEX idx_order_date (order_date),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- Order Items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
) ENGINE=InnoDB;

-- Insert sample customers
INSERT INTO customers (name, email, state, lifetime_value) VALUES
('John Doe', 'john@example.com', 'CA', 5000.00),
('Jane Smith', 'jane@example.com', 'NY', 8500.00),
('Bob Johnson', 'bob@example.com', 'TX', 3200.00),
('Alice Williams', 'alice@example.com', 'CA', 12000.00),
('Charlie Brown', 'charlie@example.com', 'FL', 6700.00);

-- Insert sample products
INSERT INTO products (name, category, price, cost, stock_quantity) VALUES
('Laptop Pro', 'Electronics', 1299.99, 800.00, 50),
('Wireless Mouse', 'Electronics', 29.99, 15.00, 200),
('Office Chair', 'Furniture', 299.99, 150.00, 75),
('Desk Lamp', 'Furniture', 49.99, 25.00, 150),
('USB Cable', 'Accessories', 9.99, 3.00, 500);

-- Insert sample orders
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15', 1329.98, 'completed'),
(2, '2024-01-20', 349.98, 'completed'),
(3, '2024-02-01', 1299.99, 'completed'),
(4, '2024-02-10', 379.97, 'pending'),
(5, '2024-02-15', 59.98, 'completed');

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1299.99),
(1, 2, 1, 29.99),
(2, 3, 1, 299.99),
(2, 4, 1, 49.99),
(3, 1, 1, 1299.99);
