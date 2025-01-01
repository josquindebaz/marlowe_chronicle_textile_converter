from sigmajs_generator import SigmaJsGenerator

expected_intro = '<script class="code" type="text/javascript"> var sigma_1 = new sigma (\'graph-container_1\');'


def test_can_add_intro():
    generated_graph = SigmaJsGenerator("", 1)

    result = generated_graph.graph.split("\n")[0]

    assert result == expected_intro


def test_can_add_ending():
    generated_graph = SigmaJsGenerator("", 1)

    result = generated_graph.graph.split("\n")

    assert result[2] == "sigma_1.settings({labelThreshold: 1, defaultEdgeType: 'curve'});"
    assert result[3] == "sigma_1.refresh();"
    assert (result[4] == "sigma_1.startForceAtlas2({barnesHutOptimize: true, slowDown: 1, strongGravityMode: true, "
                         "outboundAttractionDistribution: false, linLogMode: false, adjustSizes: true});")
    assert result[5] == "setTimeout(function() {sigma_1.stopForceAtlas2();}, 3000);"


def test_can_add_edges():
    network_text = "foo : foo , bar ;"

    generated_graph = SigmaJsGenerator(network_text, 1)

    result = generated_graph.graph.split("\n")

    expected_nodes = (
        "sigma_1.graph.addNode({id: 'n0', label: \"foo\", x: 1.000000, y: 0.000000, size: 1, color: '#c07282'}); "
        "sigma_1.graph.addNode({id: 'n1', label: \"bar\", x: -1.000000, y: 0.000000, size: 1, color: '#c07282'}); ")

    assert result[1] == expected_nodes

    expected_edges = ("sigma_1.graph.addEdge({ id: 'e0', source: 'n0',target: 'n1', color: '#c07282'}); "
                      "sigma_1.settings({labelThreshold: 1, defaultEdgeType: 'curve'});")

    assert result[2] == expected_edges
