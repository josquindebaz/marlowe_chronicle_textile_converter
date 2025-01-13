import random
import re

from CityLocator import CityLocator

class MapDrawer:

    def __init__(self, core):
        city_locator = CityLocator()

        self.map = ('\n\n<notextile>\n\n<div id="map">\n<script class="code" '
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

            self.map += "\tvar %s = new com.modestmaps.Location(%s,%s);\n" % \
                        (re.sub(r'[\s\-éè]', '_', city), latitude, longitude)

        self.map += "\tvar locations = [%s];\n" % \
               ", ".join([re.sub(r'[\s\-éè]', '_', town) for town in cities.keys()])
        self.map += "\tvar values = [%s];\n" % ", ".join(cities.values())
        self.map += ("\tvar max = Math.max.apply(Math, values);\n\t"
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

        self.map += 'p(reference). "Fond et positions © les contributeurs ' \
           'd\'OpenStreetMap":https://www.openstreetmap.org/copyright\n\n'