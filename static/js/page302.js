
function onHomeIndexLoad(){
	$('div.member-info p:nth-child(3)').html('hello, world!');
};



$(document).ready(function(){
	var loc = $(location).attr('pathname')
	if( loc == '/home'){
		onHomeIndexLoad();	
	}	
})
