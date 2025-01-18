import random
import re


def introducing_barplot(barplot_name):
    return ("\n\n<notextile>\n <script class='code'  type='text/javascript'>\n  $(document).ready(function(){\n"
            f"   var plot_palm = $.jqplot('{barplot_name}',\n    [[ ")


def closing_barplot(barplot_id, color, values, height):
    result = "".join(values)
    result += ("]],\n    {"
               f"seriesColors: ['{color}'],\n"
               "     seriesDefaults: {\n      renderer: $.jqplot.BarRenderer,\n"
               "      pointLabels: {show: true, location: 'e', edgeTolerance: -15},\n      shadow: false,\n"
               "      rendererOptions: {barDirection: 'horizontal'}},\n"
               "     axes: {\n      yaxis: {tickOptions: {fontSize: '11pt'}, renderer: $.jqplot.CategoryAxisRenderer}},\n"
               "     grid: {background: '#fff'}\n    });});\n </script>\n"
               "</notextile>\n\n"
               f"<div id='{barplot_id}' style=' width: 700px; height: {height}px;'></div>\n\n")

    return result


def format_values(raw_values):
    max_to_min_values = [
        re.sub(r'(\d+)\s+- (.*) - ', '[\\1, "\\2"], ', value)
        for value in raw_values[1:-1]
    ]

    return reversed(max_to_min_values)


class BarplotDrawer:
    """Draw a js barplot from values"""

    def __init__(self):
        self.plot = ""
        self.colors = ['#fba919', '#00749F', '#73C774', '#C7754C']

    def draw(self, barplot_id, value_block, color=None):
        raw_values = re.split("<BR>", value_block)

        result = raw_values[0] + introducing_barplot(barplot_id)

        if color is None:
            color = self.colors.pop(random.randint(0, len(self.colors) - 1))

        height = "%d" % (len(raw_values) * 16 / 100 * 100)
        min_to_max_values = format_values(raw_values)

        self.plot = result + closing_barplot(barplot_id, color, min_to_max_values, height)
