import random
import re

from js.BarplotDrawer import BarplotDrawer
from sigmajs_generator import SigmaJsGenerator


def format_links(block):
    """format link for textile according to their target type
        including video and images"""

    substitutions = {
        r"(https?\S*.(jpg|png|gif|jpeg|JPG|img))":
            " !\\1!",
        r'https?://www.youtube.com/watch?\S*v=([^\s&]*)':
            "\n\n<iframe frameborder='0' width='500' height='352' src='http://www.youtube.com/embed/\\1' allowfullscreen='allowfullscreen'></iframe>\n\n",
        r"https?://youtu.be/(.*)":
            "\n\n<iframe frameborder='0' width='500' height='352' src='http://www.youtube.com/embed/\\1' allowfullscreen='allowfullscreen'></iframe>\n\n",
        r"(https?://\S*\.pdf)":
            '"\\1":\\1\n\n<object data="\\1#toolbar=0&navpanes=0&view=Fit" width="500" height="650" type="application/pdf"></object>',
        r"(https?://www.dailymotion.com/embed/video/\S*)":
            '\n\n<iframe frameborder="0" width="500" height="352" src="\\1"></iframe>\n\n',
        r"(https?://www.dailymotion.com/)(video/[^_]*).*\s*":
            '\n\n<iframe frameborder="0" width="500" height="352" src="\\1embed/\\2\"></iframe>\n\n',
        r"https?://vimeo.com/(\d+)":
            '\n\n<iframe frameborder="0" width="500" height="352" src="https://player.vimeo.com/video/\\1\" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>\n\n',
        r"https?://www.canal-u.tv/video/(\S*)/(\S*)":
            '\n\n<iframe src="https://www.canal-u.tv/video/\\1/embed.1/\\2" width="550" height="306" frameborder="0" allowfullscreen scrolling="no"></iframe>'
    }

    fragments = re.split(r'[^:](http\S*)', block)
    block = fragments[0]

    for i, fragment in enumerate(fragments[1:]):
        if i % 2 != 0:
            pass

        if not re.search("|".join(substitutions.keys()), fragment):
            fragment = re.sub(r'(https?://\S*)', ' "\\1":\\1', fragment)
        else:
            for pattern, replacement in substitutions.items():
                fragment = re.sub(pattern, replacement, fragment)

        block += fragment

    return block


def format_table(block):
    """format a table for textile"""

    parts = block.split('<BR>')

    result = f"{parts[0]}\n\ntable(marloblog)."

    for value in parts[1:-1]:
        if re.search('<br>', value):
            table_separator = re.sub('<br>', '', value)
            table_separator = table_separator.strip()
            line = f"\n\np. {table_separator}\n\ntable(marloblog)."
        else:
            line = re.sub(r'(\d+)\s*-\s*(.*)\s*-\s*',
                          '\n| \\1 | \\2 |', value)
        result += line

    result += parts[-1]

    return result


def format_barplot(block, barplot_count):
    """create script content for barplot"""

    result = ""
    barplot_sub_count = 0
    barplot_id_prefix = f"palm_{barplot_count}_"
    barplot_drawer = BarplotDrawer()

    for part in block.split("<br> <br>"):
        if not re.search(r"<BR>\d+", part):
            transformed_part = f"\n\np. {part}"
        else:
            barplot_sub_count += 1
            barplot_id = f"{barplot_id_prefix}{barplot_sub_count}"
            barplot_drawer.draw(barplot_id, part)
            transformed_part = barplot_drawer.plot

        result += transformed_part

    return result


def table_or_barplot(block, barplot_count):
    """Format data in table or graph"""

    if re.search(r"\n\nh3\.", block):
        select = "table"
    else:
        select = random.choice(["table", "barplot"])

    if select == 'table':
        return "table", format_table(block)

    try:
        test = format_barplot(block, barplot_count)
        return "barplot", test
    except:
        return "table", format_table(block)


def format_graph(block, graphe_count):
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
