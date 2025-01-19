import re


class CloudDrawer:
    def __init__(self, block, cloud_count):
        """format a cloud word in js"""

        parts = re.split("--nuage--", block)

        self._cloud = parts[
                          0] + f'\n\n<notextile>\n <script type="text/javascript">\n  var word_array{cloud_count} = [ '

        for raw_value in parts[1].split(";"):
            if raw_value:
                key, value = re.search(r"\s*(.*)\s+,\s*(.*)\s+", raw_value).group(1, 2)

                self._cloud += f'\t\t{{text: "{key}", weight: {value}, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)}},\n '

        self._cloud += (f' ];\n  $(function() {{ $("#cloud_{cloud_count}").jQCloud(word_array{cloud_count});}});\n'
                        f' </script>\n</notextile>\n\n'
                        f'<div id="cloud_{cloud_count}" style="width: 700px; height: 350px;"></div>\n\n')

        self._cloud += parts[2]

    @property
    def cloud(self):
        return self._cloud
