$(document).ready(function(){
    $("#search-text").keyup(function(){
        var title = $("#search-text").val();                         
        $.get("/rango/search/",{'title':title}, function(data){               
            for (var i = data.length - 1; i >= 0; i--) {        
                var result_list = document.getElementById('operator-search-list');
                var result = document.createElement("div");
                result.innerHTML = '<span>'+ data[i] + '</span>';
                result_list.appendChild(result);                           
            };
        })
    });
    
    $('#search-text').keydown(function(){
        $('#operator-search-list').empty();
    })
    $('#search-text').blur(function(){
        if ($('#operator-search-list').blur){
            $('#operator-search-list').empty();
        }
    })
});