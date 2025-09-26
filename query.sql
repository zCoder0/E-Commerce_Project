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



create table if not exists category_details(
    category_id int primary key auto_increment,
    category_name varchar(100) not null unique,
    description text,
    created_at timestamp default current_timestamp
);

create table if not exists supplier_details(
    supplier_id int primary key auto_increment,
    supplier_name varchar(100) not null,
    contact_name varchar(100),
    address varchar(255),
    city varchar(100),
    postal_code varchar(20),
    country varchar(100),
    phone varchar(20),
    created_at timestamp default current_timestamp
);

create table if not exists product_details(
    product_id int primary key auto_increment,
    product_name varchar(100) not null,
    description text,
    price decimal(10, 2) not null,
    offer int default 0,
    stock int not null,
    category_id int,
    supplier_id int,
    created_at timestamp default CURRENT_TIMESTAMP,
    foreign key (category_id) references category_details(category_id) on delete set NULL,
    foreign key (supplier_id) references supplier_details(supplier_id) on delete set null
);

create table if not exists product_images(
    image_id int primary key auto_increment,
    product_id int,
    image_url varchar(255) not null,
    uploaded_at timestamp default current_timestamp,
    foreign key (product_id) references product_details(product_id) on delete cascade
);

DELIMITER $$
CREATE TRIGGER after_product_insert
AFTER INSERT ON product_details
FOR EACH ROW
BEGIN
    INSERT INTO product_images (product_id, image_url)
    VALUES (NEW.product_id, 'default_image.png');
END$$
DELIMITER ;


create table if not exists reviews(
    review_id int primary key auto_increment,
    user_id int,
    product_id int,
    rating int check (rating >= 1 and rating <= 5),
    comment text,
    review_date timestamp default current_timestamp,
    foreign key (user_id) references user_register(user_id) on delete cascade,
    foreign key (product_id) references product_details(product_id) on delete cascade
);