/* Creating a new table with different data types
CREATE TABLE customer(
first_name VARCHAR(30) NOT NULL,
last_name VARCHAR(30) NOT NULL,
email VARCHAR(60) NOT NULL,
company VARCHAR(60) NOT NULL,
street VARCHAR(50) NOT NULL,
city VARCHAR(40) NOT NULL,
state CHAR(2) NOT NULL, 
zip SMALLINT NOT NULL,
phone VARCHAR(20) NOT NULL,
birth_date DATE NULL,
sex CHAR(1) NOT NULL,
date_entered TIMESTAMP NOT NULL,
id SERIAL PRIMARY KEY
); */

/* Insert values inside our table
INSERT INTO customer(first_name, last_name, email, company, street, city, state, zip, phone,
birth_date, sex, date_entered)
VALUES ('Bob', 'Jones', 'bobjones@test.com', 'ABB', 'Duhova 1444/2', 'Prague', 
'GA', '14000', '772-110-550', '1997-07-11', 'M', current_timestamp);
*/

/* Creating a new type for our variables
CREATE TYPE sex_type as enum
('M', 'F');
*/

/* Manually changing the type of our column 'sex' to a new maded 'sex_type' type.
Can do same via menu/properties on left but better through queries
ALTER TABLE customer
ALTER COLUMN sex TYPE sex_type USING sex::sex_type;
*/

/* Creating a new table which will contain sales employees 
CREATE TABLE sales_person(
first_name VARCHAR(30) NOT NULL,
last_name VARCHAR(30) NOT NULL,
email VARCHAR(60) NOT NULL,
company VARCHAR(60) NOT NULL,
street VARCHAR(50) NOT NULL,
city VARCHAR(40) NOT NULL,
state CHAR(2) NOT NULL DEFAULT 'PA', 
zip SMALLINT NOT NULL,
phone VARCHAR(20) NOT NULL,
birth_date DATE NULL,
sex CHAR(1) NOT NULL,
date_hired TIMESTAMP NOT NULL,
id SERIAL PRIMARY KEY
);
*/

/* Create a table for our product_type 
CREATE TABLE product_type(
name VARCHAR(30) NOT NULL,
id SERIAL PRIMARY KEY
);
*/

/* Creating a table of products also using REFERENCES to refer to a 'FOREIGN KEY' in another table instead of PRIMARY KEY
CREATE TABLE product(
type_id INTEGER REFERENCES product_type(id),
name VARCHAR(30)  NOT NULL,
supplier VARCHAR(30) NOT NULL,
description TEXT NOT NULL,
id SERIAL PRIMARY KEY
);
*/

-- Create a table to pack our orders with multiple products(for quantity)
-- CREATE TABLE item(
-- product_id INTEGER REFERENCES product(id),
-- size INTEGER NOT NULL,
-- color VARCHAR(30) NOT NULL,
-- picture VARCHAR(256) NOT NULL,
-- price NUMERIC(6, 2) NOT NULL,
-- id SERIAL PRIMARY KEY
-- );

-- Creating a talbe for our order
-- CREATE TABLE sales_order(
-- cust_id INTEGER REFERENCES customer(id),
-- sales_person_id INTEGER REFERENCES sales_person(id),
-- time_order_taken TIMESTAMP NOT NULL,
-- purchase_order_number INTEGER NOT NULL,
-- creadit_card_number VARCHAR(16) NOT NULL,
-- creadit_card_exper_month SMALLINT NOT NULL,
-- creadit_card_exper_day SMALLINT NOT NULL,
-- creadit_card_secret_code SMALLINT NOT NULL,
-- name_on_card VARCHAR(100) NOT NULL,
-- id SERIAL PRIMARY KEY
-- );


-- Creating a table to contain discounts, tax, if_taxed, etc.
-- CREATE TABLE sales_item(
-- item_id INTEGER REFERENCES item(id),
-- sales_order_id INTEGER REFERENCES sales_order(id),
-- quantity INTEGER NOT NULL,
-- discount NUMERIC(6,2) NULL DEFAULT 0,
-- taxable BOOLEAN NOT NULL DEFAULT FALSE, 
-- sales_tax_rate NUMERIC(6,2) NOT NULL DEFAULT 0,
-- id SERIAL PRIMARY KEY
-- )

