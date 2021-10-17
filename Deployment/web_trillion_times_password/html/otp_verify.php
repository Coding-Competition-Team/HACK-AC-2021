<?php
session_start();

$error = '';

if ($_POST["user_otp"] != '') {
    if ($_SESSION['login_otp'] === $_POST["user_otp"]) {
        $_SESSION['user_id'] = $_SESSION['login_user_id'];
        unset($_SESSION["login_user_id"]);
        unset($_SESSION["login_otp"]);
    } else {
        $error = 'Wrong OTP Number';
    }
} else {
    $error = 'OTP Number is required';
}

$output = array(
    'error' => $error
);

echo json_encode($output);

?>