DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
  customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email varchar(255) NOT NULL,
  phone_number NUMERIC NOT NULL,
  rating FLOAT,
  wallet_balance float not null,
  user_address varchar not null
);

CREATE DEFINER=`root`@`localhost` PROCEDURE `get_drivers_details`(in driver_id int)
BEGIN
select car_name,number_plate from driver_cars where driver_id=driver_id and availability=0;
END