-- !!! To add a new column 
-- ALTER TABLE sales_item ADD day_of_week VARCHAR(8);

-- !!! Modify a column
-- ALTER TABLE sales_item ALTER COLUMN day_of_week SET NOT NULL;

-- !!! Change the name of column
-- ALTER TABLE sales_item RENAME COLUMN day_of_week TO weekday;

-- !!! Drop a column
-- ALTER TABLE sales_item DROP COLUMN weekday;

-- CREATE TABLE transaction_type(
-- name VARCHAR(30) NOT NULL,
-- payment_type VARCHAR(30) NOT NULL,
-- id SERIAL PRIMARY KEY
-- )

-- !!! rename a table
-- ALTER TABLE transaction_type RENAME TO transaction;

-- !!! CREATING index on transaction
-- CREATE INDEX transaction_id ON transaction(name);

-- !!! DELETE A WHOLE DATA from the table
-- TRUNCATE TABLE transaction;

-- !!! DELETE table by itself
-- DROP TABLE transaction;

-- INSERT INTO product_type(name) VALUES ('Business');
-- INSERT INTO product_type(name) VALUES ('Casual');
-- INSERT INTO product_type(name) VALUES ('Athletic');

-- INSERT INTO product VALUES
-- (1, 'Grandview', 'Allen Edmonds', 'Classic businees shoe'),
-- (1, 'Clarkston', 'Allen Edmonds', 'Classic businees shoe'),
-- (1, 'Derby', 'John Varvatos', 'Classic businees shoe'),
-- (1, 'Ramsey', 'Mezlan', 'Classic businees shoe'),
-- (2, 'Hollis', 'Johnston & Murphy', 'Classic businees shoe'),
-- (2, 'Malek', 'Johnston & Murphy', 'Classic businees shoe'),
-- (3, 'Joyride', 'Nike', 'Classic businees shoe'),
-- (2, 'Air Force 1', 'Nike', 'Classic businees shoe'),
-- (2, 'Samba', 'Adidas', 'Classic businees shoe'),
-- (3, 'Revel 3', 'Brooks', 'Classic businees shoe'),
-- (3, 'Air Jordan', 'Johnston & Murphy', 'Classic businees shoe'),
-- (3, 'Ghost 12', 'Brooks', 'Classic businees shoe')

-- ALTER TABLE customer ALTER COLUMN zip TYPE INTEGER;

