
function editBio(){
    $('#edit-button').hide();
    $('span.member-info').hide();
    $('textarea.member-info, #submit').show();
    $('textarea.member-info').html($.trim($('span.member-info').text()));

    $('button#submit').click(function(){
        $('span.member-info').html($.trim($('textarea.member-info').val()));
        $('textarea.member-info, #submit').hide();
        $('span.member-info, #edit-button').show();
        $.ajax({
            url:"/home",
            type:"POST",
            data:{'brief':$.trim($('textarea.member-info').val())},
        });
    });
};


function expandCommentBox(){
    $("textarea.inputbox").css({"height":"100px"});
};


function deleteArticle(article_sn){
    $.ajax({
        url:"/article/" + article_sn,
        type:"DELETE",
    }).success(function() { 
        location.reload(); 
    });
};

function changeColor(){
    if(!$.trim($('#color-input').val())){
            event.preventDefault();
    }
    else{
       $.ajax({
        url:"/ajax/color",
        type:"POST",
        data: "color="+ $.trim($('#color-input').val()),
    }).success(function() { 
        location.reload(); 
    }); 
    }
    
}
