-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2023 at 03:56 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bcarbonzero`
--

-- --------------------------------------------------------

--
-- Table structure for table `advertisement`
--

CREATE TABLE `advertisement` (
  `EIN` varchar(9) NOT NULL,
  `date_posted` date NOT NULL,
  `time_posted` time NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) NOT NULL,
  `website_link` varchar(30) NOT NULL,
  `redirect_link` varchar(30) NOT NULL,
  `cost` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `advertisement`
--

INSERT INTO `advertisement` (`EIN`, `date_posted`, `time_posted`, `title`, `description`, `website_link`, `redirect_link`, `cost`) VALUES
('111222333', '2022-06-18', '17:44:43', '50% Off Running Shoes', '50% off our running shoes! Get them while supplies last!', 'www.shoes.com/runningshoes', 'www.shoes.com/checkout/running', 20),
('111222333', '2022-08-06', '13:39:36', '25% Off Walking Shoes', '25% off our walking shoes! Very comfortable and amazing ankle support! Comes in a variety of aesthetic colors and designs. Get them while supplies last!', 'www.shoes.com/walkingshoes', 'www.shoes.com/checkout/walking', 20),
('888888888', '2022-08-06', '18:51:51', '20% Off Designer Lipstick ', 'Some designer lipstick and whatnot. Very pretty colors. ', 'www.sephora.com/designerLipsti', 'www.sephora.com/designerLipsti', 20);

-- --------------------------------------------------------

--
-- Table structure for table `apply`
--

CREATE TABLE `apply` (
  `email` varchar(20) NOT NULL,
  `EIN` varchar(9) NOT NULL,
  `date_posted` date NOT NULL,
  `time_posted` time NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `apply`
--

INSERT INTO `apply` (`email`, `EIN`, `date_posted`, `time_posted`, `status`) VALUES
('a@gmail.com', '222222222', '2022-08-06', '18:47:15', 0),
('a@gmail.com', '333333333', '2022-06-01', '23:08:20', 2),
('a@gmail.com', '333333333', '2022-07-09', '08:23:39', 0),
('a@gmail.com', '333333333', '2022-08-06', '18:31:51', 1),
('afrida@gmail.com', '333333333', '2022-06-01', '23:08:20', 1),
('afrida@gmail.com', '333333333', '2022-06-18', '19:30:26', 1),
('afrida@gmail.com', '333333333', '2022-07-09', '08:23:39', 0),
('rady@gmail.com', '333333333', '2022-06-01', '23:08:20', 2),
('rady@gmail.com', '333333333', '2022-06-18', '19:30:26', 1),
('rady@gmail.com', '333333333', '2022-07-09', '08:23:39', 0),
('shafa@gmail.com', '222222222', '2022-08-06', '18:29:39', 1),
('shafa@gmail.com', '333333333', '2022-06-01', '23:08:20', 1),
('shafa@gmail.com', '333333333', '2022-06-18', '19:30:26', 1),
('shafa@gmail.com', '333333333', '2022-07-09', '08:23:39', 0),
('shafa@gmail.com', '333333333', '2022-08-06', '18:31:51', 1),
('v1@gmail.com', '333333333', '2022-06-01', '23:08:20', 2),
('v2@gmail.com', '333333333', '2022-06-18', '19:30:26', 1),
('waji@gmail.com', '222222222', '2022-08-06', '18:29:39', 1),
('waji@gmail.com', '333333333', '2022-06-01', '23:08:20', 1),
('waji@gmail.com', '333333333', '2022-06-18', '19:30:26', 1),
('waji@gmail.com', '333333333', '2022-07-09', '08:23:39', 0),
('waji@gmail.com', '333333333', '2022-08-06', '18:31:51', 1);

-- --------------------------------------------------------

--
-- Table structure for table `exchange`
--

CREATE TABLE `exchange` (
  `email` varchar(20) NOT NULL,
  `EIN` varchar(9) NOT NULL,
  `date_posted` date NOT NULL,
  `time_posted` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `exchange`
--

INSERT INTO `exchange` (`email`, `EIN`, `date_posted`, `time_posted`) VALUES
('shafa@gmail.com', '111222333', '2022-06-18', '17:44:43'),
('shafa@gmail.com', '111222333', '2022-08-06', '13:39:36');

-- --------------------------------------------------------

--
-- Table structure for table `opportunity`
--

CREATE TABLE `opportunity` (
  `EIN` varchar(9) NOT NULL,
  `date_posted` date NOT NULL,
  `time_posted` time NOT NULL,
  `title` varchar(50) NOT NULL,
  `description` varchar(500) NOT NULL,
  `reward` int(11) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `zip_code` varchar(5) NOT NULL,
  `updated` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `opportunity`
--

INSERT INTO `opportunity` (`EIN`, `date_posted`, `time_posted`, `title`, `description`, `reward`, `city`, `state`, `zip_code`, `updated`) VALUES
('222222222', '2022-08-06', '18:29:39', 'Shelter Services', 'Shelter volunteers support the day-to-day activities within a shelter which may include working in reception, registration, feeding, dormitory, information or other vital areas within a shelter. Train now to be a Red Cross Shelter Volunteer so you can answer the call directly help those affected by disaster. For more info, visit https://www.redcross.org/volunteer/become-a-volunteer/urgent-need-for-volunteers.html/?icid=surge&imed=referral&isource=homepage ', 10, 'Bronz', 'NY', '11111', 1),
('222222222', '2022-08-06', '18:47:15', 'Soup Kitchen???', 'Come volunteer and whatnot. Some more stuffs and moreeeee why are you still reading okay that\'s enough words', 10, 'Manhattan', 'NY', '10010', 0),
('333333333', '2022-06-01', '23:08:20', 'Plant Trees In Central Park!', 'Help us plant trees in Central Park and make a big impact on the environment. For more information, check out www.treeplanter/centralpark', 10, 'Manhattan', 'NY', '10019', 1),
('333333333', '2022-06-18', '19:30:26', 'Plant Trees In Cunningham Park', 'Come help us plant more trees in Cunningham Park! Visit our website for more info: www.treeplanter.com/cunninghamppark', 10, 'Queens', 'NY', '11427', 1),
('333333333', '2022-08-06', '18:31:51', 'Plant Trees At Union Square!', 'Help us plant trees at Union Square Park and make a big impact on the environment. For more information, check out www.treeplanter/unionSquare', 10, 'Manhattan', 'NY', '22222', 1);

-- --------------------------------------------------------

--
-- Stand-in structure for view `org`
-- (See below for the actual view)
--
CREATE TABLE `org` (
`EIN` varchar(9)
,`name` varchar(50)
,`email` varchar(50)
);

-- --------------------------------------------------------

--
-- Table structure for table `organization`
--

CREATE TABLE `organization` (
  `EIN` varchar(9) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `building_num` int(11) NOT NULL,
  `street` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `zip_code` varchar(5) NOT NULL,
  `phone_num` varchar(20) NOT NULL,
  `mission_statement` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL,
  `website` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `organization`
--

INSERT INTO `organization` (`EIN`, `name`, `email`, `password`, `building_num`, `street`, `city`, `state`, `zip_code`, `phone_num`, `mission_statement`, `description`, `website`) VALUES
('222222222', 'American Red Cross', 'redcross@gmail.com', '202cb962ac59075b964b07152d234b70', 879, 'somewhere', 'NY', '10457', 'Bronx', '1234567891', 'Help people.', 'The American Red Cross Greater New York Region operates the largest and busiest disaster-response program in the nation, providing assistance, compassion and comfort to more than 12,000 New Yorkers af', 'www.redcross.org'),
('333333333', 'Tree Planter', 'treeplanter@gmail.com', '202cb962ac59075b964b07152d234b70', 111, 'Blah Street', 'NY', 'NY', '11111', '1111111111', 'We plant trees across parks in New York City. ', 'We help make an impact in our neighborhoods by planting trees and beautifying parks in NYC. Join our many opportunities to help the cause!', 'www.treeplanter.com');

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `EIN` varchar(9) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `website` varchar(30) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vendor`
--

