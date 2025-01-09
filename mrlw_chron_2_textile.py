""" Convert Marlowe chronicle to textile and enrich it with plugins for blog
Author Josquin Debaz
GPL 3
"""

import re
import datetime
import random
import libmrlwchrnck
from Referencer import Referencer
from sigmajs_generator import SigmaJsGenerator
from CityLocator import CityLocator


def format_sigles(block):
    """format for acronym list"""
    fragments = re.split(r"\s*<BR>\s*", block)
    block = re.sub('<br> <br>', '\n\n', fragments[0])
    block += "- " + "\n- ".join([re.sub(r"(.*)\s*:\s*(.*)",
                                        "\\1 := \\2 ",
                                        fragment).strip()
                                 for fragment in fragments[1:]])

    return block


def format_links(block):
    """format link for textile according to their target type
        including video and images"""
    block = re.sub("gspr.ehess.free.fr", "gspr-ehess.com", block)
    block = re.sub("92.243.27.161", "prosperologie.org", block)
    motif_images = re.compile(r"(http\S*.(jpg|png|gif|jpeg|JPG|img))")
    fragments = re.split(r'[^:](http\S*)', block)
    block = fragments[0]
    for i, fragment in enumerate(fragments[1:]):
        if i % 2 == 0:
            if motif_images.search(fragment):
                fragment = re.sub(r"(http\S*.(jpg|png|gif|jpeg|JPG|img))",
                                  "!\\1!", fragment)
            elif re.search("youtube.com/watch", fragment):
                fragment = re.sub(r'http\S?://www.youtube.com/watch?'
                                  r'\S*v=([^\s&]*)',
                                  "\n\n<iframe frameborder='0'  width='500' "
                                  " height='352' "
                                  "src='http://www.youtube.com/embed/\\1' "
                                  " allowfullscreen='allowfullscreen'>"
                                  "</iframe>\n\n",
                                  fragment)
            elif re.search("youtu.be", fragment):
                fragment = re.sub(r"http\S?://youtu.be/(.*)",
                                  "\n\n<iframe frameborder='0' width='500' "
                                  "height='352' "
                                  "src='http://www.youtube.com/embed/\\1'  "
                                  "allowfullscreen='allowfullscreen'>"
                                  "</iframe>\n\n",
                                  fragment)
            elif re.search(r"http[s]?://\S*\.pdf", fragment):
                fragment = re.sub(r"(http[s]?://\S*\.pdf)",
                                  '"\\1":\\1\n\n<object '
                                  'data="\\1#toolbar=0&navpanes=0&view=Fit" '
                                  'width="500" height="650" '
                                  'type="application/pdf"></object>',
                                  fragment)
            elif re.search(r"http[s]?://www.dailymotion.com/\S*", fragment):
                if re.search(r"http[s]?://www.dailymotion.com/embed/video/\S*",
                             fragment):
                    fragment = re.sub(r"(http[s]?://www.dailymotion.com/"
                                      r"embed/video/\S*)",
                                      '\n\n<iframe frameborder="0" '
                                      'width="500" height="352" '
                                      'src="\\1"></iframe>\n\n',
                                      fragment)
                elif re.search(r"http[s]?://www.dailymotion.com/video/.*",
                               fragment):
                    fragment = re.sub(r"(http[s]?://www.dailymotion.com/)"
                                      r"(video/[^_]*).*\s*",
                                      '\n\n<iframe frameborder="0" '
                                      'width="500" height="352" '
                                      'src="\\1embed/\\2\"></iframe>\n\n',
                                      fragment)
            elif re.search(r"http[s]?://vimeo.com/\d{1,}", fragment):
                fragment = re.sub(r"http[s]?://vimeo.com/(\d{1,})",
                                  '\n\n<iframe frameborder="0" '
                                  'width="500" height="352" '
                                  'src="https://player.vimeo.com/video/\\1\" '
                                  'webkitAllowFullScreen mozallowfullscreen '
                                  'allowFullScreen></iframe>\n\n',
                                  fragment)
            elif re.search(r"http[s]?://www.canal-u.tv/video/S*", fragment):
                fragment = re.sub(r"http[s]?://www.canal-u.tv/video/(\S*)"
                                  r"/(\S*)",
                                  '\n\n<iframe src="https://www.canal-u.tv/'
                                  'video/\\1/embed.1/\\2" width="550" '
                                  'height="306" frameborder="0" '
                                  'allowfullscreen scrolling="no"></iframe>',
                                  fragment)
            else:
                fragment = re.sub(r'http\S*://(\S*)',
                                  ' "http://\\1":http://\\1',
                                  fragment)
        block += fragment

    return block


