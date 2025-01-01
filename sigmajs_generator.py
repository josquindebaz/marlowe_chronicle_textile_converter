import math
import re


class SigmaJsGenerator:
    """Convert a description of a word network to a SigmaJs graph"""

    def __init__(self, network_text, graph_number):
        self.list_nodes = []
        self.list_edges = {}
        self.graph = ""

        self.graph_id = "sigma_%d" % graph_number
        self.set_intro(graph_number)

        self.set_lists(network_text)
        self.add_edges()

        self.add_ending()

    def set_intro(self, graph_count):
        """Set first lines of the graph"""

        self.graph = ('<script class="code" type="text/javascript"> '
                      'var %s = new sigma (\'graph-container_%d\');\n') % \
                     (self.graph_id, graph_count)

    def add_ending(self):
        """Add last lines of the graph"""

        self.graph += ("%s.settings({labelThreshold: 1, defaultEdgeType: 'curve'});\n"
                       "%s.refresh();\n"
                       "%s.startForceAtlas2({barnesHutOptimize: true, slowDown: 1, strongGravityMode: true, "
                       "outboundAttractionDistribution: false, linLogMode: false, adjustSizes: true});\n"
                       "setTimeout(function() {%s.stopForceAtlas2();}, 3000);\n"
                       "</script>\n") % (self.graph_id, self.graph_id, self.graph_id, self.graph_id)

    def set_lists(self, text):
        """compute node lists """

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

    def add_edges(self):
        """generate edges text"""

        node_count = 0
        color_dictionary = {}
        size_dictionary = {}
        color_list = ["#c69749",
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

            size_dictionary[node] = size

            if size not in color_dictionary:
                if color_list:
                    color_dictionary[size] = color_list.pop()
                else:
                    color_dictionary[size] = "#7e8cc6"

            self.graph += ("%s.graph.addNode({id: 'n%d', label: \"%s\", "
                           "x: %f, y: %f, size: %d, color: '%s'}); ") % (
                              self.graph_id,
                              self.list_nodes.index(node),
                              node,
                              math.cos(node_count * 2 * math.pi / len(self.list_nodes)),
                              math.sin(node_count * 2 * math.pi / len(self.list_nodes)),
                              size,
                              color_dictionary[size])
            node_count += 1

        edge_count = 0
        self.graph += "\n"

        for node, edges in self.list_edges.items():
            for edge in edges:
                if size_dictionary[node] > size_dictionary[edge]:
                    color = color_dictionary[size_dictionary[node]]
                else:
                    color = color_dictionary[size_dictionary[edge]]

                if node != edge:
                    self.graph += ("%s.graph.addEdge({ id: 'e%d', source: 'n%d',"
                                   "target: 'n%d', color: '%s'}); ") % (
                                      self.graph_id,
                                      edge_count,
                                      self.list_nodes.index(node),
                                      self.list_nodes.index(edge),
                                      color)
                    edge_count += 1
