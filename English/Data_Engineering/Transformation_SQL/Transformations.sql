#We create the database where we are going to work
CREATE DATABASE Sales;

#We select it, so we can work on it
USE Sales;

#Now we need to import the data that we have in CSV and Excel files

#We create the table
DROP TABLE IF EXISTS Customers;
CREATE TABLE IF NOT EXISTS Customers (
Cust_Id SMALLINT(4) unsigned not null,
Cust_Province VARCHAR (45) default null,
Cust_CompleteName VARCHAR (60) default null,
Cust_Address varchar(140) default null,
Cust_PhoneNumber varchar(45) default null,
Cust_Age tinyint unsigned default null,
Cust_City  varchar(60) default null,
Cust_Longitude varchar(20) default null,	#We define this column first as varchar. We are going to come back later
Cust_Latitude varchar(20) default null,		#We define this column first as varchar. We are going to come back later
Cust_Col10 varchar(145) default null)
default charset=utf8mb4 collate=utf8mb4_spanish_ci;

#We import the data for this table
LOAD DATA infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Clientes.csv'
INTO TABLE customers
fields terminated by ';' enclosed by '' escaped by ''
lines terminated by '\n'ignore 1 lines;

#We create the next table
DROP table if exists purchases;
CREATE TABLE purchases (
Purchase_Id INT unsigned not null,
Purchase_Date date default null,
Prod_Id int unsigned not null,
Purchase_Quantity int unsigned default null,
Purchase_Price decimal(9,2) unsigned default null,
Supplier_Id smallint(4) unsigned not null)
default charset=utf8mb4 collate=utf8mb4_spanish_ci;

#We import the data for this table
LOAD DATA infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Compra.csv'
INTO TABLE purchases
fields terminated by ',' enclosed by '' escaped by ''
lines terminated by '\n'ignore 1 lines;

#We create the next table
DROP table if exists expenses;
CREATE TABLE expenses (
Expense_Id INT unsigned not null,
Branch_Id smallint unsigned not null,
ExpenseType_Id tinyint unsigned not null,
Expense_Date date default null,
Expense_Amount decimal(9,2) unsigned default null)
default charset=utf8mb4 collate=utf8mb4_spanish_ci;

#We import the data for this table
LOAD DATA infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Gasto.csv'
INTO TABLE expenses
fields terminated by ',' enclosed by '' escaped by ''
lines terminated by '\n'ignore 1 lines;

#We create the next table
DROP table if exists branches;
CREATE TABLE branches (
Branch_Id smallint unsigned not null,
Branch_Name varchar(45) default null,
Branch_Address varchar(140) default null,
Branch_City  varchar(60) default null,
Branch_Province  varchar(60) default null,
Branch_Longitude varchar(20) default null,	#We define this column first as varchar. We are going to come back later
Branch_Latitude varchar(20) default null)	#We define this column first as varchar. We are going to come back later
default charset=utf8mb4 collate=utf8mb4_spanish_ci;

#We import the data for this table
LOAD DATA infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Sucursales.csv'
INTO TABLE branches
fields terminated by ';' enclosed by '' escaped by ''
lines terminated by '\n'ignore 1 lines;

#We create the next table
DROP table if exists expenseTypes;
CREATE TABLE expenseTypes (
ET_Id tinyint unsigned not null,
ET_Description varchar(45) default null,
ET_AproxAmount mediumint unsigned default null)
default charset=utf8mb4 collate=utf8mb4_spanish_ci;

#We import the data for this table
LOAD DATA infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\TiposDeGasto.csv'
INTO TABLE expenseTypes
fields terminated by ',' enclosed by '' escaped by ''
lines terminated by '\n'ignore 1 lines;

#We create the next table
DROP table if exists sales;
CREATE TABLE sales (
Sale_Id BIGINT unsigned not null,
Sale_Date date default null,
Sale_DeliverDate date default null,
SC_Id tinyint unsigned not null,
Cust_Id SMALLINT(4) unsigned not null,
Branch_Id smallint unsigned not null,
Emp_Id smallint unsigned not null,
Prod_Id int unsigned not null,
Sale_Price varchar(10) default null,
Sale_Quantity varchar(10) default null)		#We define this column first as varchar. We are going to come back later
default charset=utf8mb4 collate=utf8mb4_spanish_ci;

#We import the data for this table
LOAD DATA infile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Venta.csv'
INTO TABLE sales
fields terminated by ',' enclosed by '' escaped by ''
lines terminated by '\n'ignore 1 lines;

#The other tables are in excel format we are going to do the import with Python and export them here