-- INSERT INTO customer(
-- first_name, last_name, email, company, street, city, state, zip, phone, birth_date, sex, date_entered
-- ) VALUES
-- ('Alice','Johnson','alice.johnson@example.com','Acme Corp','123 Market St','San Francisco','CA',94105,'+1-415-555-0101','1992-04-18','F',TIMESTAMP '2025-10-31 10:05:00'),
-- ('Bob','Smith','bob.smith@example.com','Apex LLC','450 7th Ave','New York','NY',10001,'+1-212-555-0102','1988-11-23','M',TIMESTAMP '2025-10-31 11:15:00'),
-- ('Carla','Diaz','carla.diaz@example.com','ByteWorks','200 Congress Ave','Austin','TX',73301,'+1-512-555-0103','1995-07-12','F',TIMESTAMP '2025-10-31 12:30:00'),
-- ('Daniel','Kim','daniel.kim@example.com','SunTech','50 Ocean Dr','Miami','FL',33101,'+1-305-555-0104','1990-09-05','M',TIMESTAMP '2025-10-31 13:45:00'),
-- ('Eva','Novak','eva.novak@example.com','RainCloud Inc','400 Pine St','Seattle','WA',98101,'+1-206-555-0105','1993-02-02','F',TIMESTAMP '2025-10-31 14:00:00'),
-- ('Frank','Muller','frank.muller@example.com','Windy City Co','233 Wacker Dr','Chicago','IL',60601,'+1-312-555-0106','1985-12-17','M',TIMESTAMP '2025-10-31 15:10:00'),
-- ('Grace','Lee','grace.lee@example.com','Harbor Labs','1 Beacon St','Boston','MA',2116,'+1-617-555-0107','1997-05-21','F',TIMESTAMP '2025-10-31 16:20:00'),
-- ('Henry','Adams','henry.adams@example.com','Keystone Analytics','1600 Market St','Philadelphia','PA',19103,'+1-215-555-0108','1991-08-30','M',TIMESTAMP '2025-10-31 17:35:00'),
-- ('Isabella','Rossi','isabella.rossi@example.com','Desert Data','101 N Central Ave','Phoenix','AZ',85001,'+1-602-555-0109','1994-03-03','F',TIMESTAMP '2025-11-01 09:05:00'),
-- ('Jack','Wilson','jack.wilson@example.com','Mile High Ventures','1700 Broadway','Denver','CO',80202,'+1-303-555-0110','1989-01-10','M',TIMESTAMP '2025-11-01 10:10:00'),
-- ('Karen','Chen','karen.chen@example.com','PeachTech','200 Peachtree St','Atlanta','GA',30301,'+1-404-555-0111','1996-06-06','F',TIMESTAMP '2025-11-01 11:20:00'),
-- ('Liam','Oneil','liam.oneil@example.com','Triangle BI','500 Walnut St','Cary','NC',27513,'+1-919-555-0112','1992-10-14','M',TIMESTAMP '2025-11-01 12:25:00'),
-- ('Maya','Patel','maya.patel@example.com','Lakefront Labs','600 Superior Ave','Cleveland','OH',44101,'+1-216-555-0113','1993-11-11','F',TIMESTAMP '2025-11-01 13:35:00'),
-- ('Noah','Fisher','noah.fisher@example.com','Motor City Data','2211 Woodward Ave','Detroit','MI',48201,'+1-313-555-0114','1987-04-28','M',TIMESTAMP '2025-11-01 14:40:00'),
-- ('Olivia','Martin','olivia.martin@example.com','Rose City Apps','120 SW 5th Ave','Portland','OR',97201,'+1-503-555-0115','1998-12-01','F',TIMESTAMP '2025-11-01 15:50:00'),
-- ('Peter','Novak','peter.novak@example.com','Strip Systems','10 Fremont St','Las Vegas','NV',89101,'+1-702-555-0116','1986-03-09','M',TIMESTAMP '2025-11-02 09:00:00'),
-- ('Quinn','Garcia','quinn.garcia@example.com','Garden State Data','300 Main St','Edison','NJ',8817,'+1-732-555-0117','1995-09-19','F',TIMESTAMP '2025-11-02 10:05:00'),
-- ('Ryan','Hall','ryan.hall@example.com','Potomac Analytics','1550 Wilson Blvd','Arlington','VA',22201,'+1-703-555-0118','1991-07-07','M',TIMESTAMP '2025-11-02 11:10:00'),
-- ('Sofia','Lopez','sofia.lopez@example.com','Harbor Data','500 Pratt St','Baltimore','MD',21201,'+1-410-555-0119','1994-05-25','F',TIMESTAMP '2025-11-02 12:20:00'),
-- ('Thomas','Nguyen','thomas.nguyen@example.com','North Star Systems','50 Hennepin Ave','Minneapolis','MN',55401,'+1-612-555-0120','1990-02-15','M',TIMESTAMP '2025-11-02 13:30:00')


-- INSERT INTO sales_person
-- (first_name, last_name, email, company, street, city, state, zip, phone, birth_date, sex, date_hired)
-- VALUES
-- ('Ava','Reed','ava.reed@acmecorp.com','Acme Corp','100 Market St','San Francisco','CA',94105,'+1-415-555-0142','1993-04-10','F',TIMESTAMP '2024-01-15 09:00:00'),
-- ('Benjamin','Cole','ben.cole@northstar.io','North Star Systems','500 Broadway','New York','NY',10012,'+1-212-555-0198','1989-11-22','M',TIMESTAMP '2023-10-02 10:30:00'),
-- ('Clara','Meyer','clara.meyer@rivertech.com','RiverTech','200 Lakeshore Dr','Chicago','IL',60601,'+1-312-555-0266','1995-06-05','F',TIMESTAMP '2024-05-20 11:15:00'),
-- ('Diego','Ruiz','diego.ruiz@sunsetdata.com','Sunset Data','420 Ocean Ave','Miami','FL',33101,'+1-305-555-0734','1991-02-14','M',TIMESTAMP '2022-09-01 08:45:00'),
-- ('Elena','Novak','elena.novak@skylabs.eu','SkyLabs','12 Harbor Way','Seattle','WA',98101,'+1-206-555-0888','1997-12-01','F',TIMESTAMP '2025-03-05 13:20:00');

