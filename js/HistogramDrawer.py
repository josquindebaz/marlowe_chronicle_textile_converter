import random
import uuid

COLORS = ['#fba919', '#00749F', '#73C774', '#C7754C']


def compute(values):
    series = []
    ticks = []

    for fragment in values.split(";")[:-1]:
        tick, value = fragment.split(",")
        ticks.append(tick)
        series.append(value)

    return series, ticks


def draw(color, plot_id, series, ticks):
    return (f"<notextile>\n "
            f"<script class=\"code\" type=\"text/javascript\">\n"
            f"$(document).ready(function()" "{"" \n"
            f"var s = [{",".join(series)}];\n"
            f"var ticks = ['{"','".join(ticks)}'];\n"
            f"var plot = $.jqplot('chart_{plot_id}', [s,],""{\n"
            f"\tseriesColors: ['{color}'], \n"
            "\tseriesDefaults:{renderer:$.jqplot.BarRenderer, rendererOptions:{fillToZero: true}},\n\taxes:{\n"
            "\t\txaxis:{renderer: $.jqplot.CategoryAxisRenderer, ticks: ticks},\n"
            "\t\tyaxis: {pad: 1.05, tickOptions: {formatString: '%d'}}\n\t}\n});\n});\n </script>\n"
            "</notextile>\n\n"
            f"<div id=\"chart_{plot_id}\" style=\"width: 700px;\"></div>")


class HistogramDrawer:
    """Make a histogram in js"""

    def __init__(self, values, plot_id=None, color=None):
        if not color:
            color = random.choice(COLORS)

        if plot_id is None:
            plot_id = uuid.uuid1()

        series, ticks = compute(values)

        self.histogram = draw(color, plot_id, series, ticks)
