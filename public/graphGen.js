function generate(path){
    // Parameter declaration, the height and width of our viz.
    var width = 800, height = 800;

    // Colour scale for node colours.
    var color = d3.scale.category10();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("#d3-container").select("svg")
    if (svg.empty()) {
        svg = d3.select("#d3-container").append("svg")
            .attr("width", width)
            .attr("height", height);
    }

    // We load the JSON network file.
    d3.json(path, function (error, graph) {
        // Within this block, the network has been loaded
        // and stored in the 'graph' object.

        // We load the nodes and links into the force-directed
        // graph and initialise the dynamics.
        force.nodes(graph.nodes)
            .links(graph.links)
            .start();

        // We create a < line> SVG element for each link
        // in the graph.
        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link");

        // We create a < circle> SVG element for each node
        // in the graph, and we specify a few attributes.
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 5)  // radius
            .style("fill", function (d) {
                // We colour the node depending on the degree.
                return color(d.degree);
            })
            .call(force.drag);

        // The label each node its node number from the networkx graph.
        node.append("title").text(function (d) {
            return "Node: " + d.id + "\n" + "Degree: " + d.degree + "\n";
        });

        // We bind the positions of the SVG elements
        // to the positions of the dynamic force-directed graph,
        // at each time step.
        force.on("tick", function () {
            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

            node.attr("cx", function (d) { return d.x; })
                .attr("cy", function (d) { return d.y; });
        });
    });
}

generate("data/nogamenolife_pages_current.json")