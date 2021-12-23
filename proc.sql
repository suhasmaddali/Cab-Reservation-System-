
CREATE DEFINER=`root`@`localhost` PROCEDURE `csp_1`(IN p_name VARCHAR(45),
IN p_username VARCHAR(45),
IN p_password VARCHAR(45),
IN p_address varchar(300))
BEGIN
if ( select exists (select 1 from customer where user_name = p_username and password=p_password) ) THEN

select 'Username Exists !!';
-- elseif ( select exists (select 1 from customer where user_name = p_username ) ) then select "username there but password incorrect";
ELSE

insert into customer
(
name,
user_name,
password,
wallet_balance,
rating,
address
)
values
(
p_name,
p_username,
p_password,
0,
0,
p_address
);

END IF;
END


CREATE DEFINER=`root`@`localhost` PROCEDURE `check_username`(
IN p_username VARCHAR(45),
IN p_password VARCHAR(45))
BEGIN
if ( select exists (select 1 from customer where user_name = p_username and password=p_password) ) THEN

	select 1;
elseif ( select exists (select 1 from customer where user_name = p_username ) ) then 
	select 2;
ELSE
	select 0;



END IF;
END


CREATE DEFINER=`root`@`localhost` PROCEDURE `check_admin`(
IN p_username VARCHAR(45),
IN p_password VARCHAR(45))
BEGIN
if ( select exists (select 1 from admin where user_name = p_username and password=p_password) ) THEN

	select 1;
elseif ( select exists (select 1 from admin where user_name = p_username ) ) then 
	select 2;
ELSE
	select 0;



END IF;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `check_driver`(
IN p_username VARCHAR(45),
IN p_password VARCHAR(45))
BEGIN
if ( select exists (select 1 from driver where user_name = p_username and password=p_password) ) THEN

	select 1;
elseif ( select exists (select 1 from driver where user_name = p_username ) ) then 
	select 2;
ELSE
	select 0;



END IF;
END

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `customer_count` AS
    SELECT 
        `customer`.`customer_id` AS `customer_id`
    FROM
        `customer`


CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `driver_count` AS
    SELECT 
        `driver`.`driver_id` AS `driver_id`
    FROM
        `driver`



CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `feedback_view` AS
    SELECT 
        `feedback`.`message` AS `message`
    FROM
        `feedback`


CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `trip_time_view` AS
    SELECT 
        `trip`.`trip_id` AS `trip_id`,
        `trip`.`start_time` AS `start_time`,
        `trip`.`est_arrival_time` AS `est_arrival_time`,
        `trip`.`act_end_time` AS `act_end_time`
    FROM
        `trip`