-- INSERT INTO item (product_id, size, color, picture, price) VALUES
-- (1, 10, 'Black',        'Coming soon', 4999),
-- (1,  9, 'White',        'Coming soon', 4599),
-- (1, 11, 'Navy',         'Coming soon', 5199),
-- (2, 10, 'Gray',         'Coming soon', 4899),
-- (2, 12, 'Red',          'Coming soon', 5399),
-- (2,  8, 'Blue',         'Coming soon', 4799),
-- (3, 10, 'Green',        'Coming soon', 5099),
-- (3,  9, 'Beige',        'Coming soon', 4699),
-- (3, 11, 'Brown',        'Coming soon', 5299),
-- (4, 10, 'Olive',        'Coming soon', 4990),
-- (4, 12, 'Maroon',       'Coming soon', 5450),
-- (4,  8, 'Purple',       'Coming soon', 4750),
-- (5, 10, 'Teal',         'Coming soon', 5050),
-- (5,  9, 'Orange',       'Coming soon', 4650),
-- (5, 11, 'Gold',         'Coming soon', 5250),
-- (6, 10, 'Silver',       'Coming soon', 4980),
-- (6, 12, 'Charcoal',     'Coming soon', 5480),
-- (6,  8, 'Cyan',         'Coming soon', 4780),
-- (7, 10, 'Magenta',      'Coming soon', 5080),
-- (7,  9, 'Lime',         'Coming soon', 4680),
-- (7, 11, 'Khaki',        'Coming soon', 5280),
-- (8, 10, 'Ivory',        'Coming soon', 4975),
-- (8, 12, 'Coral',        'Coming soon', 5475),
-- (8,  8, 'Mint',         'Coming soon', 4775),
-- (9, 10, 'Lavender',     'Coming soon', 5075),
-- (9,  9, 'Burgundy',     'Coming soon', 4675),
-- (9, 11, 'Taupe',        'Coming soon', 5275),
-- (10, 10, 'Mustard',     'Coming soon', 4960),
-- (10, 12, 'Sky',         'Coming soon', 5460),
-- (10,  8, 'Tan',         'Coming soon', 4760),
-- (1, 10, 'Denim',        'Coming soon', 5060),
-- (1,  9, 'Rust',         'Coming soon', 4660),
-- (1, 11, 'Peach',        'Coming soon', 5260),
-- (2, 10, 'Rose',         'Coming soon', 4955),
-- (2, 12, 'Sand',         'Coming soon', 5455),
-- (2,  8, 'Chocolate',    'Coming soon', 4755),
-- (3, 10, 'Forest',       'Coming soon', 5055),
-- (3,  9, 'Plum',         'Coming soon', 4655),
-- (3, 11, 'Slate',        'Coming soon', 5255),
-- (4, 10, 'Indigo',       'Coming soon', 4945),
-- (4, 12, 'Aqua',         'Coming soon', 5445),
-- (4,  8, 'Crimson',      'Coming soon', 4745),
-- (5, 10, 'Sage',         'Coming soon', 5045),
-- (5,  9, 'Amber',        'Coming soon', 4645),
-- (5, 11, 'Copper',       'Coming soon', 5245),
-- (6, 10, 'Fuchsia',      'Coming soon', 4935),
-- (6, 12, 'Steel',        'Coming soon', 5435),
-- (6,  8, 'Graphite',     'Coming soon', 4735),
-- (7, 10, 'Wine',         'Coming soon', 5035),
-- (7,  9, 'Pearl',        'Coming soon', 4635);

