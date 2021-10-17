CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ctf_web` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `ctf_web`;
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('administrator','ACSI{E4sy_p34sy_l3m0n_squ33zy}');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;