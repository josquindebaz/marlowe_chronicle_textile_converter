import math
from re import split


def make_intro(graph_id, graph_number):
    """Set first lines of the graph"""

    return (f'<script class="code" type="text/javascript"> '
            f'var {graph_id} = new sigma (\'graph-container_{graph_number}\');\n')


def make_ending(graph_id):
    """Set last lines of the graph"""

    return (f"{graph_id}.settings(""{labelThreshold: 1, defaultEdgeType: 'curve'});\n"
            f"{graph_id}.refresh();\n"
            f"{graph_id}.startForceAtlas2(""{barnesHutOptimize: true, slowDown: 1, strongGravityMode: true, "
            "outboundAttractionDistribution: false, linLogMode: false, adjustSizes: true});\nsetTimeout(function() {"
            f"{graph_id}.stopForceAtlas2();""}, 3000);\n</script>\n")


def set_lists(network_text):
    """compute node lists"""

    nodes = []
    edges = {}

    groups = [item for item in split(r"\s*;\s*", network_text) if item]
    for group in groups:
        items = split(r"(.*)\s*:\s*", group)
        node = items[1].strip()

        if node not in nodes:
            nodes.append(node)

        network = [item
                   for item in split(r"\s*,\s*", items[2])
                   if item != node]

        if network:
            edges[node] = network

            [nodes.append(item)
             for item in network
             if item not in nodes]

    return nodes, edges


def set_edges(graph_id, nodes, edges):
    """generate text to describe edges in SigmaJS format"""

    default_color = "#7e8cc6"

    principal_colors = ["#c69749",
                        "#7d48c8",
                        "#70b147",
                        "#d353ad",
                        "#5aa992",
                        "#c24638",
                        "#7389c5",
                        "#5a592a",
                        "#623466",
                        "#c07282"]

    edge_text = ""
    partition_colors = {}
    degrees = {}

    for node_count, source in enumerate(nodes):
        theta = node_count * 2 * math.pi / len(nodes)
        position = "x: %f, y: %f" % (math.cos(theta), math.sin(theta))

        node_degree = get_node_degree(edges, source)
        degrees[source] = node_degree

        if node_degree not in partition_colors:
            if principal_colors:
                partition_colors[node_degree] = principal_colors.pop()
            else:
                partition_colors[node_degree] = default_color

        edge_text += (f"{graph_id}.graph.addNode(""{id: "f"'n{nodes.index(source)}', label: \"{source}\", "
                      f"{position}, size: {node_degree}, color: '{partition_colors[node_degree]}'""}); ")

    edge_text += "\n"

    edge_number = 0
    for source, targets in edges.items():
        for target in targets:
            if degrees[source] > degrees[target]:
                edge_color = partition_colors[degrees[source]]
            else:
                edge_color = partition_colors[degrees[target]]

            edge_text += (f"{graph_id}.graph.addEdge(""{"f" id: 'e{edge_number}', "
                          f"source: 'n{nodes.index(source)}',target: "f"'n{nodes.index(target)}',"
                          f" color: '{edge_color}'""}); ")

            edge_number += 1

    return edge_text


def get_node_degree(edges, node):
    if node not in edges:
        return 1

    degree = 0
    for source, targets in edges.items():
        if node == source:
            degree += len(targets)
        elif node in targets:
            degree += 1

    return degree


class SigmaJsGenerator:
    """Convert a description of a word network to a SigmaJs graph"""

    def __init__(self, network_text, graph_number):
        graph_id = "sigma_%d" % graph_number

        self.graph = make_intro(graph_id, graph_number)

        nodes, edges = set_lists(network_text)

        self.graph += set_edges(graph_id, nodes, edges)
        self.graph += make_ending(graph_id)
