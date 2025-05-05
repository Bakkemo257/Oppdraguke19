drop database if exists ticket_system;
create database ticket_system;

use ticket_system;

create table tickets (
  id char(36) not null, -- UUID / GUID
  title varchar(64) not null,
  description varchar(255) not null,
  email varchar(64) not null,
  name varchar(64) not null,
  status enum('open', 'closed', 'in progress'),
  deleted boolean not null default false
);

create table clients (
  id int not null auto_increment primary key,
  email varchar(64) not null unique,
  name varchar(64) not null,
  hash varchar(32) not null,
  salt varchar(32) not null,
  admin boolean not null default false
);

create table categories (
  id int not null auto_increment primary key,
  label varchar(32) not null
);

create table ticket_categories (
  ticket_id int not null references tickets(id),
  category_id int not null references categories(id),
  primary key (ticket_id, category_id)
);