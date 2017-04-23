function reloadOptions(){
    $.ajax({url: "./data/filelist", success: function(result){

        window.info.fullOptions = result;

        resultSummary = Object.keys(result).map(function(el){
            let splitVersion = el.split("/");
            splitVersion.shift();
            return splitVersion.join("/");
        })

        window.info.options = resultSummary;

        // if (hasher.getHash() == ""){
        //     let defaultOption = "";
        //     let noGame = /^.*(nogamenolife).*$/
        //         for (let i = 0; i < window.info.options.length; i++){
        //             let opt = window.info.options[i];
        //             if (noGame.test(opt)){
        //                 defaultOption = opt;
        //                 break;
        //             }
        //         }
        //     hasher.setHash(defaultOption);
        // }
        
        window.info.updateData(resultSummary[0])
    }});

    $.ajax({url:"./res/links.json", success: function(result){
        window.info.links = result;
    }});
}

reloadOptions()

