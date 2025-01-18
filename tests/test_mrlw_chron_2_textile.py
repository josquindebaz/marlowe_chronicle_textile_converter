import datetime
import re

import mrlw_chron_2_textile
from mrlw_chron_2_textile import make_histogram
from tests.test_textile_utils import remove_random_color


def test_entire_chronicle():
    with open("source_samples/2024-12-28-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    assert parser.logs == "Saturday 28 December 2024 23:04:53\nchronicle text size: 171446 chars\nfound 22 blocks\nNow, I'm taking the head out of the jumble, the mayhem, the mess ...\n"

    expected_publish_date = r'\np\(publish_date\). samedi 28 décembre 2024 23:04:53\n'
    assert re.search(expected_publish_date, parser.chronique)

    expected_preamble_first = '---\nlayout: post\ntitle: "Now, I\'m taking the head out of the jumble, the mayhem, the mess ..."\nexcerpt: "J\'ai repéré que le champ <i>\[DATE\]</i> était particulièrement fragile aux influences extérieures - il est en effet facile à des agents externes d\'insérer des lignes juste avant le lancement de la chronique. Ne pas hésiter à me dire s\'il y a des choses outrageantes - car en réalité je ne lis pas ce qui s\'écrit dans ce champ !"\nextra_js: '
    assert re.search(expected_preamble_first, parser.chronique)
    expected_preamble_second = '\n---\n\nh2. {{ page.title }}\n\np\(publish_date\). samedi 28 décembre 2024 23:04:53\n'
    assert re.search(expected_preamble_second, parser.chronique)

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

    preamble = """---
layout: post
title: "Bonsoir. Un internaute m'a adressé une série d'insultes sur Aliev ... Je les ai détruites... Bien sûr, un procès me rendrait très inoubliable , mais devant des juges, outre que je serais réduit à des lignes de code indigestes et ausculté par des experts, je ne ferais pas le malin ! Merci de modérer vos propos chers interlocuteurs "
excerpt: " Je ne parviens pas à choisir d'événement. En un clic, ah ah ! En un clic, tu as accès à l'encyclopédie mondiale ! Et moi qui rame pour produire des recoupements et des rapprochements qui sont le plus souvent inutiles ! :"
extra_js:"""

    assert re.search(preamble, parser.chronique)

    assert parser.logs == ('Sunday 29 December 2024 23:06:03\n'
                           'chronicle text size: 30219 chars\n'
                           'found 23 blocks\n'
                           "Bonsoir. Un internaute m'a adressé une série d'insultes sur Aliev ... Je les "
                           'ai détruites... Bien sûr, un procès me rendrait très inoubliable , mais '
                           'devant des juges, outre que je serais réduit à des lignes de code indigestes '
                           'et ausculté par des experts, je ne ferais pas le malin ! Merci de modérer '
                           'vos propos chers interlocuteurs \n')

    expected_publish_date = r'\np\(publish_date\). dimanche 29 décembre 2024 23:06:03\n'
    assert re.search(expected_publish_date, parser.chronique)


def test_chronicle_with_map():
    with open("source_samples/2025-01-03-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    title = "Marlowe, c'est à toi ( pour ce qu'il en est de ma propre vision des choses ...)"
    assert parser.chronique.find(title)

    assert parser.logs == "Friday 3 January 2025 23:07:02\nchronicle text size: 17002 chars\nfound 24 blocks\nMarlowe, c'est à toi ( pour ce qu'il en est de ma propre vision des choses ...)\n"

    expected_publish_date = r'\np\(publish_date\). vendredi 3 janvier 2025 23:07:02\n'
    assert re.search(expected_publish_date, parser.chronique)

    expected_map = """La collection des capitales mondiales récupérée sur Wikipedia est mise à contribution pour faire des cartes. Voici la projection du jour - les gros points sont cela va de soi les capitales les plus citées... Vous suivez ? 

p.

<notextile>

<div id="map">
<script class="code" type="text/javascript">
var initMap = function(){
	var provider = new com.modestmaps.TemplatedLayer("http://tile.openstreetmap.org/{Z}/{X}/{Y}.png");
	var map = new com.modestmaps.Map("map", provider);
	var canvas = document.createElement("canvas");
	canvas.style.position = "absolute";
	canvas.style.left = "0";
	canvas.style.top = "0";
	canvas.width = map.dimensions.x;
	canvas.height = map.dimensions.y;
	map.parent.appendChild(canvas);
	var Lisbonne = new com.modestmaps.Location(38.7069320,-9.1356321);
	var Ath_nes = new com.modestmaps.Location(37.9841493,23.7279843);
	var Monaco = new com.modestmaps.Location(43.7311424,7.4197576);
	var Santiago = new com.modestmaps.Location(-33.4377968,-70.6504451);
	var T_h_ran = new com.modestmaps.Location(35.6892523,51.3896004);
	var Vatican = new com.modestmaps.Location(41.9034912,12.4528349);
	var Tirana = new com.modestmaps.Location(41.3279457,19.8185323);
	var Sucre = new com.modestmaps.Location(-19.047862,-65.2596023);
	var Podgorica = new com.modestmaps.Location(42.4415238,19.2621081);
	var Montevideo = new com.modestmaps.Location(-34.9059039,-56.1913569);
	var Freetown = new com.modestmaps.Location(8.4790017,-13.2680158);
	var Bakou = new com.modestmaps.Location(40.3754289,49.8328549);
	var Accra = new com.modestmaps.Location(5.5600141,-0.2057436);
	var Bangkok = new com.modestmaps.Location(13.5859219,100.416086601645);
	var Kiev = new com.modestmaps.Location(50.4501071,30.5240501);
	var Bruxelles = new com.modestmaps.Location(50.8503396,4.3517103);
	var Moscou = new com.modestmaps.Location(55.7557860,37.6176330);
	var Madrid = new com.modestmaps.Location(40.4167047,-3.7035825);
	var Vienne = new com.modestmaps.Location(48.156,16.371);
	var Copenhague = new com.modestmaps.Location(55.6760968,12.5683371);
	var Lima = new com.modestmaps.Location(-12.0433333,-77.0283333);
	var Tel_Aviv = new com.modestmaps.Location(32.0804808,34.7805274);
	var Oslo = new com.modestmaps.Location(59.9138688,10.7522454);
	var Sanaa = new com.modestmaps.Location(15.342101,44.2005197);
	var J_rusalem = new com.modestmaps.Location(31.7968155,35.2137815559015);
	var New_York = new com.modestmaps.Location(40.7143528,-74.0059731);
	var Rome = new com.modestmaps.Location(41.8933439,12.4830718);
	var Bagdad = new com.modestmaps.Location(33.3024248,44.3787992);
	var Tokyo = new com.modestmaps.Location(34.2255804,139.294774527387);
	var Abidjan = new com.modestmaps.Location(5.4091179,-4.0422099);
	var P_kin = new com.modestmaps.Location(39.9042140,116.4074130);
	var Berlin = new com.modestmaps.Location(52.5234051,13.4113999);
	var Buenos_Aires = new com.modestmaps.Location(-34.612869,-58.4459789);
	var Doha = new com.modestmaps.Location(25.3014957,51.4996673988223);
	var Londres = new com.modestmaps.Location(51.5001524,-0.1262362);
	var Washington = new com.modestmaps.Location(38.8951118,-77.0363658);
	var Caracas = new com.modestmaps.Location(10.506098,-66.9146017);
	var S_oul = new com.modestmaps.Location(37.5666791,126.9782914);
	var Paris = new com.modestmaps.Location(48.8566101,2.3514992);
	var Damas = new com.modestmaps.Location(33.5130695,36.3095814);
	var locations = [Lisbonne, Ath_nes, Monaco, Santiago, T_h_ran, Vatican, Tirana, Sucre, Podgorica, Montevideo, Freetown, Bakou, Accra, Bangkok, Kiev, Bruxelles, Moscou, Madrid, Vienne, Copenhague, Lima, Tel_Aviv, Oslo, Sanaa, J_rusalem, New_York, Rome, Bagdad, Tokyo, Abidjan, P_kin, Berlin, Buenos_Aires, Doha, Londres, Washington, Caracas, S_oul, Paris, Damas];
	var values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5, 5, 7, 14, 18, 23, 29, 48];
	var max = Math.max.apply(Math, values);
	map.setExtent(locations);
	map.zoomOut();
	function redraw(){
		var ctx = canvas.getContext('2d');
		ctx.clearRect(0,0,canvas.width,canvas.height);
		for (var i = 0; i < locations.length; i++){
			ctx.beginPath();
			var p = map.locationPoint(locations[i]);
			ctx.fillStyle = '#00749F';
			ctx.globalAlpha = 0.6;
			radius = values[i] * 15 / max + 5;
			ctx.arc(p.x,p.y,radius,0,2 * Math.PI, false);
			ctx.fill();
			ctx.stroke();
		}
	}
	map.addCallback('drawn', redraw);
	map.addCallback('resized', function(){
		canvas.width = map.dimensions.x;
		canvas.height = map.dimensions.y;
		redraw();
	});
	redraw();
}
</script>
</div>

</notextile>

p(reference). "Fond et positions © les contributeurs d'OpenStreetMap":https://www.openstreetmap.org/copyright


J'ose présumer que Tirésias et Nominatim ont les bonnes coordonnées !\r\n\r\r\n"""

    assert (parser.typed_sentences[20][0][:4230] == expected_map[:4230])
    assert (parser.typed_sentences[20][0][4236:] == expected_map[4236:])


def test_chronicle_with_histogram():
    with open("source_samples/2025-01-04-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    title = 'Pour tout dire La sociologie informatique ne passionne pas les foules :'
    assert parser.chronique.find(title)

    assert parser.logs == ('Saturday 4 January 2025 23:05:45\nchronicle text size: 20167 chars\nfound 24 blocks\n'
                           'Pour tout dire La sociologie informatique ne passionne pas les foules :\n')

    expected_publish_date = r'\np\(publish_date\). samedi 4 janvier 2025 23:05:45\n'
    assert re.search(expected_publish_date, parser.chronique)

    assert "barplot" in parser.extra_js

    expected_histogram_1 = '<notextile>\n <script class="code" type="text/javascript">\n$(document).ready(function(){ \nvar s = [ 0, 259, 279, 320, 318, 315, 287, 267, 291, 312, 308, 357, 361, 348, 342, 306, 280, 220, 272, 205, 228, 4 ];\nvar ticks = [\' 2004 \',\' 2005 \',\' 2006 \',\' 2007 \',\' 2008 \',\' 2009 \',\' 2010 \',\' 2011 \',\' 2012 \',\' 2013 \',\' 2014 \',\' 2015 \',\' 2016 \',\' 2017 \',\' 2018 \',\' 2019 \',\' 2020 \',\' 2021 \',\' 2022 \',\' 2023 \',\' 2024 \',\' 2025 \'];\nvar plot = $.jqplot(\'chart_0\', [s,],{\n\tseriesColors: [\'#'
    expected_histogram_2 = '\'], \n\tseriesDefaults:{renderer:$.jqplot.BarRenderer, rendererOptions:{fillToZero: true}},\n\taxes:{\n\t\txaxis:{renderer: $.jqplot.CategoryAxisRenderer, ticks: ticks},\n\t\tyaxis: {pad: 1.05, tickOptions: {formatString: \'%d\'}}\n\t}\n});\n});\n </script>\n</notextile>\n\n<div id="chart_0" style="width: 700px;"></div>'

    assert parser.typed_sentences[7][0][484:960] == expected_histogram_1
    assert parser.typed_sentences[7][0][966:1267] == expected_histogram_2


def test_chronicle_with_barplot():
    with open("source_samples/2025-01-02-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    expected_barplot = '\n\np. Soit, le "baromètre" habituel des personnalités qui font l\'actualité. Deux périodes : une période "ancienne" qui mène du 14 septembre 2004  au 2 décembre 2024  et une période "récente" qui va du 3 décembre 2024  au 1 janvier 2025  \n\np.  « Période ancienne » :  \n\n<notextile>\n <script class=\'code\'  type=\'text/javascript\'>\n  $(document).ready(function(){\n   var plot_palm = $.jqplot(\'palm_0_1\',\n    [[ [337, " Ayrault "],  [338, " Le Maire "],  [359, " Kerry "],  [366, " Abbas "],  [367, " Aubry "],  [367, " Darmanin "],  [383, " Maduro "],  [384, " Assange "],  [443, " Zelensky "],  [490, " Bayrou "],  [497, " Johnson "],  [520, " Netanyahu "],  [545, " Villepin "],  [551, " Erdogan "],  [715, " Clinton "],  [860, " Chirac "],  [871, " Bush "],  [899, " Valls "],  [922, " Royal "],  [958, " Merkel "],  [994, " Mélenchon "],  [1054, " Fillon "],  [1310, " Biden "],  [1507, " Le Pen "],  [1832, " Obama "],  [2066, " Poutine "],  [2070, " Hollande "],  [2515, " Trump "],  [2946, " Macron "],  [3346, " Sarkozy "],  ]],\n    {seriesColors: [\'#00749F\'],\n     seriesDefaults: {\n      renderer: $.jqplot.BarRenderer,\n      pointLabels: {show: true, location: \'e\', edgeTolerance: -15},\n      shadow: false,\n      rendererOptions: {barDirection: \'horizontal\'}},\n     axes: {\n      yaxis: {tickOptions: {fontSize: \'11pt\'}, renderer: $.jqplot.CategoryAxisRenderer}},\n     grid: {background: \'#fff\'}\n    });});\n </script>\n</notextile>\n\n<div id=\'palm_0_1\' style=\' width: 700px; height: 512px;\'></div>\n\n\n\np.  « Période récente » :  \n\n<notextile>\n <script class=\'code\'  type=\'text/javascript\'>\n  $(document).ready(function(){\n   var plot_palm = $.jqplot(\'palm_0_2\',\n    [[ [3, " Borne "],  [4, " Al-Joulani "],  [4, " Vallaud "],  [4, " Haenel "],  [4, " Ruggia "],  [4, " Paty "],  [4, " Sánchez "],  [5, " Wauquiez "],  [5, " Valls "],  [5, " Attal "],  [6, " Meloni "],  [6, " Tondelier "],  [6, " Tusk "],  [7, " Mélenchon "],  [7, " Darmanin "],  [7, " Scholz "],  [7, " Pelicot "],  [9, " Faure "],  [10, " Musk "],  [10, " Biden "],  [14, " Retailleau "],  [14, " Yoon "],  [15, " Zelensky "],  [18, " Le Pen "],  [24, " Barnier "],  [24, " Poutine "],  [24, " Al-Assad "],  [28, " Bayrou "],  [30, " Trump "],  [30, " Macron "],  ]],\n    {seriesColors: [\'#C7754C\'],\n     seriesDefaults: {\n      renderer: $.jqplot.BarRenderer,\n      pointLabels: {show: true, location: \'e\', edgeTolerance: -15},\n      shadow: false,\n      rendererOptions: {barDirection: \'horizontal\'}},\n     axes: {\n      yaxis: {tickOptions: {fontSize: \'11pt\'}, renderer: $.jqplot.CategoryAxisRenderer}},\n     grid: {background: \'#fff\'}\n    });});\n </script>\n</notextile>\n\n<div id=\'palm_0_2\' style=\' width: 700px; height: 512px;\'></div>\n\n\n\np.  Pour ceux qui commencent à se lasser de ce genre de palmarès, je me permets de renvoyer à ce site beaucoup plus "in" et dont la métrologie est à passer en revue de près : \n Un site qui propose une "métrologie" du degré de présence des personnages politiques dans les "blogs" et les "conversations" sur l\'internet : \n "http://presidentielle-2007.buzz-blog.com/IBBP-top5.php":http://presidentielle-2007.buzz-blog.com/IBBP-top5.php\r\n\r\r\n'

    if not parser.typed_sentences[15][0].find("table(marloblog)"):
        assert remove_random_color(parser.typed_sentences[15][0]) == remove_random_color(expected_barplot)


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


# def test_format_numbered_list():
#     assert False
#



def test_format_histogram():
    block = "--histo-- 2004 , 0 ; 2005 , 259 ; 2006 , 279 ; 2007 , 320 ; 2008 , 318 ; 2009 , 315 ; 2010 , 287 ; 2011 , 267 ; 2012 , 291 ; 2013 , 312 ; 2014 , 308 ; 2015 , 357 ; 2016 , 361 ; 2017 , 348 ; 2018 , 342 ; 2019 , 306 ; 2020 , 280 ; 2021 , 220 ; 2022 , 272 ; 2023 , 205 ; 2024 , 228 ; 2025 , 4 ;  --histo--  "
    count = 1

    expected = """<notextile>
 <script class="code" type="text/javascript">
$(document).ready(function(){ 
var s = [ 0 , 259 , 279 , 320 , 318 , 315 , 287 , 267 , 291 , 312 , 308 , 357 , 361 , 348 , 342 , 306 , 280 , 220 , 272 , 205 , 228 , 4 ];
var ticks = [' 2004 ',' 2005 ',' 2006 ',' 2007 ',' 2008 ',' 2009 ',' 2010 ',' 2011 ',' 2012 ',' 2013 ',' 2014 ',' 2015 ',' 2016 ',' 2017 ',' 2018 ',' 2019 ',' 2020 ',' 2021 ',' 2022 ',' 2023 ',' 2024 ',' 2025 '];
var plot = $.jqplot('chart_1', [s,],{
	seriesColors: ['#color'], 
	seriesDefaults:{renderer:$.jqplot.BarRenderer, rendererOptions:{fillToZero: true}},
	axes:{
		xaxis:{renderer: $.jqplot.CategoryAxisRenderer, ticks: ticks},
		yaxis: {pad: 1.05, tickOptions: {formatString: '%d'}}
	}
});
});
 </script>
</notextile>

<div id="chart_1" style="width: 700px;"></div>  """

    result = make_histogram(block, count)
    result = re.sub(r"seriesColors: \['#.*']", "seriesColors: ['#color']", result)

    assert result == expected


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
def test_make_html_quotes_do_nothing_if_no_quotes():
    text = "any thing"

    result = mrlw_chron_2_textile.make_html_quotes(text)

    assert result == text


def test_make_html_quotes_replace_double_quotes():
    text = "Zola écrivait : \" La vérité est en marche ; rien ne peut plus l'arrêter \" en 1897."
    expected = "Zola écrivait :  &#171;&#160;La vérité est en marche ; rien ne peut plus l'arrêter&#160;&#187;  en 1897."

    result = mrlw_chron_2_textile.make_html_quotes(text)

    assert result == expected


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

def test_generate_preamble_without_extra_js():
    title = "a title"
    excerpt = "an excerpt"
    extra_js = []
    date = datetime.datetime(2025, 1, 11, 19, 41, 52)

    result = mrlw_chron_2_textile.generate_preamble(title, excerpt, extra_js, date)

    expected = """title: "a title"
excerpt: "an excerpt"
---

h2. {{ page.title }}

p(publish_date). samedi 11 janvier 2025 19:41:52"""

    assert result == expected


def test_generate_preamble_with_extra_js():
    title = "a title"
    excerpt = "an excerpt"
    extra_js = ['an_extra', 'another_extra']
    date = datetime.datetime(2025, 1, 11, 19, 41, 52)

    result = mrlw_chron_2_textile.generate_preamble(title, excerpt, extra_js, date)

    expected = """title: "a title"
excerpt: "an excerpt"
extra_js: an_extra, another_extra 
---

h2. {{ page.title }}

p(publish_date). samedi 11 janvier 2025 19:41:52"""

    assert result == expected


# def test_write_textile():
#     assert False


def test_split_date_and_following():
    content = " 3/ 1/2025 23:7:2 \r\n\r\r\nMarlowe : "

    result = mrlw_chron_2_textile.split_date_and_following(content)

    assert len(result) == 2
    assert result[0] == " 3/ 1/2025 23:7:2 "
    assert result[1] == '\r\r\nMarlowe : '
