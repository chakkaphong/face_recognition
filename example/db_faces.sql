-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Aug 12, 2019 at 06:10 AM
-- Server version: 5.7.26
-- PHP Version: 7.3.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
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
-- Table structure for table `tb_employ`
--

CREATE TABLE `tb_employ` (
  `employ_id` int(10) NOT NULL,
  `employ_Fname` varchar(40) NOT NULL,
  `employ_Lname` varchar(40) NOT NULL,
  `employ_picture` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tb_employ`
--

INSERT INTO `tb_employ` (`employ_id`, `employ_Fname`, `employ_Lname`, `employ_picture`) VALUES
(456123, 'Lee', 'Ji Eun', 'Lee Ji Eun.jpg'),
(456124, 'อาคม', 'ปรีดากุล', 'Rkom.jpg'),
(456125, 'Barack', 'Obama', 'Obama.jpg'),
(456126, 'นิติ', 'ชัยชิตาทร', 'niti.jpg'),
(456127, 'จักรพงษ์', 'คลังศรี', 'chakka.jpg'),
(456128, 'Calla', 'Bot', 'Calla.jpg'),
(456227, 'Salvador', 'Mallo', 'Salvador.jpg'),
(456327, 'Venancio', 'Mallo', 'Venancio.jpg'),
(456427, 'Alberto', 'Crespo', 'Alberto.jpg'),
(456527, 'Federico', 'Delgado', 'Federico.jpg'),
(456627, 'Eddie', 'Morra', 'Eddie.jpg'),
(456727, 'Skyler', 'White', 'Skyler.jpg'),
(457027, 'John', 'Wick', 'John.jpg'),
(457028, 'Prayut', 'Chan-o-cha', 'Prayut.jpg'),
(457029, 'Vladimir', 'Putin', 'Putin.jpg'),
(457030, 'Andre', 'Romelle Young', 'Andre.jpg'),
(457031, 'Walter', 'White', 'Walter.jpg'),
(457032, 'TeeRa', 'Panchaisee', 'TeeRa.jpg'),
(457727, 'Marie', 'Schrader', 'Marie.jpg'),
(457827, 'Lydia', 'Rodarte-Quayle', 'Lydia.jpg'),
(457927, 'Slim', 'Shady', 'Slim.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tb_faces`
--

CREATE TABLE `tb_faces` (
  `face_id` int(11) NOT NULL,
  `face_fileName` varchar(40) NOT NULL,
  `employ_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tb_faces`
--

INSERT INTO `tb_faces` (`face_id`, `face_fileName`, `employ_id`) VALUES
(11, 'training0', 456123),
(12, 'training1', 456124),
(13, 'training2', 456125),
(14, 'training3', 456126),
(15, 'training4', 456127),
(16, 'training5', 456128),
(17, 'training6', 456227),
(18, 'training7', 456327),
(19, 'training8', 456427),
(20, 'training9', 456527),
(21, 'training10', 456627),
(22, 'training11', 456727),
(23, 'training12', 457727),
(24, 'training13', 457827),
(25, 'training14', 457927),
(26, 'training15', 457027),
(27, 'training16', 457028),
(28, 'training17', 457029),
(29, 'training18', 457030),
(30, 'training19', 457031),
(31, 'training20', 457032);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_employ`
--
ALTER TABLE `tb_employ`
  ADD PRIMARY KEY (`employ_id`);

--
-- Indexes for table `tb_faces`
--
ALTER TABLE `tb_faces`
  ADD PRIMARY KEY (`face_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
