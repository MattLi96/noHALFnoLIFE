function reloadOptions(){
    $.ajax({url: "./data/filelist", success: function(result){
        result.forEach(function(el){
            $("#options").append("<li><a href="+"#"+" class="+"dropDownListItem"+">" + el + "</a></li>");
        });
    }});
}

$(document).on('click', '.dropDownListItem', function(e) {
    console.log("derp");
    var name = e.currentTarget;
    console.log(name.innerHTML);

    var loadName = name.innerHTML.split("/")
    loadName.shift()
    loadName = loadName.join("/")

    console.log(loadName)
    generate(loadName)
});

reloadOptions()

