$(document).ready(function(){
	$('.demo').dblclick(function(){
		$(this).slideUp(500);
	});
});


function delArticle(sn){
	// using ajax to delete a aricle from database
	if(confirm("Are you sure to delet this article ?"))
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.open('POST', '/ajax?o=del&sn=' + sn, true); // o for option
		xmlhttp.send();
		xmlhttp.onreadystatechange=function(){
  		if (xmlhttp.readyState==4 && xmlhttp.status==200){
    		$(this).parent("div").slideUp(500);
    	};
  	};
};
