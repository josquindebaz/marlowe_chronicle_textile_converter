import random
import re

class Histogram:
    """Make a histogram in js"""

    def __init__(self, values, plot_id = None):
        series = []
        ticks = []
        random_color = random.choice(['#fba919', '#00749F', '#73C774', '#C7754C'])

        for fragment in re.split(";", values)[:-1]:
            tick, value = re.split(",", fragment)
            ticks.append(tick)
            series.append(value)

        series = ",".join(series)
        ticks = "','".join(ticks)

        self.histogram = (f"<notextile>\n "
                     f"<script class=\"code\" type=\"text/javascript\">\n"
                     f"$(document).ready(function()" "{"" \n"
                     f"var s = [{series}];\n"
                     f"var ticks = ['{ticks}'];\n"
                     f"var plot = $.jqplot('chart_{plot_id}', [s,],""{\n"
                     f"\tseriesColors: ['{random_color}'], \n"
                     "\tseriesDefaults:{renderer:$.jqplot.BarRenderer, rendererOptions:{fillToZero: true}},\n\taxes:{\n"
                     "\t\txaxis:{renderer: $.jqplot.CategoryAxisRenderer, ticks: ticks},\n"
                     "\t\tyaxis: {pad: 1.05, tickOptions: {formatString: '%d'}}\n\t}\n});\n});\n </script>\n"
                     "</notextile>\n\n"
                     f"<div id=\"chart_{plot_id}\" style=\"width: 700px;\"></div>")

