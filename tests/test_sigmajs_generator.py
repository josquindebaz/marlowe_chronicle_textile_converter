from sigmajs_generator import SigmaJsGenerator, set_lists, set_edges

expected_intro = '<script class="code" type="text/javascript"> var sigma_1 = new sigma (\'graph-container_1\');'
expected_ending = ("sigma_1.settings({labelThreshold: 1, defaultEdgeType: 'curve'});\n"
                   "sigma_1.refresh();\n"
                   "sigma_1.startForceAtlas2({barnesHutOptimize: true, slowDown: 1, strongGravityMode: true, "
                   "outboundAttractionDistribution: false, linLogMode: false, adjustSizes: true});\n"
                   "setTimeout(function() {sigma_1.stopForceAtlas2();}, 3000);\n"
                   '</script>\n')


def test_can_add_intro():
    generated_graph = SigmaJsGenerator("", 1)

    result = generated_graph.graph.split("\n")[0]

    assert result == expected_intro


def test_can_add_ending():
    generated_graph = SigmaJsGenerator("", 1)

    result = generated_graph.graph

    assert result == expected_intro + "\n\n" + expected_ending


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


def test_can_set_lists():
    network_text = "foo : foo, bar ; bar : bar ; alice : foo, bar, alice ; ;"

    result_nodes, result_edges = set_lists(network_text)

    assert result_nodes == ['foo', 'bar', 'alice']
    assert result_edges == {'foo': ['bar'], 'alice': ['foo', 'bar']}


def test_can_set_edges():
    result = set_edges(1, ['foo', 'bar', 'alice'], {'foo': ['bar'], 'alice': ['foo', 'bar']})

    expected_edges_text = \
        ("1.graph.addNode({id: 'n0', label: \"foo\", x: 1.000000, y: 0.000000, size: 2, color: '#c07282'}); "
         "1.graph.addNode({id: 'n1', label: \"bar\", x: -0.500000, y: 0.866025, size: 1, color: '#623466'}); "
         "1.graph.addNode({id: 'n2', label: \"alice\", x: -0.500000, y: -0.866025, size: 2, color: '#c07282'}); \n"
         "1.graph.addEdge({ id: 'e0', source: 'n0',target: 'n1', color: '#c07282'}); "
         "1.graph.addEdge({ id: 'e1', source: 'n2',target: 'n0', color: '#c07282'}); "
         "1.graph.addEdge({ id: 'e2', source: 'n2',target: 'n1', color: '#c07282'}); ")

    assert result == expected_edges_text