def format_numbered_list(block):
    """format a numbered list for textile"""
    block = re.sub(r"<br>\s*<br> (\d)\. ", "\n\nh3. \\1. ", block)

    return block


def table_or_barplot(block, barplot_count):
    """Format data in table or graph"""
    if re.search(r"\n\nh3\.", block):
        select = "table"
    else:
        select = random.choice(["table", "barplot"])

    if select == 'table':
        return "table", format_table(block)

    try:
        return "barplot", format_barplot(block, barplot_count)
    except:
        return "table", format_table(block)


def format_table(block):
    """format a table for textile"""
    fragments = re.split('<BR>', block)
    block = fragments[0] + "\n\ntable(marloblog)."
    for fragment in fragments[1:-1]:
        if re.search('<br>', fragment):
            fragment = re.sub('<br>', '', fragment)
            fragment = "\n\np. %s\n\ntable(marloblog)." % fragment.strip()
        else:
            fragment = re.sub(r'(\d{1,})\s*-\s*(.*)\s*-\s*',
                              '\n| \\1 | \\2 |', fragment)
        block += fragment
    block += fragments[-1]

    return block


def format_barplot(block, barplot_count):
    """create script content for barplot"""
    new = ""
    barplot_sub_count = 0
    colors = ['#fba919', '#00749F', '#73C774', '#C7754C']
    for item in re.split("<br> <br>", block):
        if re.search(r"<BR>\d{1,}", item):
            fragments = re.split("<BR>", item)
            reverse_fragments = []
            for i, fragment in enumerate(fragments):
                if i == 0:
                    item = fragment
                elif re.search(r'\d{1,}\s{1,}- ', fragment):
                    if i == 1:
                        barplot_sub_count += 1
                        item += ("\n\n<notextile>\n <script class='code' "
                                 " type='text/javascript'>\n  $(document).ready("
                                 "function(){\n   var plot_palm = $.jqplot("
                                 "'palm_%s_%s',\n    [[ ") % \
                                (barplot_count, barplot_sub_count)
                    fragment = re.sub(r'(\d{1,})\s{1,}- (.*) - ',
                                      '[\\1, "\\2"], ',
                                      fragment)
                    reverse_fragments.append(fragment)
                    fragment = ""
                elif i == len(fragments) - 1:
                    fragment = "".join(reversed(reverse_fragments))
                    color = colors.pop(random.randint(0, len(colors) - 1))
                    fragment += ("]],\n    {seriesColors: ['%s'],"
                                 "\n     seriesDefaults: {\n      renderer: "
                                 "$.jqplot.BarRenderer,\n      pointLabels:"
                                 " {show: true, location: 'e', edgeTolerance: "
                                 "-15},\n      shadow: false,\n      "
                                 "rendererOptions: {"
                                 "barDirection: 'horizontal'}},\n     axes: {"
                                 "\n      yaxis: {tickOptions: {fontSize: "
                                 "'11pt'}, renderer: "
                                 "$.jqplot.CategoryAxisRenderer}},\n     "
                                 "grid: {background: '#fff'}\n    });});\n"
                                 " </script>\n</notextile>\n\n"
                                 "<div id='palm_%s_%s' "
                                 "style=' width: 700px; height: %dpx;'></div>"
                                 "\n\n") % (color,
                                            barplot_count,
                                            barplot_sub_count,
                                            len(fragments) * 16 / 100 * 100)
                item += fragment
        else:
            item = "\n\np. " + item
        new += item

    return new


