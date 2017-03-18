function reloadOptions(){
    $.ajax({url: "./data/filelist", success: function(result){
        result = result.map(function(el){
            let splitVersion = el.split("/");
            splitVersion.shift();
            return splitVersion.join("/");
        })
        window.info.options = result;
        let defaultOption = "";
        let noGame = /^.*(nogamenolife).*$/
        for (let i = 0; i < window.info.options.length; i++){
            let opt = window.info.options[i];
            if (noGame.test(opt)){
                defaultOption = opt;
                break;
            }
        }
        hasher.setHash(defaultOption);
    }});
}

reloadOptions()

