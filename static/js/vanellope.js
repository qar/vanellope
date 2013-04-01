function deleteArticle(article_sn){
    $.ajax({
        url:"/article/" + article_sn,
        type:"DELETE",
    }).success(function() { 
        /* hide the current element's parent element.
        ** I don't know how to do it, so I add each "div.article-list" element an id.
        */
        $("#"+article_sn).slideUp(300);
    });
};

function recoverArticle(article_sn){
    $.ajax({
        url:"/article/recover/" + article_sn,
        type:"POST",
    }).success(function(){
        $("#"+article_sn).slideUp(300);
    });
};

function changeColor(){
    var color = $.trim($('#colorInput').val());
    if(!color){
            event.preventDefault();
    }
    else{
       $.ajax({
        url:"/ajax/color",
        type:"POST",
        data: "color="+ color,
    }).success(function() { 
        //$(".common-color").css("background", color);
        location.reload();
    }); 
    }   
};


function getPageByAuthor(page, uname){
    var url = "/article/page/"+page+".json"
    $("#jq-insert-mark").empty();
    $.ajax({
        dataType: "json",
        type:"GET",
        url: url,
        data:"name="+uname,
        success: function(data){
            $.each(data, function(key, val){
                var items = [];
                items.push('<div class="article-list primary-item-container" id="'+val.sn+'" style="margin:0px 20px 20px">');
                items.push('<span class="article-caption"><a href="/article/' + val.sn + '" title="'+val.title+'">' + val.title + '</a></span>');
                items.push('<span class="article-option-right option" onclick="deleteArticle('+val.sn+')" style="visibility:hidden"><i class="icon-trash  icon-large"></i></span>');
                items.push('<span class="article-option option" style="visibility:hidden"><a href="/update/'+val.sn+'"><i class="icon-edit icon-large"></i></a></span>');
                items.push('<span class="article-option option" style="visibility:hidden"><i class="icon-eye-open icon-large"></i></span></div>');
                $("#jq-insert-mark").append(items.join(''));
            });
        }
    });
};


function sendMessage(msg, dst){
    $.ajax({
        url: dst,
        type: "POST",
        dataType:"json",
        data: "message="+msg,
        success: function(data){
            console.log("message sent");
        }
    });
}; // end of button click event