def format_histo(block, num):
    """format an histogram for js"""
    core = re.split("--histo--", block)
    new = ('<notextile>\n <script class="code" type="text/javascript">\n'
           '$(document).ready(function(){ \n')
    serie = []
    ticks = []
    for fragment in re.split(";", core[1])[:-1]:
        tick, value = re.split(",", fragment)
        ticks.append(tick)
        serie.append(value)
    new += "var s = [%s];\n" % (",".join(serie))
    new += "var ticks = ['%s'];\n" % ("','".join(ticks))
    new += "var plot = $.jqplot('chart_%d', [s,]," % num
    new += "{\n\tseriesColors: ['%s'], " % \
           random.choice(['#fba919', '#00749F', '#73C774', '#C7754C'])
    new += ("\n\tseriesDefaults:{renderer:$.jqplot.BarRenderer, "
            "rendererOptions:{fillToZero: true}},\n\taxes:{\n"
            "\t\txaxis:{renderer: $.jqplot.CategoryAxisRenderer, "
            "ticks: ticks},\n\t\tyaxis: {pad: 1.05, "
            "tickOptions: {formatString: '%d'}}\n\t}\n});\n});\n"
            " </script>\n</notextile>\n\n")
    new += '<div id="chart_%d" style="width: 700px;"></div>' % num

    return core[0] + new + core[2]


def format_graphe(block, graphe_count):
    """format a graphe for js"""
    fragments = re.split("--graphe--", block)
    block = fragments[0]
    block += ('\n\n<notextile>\n  <div id="graph-container_%d" '
              'class="graph-container"> </div>\n') % graphe_count
    formed = SigmaJsGenerator(fragments[1], graphe_count)
    block += formed.graph
    block += "</notextile>\n\n"
    block += fragments[2]

    return block


def format_cloud(block, cloud_count):
    """format a cloud word in js"""
    fragments = re.split("--nuage--", block)
    block = fragments[0] + ('\n\n<notextile>\n <script '
                            'type="text/javascript">\n '
                            ' var word_array%d = [ ') % cloud_count
    block += "".join([re.sub(r"\s*(.*)\s{1,},\s*(.*)\s{1,}",
                             '\t\t{text: "\\1", weight: \\2, color: "#"+("000000"'
                             '+Math.random().toString(16).slice(2, '
                             '8).toUpperCase()).slice(-6)},\n ',
                             item)
                      for item in re.split(";", fragments[1])])
    block += (' ];\n  $(function() { $("#cloud_%d").jQCloud(word_array%d);'
              '});\n </script>\n</notextile>\n\n<div id="cloud_%d" '
              'style="width: 700px; height: 350px;">'
              '</div>\n\n') % (cloud_count, cloud_count, cloud_count)
    block += fragments[2]

    return block


