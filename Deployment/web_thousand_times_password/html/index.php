<?php

//index.php

session_start();

if (isset($_SESSION["user_id"])) {
    header("location:home.php");
} else {
    header("location:login.php");
}