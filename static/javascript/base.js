$(document).ready(function(){
    $("#search-text").keyup(function(){
        var title = $("#search-text").val();                         
        $.get("{% url 'rango:search' %}",{'title':title}, function(data){               
            for (var i = data.length - 1; i >= 0; i--) {        
                //$('#search-result').append(data[i]+'<br/>') 
                var result_list = document.getElementById('search-list');
                var result = document.createElement("div");
                result.innerHTML = '<span>'+ data[i] + '</span>';
                result_list.appendChild(result);                           
            };
        })
    });
    
    $('#search-text').keydown(function(){
        $('#search-list').empty();
    })
    $('#search-text').blur(function(){
        if ($('#search-list').blur){
            $('#search-list').empty();
        }
    })
});