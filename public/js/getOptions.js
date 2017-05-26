/** 
 * Get all wiki options from an external file
 */
function reloadOptions(){
    $.ajax({url: "./public/data/filelist.json", success: function(result){

        window.info.fullOptions = result;

        resultSummary = Object.keys(result).map(function(el){
            let splitVersion = el.split("/");
            splitVersion.shift();
            return splitVersion.join("/");
        })

        window.info.options = resultSummary;        
        window.info.updateData(resultSummary[0])
    }});

    $.ajax({url:"./public/res/links.json", success: function(result){
        window.info.links = result;
    }});
}

reloadOptions()