def format_map(block):
    """format map of towns"""
    city_locator = CityLocator()

    new, core, end = re.split(r"\s*--mapcapeurop--\s*", block)

    new += ('\n\n<notextile>\n\n<div id="map">\n<script class="code" '
            'type="text/javascript">\nvar initMap = function(){\n\t'
            'var provider = new com.modestmaps.TemplatedLayer('
            '"http://tile.openstreetmap.org/{Z}/{X}/{Y}.png");\n\t'
            'var map = new com.modestmaps.Map("map", provider);\n\t'
            'var canvas = document.createElement("canvas");\n\t'
            'canvas.style.position = "absolute";\n\tcanvas.style.left = '
            '"0";\n\tcanvas.style.top = "0";\n\tcanvas.width = '
            'map.dimensions.x;\n\tcanvas.height = map.dimensions.y;\n\t'
            'map.parent.appendChild(canvas);\n')

    cities = dict(re.split(",", line)
                 for line in re.split(r"\s*;\s*", core)[:-1])

    for city in cities:
        latitude, longitude = city_locator.get_coordinates(city)

        new += "\tvar %s = new com.modestmaps.Location(%s,%s);\n" % \
               (re.sub(r'[\s\-éè]', '_', city), latitude, longitude)

    new += "\tvar locations = [%s];\n" % \
           ", ".join([re.sub(r'[\s\-éè]', '_', town) for town in cities.keys()])
    new += "\tvar values = [%s];\n" % ", ".join(cities.values())
    new += ("\tvar max = Math.max.apply(Math, values);\n\t"
            "map.setExtent(locations);\n\tmap.zoomOut();\n\t"
            "function redraw(){\n\t\tvar ctx = canvas.getContext('2d');\n"
            "\t\tctx.clearRect(0,0,canvas.width,canvas.height);\n"
            "\t\tfor (var i = 0; i < locations.length; i++){\n"
            "\t\t\tctx.beginPath();\n\t\t\tvar p = "
            "map.locationPoint(locations[i]);\n\t\t\tctx.fillStyle = '%s';\n"
            "\t\t\tctx.globalAlpha = 0.6;\n"
            "\t\t\tradius = values[i] * 15 / max + 5;\n"
            "\t\t\tctx.arc(p.x,p.y,radius,0,2 * Math.PI, false);\n"
            "\t\t\tctx.fill();\n\t\t\tctx.stroke();\n\t\t}\n\t}\n"
            "\tmap.addCallback('drawn', redraw);\n"
            "\tmap.addCallback('resized', function(){\n"
            "\t\tcanvas.width = map.dimensions.x;\n"
            "\t\tcanvas.height = map.dimensions.y;\n\t\tredraw();\n"
            "\t});\n\tredraw();\n}\n"
            "</script>\n</div>\n\n</notextile>\n\n") % \
           random.choice(['#fba919', '#00749F', '#73C774', '#C7754C',
                          '#c82124'])
    new += 'p(reference). "Fond et positions © les contributeurs ' \
           'd\'OpenStreetMap":https://www.openstreetmap.org/copyright\n\n'

    return new + end


def format_quotes(block):
    """replace quotes by html"""
    if not len(re.findall('"', block)) % 2:
        while re.search('"', block):
            block = re.sub(r'"', " &#171;&#160;", block, 1)
            block = re.sub(r'"', "&#160;&#187; ", block, 1)
    #block = re.sub("&#8220;\s*"," &#171;&#160;",block)
    #block = re.sub("\u201c\s*"," &#171;&#160;;", block)
    #block = re.sub("\s*\xab"," &#171;&#160;", block)
    #block = re.sub("\s*&#8221;","&#160;&#187; ", block)
    #block = re.sub("\s*\u201d","&#160;&#187; ", block)
    #block = re.sub("\s*\xbb","&#160;&#187; ", block)

    return block


def protect_quotes(block):
    """quotes to html or echap for preambule"""
    if not len(re.findall('"', block)) % 2:
        block = format_quotes(block)
    else:
        block = re.sub('"*', '\\"', block)

    return block


def format_date(block):
    """better date forms"""
    # locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    dates = re.findall(r"[\s:](\d{1,2}/\s*\d{1,2}/\d{4})[^/]", block)
    for date in list(set(dates)):
        day, month, year = re.split(r"/", date)
        new = datetime.date(int(year), int(month), int(day))
        block = re.sub(date, new.strftime("%-d %B %Y"), block)

    return block


def format_marks(block):
    """add, delete and simplify marks for textile"""
    block = format_date(block)
    #block = format_quotes(block)
    block = re.sub(r"\s+&#160;", "&#160;", block)
    block = re.sub(r"&#160;\s+", "&#160;", block)
    block = re.sub("<br> <br> - ", "\n\n- ", block)
    block = re.sub(r"<br> <br>(\S*)$", "\n\np.\\1", block)
    block = re.sub("(<br> <br>)", "\n\np.", block)
    block = re.sub("(<br>|<BR>)", "\n", block)
    block = re.sub(r"\s+([).,…])", "\\1", block)
    block = re.sub(r"(\()\s+", "\\1", block)
    block = re.sub(r"\s+'\s+", "'", block)
    block = re.sub(r"\s-(\w.*\w)-([\s&])", " - \\1 -\\2", block)
    block = re.sub(r"(bq\.)([^ ])", "\\1 \\2", block)

    return block


