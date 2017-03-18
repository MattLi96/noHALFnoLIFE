function reloadOptions(){
    $.ajax({url: "./data/filelist", success: function(result){
        result = result.map(function(el){
            let splitVersion = el.split("/");
            splitVersion.shift();
            return splitVersion.join("/");
        })
        window.info.options = result;
        //window.info.currentOption = window.info.options[0]
        //generate(window.info.currentOption)
    }});
}

reloadOptions()

