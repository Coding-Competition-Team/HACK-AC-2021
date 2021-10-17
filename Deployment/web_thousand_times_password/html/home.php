<?php

//home.php

session_start();

if (!isset($_SESSION["user_id"])) {
    header("location:login.php");
}

?>
<!DOCTYPE html>
<html>
	<head>
		<title>Home</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script src="http://code.jquery.com/jquery.js"></script>
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	</head>
	<body>
		<br />
		<div class="container">
			<div class="panel panel-default">
				<div class="panel-heading">
					<h3 class="panel-title">Flag</h3>
				</div>
				<div class="panel-body">
					<h3 align="center"> <?php echo file_get_contents('flag') ?></h3>
				</div>
			</div>
		</div>
		<div class="container">
			<a href="logout.php" class="btn btn-default" align="center">Logout</a>
		</div>
		<br />
		<br />
	</body>
</html>