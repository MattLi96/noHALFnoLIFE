$('#graph-container').bind('contextmenu', function (e) {
    return false;
});

/**
 * Additional function for identifying neighbors
 * @param {String} nodeId - name of the node
 */
sigma.classes.graph.addMethod('neighbors', function (nodeId) {
    var k,
        neighbors = {},
        index = this.allNeighborsIndex[nodeId] || {};

    for (k in index)
        neighbors[k] = this.nodesIndex[k];

    return neighbors;
});

/**
 * Generate the graph from the given wiki path
 * @param {string} path - string path to the wiki source
 */
function generate(path) {
    if(window.info.$data.currentTime == ""){
        path = "public/" + path;
        lastOne = window.info.$data.fullOptions[path].length;
        path = window.info.$data.fullOptions[path][lastOne-1];
        path = path.slice(7);
        window.info.$data.currentTime = path;
    }

    $("#graph-container").html("")

    $.getJSON(decodeURI("public/" + path), function (data) {
        var i,
            N = data["nodes"].length,
            E = data["edges"].length,
            g = {
                nodes: data["nodes"],
                edges: data["edges"]
            };

        window.info.basicInfo = data["basic"]

        maxdeg = 0
        color1 = '#cf1515'
        color2 = '#15cfcf'
        for (i = 0; i < N; i++) {
            if (g.nodes[i].degree > maxdeg) {
                maxdeg = g.nodes[i].degree;
            }
        }
        for (i = 0; i < N; i++) {
            g.nodes[i]["label"] = g.nodes[i].id;
            g.nodes[i]["x"] = Math.random();
            g.nodes[i]["y"] = Math.random();
            g.nodes[i]["size"] = 10;
            g.nodes[i]["color"] = interpolate(color1, color2, g.nodes[i].degree / maxdeg);
            g.nodes[i]["originalColor"] = interpolate(color1, color2, g.nodes[i].degree / maxdeg);
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
            renderer: {
                container: "graph-container",
                type: "canvas"
            },
            settings: {
                drawLabels: window.info.$data.showAllLabels
            }
        });

        window.s.bind('rightClickNode', function (e) {
            // console.log(e)
            let url = window.info.links[window.info.currentOption] + e.data.node.id;
            $(e.target).trigger("click");

            setInterval(function(){
                openInNewTab(url);
            }, 200);
        });

        window.s.bind('clickNode', focus);
        window.s.bind('clickStage', resetColors);

        // Initialize the dragNodes plugin:
        var dragListener = sigma.plugins.dragNodes(window.s, window.s.renderers[0]);
        dragListener.bind('startdrag', function (event) {
            window.s.stopForceAtlas2();
            window.info.forceOn = false;
        });
    });
}