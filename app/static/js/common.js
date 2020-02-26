$("#search_btn").click(function () {
    var key = $("#key").val();
    console.log(key);
    if(key!=null && key != ""){
        window.location.href = "/search/?key="+key
    }
});

