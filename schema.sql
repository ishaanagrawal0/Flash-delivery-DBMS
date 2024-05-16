CREATE DATABASE flash;
USE flash;

CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    Age INT NOT NULL CHECK (Age BETWEEN 5 AND 105),
    Address VARCHAR(255) NOT NULL,
    Membership VARCHAR(255),
    Email_id VARCHAR(255) UNIQUE CHECK (Email_id LIKE '%@%.%'),
    Password VARCHAR(255) NOT NULL
);
ALTER TABLE customer AUTO_INCREMENT = 1;

CREATE TABLE customer_contact (
    customer_id INT NOT NULL,
    contact_number VARCHAR(255) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    CHECK (contact_number REGEXP '^[0-9]{10}$')
);

CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(255) NOT NULL,
    Age INT NOT NULL CHECK (Age BETWEEN 5 AND 105),
    Address VARCHAR(255),
    Email_id VARCHAR(255) UNIQUE CHECK (Email_id LIKE '%@%.%'),
    Password VARCHAR(255) NOT NULL
);
ALTER TABLE admin AUTO_INCREMENT = 1;

CREATE TABLE supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(255) NOT NULL UNIQUE,
    CHECK (contact_number REGEXP '^[0-9]{10}$')
);
ALTER TABLE supplier AUTO_INCREMENT = 1;


CREATE TABLE payment (
    final_price INT NOT NULL,
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_method VARCHAR(255) NOT NULL
);
ALTER TABLE payment AUTO_INCREMENT = 1;

CREATE TABLE coupon (
    coupon_id INT AUTO_INCREMENT PRIMARY KEY,
    discount INT NOT NULL
);
ALTER TABLE coupon AUTO_INCREMENT = 1;

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    billing_address VARCHAR(255) NOT NULL,
    final_price INT NOT NULL,
    payment_id INT NOT NULL,
    customer_id INT NOT NULL,
    coupon_id INT,
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
ALTER TABLE orders AUTO_INCREMENT = 1;

CREATE TABLE delivery_partner (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    order_id INT NOT NULL,
    contact_number INT NOT NULL UNIQUE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CHECK (contact_number REGEXP '^[0-9]{10}$')
);
ALTER TABLE delivery_partner AUTO_INCREMENT = 1;

ALTER TABLE delivery_partner
    MODIFY COLUMN contact_number BIGINT;


CREATE TABLE order_history (
    total_cost INT NOT NULL,
    deliver_address VARCHAR(255),
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);
ALTER TABLE category AUTO_INCREMENT = 1;

CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
ALTER TABLE product AUTO_INCREMENT = 1;


CREATE TABLE cart (
    cost INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);

CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);
ALTER TABLE inventory AUTO_INCREMENT = 1;

