function openInNewTab(url) {
    var win = window.open(url, '_blank');
    win.focus();
}

function highlightPath(path, graph) {
    window.info.selectedPath = path;

    if (path == undefined) {
        resetColors(null);
        return;
    }

    graph.nodes().forEach(function (n) {
        let keep = !(_.find(path, { 'id': n.id }) == undefined);
        n.color = (keep) ? n.originalColor : '#eee';
    });

    graph.edges().forEach(function (e) {
        let keep1 = !(_.find(path, { 'id': e.source }) == undefined);
        let keep2 = !(_.find(path, { 'id': e.target }) == undefined);
        e.color = (keep1 && keep2) ? e.originalColor : '#eee';
    });

    window.s.refresh();
}

function resetColors(event) {
    window.info.selectedNode = null;
    window.info.selectedPath = null;

    window.s.graph.nodes().forEach(function (n) {
        n.color = n.originalColor;
        n.hidden = 0;
        n.size = 10;
    });

    window.s.graph.edges().forEach(function (e) {
        e.color = e.originalColor;
    });

    window.s.refresh();
}

function colorNeighbors(node){
    var nodeId = node.id,
        toKeep = window.s.graph.neighbors(nodeId);

        toKeep[nodeId] = node;

        window.s.graph.nodes().forEach(function (n) {
            if(n.id === nodeId){
                n.color = "#000";
                return;
            }

            n.color = (toKeep[n.id]) ? n.originalColor : '#eee';
            if (!toKeep[n.id] && window.info.$data.componentMode) {
                n.hidden = 1;
            }
        });

        window.s.graph.edges().forEach(function (e) {
            e.color = (toKeep[e.source] && toKeep[e.target]) ? e.originalColor : '#eee';
        });

        window.s.refresh();
}

function focus(e){
    if (window.info.selectedNode == null) {
        window.info.selectedNode = e.data.node;

        console.log(e.data.node)
        colorNeighbors(e.data.node)
    }
    else {
        //Path-finding
        var nodeId = e.data.node.id,
            toKeep = window.s.graph.astar(window.info.selectedNode.id, nodeId);

        highlightPath(toKeep, s.graph)
    }
}

// used to interpolate between two colors
// format is "#rrggbb" as string for both colors 
function interpolate(color1, color2, frac) {
    r1 = parseInt(color1.substring(1, 3), 16)
    g1 = parseInt(color1.substring(3, 5), 16)
    b1 = parseInt(color1.substring(5, 7), 16)
    r2 = parseInt(color2.substring(1, 3), 16)
    g2 = parseInt(color2.substring(3, 5), 16)
    b2 = parseInt(color2.substring(5, 7), 16)
    retR = Math.min(Math.floor(r1 * frac + r2 * (1 - frac)), 255)
    retG = Math.min(Math.floor(g1 * frac + g2 * (1 - frac)), 255)
    retB = Math.min(Math.floor(b1 * frac + b2 * (1 - frac)), 255)
    retstr = '#' + retR.toString(16) + retG.toString(16) + retB.toString(16);
    return retstr;
}
