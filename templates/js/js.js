// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
/**
 * @meikandamoorthi.n 
 */
function login(){
	$("#li").css('display','block');
	$("#su").css('display','none');
	$("#fgpw").css('display','none');
}

function signup(){
	$("#li").css('display','none');
	$("#su").css('display','block');
	$("#fgpw").css('display','none');
}

function forgotpass(){
	$("#li").css('display','none');
	$("#su").css('display','none');
	$("#fgpw").css('display','block');
}

function lif(){
	var uname=$("#liun").val();
	var pword=$("#lipw").val();
	var url=$("#lireturn").val();
	querystr="username="+uname+"&password="+pword+"&return="+url;
	$.post("/accounts/login/",querystr,function(data){
		if(data.match('html')){
			window.location="/accounts/";
		}
		else if(data.match('http')){
			window.location=data;
		}
		else{
			$("#lires").html(data);
		}
	})
}

function suf(){
	var un=$("#suun").val();
	var em=$("#suem").val();
	var pw=$("#supw").val();
	var cpw=$("#sucpw").val();
	var url=$("#sureturn").val();
	querystr="username="+un+"&email="+em+"&password="+pw+"&conformpassword="+cpw+"&return="+url;
	$.post("/accounts/create/",querystr,function(data){
		if(data.match('div')){
			$("#bodydiv").html(data);
		}
		else{
			$("#sures").html(data);
		}
	})
}

function validateuname(uname){
	if (uname==""){
		$("#sures").html("Please enter username");
		$("#sures").fadeIn(100);
		$("#sures").fadeOut(6000);
	}
	else if (uname.length >= 6 && uname.length <= 30){
		if ((/[A-Z]/g).test(uname)){
			$("#sures").html("Please enter username not using capital letter");
			$("#sures").fadeIn(100);
			$("#sures").fadeOut(6000);
		}
	}
	else{
		$("#sures").html("Minimum 6 letters in username");
		$("#sures").fadeIn(100);
		$("#sures").fadeOut(6000);
	}
}

function validatemail(mailid){
	if (mailid==""){
		$("#sures").html("Please enter mail id");
		$("#sures").fadeIn(100);
		$("#sures").fadeOut(6000);
	}
}

function cmfvalidatemail(mailid){
	if (mailid==""){
		$("#cmres").html("Please enter mail id");
		$("#cmres").fadeIn(100);
		$("#cmres").fadeOut(6000);
	}
}

function supassval(pass){
	check = Validation(pass);
	if(check=="True"){
		$("#sures").html("");
	}
	else{
		$("#sures").css('display','block');
		$("#sures").html(check);
	}
}

function fgppassval(pass){
	check = Validation(pass);
	if(check=="True"){
		$("#fgpres").html("");
	}
	else{
		$("#fgpres").css('display','block');
		$("#fgpres").html(check);
	}
}

function chpassval(pass){
	check = Validation(pass);
	if(check=="True"){
		$("#cpres").html("");
	}
	else{
		$("#cpres").css('display','block');
		$("#cpres").html(check);
	}
}

