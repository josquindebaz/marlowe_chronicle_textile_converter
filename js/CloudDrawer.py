import re


class CloudDrawer:
    def __init__(self, block, cloud_count):
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

        self.cloud = block