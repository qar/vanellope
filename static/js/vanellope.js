
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
        /* hide the current element's parent element.
        ** I don't know how to do it, so I add each "div.article-list" element an id.
        */
        $("#article-list-"+article_sn).slideUp(300);
    });
};

function recoverArticle(article_sn){
    $.ajax({
        url:"/article/recover/" + article_sn,
        type:"POST",
    }).success(function(){
        $("#article-list-"+article_sn).slideUp(300);
    });
};

function changeColor(){
    color = $.trim($('#color-input').val())
    if(!color){
            event.preventDefault();
    }
    else{
       $.ajax({
        url:"/ajax/color",
        type:"POST",
        data: "color="+ color,
    }).success(function() { 
        $(".common-color").css("background", color);
    }); 
    }
    
}
