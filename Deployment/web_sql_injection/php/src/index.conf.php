<?php
  $host = 'db';
  $user = 'ctf_web';
  $pass = 'oSnkiSJ609SlG4w';
  $mydatabase = 'ctf_web';
  
  // check the mysql connection status
  $conn = new mysqli($host, $user, $pass, $mydatabase);

  // Check connection
  if ($conn->connect_error) {
      die("Unable to connect to MYSQL server");
  }
?>