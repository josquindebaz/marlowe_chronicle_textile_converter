""" Convert Marlowe chronicle to textile and enrich it with plugins for blog
Author Josquin Debaz
GPL 3
"""

import re

from Referencer import Referencer
from js.CloudDrawer import CloudDrawer
from js.HistogramDrawer import HistogramDrawer
from js.MapDrawer import MapDrawer
from textile_utils import format_links, table_or_barplot, format_graph
from utils import get_introduction_date, dates_to_long_dates, datetime_to_long_datetime, harmonize_domain_url


def format_sigles(block):
    """format for acronym list"""
    fragments = re.split(r"\s*<BR>\s*", block)
    block = re.sub('<br> <br>', '\n\n', fragments[0])
    block += "- " + "\n- ".join([re.sub(r"(.*)\s*:\s*(.*)",
                                        "\\1 := \\2 ",
                                        fragment).strip()
                                 for fragment in fragments[1:]])

    return block


def format_numbered_list(block):
    """format a numbered list for textile"""
    block = re.sub(r"<br>\s*<br> (\d)\. ", "\n\nh3. \\1. ", block)

    return block


def make_histogram(block, plot_id):
    """Make a histogram in js"""

    division = block.split("--histo--")
    drawer = HistogramDrawer(division[1], plot_id)

    return division[0] + drawer.histogram + division[2]


def format_map(block):
    """format map of towns"""

    start, core, end = re.split(r"\s*--mapcapeurop--\s*", block)

    drawer = MapDrawer(core)
    new = drawer.map

    return start + new + end


def make_html_quotes(text):
    """replace quotes by html quotes"""

    if text.find('"') == -1:
        return text

    while re.search('"', text):
        text = re.sub(r'"\s*', " &#171;&#160;", text, 1)
        text = re.sub(r'\s*"', "&#160;&#187; ", text, 1)

    return text


def format_marks(block):
    """add, delete and simplify marks for textile"""
    block = dates_to_long_dates(block)
    # block = format_quotes(block)
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

    return re.split("\r\n", content, 1)


def generate_preamble(title, excerpt, extra_js, date):
    """the preamble of the Jekyll file"""

    result = f'title: "{make_html_quotes(title)}"\nexcerpt: "{make_html_quotes(excerpt)}"\n'
    if extra_js:
        result += f'extra_js: {", ".join(extra_js)} \n'

    result += ("---\n\n"
               "h2. {{ page.title }}\n\n"
               f"p(publish_date). {datetime_to_long_datetime(date)}")

    return result


class ChroniqueParser:
    """Analyse and parse chronicle content"""

    def __init__(self, texte, database):
        self.excerpt = ""
        self.chronique = "---\nlayout: post\n"
        self.typed_sentences = []
        self.extra_js = []
        self.logs = ""

        origin = texte.decode("cp1252")
        introduction_date, following = split_date_and_following(origin)
        date = get_introduction_date(introduction_date)
        self.url_referencer = Referencer(database, date.strftime("%Y-%m-%d"))

        self.add_log(date.strftime("%A %-d %B %Y %H:%M:%S"))
        self.add_log(f"chronicle text size: {len(following)} chars")

        self.type_sentences(re.split(r"Marlowe\s*:\s*", following)[1:])
        self.add_log(f"found {len(self.typed_sentences)} blocks")

        title = self.prepare_blocks()
        self.add_log(title)

        self.chronique += generate_preamble(title, self.excerpt, self.extra_js, date)
        self.generate_blocks()

    def add_log(self, text):
        self.logs += f"{text}\n"

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

        title = ""
        barplot_count = 0
        graphe_count = 0
        cloud_count = 0
        histo_count = 0

        for i, sentence in enumerate(self.typed_sentences):
            if sentence[1] == 'title':
                title = self.typed_sentences[0][0]
                if re.search(r"\r\n", title):
                    title, self.excerpt = re.split(r"[\r\n]+", title)
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
                    # citation, source = re.split("\r\n", sentence[0])[1:]
                    self.typed_sentences[i][0] = \
                        "\n\nbq. %s\n\np(source). %s\n\n" % (citation, source)
            elif sentence[1] == "par":
                block = sentence[0]

                if re.search(r"<br>\s*<br> 1\. ", block):
                    block = format_numbered_list(block)

                block = self.generate_citations(block)

                if re.search(r"http\S?://\S*", block):
                    block = harmonize_domain_url(block)

                    block = format_links(block)

                if re.search(r'\d*\s{2}-\s{2}', block):
                    choice, block = table_or_barplot(block, barplot_count)
                    if choice == "barplot":
                        barplot_count += 1
                        if "barplot" not in self.extra_js:
                            self.extra_js.append("barplot")

                if re.search("--histo--", block):
                    if "barplot" not in self.extra_js:
                        self.extra_js.append("barplot")
                    block = make_histogram(block, histo_count)
                    histo_count += 1

                if re.search("--graphe--", block):
                    graphe_count += 1
                    if graphe_count < 2:
                        self.extra_js.append("sigma")
                    block = format_graph(block, graphe_count)

                if re.search("--nuage--", block):
                    cloud_count += 1
                    if "jqcloud" not in self.extra_js:
                        self.extra_js.append("jqcloud")
                    cloud_drawer = CloudDrawer(block, cloud_count)
                    block = cloud_drawer.cloud

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

        return title

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
        # how many quotes ?
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
        # print(citation)
        fragments = re.split("<br> Auteur ", citation)
        if len(fragments) == 1:
            if not re.search(r"^\s*$", citation):
                citation = "\n\np. %s" % citation.strip()
        elif len(fragments) == 2:
            table = False

            # check for url in database
            try:
                aut, date, tit = re.search(r":\s*(.*)\s*Date :\s*(.*)\s* "
                                           r"Titre :(.*)",
                                           fragments[1]).group(1, 2, 3)
                # when table
                if re.search(r'\d*  -  ', tit):
                    tit, table = re.split("<br> <br>", tit)

                un_br = re.compile('<br>', re.IGNORECASE)
                tit = un_br.sub('', tit)
                url = self.url_referencer.get_url(aut.strip(),
                                                  date.strip(),
                                                  tit.strip())
                # for the test comment above and uncomment HERE
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
