/**
 * Reformats the date into a human-readable string for display purposes
 * @param {string} dateString - the date string before processing
 */
function formatDate(dateString){
    //Chop off the beginning
    dateString = dateString.substring(dateString.lastIndexOf("_")+1, dateString.length-1);

    //Remove the .json tail
    dateString = dateString.substring(0, dateString.lastIndexOf("."));

    //Reform the string
    let divide = dateString.split("-");
    dateString = divide[1] + "/" + divide[2] + "/" + divide[0] + " at " + divide[3];

    return dateString;
}

/**
 * Searches for the given node in the current network. If node present, it highlights it
 * @param {string} nodeName - The name of the node
 */
function searchNode(nodeName){           
    let found = (_.find(window.s.graph.nodes(), { 'id': nodeName }));
    (found == undefined) ? alert("Node not found...") : colorNeighbors(found);
}
