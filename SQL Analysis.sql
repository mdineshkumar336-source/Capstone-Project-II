CREATE DATABASE capstone_project_2;
USE capstone_project_2;

-- 1. Create the Customers Table

CREATE TABLE Customers (
    CustomerID VARCHAR(20) PRIMARY KEY,
    CustomerName VARCHAR(100),
    Region VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    SignupDate DATE,
    AgeGroup VARCHAR(20),
    Segment VARCHAR(50)
);

DESCRIBE Customers;

SELECT COUNT(*) AS Customer_Count
FROM Customers;

SELECT *
FROM Customers
LIMIT 10;

-- 2. Create the Orders Table

CREATE TABLE Orders (
    OrderID VARCHAR(20) PRIMARY KEY,
    OrderDate DATE,
    CustomerID VARCHAR(20),
    ProductCategory VARCHAR(100),
    Product VARCHAR(100),
    Quantity INT,
    Discount DECIMAL(10,2),
    Sales DECIMAL(15,2),
    Profit DECIMAL(15,2),
    PaymentMethod VARCHAR(50),
    OrderStatus VARCHAR(50),
    Loss_Flag VARCHAR(20)
);

DESCRIBE Orders;

SELECT COUNT(*) AS Order_Count
FROM Orders;

SELECT *
FROM Orders
LIMIT 10;

-- Join

SELECT
    c.CustomerID,
    c.CustomerName,
    o.OrderID,
    o.Sales,
    o.Profit
FROM Customers c
INNER JOIN Orders o
    ON c.CustomerID = o.CustomerID
LIMIT 20;

-- Group By

SELECT
    c.Region,
    SUM(o.Sales) AS Total_Sales,
    SUM(o.Profit) AS Total_Profit,
    COUNT(o.OrderID) AS Order_Count
FROM Customers c
INNER JOIN Orders o
    ON c.CustomerID = o.CustomerID
GROUP BY c.Region
ORDER BY Total_Sales DESC;

-- Having

SELECT
    c.Region,
    SUM(o.Sales) AS Total_Sales
FROM Customers c
INNER JOIN Orders o
    ON c.CustomerID = o.CustomerID
GROUP BY c.Region
HAVING SUM(o.Sales) > 10000000
ORDER BY Total_Sales DESC;

-- Case

SELECT
    OrderID,
    Sales,
    Profit,
    CASE
        WHEN Profit > 0 THEN 'Profit'
        WHEN Profit < 0 THEN 'Loss'
        ELSE 'Break Even'
    END AS Profit_Status
FROM Orders
LIMIT 20;

-- Subquery

SELECT
    OrderID,
    CustomerID,
    Sales,
    Profit
FROM Orders
WHERE Sales > (
    SELECT AVG(Sales)
    FROM Orders
)
ORDER BY Sales DESC;

-- CTE

WITH Region_Sales AS (
    SELECT
        c.Region,
        SUM(o.Sales) AS Total_Sales
    FROM Customers c
    INNER JOIN Orders o
        ON c.CustomerID = o.CustomerID
    GROUP BY c.Region
)

SELECT
    Region,
    Total_Sales
FROM Region_Sales
WHERE Total_Sales > 10000000
ORDER BY Total_Sales DESC;

-- Window Functions

WITH Region_Sales AS (
    SELECT
        c.Region,
        SUM(o.Sales) AS Total_Sales
    FROM Customers c
    INNER JOIN Orders o
        ON c.CustomerID = o.CustomerID
    GROUP BY c.Region
)

SELECT
    Region,
    Total_Sales,
    RANK() OVER (
        ORDER BY Total_Sales DESC
    ) AS Sales_Rank
FROM Region_Sales
ORDER BY Sales_Rank;

-- Orphan CustomerID

SELECT
    o.OrderID,
    o.CustomerID,
    o.Sales,
    o.Profit
FROM Orders o
LEFT JOIN Customers c
    ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL;
