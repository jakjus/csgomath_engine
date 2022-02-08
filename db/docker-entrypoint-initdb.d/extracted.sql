-- Adminer 4.8.1 MySQL 5.5.5-10.6.5-MariaDB-1:10.6.5+maria~focal dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `extracted`;
CREATE DATABASE `extracted` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `extracted`;

DROP TABLE IF EXISTS `caseKeys`;
CREATE TABLE `caseKeys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caseId` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  `icon_url` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `caseId` (`caseId`),
  CONSTRAINT `caseKeys_ibfk_1` FOREIGN KEY (`caseId`) REFERENCES `cases` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `cases`;
CREATE TABLE `cases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `icon_url` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=392 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `descriptionFields`;
CREATE TABLE `descriptionFields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caseId` int(11) NOT NULL,
  `ind` tinyint(4) NOT NULL,
  `value` varchar(256) DEFAULT NULL,
  `color` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `caseId_value_ind` (`caseId`,`value`,`ind`),
  KEY `caseId` (`caseId`),
  CONSTRAINT `descriptionFields_ibfk_1` FOREIGN KEY (`caseId`) REFERENCES `cases` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6854 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `descriptionPrices`;
CREATE TABLE `descriptionPrices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descriptionFieldId` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `descriptionFieldId_timestamp` (`descriptionFieldId`,`timestamp`),
  CONSTRAINT `descriptionPrices_ibfk_1` FOREIGN KEY (`descriptionFieldId`) REFERENCES `descriptionFields` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2867 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `keysDescriptionFields`;
CREATE TABLE `keysDescriptionFields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyId` varchar(32) NOT NULL,
  `ind` tinyint(4) NOT NULL,
  `value` varchar(256) DEFAULT NULL,
  `color` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `keyId_value_ind` (`keyId`,`value`,`ind`),
  CONSTRAINT `keysDescriptionFields_ibfk_1` FOREIGN KEY (`keyId`) REFERENCES `caseKeys` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `prices`;
CREATE TABLE `prices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `caseId` int(11) NOT NULL,
  `sale_price` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `timestamp` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `caseId_timestamp` (`caseId`,`timestamp`),
  CONSTRAINT `prices_ibfk_1` FOREIGN KEY (`caseId`) REFERENCES `cases` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=386 DEFAULT CHARSET=utf8mb4;


-- 2022-02-08 12:02:25
