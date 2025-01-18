import random
import re


def introducing_barplot(barplot_name):
    return ("\n\n<notextile>\n <script class='code'  type='text/javascript'>\n  $(document).ready(function(){\n"
            f"   var plot_palm = $.jqplot('{barplot_name}',\n    [[ ")


def closing_barplot(barplot_id, color, values, height):
    result = "".join(values)
    result += ("]],\n    {"
               f"seriesColors: ['{color}'],\n"
               "     seriesDefaults: {\n      renderer: $.jqplot.BarRenderer,\n      pointLabels: {show: true, location: 'e', edgeTolerance: -15},\n      shadow: false,\n      rendererOptions: {barDirection: 'horizontal'}},\n     axes: {\n      yaxis: {tickOptions: {fontSize: '11pt'}, renderer: $.jqplot.CategoryAxisRenderer}},\n     grid: {background: '#fff'}\n    });});\n </script>\n</notextile>\n\n"
               f"<div id='{barplot_id}' style=' width: 700px; height: {height}px;'></div>\n\n")

    return result


class BarplotDrawer:
    def __init__(self, barplot_name, barplot_sub_count, item):
        colors = ['#fba919', '#00749F', '#73C774', '#C7754C']

        raw_values = re.split("<BR>", item)
        reversed_values = []

        result = ""

        for i, value in enumerate(raw_values):
            if i == 0:
                result = value
            elif re.search(r'\d+\s+- ', value):
                if i == 1:
                    barplot_sub_count += 1
                    result += introducing_barplot(f"{barplot_name}{barplot_sub_count}")
                reversed_value = re.sub(r'(\d+)\s+- (.*) - ', '[\\1, "\\2"], ', value)
                reversed_values.append(reversed_value)
            elif i == len(raw_values) - 1:
                barplot_id = f"{barplot_name}{barplot_sub_count}"
                color = colors.pop(random.randint(0, len(colors) - 1))
                values = reversed(reversed_values)
                height = "%d" % (len(raw_values) * 16 / 100 * 100)
                value = closing_barplot(barplot_id, color, values, height)

                result += value

        self.barplot_sub_count = barplot_sub_count
        self.result = result