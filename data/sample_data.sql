-- Additional sample data for testing

-- More customers
INSERT INTO customers (name, email, state, lifetime_value) VALUES
('David Lee', 'david@example.com', 'WA', 4500.00),
('Emma Davis', 'emma@example.com', 'CA', 9200.00),
('Frank Miller', 'frank@example.com', 'NY', 7800.00),
('Grace Wilson', 'grace@example.com', 'TX', 5600.00),
('Henry Moore', 'henry@example.com', 'FL', 3900.00);

-- More products
INSERT INTO products (name, category, price, cost, stock_quantity) VALUES
('Mechanical Keyboard', 'Electronics', 149.99, 80.00, 100),
('Monitor Stand', 'Furniture', 79.99, 40.00, 80),
('Webcam HD', 'Electronics', 89.99, 50.00, 120),
('Ergonomic Mouse Pad', 'Accessories', 24.99, 10.00, 300),
('Phone Holder', 'Accessories', 19.99, 8.00, 250);