function Validation(pw){
	if (pw.length >= 6){
		var result = "";
		if (!(/[A-Z]/g).test(pw)){
			result = result.concat("Atleast one capital letter in your password<br>");
		}
		if (!(/[0-9]/i).test(pw)){
			result = result.concat("Atleast one number in your password<br>");
		}
		if (!(/[`~!@#$%^&*()_+{}|:"?></.,;'\=[-]/i).test(pw)){
			result = result.concat("Atleast one special character in your password");
		}
		if(result==""){
			return "True";
		}
		return result;
	}
	return ("Minimum 6 characters in the password");
}

function supasscheck(confpass){
	pass=$("#supw").val();
	name=$("#suun").val();
	mail=$("#suem").val();
	len=confpass.length;
	if((pass[len-1]==confpass[len-1])&&len>1){
		$("#sures").html("");
		if((pass==confpass)&&(name!="")&&(mail!="")){
			$("#susub").prop('disabled',false);
		}
		else{
			$("#susub").prop('disabled',true);
		}
	}
	else{
		if(pass.length<confpass.length || pass.length>confpass.length){
			$("#sures").html("Password not matched");
		}
		$("#susub").prop('disabled',true);
	}
}

function fgppasscheck(confpass){
	pass=$("#fgppw").val();
	ans=$("#fgpans").val();
	len=confpass.length;
	if((pass[len-1]==confpass[len-1])&&len>1){
		$("#fgpres").html("");
		if((pass==confpass)&&(ans!="")){
			$("#fgpsub").prop('disabled',false);
		}
		else{
			$("#fgpsub").prop('disabled',true);
		}
	}
	else{
		if(pass.length<confpass.length || pass.length>confpass.length){
			$("#fgpres").html("Password not matched");
		}
		$("#fgpsub").prop('disabled',true);
	}
}

function chpasscheck(confpass){
	pass=$("#cppw").val();
	len=confpass.length;
	if((pass[len-1]==confpass[len-1])&&len>1){
		$("#cpres").html("");
		if(pass==confpass){
			$("#cpsub").prop('disabled',false);
		}
		else{
			$("#cpsub").prop('disabled',true);
		}
	}
	else{
		if(pass.length<confpass.length || pass.length>confpass.length){
			$("#cpres").html("Password not matched");
		}
		$("#cpsub").prop('disabled',true);
	}
}

function pdf(){
	name=$("#wel").text();
	fname=$("#pdfn").val();
	gen=$("#pdgen option:selected").text();
	lang=$("#pdlang option:selected").text();
	coun=$("#pdcoun option:selected").text();
	tz=$("#pdtz option:selected").text();
	ph=$("#pdph").val();
	url=$("#pdreturn").val();
	querystr="username="+name+"&fname="+fname+"&gender="+gen+"&lang="+lang+"&coun="+coun+"&time="+tz+"&phone="+ph+"&return="+url;
	$.post("/accounts/profile/create/",querystr,function(data){
		if(data.match('div')){
			$("#bodydiv").html(data);
		}
	})
}

function sdf(){
	name=$("#wel").text();
	ques=$("#sdsq").val();
	ans=$("#sdsa").val();
	url=$("#sdreturn").val();
	querystr="username="+name+"&question="+ques+"&answer="+ans+"&return="+url;
	$.post("/accounts/security/create/",querystr,function(data){
		if(data.match('html')){
			window.location="/accounts/";
		}
		else if(data.match('http')){
			window.location=data;
		}
		else{
			window.location=data;
		}
	})
}

function fgpwf(){
	var email=$("#fgpwem").val();
	var url=$("#fgpwreturn").val();
	querystr="email="+email+"&return="+url;
	$.post("/accounts/recovery/",querystr,function(data){
		if(data.match('div')){
			$("#bodydiv").html(data);
		}
	})
}

function fgpf(){
	email=$("#fgpmail").val();
	ques=$("#fgpqu").val();
	ans=$("#fgpans").val();
	pass=$("#fgppw").val();
	confpass=$("#fgpcpw").val();
	var url=$("#fgpreturn").val();
	querystr="email="+email+"&question="+ques+"&answer="+ans+"&newpass="+pass+"&confpass="+confpass+"&return="+url;
	$.post("/accounts/password/recovery/",querystr,function(data){
		window.location=data;
	})
}

function load(){
	$("#popup").css('display','none');
}

function upload(){
	$( "#popup" ).dialog({ width: 500, resizable: false });
}

function closePhotoPopUp(){
	$( "#popup" ).dialog( "close" );
}

/*function home(){
	$.post("/")
}

function profile(){
	$.post("/accounts")
}*/

function settings(){
	$.post("set/",function(data){
		$("#content").html(data);
	})
}

function cpf(){
	var oldpass=$("#cpop").val();
	var newpass=$("#cppw").val();
	var confpass=$("#cpcpw").val();
	querystr="oldpass="+oldpass+"&newpass="+newpass+"&confpass="+confpass;
	$.post("/accounts/change/password/",querystr,function(data){
		$("#content").html(data);
	})
}

function chpa(){
	$.post("/accounts/change/password/form/",function(data){
		$("#content").html(data);
	})
}

function csqf(){
	var pass=$("#csqpw").val();
	var ques=$("#csqsq").val();
	var ans=$("#csqsa").val();
	querystr="password="+pass+"&question="+ques+"&answer="+ans;
	$.post("/accounts/change/security/",querystr,function(data){
		if(data=="success"){
			$("#csqpw").prop('disabled',true);
			$("#csqsq").prop('disabled',true);
			$("#csqsa").prop('disabled',true);
			$("#csqsub").prop('disabled',true);
			$("#csqres").html(data);
		}
		else{
			$("#csqres").html(data);
		}
	})
}

function chqa(){
	$.post("/accounts/change/security/form/",function(data){
		$("#content").html(data);
	})
}

function cmf(){
	var pass=$("#cmpw").val();
	var email=$("#cmem").val();
	querystr="password="+pass+"&newmail="+email;
	$.post("/accounts/change/mail/",querystr,function(data){
		if(data=="success"){
			$("#cmpw").prop('disabled',true);
			$("#cmem").prop('disabled',true);
			$("#cmsub").prop('disabled',true);
			$("#cmres").html(data);
		}
		else{
			$("#cmres").html(data);
		}
	})
}

function chem(){
	$.post("/accounts/change/mail/form/",function(data){
		$("#content").html(data);
	})
}

function photo(){
	$("#submit").click(function(){
		filename=$("#file").val();
	    $.ajax({
	        type: "POST",
	        url: "/accounts/picture/",
	        enctype:"multipart/form-data",
	        data: {
	            file: filename
	        },
	        success: function () {
	            alert("Data Uploaded: ");
	        }
	    });
	})
}
