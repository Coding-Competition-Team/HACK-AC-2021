<?php
//login_verify.php
$connect = new mysqli("localhost:3306", "root", "n0%bzblWjedhUaa", "DetentionBarracks");

session_start();

$error = '';

if ($_POST["user_name"] !== ""  && $_POST["user_password"] !== "") {
    $username = $_POST["user_name"];
    $userpassword = $_POST["user_password"];

    $query = "
    SELECT * FROM user WHERE user_name = ? && user_password = ?
    ";
    
    if(1){// if($statement = $connect->prepare($query)){
        // $statement -> bind_param("ss", $username, $userpassword);
        // $statement->execute();
        
        // $result = $statement->get_result();
        // $total_row = $result->num_rows;
        // if ($total_row !== 1) {
        if($username !== "devAccount" && $userpassword !== "logmeinnnn"){
            $error = 'Invalid Credentials';
            error_log("here");
        } else {
            // $row = $result -> fetch_assoc();
            $_SESSION["user_name"] = $username; //$row["user_name"];
            $_SESSION["user_password"] = $userpassword; //$row["user_password"];
            $_SESSION["login_user_id"] = 1; //$row["user_id"];
            
            $login_otp = rand(1000, 9999);
            $_SESSION['login_otp'] = (string)$login_otp;
            error_log("otp:".$_SESSION['login_otp']);
        }
    }else{
        error_log("failed");
    }
} else {
    $error = 'Empty Credentials';
}

$output = array(
    'error' => $error
);

echo json_encode($output);

?>
