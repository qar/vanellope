
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
};


function getPage(page){
    var url = "/article/page/"+page+".json"
    $("#jq-insert-mark").empty();
    $.ajax({
        dataType: "json",
        url: url,
        success: function(data){
            $.each(data, function(key, val){
                var items = [];
                items.push('<div class="article-list primary-item-container" id="article-list-'+val.sn+'" style="margin:0px 20px 20px">');
                items.push('<span class="article-caption"><a href="/article/' + val.sn + '" title="'+val.title+'">' + val.title + '</a></span>');
                items.push('<span class="article-option-right option" onclick="deleteArticle('+ val.sn +')" style="visibility:hidden"><i class="icon-trash  icon-large"></i></span>');
                items.push('<span class="article-option option" style="visibility:hidden"><a href="/update/'+val.sn+'"><i class="icon-edit icon-large"></i></a></span></div>');
                $("#jq-insert-mark").append(items.join(''));
            });
        }
    });
};

