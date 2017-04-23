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
    });

    window.s.graph.edges().forEach(function (e) {
        e.color = e.originalColor;
    });

    window.s.refresh();
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

function generate(path) {
    if(window.info.$data.currentTime == ""){
        path = "public/" + path;
        path = window.info.$data.fullOptions[path][0]
        path = path.slice(7);
        window.info.$data.currentTime = path;
    }

    $("#graph-container").html("")

    $.getJSON(decodeURI(path), function (data) {
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
            openInNewTab(url)
        })

        window.s.bind('clickNode', function (e) {
            if (window.info.selectedNode == null) {
                window.info.selectedNode = e.data.node;

                var nodeId = e.data.node.id,
                    toKeep = s.graph.neighbors(nodeId);
                toKeep[nodeId] = e.data.node;

                s.graph.nodes().forEach(function (n) {
                    n.color = (toKeep[n.id]) ? n.originalColor : '#eee';
                    if (!toKeep[n.id] && window.info.$data.componentMode) {
                        n.hidden = 1;
                    }
                });

                s.graph.edges().forEach(function (e) {
                    e.color = (toKeep[e.source] && toKeep[e.target]) ? e.originalColor : '#eee';
                });

                window.s.refresh();
            }
            else {
                //Path-finding
                var nodeId = e.data.node.id,
                    toKeep = window.s.graph.astar(window.info.selectedNode.id, nodeId);

                highlightPath(toKeep, s.graph)
            }
        });

        window.s.bind('clickStage', resetColors);

        // Initialize the dragNodes plugin:
        var dragListener = sigma.plugins.dragNodes(window.s, window.s.renderers[0]);
        dragListener.bind('startdrag', function (event) {
            window.s.stopForceAtlas2();
            window.info.forceOn = false;
        });
    });
}
