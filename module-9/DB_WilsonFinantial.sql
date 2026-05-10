-- Name: Red Team
-- Date: May 2026
-- Assignment: Milestone 2 - Willson Financial
-- Purpose: Create and populate a normalized MySQL database for the Willson Financial case study.
-- Source: Based on the Willson Financial case study and Red Team Milestone 1 business rules.

-- drop database user if exists 
DROP USER IF EXISTS 'financial_user'@'localhost';


-- create financial_user and grant them all privileges to the willson database 
CREATE USER 'financial_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'willson';

-- grant all privileges to the willson database to user financial_user on localhost 
GRANT ALL PRIVILEGES ON willson_financial.* TO 'financial_user'@'localhost';

DROP DATABASE IF EXISTS willson_financial;
CREATE DATABASE IF NOT EXISTS willson_financial;
USE willson_financial;

-- Drop tables in order of dependency to avoid constraint errors
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS billing_structure;
DROP TABLE IF EXISTS employee;

-- 1. EMPLOYEE TABLE
-- Complies with 3NF: No transitive dependencies (F_Name/L_Name depend only on ID)
CREATE TABLE employee (
    employee_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    f_name VARCHAR(50) NOT NULL,
    l_name VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL, -- e.g., Advisor, Office Employee
    hire_date DATE NOT NULL
);

-- 2. BILLING STRUCTURE TABLE
-- Complies with 3NF: Separates rate/type from the Client table to avoid redundancy 
CREATE TABLE billing_structure (
    billing_structure_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    rate DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50) NOT NULL
);

-- 3. CLIENT TABLE
-- Complies with 3NF: Every field (Join_Date, Assets) depends directly on Client_ID
CREATE TABLE client (
    client_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    advisor_id INT NOT NULL, -- Link to Jake or Ned
    f_name VARCHAR(50) NOT NULL,
    l_name VARCHAR(50) NOT NULL,
    join_date DATE NOT NULL,
    total_assets DECIMAL(15, 2) NOT NULL,
    billing_structure_id INT NOT NULL,
    CONSTRAINT fk_advisor FOREIGN KEY (advisor_id) REFERENCES employee(employee_id),
    CONSTRAINT fk_billing FOREIGN KEY (billing_structure_id) REFERENCES billing_structure(billing_structure_id)
);

-- 4. TRANSACTION TABLE
-- Complies with 3NF: Records individual events tied only to a specific Client
CREATE TABLE transaction (
    transaction_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_amount DECIMAL(15, 2) NOT NULL,
    transaction_description VARCHAR(255),
    CONSTRAINT fk_client_trans FOREIGN KEY (client_id) REFERENCES client(client_id)
);

-- 5. APPOINTMENT TABLE
-- Complies with 3NF: Links a Client and Employee for a specific time/date
CREATE TABLE appointment (
    appointment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    employee_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    notes TEXT,
    CONSTRAINT fk_client_appt FOREIGN KEY (client_id) REFERENCES client(client_id),
    CONSTRAINT fk_employee_appt FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- POPULATE DATA
INSERT INTO employee (f_name, l_name, role, hire_date) VALUES 
('Jake', 'Willson', 'Advisor', '2022-01-10'),
('Ned', 'Willson', 'Advisor', '2022-01-10'),
('Phoenix', 'Two Star', 'Office Employee', '2022-02-15'),
('June', 'Santos', 'Compliance Manager', '2022-03-01');

INSERT INTO billing_structure (rate, type) VALUES 
(0.01, 'Assets Under Management'),
(0.015, 'Assets Under Management'),
(250.00, 'Flat Monthly Fee'),
(500.00, 'Flat Monthly Fee'),
(75.00, 'Hourly Consulting'),
(150.00, 'Hourly Consulting');

INSERT INTO client (advisor_id, f_name, l_name, join_date, total_assets, billing_structure_id) VALUES 
(1, 'Maria', 'Lopez', '2025-11-01', 500000.00, 1),
(2, 'Robert', 'Miller', '2025-12-15', 1250000.00, 2),
(1, 'Alice', 'Johnson', '2026-01-20', 75000.00, 3),
(2, 'Samuel', 'Rancher', '2026-02-10', 3000000.00, 1),
(1, 'Elena', 'Garcia', '2026-03-05', 150000.00, 5),
(2, 'David', 'Farmer', '2026-04-12', 850000.00, 4);

INSERT INTO transaction (client_id, transaction_date, transaction_amount, transaction_description) VALUES 
(1, '2026-05-01', -1500.00, 'Monthly Withdrawal'),
(2, '2026-05-02', 10000.00, 'Stock Dividend'),
(4, '2026-05-02', 50000.00, 'Land Sale Deposit'),
(4, '2026-05-03', -500.00, 'Management Fee'),
(6, '2026-05-04', 2500.00, 'Quarterly Interest'),
(1, '2026-05-05', 300.00, 'Account Rebalance');

INSERT INTO appointment (client_id, employee_id, appointment_date, notes) VALUES 
(1, 1, '2026-05-10 10:00:00', 'Annual portfolio review'),
(2, 2, '2026-05-11 14:00:00', 'Tax planning strategy'),
(3, 3, '2026-05-12 09:00:00', 'New client intake with Phoenix'),
(4, 2, '2026-05-13 11:30:00', 'Estate planning discussion'),
(5, 1, '2026-05-14 15:00:00', 'Consulting on retirement'),
(6, 4, '2026-05-15 13:00:00', 'Compliance document signing');