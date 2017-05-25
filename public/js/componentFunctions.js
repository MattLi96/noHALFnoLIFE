function formatDate(dateString){
    //Chop off the beginning
    dateString = dateString.substring(dateString.lastIndexOf("_")+1, dateString.length-1);
    //Remove the .json tail
    dateString = dateString.substring(0, dateString.lastIndexOf("."));
    let divide = dateString.split("-");

    dateString = divide[1] + "/" + divide[2] + "/" + divide[0] + " at " + divide[3];

    return dateString;
}

function searchNode(nodeName){           
    let found = (_.find(window.s.graph.nodes(), { 'id': nodeName }));

    if(found == undefined){
        alert("Node not found...")
    }
    else{
        colorNeighbors(found);
    }
}
