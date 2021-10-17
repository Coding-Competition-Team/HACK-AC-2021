<?php

session_start();

if (isset($_SESSION["user_id"])) {
    header("location:home.php");
}

?>
<?php
// echo system("cat /usr/local/etc/php/conf.d/*");
// phpinfo();
?>
<!DOCTYPE html>
<html>
	<head>
		<title>PHP Login with OTP Authentication</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script src="http://code.jquery.com/jquery.js"></script>
    	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	</head>
	<body>
		<br />
		<div class="container">
			<h3 align="center">Login</h3>
			<br />
			<div class="row">
				<div class="col-md-3">&nbsp;</div>
				<div class="col-md-6">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h3 class="panel-title">Login</h3>
						</div>
						<div class="panel-body" id="login_area">
							<form method="POST" id="login_form">
								<div class="form-group">
									<!-- TODO: Remove creds devAccount:logmeinnnn -->
									<label>Enter Username</label>
									<input type="text" name="user_name" id="user_name" class="form-control" />
									<label>Enter Password</label>
									<input type="password" name="user_password" id="user_password" class="form-control" />
									<span id="user_login_error" class="text-danger"></span>
								</div>
								<div class="form-group" align="right">
									<input type="submit" name="next" id="next" class="btn btn-primary" value="Next" />
								</div>
							</form>
						</div>
						<div class="panel-body" id="otp_area" style="display:none;">
							<form method="POST" id="otp_form">
								<div class="form-group" id="otp_area">
									<label>Enter 13 Digit OTP Number</label>
									<input type="text" name="user_otp" id="user_otp" class="form-control" />
									<span id="user_otp_error" class="text-danger"></span>
								</div>
								<div class="form-group" align="right">
									<input type="submit" name="next" id="next_otp" class="btn btn-primary" value="Next" />
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>

		</div>
		<br />
		<br />
	</body>
</html>

<script>

$(document).ready(function(){
	$('#login_form').on('submit', function(event){
		event.preventDefault();
		$.ajax({
			url:"login_verify.php",
			method:"POST",
			data:$(this).serialize(),
			dataType:"json",
			beforeSend:function(){
				$('#next').attr('disabled', 'disabled');
			},
			success:function(data){
				$('#next').attr('disabled', false);
				if(data.error != ''){
					$('#user_login_error').text(data.error);
				}else{
					$('#user_login_error').text('');
					$('#login_area').css('display', 'none');
					$('#otp_area').css('display', 'block');
				}
			},
			fail: function(){
				console.log('test');
				alert('test');
			}
		})
	});
});


$(document).ready(function(){
	$('#otp_form').on('submit', function(event){
		event.preventDefault();
		$.ajax({
			url:"otp_verify.php",
			method:"POST",
			data:$(this).serialize(),
			dataType:"json",
			beforeSend:function(){
				$('#next_otp').attr('disabled', 'disabled');
			},
			success:function(data){
				$('#next_otp').attr('disabled', false);
				if(data.error != ''){
					$('#user_otp_error').text(data.error);
				}else{
					window.location='home.php';
				}
			}
		})
	});
});

</script>
