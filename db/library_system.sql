-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 02, 2024 at 03:43 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `borrowed_by` int(11) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `borrowed_by`, `due_date`, `is_available`) VALUES
(1, 'Peter Pan', NULL, NULL, 1),
(2, 'English for You and Me', NULL, NULL, 1),
(3, 'Filipino', NULL, NULL, 1),
(4, 'Music and Arts', NULL, NULL, 1),
(5, 'Physical Education', NULL, NULL, 1),
(6, 'Earth and Science', NULL, NULL, 1),
(7, 'Fundamentals of ABM', NULL, NULL, 1),
(8, 'ESP', NULL, NULL, 1),
(9, 'kenshin', NULL, NULL, 1),
(10, 'Cyber security basics', NULL, NULL, 1),
(11, 'Joshua book', 5, '2024-10-09', 1),
(12, 'Test', NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `return_books`
--

CREATE TABLE `return_books` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `return_date` date NOT NULL,
  `penalty` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `return_books`
--

INSERT INTO `return_books` (`id`, `book_id`, `user_id`, `return_date`, `penalty`) VALUES
(1, 4, 1, '2024-09-30', 0.00),
(2, 3, 1, '2024-10-01', 0.00),
(3, 7, 1, '2024-10-01', 0.00),
(4, 11, 5, '2024-10-02', 0.00),
(5, 4, 5, '2024-10-02', 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `age` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `firstname`, `lastname`, `age`) VALUES
(1, '123', '123', 'jake', 'robot', 19),
(2, 'alden', 'alden', 'gems', 'tilap', 18),
(3, 'aldenkenshin', '123', 'alden', 'cedeño', 20),
(5, 'joshua', 'joshua', 'joshua ', 'padilla', 24),
(8, 'andy', 'andy', 'andy', 'andy', 10),
(9, 'ako', 'ako', 'ako', 'ako', 5),
(10, 'admin', 'admin', 'joshua anderson', 'padilla', 23);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `borrowed_by` (`borrowed_by`);

--
-- Indexes for table `return_books`
--
ALTER TABLE `return_books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `return_books`
--
ALTER TABLE `return_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`borrowed_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `return_books`
--
ALTER TABLE `return_books`
  ADD CONSTRAINT `return_books_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  ADD CONSTRAINT `return_books_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
