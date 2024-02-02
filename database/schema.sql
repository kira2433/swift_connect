CREATE DATABASE swift_connect;
USE swift_connect;

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role ENUM('customer', 'administrator') NOT NULL DEFAULT 'customer',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  company_name VARCHAR(255) NOT NULL,
  platform_name VARCHAR(255) NOT NULL,
  contact_name VARCHAR(255) NOT NULL,
  contact_email VARCHAR(255) NOT NULL,
  status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE connection_requests (
  id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  swift_address VARCHAR(255) NOT NULL,
  end_user_details TEXT,
  platform_integration_details TEXT,
  submitted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);


CREATE TABLE configurations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  connection_request_id INT NOT NULL,
  swift_connection_details TEXT,
  user_access_details TEXT,
  configured_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (connection_request_id) REFERENCES connection_requests(id)
);

INSERT INTO users (username, email, password, role, created_at)
VALUES ('admin', 'admin@example.com', 'hashed_password', 'administrator', CURRENT_TIMESTAMP);


INSERT INTO customers (user_id, company_name, platform_name, contact_name, contact_email)
VALUES (1, 'examplePVT', 'SWIFT', 'admininfo', 'exmaple@example.com')