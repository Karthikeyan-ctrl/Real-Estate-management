#Purpose - Stores information about each user, including property owners and buyers.

CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(35) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    phone TEXT,
    user_type VARCHAR(7) CHECK(user_type IN ('buyer', 'seller', 'agent'))
);

#Purpose - Stores details about the properties listed on the platform.

CREATE TABLE Properties (
    property_id INT PRIMARY KEY,
    address VARCHAR(200) NOT NULL,
    price INT,
    property_type VARCHAR(30),
    owner_id INT,
    status VARCHAR(25) CHECK(status IN ('available', 'sold', 'rented')),
    FOREIGN KEY(owner_id) REFERENCES Users(user_id)
);

#Purpose - Records completed transactions between buyers and property owners.

CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    buyer_id INT,
    property_id INT,
    transaction_date DATE,
    price INT,
    FOREIGN KEY(buyer_id) REFERENCES Users(user_id),
    FOREIGN KEY(property_id) REFERENCES Properties(property_id)
);

#Purpose - Stores inquiries or messages from users, including those submitted via chatbot.

CREATE TABLE Inquiries (
    inquiry_id INT PRIMARY KEY,
    user_id INT,
    message TEXT,
    inquiry_date DATE,
    status TEXT CHECK(status IN ('new', 'responded')),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);

-- Users table
INSERT INTO Users (user_id, username, email, password, phone, user_type) VALUES
(1, 'Arjun', 'arjun@example.com', 'pwd123', '9876543210', 'seller'),
(2, 'Kavya', 'kavya@example.com', 'pwd234', '8765432109', 'buyer'),
(3, 'Rahul', 'rahul@example.com', 'pwd345', '7654321098', 'agent'),
(4, 'Meena', 'meena@example.com', 'pwd456', '6543210987', 'seller'),
(5, 'Priya', 'priya@example.com', 'pwd567', '5432109876', 'buyer'),
(6, 'Vijay', 'vijay@example.com', 'pwd678', '4321098765', 'agent'),
(7, 'Swathi', 'swathi@example.com', 'pwd789', '3210987654', 'buyer'),
(8, 'Ravi', 'ravi@example.com', 'pwd890', '2109876543', 'seller'),
(9, 'Arvind', 'arvind@example.com', 'pwd901', '1098765432', 'agent'),
(10, 'Rakesh', 'rakesh@example.com', 'pwd012', '1987654321', 'buyer');

-- Properties table
INSERT INTO Properties (property_id, address, price, property_type, owner_id, status) VALUES
(1, '12, North Street, Madurai', 3000000, 'apartment', 1, 'available'),
(2, '45, West Main Road, Madurai', 4500000, 'villa', 4, 'sold'),
(3, '78, South Colony, Madurai', 2500000, 'apartment', 1, 'available'),
(4, '23, East Avenue, Madurai', 5000000, 'house', 8, 'available'),
(5, '56, KK Nagar, Madurai', 3500000, 'flat', 4, 'rented'),
(6, '32, Lakshmipuram, Madurai', 7000000, 'apartment', 8, 'available'),
(7, '19, Madurai Main Road, Madurai', 2000000, 'studio', 1, 'available'),
(8, '85, Annanagar, Madurai', 10000000, 'villa', 1, 'sold'),
(9, '22, Simmakkal, Madurai', 4000000, 'apartment', 4, 'available'),
(10, '44, Kuruvikkaran Salai, Madurai', 5500000, 'house', 8, 'available');

-- Transactions table
INSERT INTO Transactions (transaction_id, buyer_id, property_id, transaction_date, price) VALUES
(1, 2, 2, '2024-01-15', 4500000),
(2, 5, 8, '2024-03-20', 10000000),
(3, 10, 5, '2024-02-25', 3500000),
(4, 7, 3, '2024-06-10', 2500000),
(5, 10, 9, '2024-08-30', 4000000),
(6, 2, 6, '2024-07-05', 7000000),
(7, 5, 1, '2024-04-12', 3000000),
(8, 10, 7, '2024-05-18', 2000000),
(9, 7, 4, '2024-09-22', 5000000),
(10, 2, 10, '2024-10-05', 5500000);


