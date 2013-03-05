
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

function sendComment(){
    //alert($.trim($('textarea.inputbox').val()));
    if( $.trim( $('textarea.inputbox').val()) ){
        alert("you did write something, good");
    }
    else{
        alert("you haven't wrote anything, not good");
    }
};

function deleteArticle(article_sn){
    alert(article_sn);
    $.ajax({
        url:"/article/" + article_sn,
        type:"GET",
        data:"option=delete",
    }).success(function() { 
        location.reload(); 
    });
};
