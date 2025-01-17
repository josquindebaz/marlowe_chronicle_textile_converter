import random
import re

from CityLocator import CityLocator

COLORS = ['#fba919', '#00749F', '#73C774', '#C7754C', '#c82124']


def get_cities(values):
    return dict(line.split(",")
                for line in re.split(r"\s*;\s*", values)[:-1])


def get_locations(cities):
    """Returns a dictionary of [latitude, longitude] for given cities"""

    city_locator = CityLocator()

    locations = {}
    for city in cities:
        locations[city] = city_locator.get_coordinates(city)

    return locations


def draw(city_values, city_locations, color):
    js_map = (
        '\n\n<notextile>\n\n<div id="map">\n<script class="code" type="text/javascript">\nvar initMap = function(){\n\t'
        'var provider = new com.modestmaps.TemplatedLayer("http://tile.openstreetmap.org/{Z}/{X}/{Y}.png");\n\t'
        'var map = new com.modestmaps.Map("map", provider);\n\tvar canvas = document.createElement("canvas");\n\t'
        'canvas.style.position = "absolute";\n\tcanvas.style.left = "0";\n\tcanvas.style.top = "0";\n\tcanvas.width = '
        'map.dimensions.x;\n\tcanvas.height = map.dimensions.y;\n\tmap.parent.appendChild(canvas);\n')

    for city, location in city_locations.items():
        latitude = location[0]
        longitude = location[1]

        js_map += f"\tvar {sanitize_city(city)} = new com.modestmaps.Location({latitude},{longitude});\n"

    joined_locations = ", ".join([sanitize_city(city) for city in city_values.keys()])
    joined_values = ", ".join(city_values.values())
    js_map += f"\tvar locations = [{joined_locations}];\n"
    js_map += f"\tvar values = [{joined_values}];\n"

    js_map += ("\tvar max = Math.max.apply(Math, values);\n\tmap.setExtent(locations);\n\tmap.zoomOut();\n\t"
               "function redraw(){\n\t\tvar ctx = canvas.getContext('2d');\n\t\tctx.clearRect(0,0,canvas.width,canvas.height);\n"
               "\t\tfor (var i = 0; i < locations.length; i++){\n\t\t\tctx.beginPath();\n\t\t\tvar p = map.locationPoint(locations[i]);\n")

    js_map += f"\t\t\tctx.fillStyle = '{color}';\n\t\t\tctx.globalAlpha = 0.6;\n"

    js_map += ("\t\t\tradius = values[i] * 15 / max + 5;\n\t\t\tctx.arc(p.x,p.y,radius,0,2 * Math.PI, false);\n"
               "\t\t\tctx.fill();\n\t\t\tctx.stroke();\n\t\t}\n\t}\n\tmap.addCallback('drawn', redraw);\n"
               "\tmap.addCallback('resized', function(){\n\t\tcanvas.width = map.dimensions.x;\n"
               "\t\tcanvas.height = map.dimensions.y;\n\t\tredraw();\n\t});\n\tredraw();\n}\n"
               "</script>\n</div>\n\n</notextile>\n\np(reference). \"Fond et positions © les contributeurs "
               "d'OpenStreetMap\":https://www.openstreetmap.org/copyright\n\n")

    return js_map


def sanitize_city(city):
    return re.sub(r'[\s\-éè]', '_', city)


class MapDrawer:
    """Make an OSM map in js"""

    def __init__(self, values, color=None):
        city_values = get_cities(values)
        city_locations = get_locations(city_values.keys())

        if not color:
            color = random.choice(COLORS)

        self.map = draw(city_values, city_locations, color)
