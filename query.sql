create database if not exists e_commerce;

use e_commerce;

create table if not exists user_register(
    user_id int primary key auto_increment,
    user_mobile varchar(15) not null unique,
    user_name varchar(50) not null,
    user_email varchar(100) not null unique,
    user_password varchar(255) not null,
    created_at timestamp default current_timestamp
);

create table if not exists user_details(
    user_id int primary key,
    address varchar(255) not null,
    city varchar(100) not null,
    state varchar(100) not null,
    zip_code varchar(20) not null,
    country varchar(100) not null,
    foreign key (user_id) references user_register(user_id) on delete cascade
);

DELIMITER $$

CREATE TRIGGER after_user_insert
AFTER INSERT ON user_register
FOR EACH ROW
BEGIN
    INSERT INTO user_details (user_id, address, city, state, zip_code, country)
    VALUES (NEW.user_id, '', '', '', '', '');
END$$

DELIMITER ;


create table if not exists cart_details(
    cart_id int primary key auto_increment,
    user_id int,
    product_id int,
    quantity int not null,
    added_at timestamp default current_timestamp,
    status varchar(50) not null,
    foreign key (user_id) references user_register(user_id) on delete cascade
)

create table if not exists category_details(
    category_id int primary key auto_increment,
    category_name varchar(100) not null unique,
    description text,
    created_at timestamp default current_timestamp
)

create table if not exists product_details(
    product_id int primary key auto_increment,
    product_name varchar(100) not null,
    description text,
    price decimal(10, 2) not null,
    stock int not null,
    category_id int,
    created_at timestamp default current_timestamp
    foreign key (category_id) references category_details(category_id) on delete set null
)

create table if not exists order_details(
    order_id int primary key auto_increment,
    user_id int,
    product_id int,
    quantity int not null,
    total_amount decimal(10, 2) not null,
    order_date timestamp default current_timestamp,
    status varchar(50) not null,
    shipping_address varchar(255) not null,
    foreign key (user_id) references user_register(user_id) on delete cascade ,
    foreign key (product_id) references product_details(product_id) on delete cascade
)
