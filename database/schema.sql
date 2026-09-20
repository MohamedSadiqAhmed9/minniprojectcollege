-- Database Schema for Visitor Pass Management System

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(20) DEFAULT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS passes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pass_number VARCHAR(50) NOT NULL,
    visitor_type VARCHAR(50) NOT NULL,
    visit_purpose VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS pass_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pass_id INT NOT NULL,
    request_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pass_id) REFERENCES passes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pass_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pass_id INT NOT NULL,
    processed_date DATE DEFAULT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pass_id) REFERENCES passes(id) ON DELETE CASCADE
);

-- Default Accounts (safe to re-run)
INSERT INTO users (name, email, password, mobile_number, role)
VALUES ('Security Officer', 'admin@example.com', 'admin123', NULL, 'Security Officer')
ON DUPLICATE KEY UPDATE name=VALUES(name), password=VALUES(password), role=VALUES(role);

INSERT INTO users (name, email, password, mobile_number, role)
VALUES ('Visitor', 'end_user@example.com', 'user123', NULL, 'Visitor')
ON DUPLICATE KEY UPDATE name=VALUES(name), password=VALUES(password), role=VALUES(role);