INSERT INTO `vendor` (`EIN`, `email`, `password`, `website`, `name`) VALUES
('888888888', 'sephora@gmail.com', '202cb962ac59075b964b07152d234b70', 'www.sephora.com', 'Sephora'),
('111222333', 'shoes@gmail.com', '202cb962ac59075b964b07152d234b70', 'www.shoes.com', 'shoes');

-- --------------------------------------------------------

--
-- Table structure for table `volunteer`
--

CREATE TABLE `volunteer` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `tokens_collected` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `volunteer`
--

INSERT INTO `volunteer` (`email`, `password`, `tokens_collected`) VALUES
('609faizaafrida@gmail.com', '81dc9bdb52d04dc20036dbd8313ed055', 0),
('a@gmail.com', '202cb962ac59075b964b07152d234b70', 10),
('afrida@gmail.com', '202cb962ac59075b964b07152d234b70', 20),
('rady@gmail.com', '202cb962ac59075b964b07152d234b70', 10),
('shafa@gmail.com', '202cb962ac59075b964b07152d234b70', 0),
('v1@gmail.com', '202cb962ac59075b964b07152d234b70', 0),
('v2@gmail.com', '202cb962ac59075b964b07152d234b70', 10),
('waji@gmail.com', '202cb962ac59075b964b07152d234b70', 40);

