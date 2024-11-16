-- kursach
drop schema if exists pc_parts;
create schema if not exists pc_parts;
use pc_parts;

create table video_cards(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20),
price int
);

create table memory_units(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20),
price int
);

create table cpus(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20)
);

create table motherboards(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20),
price int
);

create table fans(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20),
price int
);

create table cases(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20),
price int
);

create table hdds(
id int primary key auto_increment,
vendor varchar(20),
model varchar(20),
size int,
price int
);


create table users(
id int primary key auto_increment,
fio varchar(60),
e_mail varchar(30),
phone_number int,
password_ varchar(20),
profile_image varchar(20)
);

create table pcs(
id int primary key auto_increment,
user_id int unique,
video_card_id int unique,
memory_unit_id int unique,
cpu_id int unique,
motherboard_id int unique,
fan_id int unique,
case_id int unique,
hdd_id int unique,
price int unique,
foreign key (video_card_id) references video_cards(id),
foreign key (memory_unit_id) references memory_units(id),
foreign key (cpu_id) references cpus(id),
foreign key (motherboard_id) references motherboards(id),
foreign key (fan_id) references fans(id),
foreign key (case_id) references cases(id),
foreign key (user_id) references users(id),
foreign key (hdd_id) references hdds(id)
);