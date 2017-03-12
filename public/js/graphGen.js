// window.targets = []

$('#graph-container').bind('contextmenu', function (e) {
    return false;
});

sigma.classes.graph.addMethod('neighbors', function (nodeId) {
    var k,
        neighbors = {},
        index = this.allNeighborsIndex[nodeId] || {};

    for (k in index)
        neighbors[k] = this.nodesIndex[k];

    return neighbors;
});

function generate(path) {
    $("#graph-container").html("")

    $.getJSON(path, function (data) {
        var i,
            N = data["nodes"].length,
            E = data["edges"].length,
            g = {
                nodes: data["nodes"],
                edges: data["edges"]
            };

        for (i = 0; i < N; i++) {
            g.nodes[i]["label"] = g.nodes[i].id;
            g.nodes[i]["x"] = Math.random();
            g.nodes[i]["y"] = Math.random();
            g.nodes[i]["size"] = Math.random();
            g.nodes[i]["color"] = '#ff392e';
            g.nodes[i]["originalColor"] = '#ff392e';
        }
        for (i = 0; i < E; i++) {
            g.edges[i]["id"] = i;
            g.edges[i]["size"] = Math.random();
            g.edges[i]["color"] = '#ff6666';
            g.edges[i]["originalColor"] = '#ff6666';
        }
        sigma.renderers.def = sigma.renderers.canvas
        // Instantiate sigma:
        window.s = new sigma({
            graph: g,
            container: 'graph-container'
        });

        window.s.bind('clickNode', function (e) {
            if(window.info.selectedNode == null){
                window.info.selectedNode = e.data.node;

                var nodeId = e.data.node.id,
                    toKeep = s.graph.neighbors(nodeId);
                toKeep[nodeId] = e.data.node;

                s.graph.nodes().forEach(function (n) {
                    n.color = (toKeep[n.id]) ? n.originalColor : '#eee';
                });

                s.graph.edges().forEach(function (e) {
                    e.color = (toKeep[e.source] && toKeep[e.target]) ? e.originalColor : '#eee';
                });

                window.s.refresh();
            }
            else{
                //Path-finding
                var nodeId = e.data.node.id,
                    toKeep = window.s.graph.astar(nodeId, window.info.selectedNode.id);

                window.info.selectedPath = toKeep;

                s.graph.nodes().forEach(function (n) {
                    let keep = !(_.find(toKeep, { 'id': n.id }) == undefined);
                    n.color = (keep) ? n.originalColor : '#eee';
                });

                s.graph.edges().forEach(function (e) {
                    let keep1 = !(_.find(toKeep, { 'id': e.source }) == undefined);
                    let keep2 = !(_.find(toKeep, { 'id': e.target }) == undefined);
                    e.color = (keep1 && keep2) ? e.originalColor : '#eee';
                });

                window.s.refresh();


                // console.log(e.data.node);
                // window.targets.push(e.data.node)
                // if (window.targets.length > 1) {
                //     var last = window.targets[window.targets.length - 1]
                //     var last2 = window.targets[window.targets.length - 2]
                //     console.log(last)
                //     console.log(last2)
                //     console.log(window.s.graph.astar(last.label, last2.label));
                // }
            }
            
        });

        window.s.bind('clickStage', function (e) {
            window.info.selectedNode = null;
            window.info.selectedPath = null;

            window.s.graph.nodes().forEach(function (n) {
                n.color = n.originalColor;
            });

            window.s.graph.edges().forEach(function (e) {
                e.color = e.originalColor;
            });

            // Same as in the previous event:
            window.s.refresh();
        });

        // Initialize the dragNodes plugin:
        var dragListener = sigma.plugins.dragNodes(window.s, window.s.renderers[0]);
        dragListener.bind('startdrag', function (event) {
            // console.log(event);
            window.s.stopForceAtlas2();
            window.info.forceOn = false;
        });
    });
}
