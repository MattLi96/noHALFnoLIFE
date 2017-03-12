var forceConfig = {
        worker: true,
        barnesHutOptimize: true
    };

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

        // Generate a random graph:
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

        // Initialize the dragNodes plugin:
        var dragListener = sigma.plugins.dragNodes(window.s, window.s.renderers[0]);
        dragListener.bind('startdrag', function (event) {
            // console.log(event);
            window.s.stopForceAtlas2();
        });
        dragListener.bind('drag', function (event) {
            // console.log(event);
        });
        dragListener.bind('drop', function (event) {
            // console.log(event);
        });
        dragListener.bind('dragend', function (event) {
            // console.log(event);
        });
    });
}

window.forceOn = false;

$("#dance").on("click", function(){
    if(window.forceOn){
        window.s.stopForceAtlas2();
    }
    else{
        window.s.startForceAtlas2(forceConfig);
    }
    window.forceOn = !window.forceOn;
});

generate("data/nogamenolife_pages_current.json")

setTimeout(function(){
    $("#dance").trigger("click");
}, 200)