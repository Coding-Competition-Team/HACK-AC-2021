<h2>Sign In</h2>
<form action="index.php" method="post">
    <input type="text" name="uid" placeholder="Username">
    <input type="password" name="pwd" placeholder="Password">
    <button type="submit" name="submit">Submit</button>
</form>

<?php
require("index.conf.php"); 

if(isset($_POST['uid']) && isset($_POST['pwd']) && isset($_POST['submit'])) {
    $query = "SELECT * FROM users where username = '" . $_POST['uid'] . "' and password = '" . $_POST['pwd'] . "'";

    if ($result = $conn->query($query)) {
        if($user = $result->fetch_object()) {
            echo "Welcome " . $user->username . "!<br>" . $user->password;
        }else {
            echo "invalid username or password";
        }
    }
}else {
    echo "Enter a valid SQL query";	
}
?>