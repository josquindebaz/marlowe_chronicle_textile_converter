import math
import re


class SigmaJsGenerator:
    """Convert a description of a word network to a SigmaJs graph"""

    def __init__(self, text, graphe_count):
        self.list_nodes = []
        self.list_edges = {}
        self.js = ""
        self.name = "sigma_%d" % graphe_count
        self.intro(graphe_count)
        self.set_lists(text)
        self.set_edges()
        self.end()

    def intro(self, graphe_count):
        """Add first lines of the script"""
        self.js += ('<script class="code" type="text/javascript"> '
                    'var %s = new sigma (\'graph-container_%d\');\n') % \
                   (self.name, graphe_count)

    def end(self):
        """last lines"""
        self.js += ("%s.settings({labelThreshold: 1, "
                    "defaultEdgeType: 'curve'});\n") % self.name
        #        self.js += ("%s.graph.nodes().forEach(function(node) "
        #                    "{node.color = '#' + (\"000000\" + "
        #                    "Math.random().toString(16).slice(2, 8)"
        #                    ".toUpperCase()).slice(-6);});\n") % self.name
        #        self.js += ("%s.graph.edges().forEach(function(edge) "
        #                    "{edge.color = '#7389c5'});\n")% self.name
        self.js += "%s.refresh();\n" % self.name
        self.js += ("%s.startForceAtlas2({barnesHutOptimize: true, "
                    "slowDown: 1, strongGravityMode: true, "
                    "outboundAttractionDistribution: false, "
                    "linLogMode: false, adjustSizes: true});\n") % self.name
        self.js += ("setTimeout(function() {%s.stopForceAtlas2();}, "
                    "3000);\n") % self.name
        self.js += "</script>\n"

    def set_lists(self, text):
        """compute lists """
        for item in re.split(r"\s*;\s*", text):
            if item:
                elements = re.split(r"\s*(.*) :\s*", item)
                node = elements[1]
                if node not in self.list_nodes:
                    self.list_nodes.append(elements[1])
                network = re.split(r"\s*,\s*", elements[2])
                if node in network:
                    network.remove(node)
                if network:
                    for element in network:
                        if element not in self.list_nodes:
                            self.list_nodes.append(element)
                    self.list_edges[elements[1]] = network

    def set_edges(self):
        """generate edges text"""
        n_node = 0
        colordic = {}
        sizedic = {}
        colorlist = ["#c69749",
                     "#7d48c8",
                     "#70b147",
                     "#d353ad",
                     "#5aa992",
                     "#c24638",
                     "#7389c5",
                     "#5a592a",
                     "#623466",
                     "#c07282"]
        for node in self.list_nodes:
            size = 0
            if node in self.list_edges:
                for key_deg, val_deg in self.list_edges.items():
                    if node == key_deg:
                        size += len(val_deg)
                    elif node in val_deg:
                        size += 1
            else:
                size = 1
            sizedic[node] = size
            if size not in colordic:
                if colorlist:
                    colordic[size] = colorlist.pop()
                else:
                    colordic[size] = "#7e8cc6"
            self.js += ("%s.graph.addNode({id: 'n%d', label: \"%s\", "
                        "x: %f, y: %f, size: %d, color: '%s'}); ") % (
                           self.name,
                           self.list_nodes.index(node),
                           node,
                           math.cos(n_node * 2 * math.pi / len(self.list_nodes)),
                           math.sin(n_node * 2 * math.pi / len(self.list_nodes)),
                           size,
                           colordic[size])
            n_node += 1
        n_edge = 0
        self.js += "\n"
        for node, edges in self.list_edges.items():
            for edge in edges:
                if sizedic[node] > sizedic[edge]:
                    color = colordic[sizedic[node]]
                else:
                    color = colordic[sizedic[edge]]
                if node != edge:
                    self.js += ("%s.graph.addEdge({ id: 'e%d', source: 'n%d',"
                                "target: 'n%d', color: '%s'}); ") % (
                                   self.name,
                                   n_edge,
                                   self.list_nodes.index(node),
                                   self.list_nodes.index(edge),
                                   color)
                    n_edge += 1