def split_date_and_following(content):
    """get the timestamp and return the following text"""

    date_time, following = re.split("\r\n", content, 1)
    day, month, year, hour, minutes, secondes = \
        re.search(r"(\d*)/\s*(\d*)/(\d{4})\s*(\d*):(\d*):(\d*).*$",
                  date_time).group(1, 2, 3, 4, 5, 6)
    date = datetime.datetime.combine(
        datetime.date(int(year), int(month), int(day)),
        datetime.time(int(hour), int(minutes), int(secondes))
    )

    return date, following


class ChroniqueParser:
    """Analyse and parse chronicle content"""

    def __init__(self, texte):
        self.date = ""
        self.title = ""
        self.excerpt = ""
        self.chronique = "---\nlayout: post\n"
        self.typed_sentences = []
        self.extra_js = []
        self.logs = ""

        origin = texte.decode("cp1252")
        self.date, following = split_date_and_following(origin)

        self.type_sentences(re.split(r"Marlowe\s*:\s*", following)[1:])
        self.prepare_blocks()
        self.generate_preambule()
        self.generate_blocks()
        # self.write_textile()
        self.logs = "%s\n" % (self.date.strftime("%A %-d %B %Y %H:%M:%S"))
        self.logs += "chronicle text size: %d chars\n" % (len(following))
        self.logs += "found %d blocks\n" % (len(self.typed_sentences))
        self.logs += "%s\n" % self.title
        #print(self.logs)

    def type_sentences(self, sentences):
        """Attribute a type to each sentences : title, par, citation, sigles,
        subtitle"""
        title, intro = re.split(r"\s*<br>", sentences[0], 1)
        self.typed_sentences = [[title, "title"]]
        intro = re.split(r"(\r\n){2}", intro)
        self.typed_sentences += [[sentence, "par"]
                                 for sentence in intro[0:-3]
                                 if sentence != '\r\n']
        self.typed_sentences.append([intro[-3], "citation"])
        self.typed_sentences.append([intro[-1], "par"])
        sigles = 0
        for i, sentence in enumerate(sentences[1:]):
            if i % 2:
                if sigles < 2:
                    self.typed_sentences.append([sentence, "par"])
                    if sigles > 0:
                        sigles += 1
                else:
                    self.typed_sentences.append([sentence, "sigles"])
                    sigles = 0
            elif any([i == 0,
                      re.search(r"personnalit.s du jour", sentence),
                      re.search(r"quels sont les nouveaux sigles", sentence),
                      re.search(r"la n.crologie du jour", sentence),
                      re.search(r"on a fini", sentence),
                      re.search(r"g.opolit", sentence),
                      re.search(r"je passe . la suite", sentence),
                      re.search(r"palmar.s.*personnalit.s", sentence),
                      re.search("je termine avec un rapport complet",
                                sentence)]):
                self.typed_sentences.append([sentence, "subtitle"])
                if re.search("quels sont les nouveaux sigles", sentence):
                    sigles = 1

    def prepare_blocks(self):
        """textile enriching each block"""
        barplot_count = 0
        graphe_count = 0
        cloud_count = 0
        histo_count = 0
        self.url_referencer = Referencer(self.date.strftime("%Y-%m-%d"))

        for i, sentence in enumerate(self.typed_sentences):
            if sentence[1] == 'title':
                title = self.typed_sentences[0][0]
                if re.search(r"\r\n", title):
                    title, self.excerpt = re.split(r"[\r\n]+", title)
                self.title = title
            elif sentence[1] == "sigles":
                block = sentence[0]
                parts = re.split(" <br><br> ", block, 1)
                block = format_sigles(parts[0])
                if len(parts) == 2:
                    block += self.generate_citations(parts[1])
                block = format_marks(block)
                self.typed_sentences[i][0] = block
            elif sentence[1] == "citation":
                parts = re.split("\r\n", sentence[0])
                if len(parts) == 3:
                    citation, source = parts[1:]
                    #citation, source = re.split("\r\n", sentence[0])[1:]
                    self.typed_sentences[i][0] = \
                        "\n\nbq. %s\n\np(source). %s\n\n" % (citation, source)
            elif sentence[1] == "par":
                block = sentence[0]

                if re.search(r"<br>\s*<br> 1\. ", block):
                    block = format_numbered_list(block)

                block = self.generate_citations(block)

                if re.search(r"http\S?://\S*", block):
                    block = format_links(block)

                if re.search(r'\d*  -  ', block):
                    choice, block = table_or_barplot(block, barplot_count)
                    if choice == "barplot":
                        barplot_count += 1
                        if "barplot" not in self.extra_js:
                            self.extra_js.append("barplot")

                if re.search("--histo--", block):
                    if "barplot" not in self.extra_js:
                        self.extra_js.append("barplot")
                    block = format_histo(block, histo_count)
                    histo_count += 1

                if re.search("--graphe--", block):
                    graphe_count += 1
                    if graphe_count < 2:
                        self.extra_js.append("sigma")
                    block = format_graphe(block, graphe_count)

                if re.search("--nuage--", block):
                    cloud_count += 1
                    if "jqcloud" not in self.extra_js:
                        self.extra_js.append("jqcloud")
                    block = format_cloud(block, cloud_count)

                if re.search("interview-imaginaire", block):
                    block = re.sub("<interview-imaginaire>",
                                   '<div id="interview-imaginaire">\n',
                                   block)
                    block = re.sub("</interview-imaginaire>",
                                   '</div>',
                                   block)
                    block = re.sub("<br><br>", "\n\np. ", block)

                if re.search("--mapcapeurop--", block):
                    self.extra_js.append("maps")
                    block = format_map(block)

                self.typed_sentences[i][0] = format_marks(block)

    def generate_blocks(self):
        """add blocks to chronicle"""
        for sentence, type_sentence in self.typed_sentences:
            if type_sentence == "title":
                if self.excerpt:
                    self.chronique += "\n\np. %s" % self.excerpt
            elif type_sentence == "subtitle":
                self.chronique += "\n\nh2. " + sentence.strip().capitalize()
            elif type_sentence == "par":
                if sentence:
                    sentence = "\n\np. " + sentence.strip()
                    sentence = re.sub(r"\np\.\s*bq\. ", "\nbq. ", sentence)
                    sentence = re.sub(r"\np\. p\. ", "\np. ", sentence)
                    sentence = re.sub(r"\np\.([^ ])", "\np. \\1", sentence)
                    sentence = re.sub(r"\np\.\s*(h\d\.)", "\n\\1 ", sentence)
                    sentence = re.sub(r"(\n\nh\d.* : )",
                                      "\\1\n\np.", sentence)
                    self.chronique += sentence
            else:
                self.chronique += "\n\n" + sentence.strip()

    def generate_citations(self, block):
        """split and find citations"""
        #how many quotes ?
        occurences = len(re.findall("<br> Auteur :", block))
        if occurences > 1:
            decoupe = re.split("<br><br>|<br> <br>|<BR><BR>|<BR> <BR>", block)
            block = "".join([self.format_citation(fragment)
                             for fragment in decoupe[:-1]])
            if re.search("<br> Auteur ", decoupe[-1]):
                block += self.format_citation(decoupe[-1])
            elif not re.match(r"^\s*<br>\s*$", decoupe[-1]) \
                    and not re.match(r"^\s*$", decoupe[-1]):
                block += "\n\np. %s" % decoupe[-1]
        elif occurences == 1:
            block = self.format_citation(block)

        return block

    def format_citation(self, citation):
        """format citation for textile"""
        #print(citation)
        fragments = re.split("<br> Auteur ", citation)
        if len(fragments) == 1:
            if not re.search(r"^\s*$", citation):
                citation = "\n\np. %s" % citation.strip()
        elif len(fragments) == 2:
            table = False

            #check for url in database
            try:
                aut, date, tit = re.search(r":\s*(.*)\s*Date :\s*(.*)\s* "
                                           r"Titre :(.*)",
                                           fragments[1]).group(1, 2, 3)
                #when table
                if re.search(r'\d*  -  ', tit):
                    tit, table = re.split("<br> <br>", tit)

                un_br = re.compile('<br>', re.IGNORECASE)
                tit = un_br.sub('', tit)
                url = self.url_referencer.get_url(aut.strip(),
                                                  date.strip(),
                                                  tit.strip())
                #for the test comment above and uncomment HERE
                #                url = False
                if url:
                    reference = ('\n\np(reference). &#171;&#160;'
                                 '%s&#160;&#187;, "%s":%s, %s') % \
                                (tit.strip(), aut.strip(), url, date.strip())
                else:
                    reference = ('\n\np(reference). &#171;&#160;'
                                 '%s&#160;&#187;, %s, %s') % \
                                (tit.strip(), aut.strip(), date.strip())
            except AttributeError:
                aut, date = re.search(r":\s*(.*)\s*Date :\s*(.*)\s*",
                                      fragments[1]).group(1, 2)
                reference = '\n\np(reference). %s, %s' % \
                            (aut.strip(), date.strip())

            multi = re.split("(<br>|<BR><BR>)", fragments[0])
            if len(multi) == 1:
                fragments[0] = re.sub("^[, ]*<BR>", " ", fragments[0])
                citation = "\n\nbq. %s %s" % (fragments[0], reference)
            elif len(multi) == 2:
                citation = "\n\np. %s\n\nbq. %s %s" % (multi[0].strip(),
                                                       multi[1].strip(),
                                                       reference)
            else:
                citation = "\n\np.".join(multi[:-1]) \
                           + "\n\nbq. %s %s\n\n" % (multi[-1].strip(), reference)

            if table:
                citation += table

        elif len(fragments) > 2:
            for i, fragment in enumerate(fragments):
                decoupe = re.split("<BR>|<br>", fragment)
                if i == 0:
                    if len(decoupe) == 2:
                        citation = decoupe[0] + "\n\nbq. %s" % decoupe[1]
                    else:
                        citation = decoupe[0] + "\n\n"
                else:
                    aut, date, tit = re.search(r":\s*(.*)\s*Date :\s*(.*)\s* "
                                               "Titre :(.*)",
                                               decoupe[0]).group(1, 2, 3)
                    citation += ('\n\np(reference). &#171;&#160;'
                                 '%s&#160;&#187;, %s, %s') % \
                                (tit.strip(), aut.strip(), date.strip())
                if i and i < len(fragments) - 1:
                    if len(decoupe) == 3:
                        citation += "\n\np. %s\n\nbq. %s" % \
                                    (decoupe[1], decoupe[2])
                    elif len(decoupe) == 1:
                        citation = fragment
                    else:
                        citation += "\n\nbq. %s" % decoupe[1]

        citation = re.sub(r"^\s*(.*:)\s+p\.<br>", "\n\np. \\1", citation)
        citation = re.sub(r"^\s*<br>", "\n\np. ", citation)
        citation = re.sub(r"bq\.\s*<BR>\s*", "bq. ", citation)

        return citation

    def generate_preambule(self):
        """the preambule of the jeckyll file"""
        self.chronique += 'title: "%s"\nexcerpt: "%s"\n' % \
                          (protect_quotes(self.title),
                           protect_quotes(self.excerpt))
        if self.extra_js:
            self.chronique += "extra_js: %s \n" % (", ".join(self.extra_js))
        self.chronique += "---\n\n"
        # locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        self.chronique += "h2. {{ page.title }}\n\np(publish_date). %s" % \
                          (self.date.strftime("%A %-d %B %Y %H:%M:%S"))

    def write_textile(self):
        """write chronicle for jekyll"""
        with open("/home/josquin/marloblog/_posts/chroniques/"
                  "%s-chronique_mrlw.textile" % self.date.strftime("%Y-%m-%d"),
                  'w') as handle:
            handle.write(self.chronique)


if __name__ == '__main__':
    chronicle = libmrlwchrnck.get_chronicle()
    ChroniqueParser(chronicle)
