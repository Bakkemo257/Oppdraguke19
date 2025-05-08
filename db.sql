DROP DATABASE IF EXISTS ticket_system;
CREATE DATABASE ticket_system;

USE ticket_system;

CREATE TABLE tickets (
  id CHAR(36) NOT NULL PRIMARY KEY DEFAULT UUID(), -- UUID / GUID
  title VARCHAR(64) NOT NULL,
  description VARCHAR(255) NOT NULL,
  email VARCHAR(64) NOT NULL,
  name VARCHAR(64) NOT NULL,
  status ENUM('open', 'closed', 'in progress') DEFAULT 'open',
  deleted BOOLEAN NOT NULL DEFAULT false
) ENGINE = InnoDB;

CREATE TABLE clients (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(64) NOT NULL,
  hash CHAR(162) NOT NULL,
  admin BOOLEAN NOT NULL DEFAULT false
) ENGINE = InnoDB;

CREATE TABLE categories (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  label VARCHAR(32) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE ticket_categories (
  ticket_id CHAR(36) NOT NULL,
  category_id INT NOT NULL,
  -- PRIMARY KEY (ticket_id, category_id),
  CONSTRAINT `fk_tickets` FOREIGN KEY (ticket_id) REFERENCES tickets(id),
  CONSTRAINT `fk_categories` FOREIGN KEY (category_id) REFERENCES categories(id)
) ENGINE = InnoDB;