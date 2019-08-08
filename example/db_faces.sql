-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 08, 2019 at 08:19 AM
-- Server version: 5.7.24-log
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_faces`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_faces`
--

CREATE TABLE `tb_faces` (
  `face_id` int(11) NOT NULL,
  `face_fileName` varchar(40) NOT NULL,
  `face_name` varchar(40) DEFAULT NULL,
  `employ_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tb_faces`
--

INSERT INTO `tb_faces` (`face_id`, `face_fileName`, `face_name`, `employ_id`) VALUES
(11, 'training0', 'ui', 456123),
(12, 'training1', 'น้าค่อม', 456124),
(13, 'training2', 'obama', 456125),
(14, 'training3', 'pompam', 456126),
(15, 'training4', 'gunsavage', 456127),
(16, 'training5', 'John', 456127),
(17, 'training6', 'Jam', 456227),
(18, 'training7', 'jimmy', 456327),
(19, 'training8', 'rojer', 456427),
(20, 'training9', 'robert', 456527),
(21, 'training10', 'Lamn', 456627),
(22, 'training11', 'carlot', 456727),
(23, 'training12', 'rose', 457727),
(24, 'training13', 'lidia', 457827),
(25, 'training14', 'mary', 457927),
(26, 'training15', 'slim Shady', 457027),
(27, 'training16', 'PayutChanOcha', 457028),
(28, 'training17', 'Putin', 457029),
(29, 'training18', 'Nik', 457030),
(30, 'training19', 'snoop', 457031),
(31, 'training20', 'GusTeera', 457032);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_faces`
--
ALTER TABLE `tb_faces`
  ADD PRIMARY KEY (`face_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
