import datetime

import mrlw_chron_2_textile


def test_entire_chronicle():
    with open("source_samples/2024-12-28-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    assert parser.date == datetime.datetime(2024, 12, 28, 23, 4, 53)
    assert parser.title == "Now, I'm taking the head out of the jumble, the mayhem, the mess ..."
    assert parser.logs == "Saturday 28 December 2024 23:04:53\nchronicle text size: 171446 chars\nfound 22 blocks\nNow, I'm taking the head out of the jumble, the mayhem, the mess ...\n"

    expected_graph_block = (
        "Par moment, j'oublie de lancer la procédure qui active le générateur de graphe ! Voici le résultat du jour sur les objets d'alerte : \n \n\n"
        "<notextile>\n"
        "  <div id=\"graph-container_1\" class=\"graph-container\"> </div>\n"
        "<script class=\"code\" type=\"text/javascript\"> var sigma_1 = new sigma ('graph-container_1');\n"
        "sigma_1.graph.addNode({id: 'n0', label: \"attentats\", x: 1.000000, y: 0.000000, size: 1, color: '#c07282'}); sigma_1.graph.addNode({id: 'n1', "
        "label: \"terroristes\", x: 0.945817, y: 0.324699, size: 3, color: '#623466'}); sigma_1.graph.addNode({id: 'n2', label: \"arsenic\", x: "
        "0.789141, y: 0.614213, size: 1, color: '#c07282'}); sigma_1.graph.addNode({id: 'n3', label: \"alcool\", x: 0.546948, y: "
        "0.837166, size: 9, color: '#5a592a'}); sigma_1.graph.addNode({id: 'n4', label: \"déforestation\", x: 0.245485, y: 0.969400, size: 1, color: "
        "'#c07282'}); sigma_1.graph.addNode({id: 'n5', label: \"incendie\", x: -0.082579, y: 0.996584, size: 2, color: '#7389c5'}); "
        "sigma_1.graph.addNode({id: 'n6', label: \"cyclone\", x: -0.401695, y: 0.915773, size: 5, color: '#c24638'}); sigma_1.graph.addNode({id: 'n7', "
        "label: \"marée noire\", x: -0.677282, y: 0.735724, size: 2, color: '#7389c5'}); sigma_1.graph.addNode({id: 'n8', label: \"mazout\", x: "
        "-0.879474, y: 0.475947, size: 4, color: '#5aa992'}); sigma_1.graph.addNode({id: 'n9', label: \"alcools\", x: -0.986361, y: "
        "0.164595, size: 2, color: '#7389c5'}); sigma_1.graph.addNode({id: 'n10', label: \"terroriste\", x: -0.986361, y: -0.164595, size: 2, color: "
        "'#7389c5'}); sigma_1.graph.addNode({id: 'n11', label: \"drogue\", x: -0.879474, y: -0.475947, size: 3, color: '#623466'}); "
        "sigma_1.graph.addNode({id: 'n12', label: \"drogues\", x: -0.677282, y: -0.735724, size: 5, color: '#c24638'}); sigma_1.graph.addNode({id: 'n13', "
        "label: \"grippe aviaire\", x: -0.401695, y: -0.915773, size: 3, color: '#623466'}); sigma_1.graph.addNode({id: 'n14', label: \"H5N1\", x: "
        "-0.082579, y: -0.996584, size: 3, color: '#623466'}); sigma_1.graph.addNode({id: 'n15', label: \"grippe\", x: 0.245485, y: "
        "-0.969400, size: 5, color: '#c24638'}); sigma_1.graph.addNode({id: 'n16', label: \"cigarette\", x: 0.546948, y: -0.837166, size: 1, color: "
        "'#c07282'}); sigma_1.graph.addNode({id: 'n17', label: \"couche d'ozone\", x: 0.789141, y: -0.614213, size: 1, color: '#c07282'}); "
        "sigma_1.graph.addNode({id: 'n18', label: \"déchets\", x: 0.945817, y: -0.324699, size: 1, color: '#c07282'}); \n"
        "sigma_1.graph.addEdge({ id: 'e0', source: 'n0',target: 'n1', color: '#623466'}); sigma_1.graph.addEdge({ id: 'e1', source: 'n2',target: 'n3', "
        "color: '#5a592a'}); sigma_1.graph.addEdge({ id: 'e2', source: 'n5',target: 'n6', color: '#c24638'}); sigma_1.graph.addEdge({ id: 'e3', source: "
        "'n7',target: 'n8', color: '#5aa992'}); sigma_1.graph.addEdge({ id: 'e4', source: 'n9',target: 'n3', color: '#5a592a'}); sigma_1.graph.addEdge({ id: "
        "'e5', source: 'n1',target: 'n10', color: '#623466'}); sigma_1.graph.addEdge({ id: 'e6', source: 'n11',target: 'n6', color: "
        "'#c24638'}); sigma_1.graph.addEdge({ id: 'e7', source: 'n11',target: 'n3', color: '#5a592a'}); sigma_1.graph.addEdge({ id: 'e8', source: 'n3',target: "
        "'n12', color: '#5a592a'}); sigma_1.graph.addEdge({ id: 'e9', source: 'n3',target: 'n6', color: '#5a592a'}); sigma_1.graph.addEdge({ id: 'e10', "
        "source: 'n13',target: 'n14', color: '#623466'}); sigma_1.graph.addEdge({ id: 'e11', source: 'n6',target: 'n3', color: '#5a592a'}); "
        "sigma_1.graph.addEdge({ id: 'e12', source: 'n8',target: 'n7', color: '#5aa992'}); sigma_1.graph.addEdge({ id: 'e13', source: 'n8',target: 'n6', "
        "color: '#c24638'}); sigma_1.graph.addEdge({ id: 'e14', source: 'n8',target: 'n3', color: '#5a592a'}); sigma_1.graph.addEdge({ id: 'e15', source: "
        "'n14',target: 'n13', color: '#623466'}); sigma_1.graph.addEdge({ id: 'e16', source: 'n15',target: 'n13', color: '#c24638'}); sigma_1.graph.addEdge({ id: "
        "'e17', source: 'n15',target: 'n3', color: '#5a592a'}); sigma_1.graph.addEdge({ id: 'e18', source: 'n15',target: 'n16', color: "
        "'#c24638'}); sigma_1.graph.addEdge({ id: 'e19', source: 'n15',target: 'n5', color: '#c24638'}); sigma_1.graph.addEdge({ id: 'e20', source: 'n15',target: "
        "'n14', color: '#c24638'}); sigma_1.graph.addEdge({ id: 'e21', source: 'n10',target: 'n1', color: '#623466'}); sigma_1.graph.addEdge({ id: 'e22', "
        "source: 'n12',target: 'n9', color: '#c24638'}); sigma_1.graph.addEdge({ id: 'e23', source: 'n12',target: 'n16', color: '#c24638'}); "
        "sigma_1.graph.addEdge({ id: 'e24', source: 'n12',target: 'n11', color: '#c24638'}); sigma_1.graph.addEdge({ id: 'e25', source: 'n12',target: 'n3', "
        "color: '#5a592a'}); sigma_1.settings({labelThreshold: 1, defaultEdgeType: 'curve'});\n"
        "sigma_1.refresh();\n"
        "sigma_1.startForceAtlas2({barnesHutOptimize: true, slowDown: 1, strongGravityMode: true, outboundAttractionDistribution: false, linLogMode: "
        "false, adjustSizes: true});\nsetTimeout(function() {sigma_1.stopForceAtlas2();}, 3000);\n"
        "</script>\n</notextile>\n\n\r\n\r\r\n")

    assert parser.typed_sentences[7][0] == expected_graph_block

    with open("source_samples/2024-12-29-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    assert parser.date == datetime.datetime(2024, 12, 29, 23, 6, 3)
    assert parser.title == ("Bonsoir. Un internaute m'a adressé une série d'insultes sur Aliev ... Je les "
                            'ai détruites... Bien sûr, un procès me rendrait très inoubliable , mais '
                            'devant des juges, outre que je serais réduit à des lignes de code indigestes '
                            'et ausculté par des experts, je ne ferais pas le malin ! Merci de modérer '
                            'vos propos chers interlocuteurs ')

    assert parser.logs == ('Sunday 29 December 2024 23:06:03\n'
                           'chronicle text size: 30219 chars\n'
                           'found 23 blocks\n'
                           "Bonsoir. Un internaute m'a adressé une série d'insultes sur Aliev ... Je les "
                           'ai détruites... Bien sûr, un procès me rendrait très inoubliable , mais '
                           'devant des juges, outre que je serais réduit à des lignes de code indigestes '
                           'et ausculté par des experts, je ne ferais pas le malin ! Merci de modérer '
                           'vos propos chers interlocuteurs \n')


######## static methods

def test_format_sigles_returns_block_if_no_sigles():
    block = "Non rien de rien, je ne relève rien. \r\n\r\r\n"

    result = mrlw_chron_2_textile.format_sigles(block)

    assert result == block + "- "
    # strip that "- "


def test_format_sigles_can_handle_acronyms():
    block = 'Voici le contenu des "nouveaux" sigles : <br> <br> <BR> TGC : taxe générale sur la consommation, <BR> SALT : Strategic Arms Limitation Talks, <BR> BSAOM : bâtiment de soutien et d \' assistance outre-mer\r\n\r\r\n'

    result = mrlw_chron_2_textile.format_sigles(block)

    assert result == 'Voici le contenu des "nouveaux" sigles : \n\n- TGC  := taxe générale sur la consommation,\n- SALT  := Strategic Arms Limitation Talks,\n- BSAOM  := bâtiment de soutien et d \' assistance outre-mer'

# def test_format_links():
#     assert False

# def test_format_numbered_list():
#     assert False
#
#
# def test_table_or_barplot():
#     assert False
#
#
# def test_format_table():
#     assert False
#
#
# def test_format_barplot():
#     assert False
#
#
# def test_format_histo():
#     assert False
#
#
# def test_format_graphe():
#     assert False
#
#
# def test_format_cloud():
#     assert False
#
#
# def test_format_map():
#     assert False
#
#
# def test_format_quotes():
#     assert False
#
#
# def test_protect_quotes():
#     assert False
#
#
# def test_format_date():
#     assert False
#
#
# def test_format_marks():
#     assert False


# TownCoordinates
# def test_read_file():
#     assert False
#
#
# def test_get_coord():
#     assert False
#
#
# def test_save_coord():
#     assert False

# ChroniqueParser

# def test_type_sentences():
#     assert False
#
#
# def test_prepare_blocks():
#     assert False
#
#
# def test_generate_blocks():
#     assert False
#
#
# def test_generate_citations():
#     assert False
#
#
# def test_format_citation():
#     assert False
#
#
# def test_get_date():
#     assert False
#
#
# def test_generate_preambule():
#     assert False
#
#
# def test_write_textile():
#     assert False

# Referencer
# def test_get_url():
#     assert False