-- ALTER TABLE sales_order ALTER COLUMN purchase_order_number TYPE BIGINT


-- INSERT INTO sales_order
-- (cust_id, sales_person_id, time_order_taken, purchase_order_number, creadit_card_number, creadit_card_exper_month, creadit_card_exper_day, creadit_card_secret_code, name_on_card)
-- VALUES
-- (1, 1, TIMESTAMP '2025-11-01 10:03:00', 20251101001, 4111111111110001, 1, 1, 101, 'Customer 001'),
-- (2, 2, TIMESTAMP '2025-11-01 10:06:00', 20251101002, 4111111111110002, 2, 2, 102, 'Customer 002'),
-- (3, 3, TIMESTAMP '2025-11-01 10:09:00', 20251101003, 4111111111110003, 3, 3, 103, 'Customer 003'),
-- (4, 4, TIMESTAMP '2025-11-01 10:12:00', 20251101004, 4111111111110004, 4, 4, 104, 'Customer 004'),
-- (5, 5, TIMESTAMP '2025-11-01 10:15:00', 20251101005, 4111111111110005, 5, 5, 105, 'Customer 005'),
-- (6, 1, TIMESTAMP '2025-11-01 10:18:00', 20251101006, 4111111111110006, 6, 6, 106, 'Customer 006'),
-- (7, 2, TIMESTAMP '2025-11-01 10:21:00', 20251101007, 4111111111110007, 7, 7, 107, 'Customer 007'),
-- (8, 3, TIMESTAMP '2025-11-01 10:24:00', 20251101008, 4111111111110008, 8, 8, 108, 'Customer 008'),
-- (9, 4, TIMESTAMP '2025-11-01 10:27:00', 20251101009, 4111111111110009, 9, 9, 109, 'Customer 009'),
-- (10, 5, TIMESTAMP '2025-11-01 10:30:00', 20251101010, 4111111111110010, 10, 10, 110, 'Customer 010'),
-- (11, 1, TIMESTAMP '2025-11-01 10:33:00', 20251101011, 4111111111110011, 11, 11, 111, 'Customer 011'),
-- (12, 2, TIMESTAMP '2025-11-01 10:36:00', 20251101012, 4111111111110012, 12, 12, 112, 'Customer 012'),
-- (13, 3, TIMESTAMP '2025-11-01 10:39:00', 20251101013, 4111111111110013, 1, 13, 113, 'Customer 013'),
-- (14, 4, TIMESTAMP '2025-11-01 10:42:00', 20251101014, 4111111111110014, 2, 14, 114, 'Customer 014'),
-- (15, 5, TIMESTAMP '2025-11-01 10:45:00', 20251101015, 4111111111110015, 3, 15, 115, 'Customer 015'),
-- (16, 1, TIMESTAMP '2025-11-01 10:48:00', 20251101016, 4111111111110016, 4, 16, 116, 'Customer 016'),
-- (17, 2, TIMESTAMP '2025-11-01 10:51:00', 20251101017, 4111111111110017, 5, 17, 117, 'Customer 017'),
-- (18, 3, TIMESTAMP '2025-11-01 10:54:00', 20251101018, 4111111111110018, 6, 18, 118, 'Customer 018'),
-- (19, 4, TIMESTAMP '2025-11-01 10:57:00', 20251101019, 4111111111110019, 7, 19, 119, 'Customer 019'),
-- (1, 5, TIMESTAMP '2025-11-01 11:00:00', 20251101020, 4111111111110020, 8, 20, 120, 'Customer 020'),
-- (2, 1, TIMESTAMP '2025-11-01 11:03:00', 20251101021, 4111111111110021, 9, 21, 121, 'Customer 021'),
-- (3, 2, TIMESTAMP '2025-11-01 11:06:00', 20251101022, 4111111111110022, 10, 22, 122, 'Customer 022'),
-- (4, 3, TIMESTAMP '2025-11-01 11:09:00', 20251101023, 4111111111110023, 11, 23, 123, 'Customer 023'),
-- (5, 4, TIMESTAMP '2025-11-01 11:12:00', 20251101024, 4111111111110024, 12, 24, 124, 'Customer 024'),
-- (6, 5, TIMESTAMP '2025-11-01 11:15:00', 20251101025, 4111111111110025, 1, 25, 125, 'Customer 025'),
-- (7, 1, TIMESTAMP '2025-11-01 11:18:00', 20251101026, 4111111111110026, 2, 26, 126, 'Customer 026'),
-- (8, 2, TIMESTAMP '2025-11-01 11:21:00', 20251101027, 4111111111110027, 3, 27, 127, 'Customer 027'),
-- (9, 3, TIMESTAMP '2025-11-01 11:24:00', 20251101028, 4111111111110028, 4, 28, 128, 'Customer 028'),
-- (10, 4, TIMESTAMP '2025-11-01 11:27:00', 20251101029, 4111111111110029, 5, 1, 129, 'Customer 029'),
-- (11, 5, TIMESTAMP '2025-11-01 11:30:00', 20251101030, 4111111111110030, 6, 2, 130, 'Customer 030'),
-- (12, 1, TIMESTAMP '2025-11-01 11:33:00', 20251101031, 4111111111110031, 7, 3, 131, 'Customer 031'),
-- (13, 2, TIMESTAMP '2025-11-01 11:36:00', 20251101032, 4111111111110032, 8, 4, 132, 'Customer 032'),
-- (14, 3, TIMESTAMP '2025-11-01 11:39:00', 20251101033, 4111111111110033, 9, 5, 133, 'Customer 033'),
-- (15, 4, TIMESTAMP '2025-11-01 11:42:00', 20251101034, 4111111111110034, 10, 6, 134, 'Customer 034'),
-- (16, 5, TIMESTAMP '2025-11-01 11:45:00', 20251101035, 4111111111110035, 11, 7, 135, 'Customer 035'),
-- (17, 1, TIMESTAMP '2025-11-01 11:48:00', 20251101036, 4111111111110036, 12, 8, 136, 'Customer 036'),
-- (18, 2, TIMESTAMP '2025-11-01 11:51:00', 20251101037, 4111111111110037, 1, 9, 137, 'Customer 037'),
-- (19, 3, TIMESTAMP '2025-11-01 11:54:00', 20251101038, 4111111111110038, 2, 10, 138, 'Customer 038'),
-- (1, 4, TIMESTAMP '2025-11-01 11:57:00', 20251101039, 4111111111110039, 3, 11, 139, 'Customer 039'),
-- (2, 5, TIMESTAMP '2025-11-01 12:00:00', 20251101040, 4111111111110040, 4, 12, 140, 'Customer 040'),
-- (3, 1, TIMESTAMP '2025-11-01 12:03:00', 20251101041, 4111111111110041, 5, 13, 141, 'Customer 041'),
-- (4, 2, TIMESTAMP '2025-11-01 12:06:00', 20251101042, 4111111111110042, 6, 14, 142, 'Customer 042'),
-- (5, 3, TIMESTAMP '2025-11-01 12:09:00', 20251101043, 4111111111110043, 7, 15, 143, 'Customer 043'),
-- (6, 4, TIMESTAMP '2025-11-01 12:12:00', 20251101044, 4111111111110044, 8, 16, 144, 'Customer 044'),
-- (7, 5, TIMESTAMP '2025-11-01 12:15:00', 20251101045, 4111111111110045, 9, 17, 145, 'Customer 045'),
-- (8, 1, TIMESTAMP '2025-11-01 12:18:00', 20251101046, 4111111111110046, 10, 18, 146, 'Customer 046'),
-- (9, 2, TIMESTAMP '2025-11-01 12:21:00', 20251101047, 4111111111110047, 11, 19, 147, 'Customer 047'),
-- (10, 3, TIMESTAMP '2025-11-01 12:24:00', 20251101048, 4111111111110048, 12, 20, 148, 'Customer 048'),
-- (11, 4, TIMESTAMP '2025-11-01 12:27:00', 20251101049, 4111111111110049, 1, 21, 149, 'Customer 049'),
-- (12, 5, TIMESTAMP '2025-11-01 12:30:00', 20251101050, 4111111111110050, 2, 22, 150, 'Customer 050'),
-- (13, 1, TIMESTAMP '2025-11-01 12:33:00', 20251101051, 4111111111110051, 3, 23, 151, 'Customer 051'),
-- (14, 2, TIMESTAMP '2025-11-01 12:36:00', 20251101052, 4111111111110052, 4, 24, 152, 'Customer 052'),
-- (15, 3, TIMESTAMP '2025-11-01 12:39:00', 20251101053, 4111111111110053, 5, 25, 153, 'Customer 053'),
-- (16, 4, TIMESTAMP '2025-11-01 12:42:00', 20251101054, 4111111111110054, 6, 26, 154, 'Customer 054'),
-- (17, 5, TIMESTAMP '2025-11-01 12:45:00', 20251101055, 4111111111110055, 7, 27, 155, 'Customer 055'),
-- (18, 1, TIMESTAMP '2025-11-01 12:48:00', 20251101056, 4111111111110056, 8, 28, 156, 'Customer 056'),
-- (19, 2, TIMESTAMP '2025-11-01 12:51:00', 20251101057, 4111111111110057, 9, 1, 157, 'Customer 057'),
-- (1, 3, TIMESTAMP '2025-11-01 12:54:00', 20251101058, 4111111111110058, 10, 2, 158, 'Customer 058'),
-- (2, 4, TIMESTAMP '2025-11-01 12:57:00', 20251101059, 4111111111110059, 11, 3, 159, 'Customer 059'),
-- (3, 5, TIMESTAMP '2025-11-01 13:00:00', 20251101060, 4111111111110060, 12, 4, 160, 'Customer 060'),
-- (4, 1, TIMESTAMP '2025-11-01 13:03:00', 20251101061, 4111111111110061, 1, 5, 161, 'Customer 061'),
-- (5, 2, TIMESTAMP '2025-11-01 13:06:00', 20251101062, 4111111111110062, 2, 6, 162, 'Customer 062'),
-- (6, 3, TIMESTAMP '2025-11-01 13:09:00', 20251101063, 4111111111110063, 3, 7, 163, 'Customer 063'),
-- (7, 4, TIMESTAMP '2025-11-01 13:12:00', 20251101064, 4111111111110064, 4, 8, 164, 'Customer 064'),
-- (8, 5, TIMESTAMP '2025-11-01 13:15:00', 20251101065, 4111111111110065, 5, 9, 165, 'Customer 065'),
-- (9, 1, TIMESTAMP '2025-11-01 13:18:00', 20251101066, 4111111111110066, 6, 10, 166, 'Customer 066'),
-- (10, 2, TIMESTAMP '2025-11-01 13:21:00', 20251101067, 4111111111110067, 7, 11, 167, 'Customer 067'),
-- (11, 3, TIMESTAMP '2025-11-01 13:24:00', 20251101068, 4111111111110068, 8, 12, 168, 'Customer 068'),
-- (12, 4, TIMESTAMP '2025-11-01 13:27:00', 20251101069, 4111111111110069, 9, 13, 169, 'Customer 069'),
-- (13, 5, TIMESTAMP '2025-11-01 13:30:00', 20251101070, 4111111111110070, 10, 14, 170, 'Customer 070'),
-- (14, 1, TIMESTAMP '2025-11-01 13:33:00', 20251101071, 4111111111110071, 11, 15, 171, 'Customer 071'),
-- (15, 2, TIMESTAMP '2025-11-01 13:36:00', 20251101072, 4111111111110072, 12, 16, 172, 'Customer 072'),
-- (16, 3, TIMESTAMP '2025-11-01 13:39:00', 20251101073, 4111111111110073, 1, 17, 173, 'Customer 073'),
-- (17, 4, TIMESTAMP '2025-11-01 13:42:00', 20251101074, 4111111111110074, 2, 18, 174, 'Customer 074'),
-- (18, 5, TIMESTAMP '2025-11-01 13:45:00', 20251101075, 4111111111110075, 3, 19, 175, 'Customer 075'),
-- (19, 1, TIMESTAMP '2025-11-01 13:48:00', 20251101076, 4111111111110076, 4, 20, 176, 'Customer 076'),
-- (1, 2, TIMESTAMP '2025-11-01 13:51:00', 20251101077, 4111111111110077, 5, 21, 177, 'Customer 077'),
-- (2, 3, TIMESTAMP '2025-11-01 13:54:00', 20251101078, 4111111111110078, 6, 22, 178, 'Customer 078'),
-- (3, 4, TIMESTAMP '2025-11-01 13:57:00', 20251101079, 4111111111110079, 7, 23, 179, 'Customer 079'),
-- (4, 5, TIMESTAMP '2025-11-01 14:00:00', 20251101080, 4111111111110080, 8, 24, 180, 'Customer 080'),
-- (5, 1, TIMESTAMP '2025-11-01 14:03:00', 20251101081, 4111111111110081, 9, 25, 181, 'Customer 081'),
-- (6, 2, TIMESTAMP '2025-11-01 14:06:00', 20251101082, 4111111111110082, 10, 26, 182, 'Customer 082'),
-- (7, 3, TIMESTAMP '2025-11-01 14:09:00', 20251101083, 4111111111110083, 11, 27, 183, 'Customer 083'),
-- (8, 4, TIMESTAMP '2025-11-01 14:12:00', 20251101084, 4111111111110084, 12, 28, 184, 'Customer 084'),
-- (9, 5, TIMESTAMP '2025-11-01 14:15:00', 20251101085, 4111111111110085, 1, 1, 185, 'Customer 085'),
-- (10, 1, TIMESTAMP '2025-11-01 14:18:00', 20251101086, 4111111111110086, 2, 2, 186, 'Customer 086'),
-- (11, 2, TIMESTAMP '2025-11-01 14:21:00', 20251101087, 4111111111110087, 3, 3, 187, 'Customer 087'),
-- (12, 3, TIMESTAMP '2025-11-01 14:24:00', 20251101088, 4111111111110088, 4, 4, 188, 'Customer 088'),
-- (13, 4, TIMESTAMP '2025-11-01 14:27:00', 20251101089, 4111111111110089, 5, 5, 189, 'Customer 089'),
-- (14, 5, TIMESTAMP '2025-11-01 14:30:00', 20251101090, 4111111111110090, 6, 6, 190, 'Customer 090'),
-- (15, 1, TIMESTAMP '2025-11-01 14:33:00', 20251101091, 4111111111110091, 7, 7, 191, 'Customer 091'),
-- (16, 2, TIMESTAMP '2025-11-01 14:36:00', 20251101092, 4111111111110092, 8, 8, 192, 'Customer 092'),
-- (17, 3, TIMESTAMP '2025-11-01 14:39:00', 20251101093, 4111111111110093, 9, 9, 193, 'Customer 093'),
-- (18, 4, TIMESTAMP '2025-11-01 14:42:00', 20251101094, 4111111111110094, 10, 10, 194, 'Customer 094'),
-- (19, 5, TIMESTAMP '2025-11-01 14:45:00', 20251101095, 4111111111110095, 11, 11, 195, 'Customer 095'),
-- (1, 1, TIMESTAMP '2025-11-01 14:48:00', 20251101096, 4111111111110096, 12, 12, 196, 'Customer 096'),
-- (2, 2, TIMESTAMP '2025-11-01 14:51:00', 20251101097, 4111111111110097, 1, 13, 197, 'Customer 097'),
-- (3, 3, TIMESTAMP '2025-11-01 14:54:00', 20251101098, 4111111111110098, 2, 14, 198, 'Customer 098'),
-- (4, 4, TIMESTAMP '2025-11-01 14:57:00', 20251101099, 4111111111110099, 3, 15, 199, 'Customer 099'),
-- (5, 5, TIMESTAMP '2025-11-01 15:00:00', 20251101100, 4111111111110100, 4, 16, 200, 'Customer 100');


-- INSERT INTO sales_item
-- (item_id, sales_order_id, quantity, discount, taxable, sales_tax_rate)
-- VALUES
-- (41, 15, 1, 0.94, FALSE, 0.0),
-- (18, 32, 4, 0.17, FALSE, 0.0),
-- ...

SELECT first_name || ' ' || last_name AS full_name
FROM customer


