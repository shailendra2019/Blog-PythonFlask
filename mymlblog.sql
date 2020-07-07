-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 07, 2020 at 04:19 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.2.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mymlblog`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_num` varchar(50) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `phone_num`, `msg`, `date`) VALUES
(1, 'first post', 'testemail@abc.com', '123434345343', 'test message', '2020-07-04 12:29:27'),
(5, 'TEST 2', 'Testing2@email.com', '', 'This is a test message', NULL),
(6, 'TEST4', 'test4@testing.com', '3445566776', 'This is test', NULL),
(7, 'TEST4', 'test4@testing.com', '3445566776', 'This is test', '2020-07-04 15:27:55'),
(8, 'TEST user 5', 'test5@testing.com', '3454555656', 'A test message 5', '2020-07-04 15:28:29'),
(9, 'sdsd', 'dfdf@er.com', '3434343434', 'test', '2020-07-04 23:35:07'),
(10, 'sdsd', 'dfdf@er.com', '3434343434', 'test', '2020-07-04 23:48:19'),
(11, 'EmailTesting', 'emailtestacc@email.com', '56565656565', 'Testing to send a email to my gmail account', '2020-07-04 23:50:16'),
(12, 'wewew', 'SINGH_SHAILENDRA@HOTMAIL.COM', '34343434343', 'testmessage', '2020-07-07 19:43:24');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `Title` text NOT NULL,
  `subtitle` text NOT NULL,
  `slug` varchar(25) NOT NULL,
  `content` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `image_file` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `Title`, `subtitle`, `slug`, `content`, `date`, `image_file`) VALUES
(1, 'Title of my first post', 'This is 1st post', 'first-post', 'This is a first blog post that is written by me. The blog is about data science and covers different aspects of statistics and machine learning.', '2020-07-05 11:23:42', 'about-bg.jpg'),
(8, 'Connect Flask to a Database with Flask-SQLAlchemy3', 'This is a subtitle for the main title23232', 'new-post3', 'Test content again', '2020-07-06 18:52:48', 'img.png'),
(10, 'Basics of Jinja Template Language', 'Template File Extension', 'new-post4', 'As stated above, any file can be loaded as a template, regardless of file extension. Adding a .jinja extension, like user.html.jinja may make it easier for some IDEs or editor plugins, but is not required. Autoescaping, introduced later, can be applied based on file extension, so you’ll need to take the extra suffix into account in that case.', '2020-07-06 22:23:48', 'img.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