-- --------------------------------------------------------

--
-- Structure for view `org`
--
DROP TABLE IF EXISTS `org`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `org`  AS SELECT `organization`.`EIN` AS `EIN`, `organization`.`name` AS `name`, `organization`.`email` AS `email` FROM `organization` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `advertisement`
--
ALTER TABLE `advertisement`
  ADD PRIMARY KEY (`EIN`,`date_posted`,`time_posted`),
  ADD KEY `EIN` (`EIN`),
  ADD KEY `date_posted` (`date_posted`),
  ADD KEY `time_posted` (`time_posted`);

--
-- Indexes for table `apply`
--
ALTER TABLE `apply`
  ADD PRIMARY KEY (`email`,`EIN`,`date_posted`,`time_posted`),
  ADD KEY `date_posted` (`date_posted`),
  ADD KEY `time_posted` (`time_posted`),
  ADD KEY `email` (`email`),
  ADD KEY `EIN` (`EIN`);

--
-- Indexes for table `exchange`
--
ALTER TABLE `exchange`
  ADD PRIMARY KEY (`email`,`EIN`,`date_posted`,`time_posted`),
  ADD KEY `email` (`email`),
  ADD KEY `EIN` (`EIN`),
  ADD KEY `date_posted` (`date_posted`),
  ADD KEY `time_posted` (`time_posted`);

--
-- Indexes for table `opportunity`
--
ALTER TABLE `opportunity`
  ADD PRIMARY KEY (`EIN`,`date_posted`,`time_posted`),
  ADD KEY `date_posted` (`date_posted`),
  ADD KEY `time_posted` (`time_posted`);

--
-- Indexes for table `organization`
--
ALTER TABLE `organization`
  ADD PRIMARY KEY (`email`),
  ADD KEY `EIN` (`EIN`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`email`),
  ADD KEY `EIN` (`EIN`);

--
-- Indexes for table `volunteer`
--
ALTER TABLE `volunteer`
  ADD PRIMARY KEY (`email`),
  ADD KEY `email` (`email`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `advertisement`
--
ALTER TABLE `advertisement`
  ADD CONSTRAINT `advertisement_ibfk_1` FOREIGN KEY (`EIN`) REFERENCES `vendor` (`EIN`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `apply`
--
ALTER TABLE `apply`
  ADD CONSTRAINT `apply_ibfk_4` FOREIGN KEY (`email`) REFERENCES `volunteer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `exchange`
--
ALTER TABLE `exchange`
  ADD CONSTRAINT `exchange_ibfk_1` FOREIGN KEY (`email`) REFERENCES `volunteer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `opportunity`
--
ALTER TABLE `opportunity`
  ADD CONSTRAINT `opportunity_ibfk_1` FOREIGN KEY (`EIN`) REFERENCES `organization` (`EIN`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