CREATE TABLE supplier_product (
    supplier_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (supplier_id, product_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);


-- Relationship tables

CREATE TABLE views (
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    PRIMARY KEY (product_id, customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE has (
    order_id INT PRIMARY KEY,
    payment_id INT NOT NULL,
    transaction_fee INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id)
);

CREATE TABLE manages (
    admin_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (admin_id, category_id),
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE feedback (
	feedback_id INT AUTO_INCREMENT NOT NULL,
    customer_id INT NOT NULL,
    feedback LONGTEXT,
    PRIMARY KEY (feedback_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);
ALTER TABLE feedback AUTO_INCREMENT = 1;

-- Inserting data into customer table
INSERT INTO customer (customer_name, Age, Address, Membership, Email_id, Password)
VALUES
    ('Rahul Sharma', 30, '123 MG Road', 'Gold', 'rahul.sharma@gmail.com', 'password123'),
    ('Priya Patel', 51, '456 Greater Kailash', 'Basic', 'priya.patel@gmail.com', 'securepass'),
    ('Amit Kumar', 35, '789 Hauz Khas', 'Gold', 'amit.kumar@gmail.com', 'amit123'),
    ('Anjali Singh', 28, '456 Shahadra', 'Basic', 'anjali.singh@gmail.com', 'singh@123'),
    ('Neha Gupta', 32, '789 Nehru Enclave', 'Basic', 'neha.gupta@gmail.com', 'neha@456'),
    ('Vikram Mehta', 57, '321 Chandni Chowk', 'Gold', 'vikram.mehta@gmail.com', 'mehta123'),
    ('Pooja Shah', 29, '654 Sector-72 Noida', 'Basic', 'pooja.shah@gmail.com', 'pooja@123'),
    ('Rajesh Patel', 33, '987 Sector-69 Gurgaon', 'Gold', 'rajesh.patel@gmail.com', 'rajesh@123'),
    ('Sneha Joshi', 56, '852 Indirapuram', 'Basic', 'sneha.joshi@gmail.com', 'sneha@123'),
    ('Aryan Verma', 31, '147 Ghaziabad', 'Gold', 'aryan.verma@gmail.com', 'aryan@123'),
    ('Rajesh Kumar', 35, '123, Ganga Nagar, New Delhi', 'Gold', 'rajesh@example.com', 'password123');

-- Inserting data into customer_contact table
INSERT INTO customer_contact (customer_id, contact_number)
VALUES
    (1, '9876543210'),
    (1, '8765432109'),
    (2, '7654321098'),
    (3, '6543210987'),
    (4, '5432109876'),
    (5, '4321098765'),
    (6, '3210987654'),
    (7, '2109876543'),
    (8, '1098765432'),
    (9, '9876543210');

-- Inserting data into admin table
INSERT INTO admin (admin_name, Age, Address, Email_id, Password)
VALUES
    ('Arun Sharma', 35, '789 Gandhi St', 'arun.sharma@gmail.com', 'adminpass'),
    ('Neha Singh', 40, '654 Akbar Rd', 'neha.singh@gmail.com', 'admin@123'),
    ('Vijay Kumar', 38, '987 Nehru Rd', 'vijay.kumar@gmail.com', 'kumar@123'),
    ('Ananya Patel', 42, '321 Golf Course Ln', 'ananya.patel@gmail.com', 'ananya@123'),
    ('Raj Mehta', 37, '147 Gandhi St', 'raj.mehta@gmail.com', 'mehta@123');

-- Inserting data into supplier table
INSERT INTO supplier (supplier_name, contact_number)
VALUES
    ('Supplier1', '9876543210'),
    ('Supplier2', '8765432109'),
    ('Supplier3', '7654321098'),
    ('Supplier4', '6543210987'),
    ('Supplier5', '5432109876');

INSERT INTO payment (final_price, payment_method)
VALUES
    (589, 'Credit Card'),
    (180, 'PayPal'),
    (200, 'Net Banking'),
    (220, 'Credit Card'),
    (180, 'Debit Card'),
    (195, 'UPI'),
    (210, 'Cash on Delivery'),
    (240, 'PayTM'),
    (185, 'Google Pay'),
    (255, 'PhonePe'),
    (189, 'Debit Card'),
    (289, 'Credit Card');

INSERT INTO orders (billing_address, final_price, payment_id, customer_id, coupon_id)
VALUES
    ('123 MG Road', 589, 1, 1, NULL),
    ('456 Greater Kailash', 180, 2, 2, NULL),
    ('789 Hauz Khas', 200, 3, 3, NULL),
    ('456 Shahadra', 220, 4, 4, NULL),
    ('789 Nehru Enclave', 180, 5, 5, NULL),
    ('321 Chandni Chowk', 195, 6, 6, NULL),
    ('654 Sector-72 Noida', 210, 7, 7, NULL),
    ('987 Sector-69 Gurgaon', 240, 8, 8, NULL),
    ('852 Indirapuram', 185, 9, 9, NULL),
    ('147 Ghaziabad', 255, 10, 10, NULL),
    ('123 MG Road', 189, 11, 1, NULL),
    ('123 MG Road', 289, 12, 1, NULL);


INSERT INTO delivery_partner (Name, order_id, contact_number)
VALUES
    ('DeliveryPartner1', 1, 9876543210),
    ('DeliveryPartner2', 2, 8765432109),
    ('DeliveryPartner3', 3, 7654321098),
    ('DeliveryPartner4', 4, 6543210987),
    ('DeliveryPartner5', 5, 5432109876);

-- Inserting data into coupon table
INSERT INTO coupon (discount)
VALUES
    (10),
    (20),
    (15),
    (25),
    (30),
    (5),
    (12),
    (18),
    (22),
    (28);    

-- Inserting data into cart table
-- INSERT INTO cart (cost, coupon_id, customer_id)
-- VALUES
 --   (50, 1, 1),
 --   (75, 2, 2),
 --   (100, 3, 3),
 --   (125, 4, 4),
 --   (150, 5, 5),
 --   (175, 6, 6),
 --   (200, 7, 7),
 --   (225, 8, 8),
 --   (250, 9, 9),
 --   (275, 10, 10);

-- Inserting data into has table
INSERT INTO has (order_id, payment_id, transaction_fee)
VALUES
    (1, 1, 5),
    (2, 2, 2),
    (3, 3, 3),
    (4, 4, 4),
    (5, 5, 5),
    (6, 6, 6),
    (7, 7, 7),
    (8, 8, 8),
    (9, 9, 9),
    (10, 10, 10),
    (11, 11, 3),
    (12, 12, 4);

INSERT INTO category (category_name)
VALUES
    ('Electronics'),
    ('Clothing'),
    ('Books'),
    ('Home Appliances'),
    ('Beauty & Health');

-- Inserting data into product table
INSERT INTO product (product_name, quantity, price, category_id)
VALUES
    ('Smartphone', 50, 599, 1),
    ('T-Shirt', 100, 25, 2),
    ('Novel', 30, 15, 3),
    ('Refrigerator', 20, 799, 4),
    ('Face Cream', 50, 10, 5),
    ('Laptop', 30, 999, 1),
    ('Jeans', 80, 35, 2),
    ('Cooking Range', 15, 499, 4),
    ('Shampoo', 70, 8, 5),
    ('Tablet', 40, 299, 1);

INSERT INTO supplier_product (supplier_id, product_id, quantity)
VALUES
    (4, 4, 15),  -- Supplier 4 supplies 15 units of Product 4
    (1, 5, 40),  -- Supplier 1 supplies 40 units of Product 5
    (2, 6, 20),  -- Supplier 2 supplies 20 units of Product 6
    (3, 7, 35),  -- Supplier 3 supplies 35 units of Product 7
    (4, 8, 10),  -- Supplier 4 supplies 10 units of Product 8
    (5, 9, 50),  -- Supplier 5 supplies 50 units of Product 9
    (1, 1, 20),  -- Supplier 1 supplies 20 units of Product 1
    (2, 2, 60),  -- Supplier 2 supplies 30 units of Product 2
    (3, 3, 25),  -- Supplier 3 supplies 25 units of Product 3
    (3, 10, 100),
    (5, 2, 20);

INSERT INTO views (product_id, customer_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (2, 1),
    (5, 1),
    (6, 1);
    
-- Inserting data into manages table
INSERT INTO manages (admin_id, category_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 1),
    (4, 2),
    (4, 3),
    (5, 4),
    (5, 5);

INSERT INTO order_history (total_cost, deliver_address, order_id, customer_id)
VALUES
    (589, '123 MG Road', 1, 1),
    (180, '456 Greater Kailash', 2, 2),
    (200, '789 Hauz Khas', 3, 3),
    (220, '456 Shahadra', 4, 4),
    (180, '789 Nehru Enclave', 5, 5),
    (195, '321 Chandni Chowk', 6, 6),
    (210, '654 Sector-72 Noida', 7, 7),
    (240, '987 Sector-69 Gurgaon', 8, 8),
    (185, '852 Indirapuram', 9, 9),
    (255, '147 Ghaziabad', 10, 10),
    (189, '123 MG Road', 11, 1),
    (289, '123 MG Road', 12, 1);
    
    
INSERT INTO inventory (product_id, quantity)
VALUES
    (1, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 1)),
    (2, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 2)),
    (3, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 3)),
    (4, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 4)),
    (5, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 5)),
    (6, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 6)),
    (7, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 7)),
    (8, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 8)),
    (9, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 9)),
    (10, (SELECT SUM(quantity) FROM supplier_product WHERE product_id = 10));


UPDATE delivery_partner
SET Name = 'Mohd Aazam'
WHERE delivery_id = 1;

