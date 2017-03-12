window.targets = []

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
            g.nodes[i]["color"] = '#666';
        }
        for (i = 0; i < E; i++) {
            g.edges[i]["id"] = i;
            g.edges[i]["size"] = Math.random();
            g.edges[i]["color"] = '#ccc';
        }
        sigma.renderers.def = sigma.renderers.canvas
        // Instantiate sigma:
        window.s = new sigma({
            graph: g,
            container: 'graph-container'
        });

        window.s.graph.nodes().forEach(function (n) {
            n.originalColor = n.color;
        });
        window.s.graph.edges().forEach(function (e) {
            e.originalColor = e.color;
        });

        window.s.bind('clickNode', function (e) {
            var nodeId = e.data.node.id,
                toKeep = s.graph.neighbors(nodeId);
            toKeep[nodeId] = e.data.node;

            s.graph.nodes().forEach(function (n) {
                if (toKeep[n.id])
                    n.color = n.originalColor;
                else
                    n.color = '#eee';
            });

            s.graph.edges().forEach(function (e) {
                if (toKeep[e.source] && toKeep[e.target])
                    e.color = e.originalColor;
                else
                    e.color = '#eee';
            });

            // Since the data has been modified, we need to
            // call the refresh method to make the colors
            // update effective.
            window.s.refresh();
        });

        window.s.bind('clickStage', function (e) {
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

        window.s.bind('rightClickNode', function (e) {
            console.log(e.data.node);
            window.targets.push(e.data.node)
            if (window.targets.length > 1) {
                var last = window.targets[window.targets.length - 1]
                var last2 = window.targets[window.targets.length - 2]
                console.log(last)
                console.log(last2)
                console.log(window.s.graph.astar(last.label, last2.label));
            }
        });
    });
}
