import random
import re


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

    result =  f"{parts[0]}\n\ntable(marloblog)."

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
