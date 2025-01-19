from js.CloudDrawer import CloudDrawer


def test_can_format_cloud():
    block = "Je me suis mis à faire des nuages de tags pour être dans l'air du temps ... On en pense ce qu'on veut, mais ça change de temps en temps. Soit donc le nuage des principales personnalités du jour :<br><br> --nuage-- Carter , 64 ; Al-Assad , 35 ; Milanovic , 22 ; Aliev , 21 ; Bayrou , 20 ; Trump , 18 ; Kavelachvili , 18 ; Zourabichvili , 16 ; Darmanin , 14 ; Al-Chareh , 11 ; Musk , 11 ; Coste , 10 ; Primorac , 10 ; Macron , 9 ; Jacobelli , 9 ; Allemand , 8 ; Al-Charaa , 8 ; Dimanche , 7 ; Poutine , 7 ; Rahmane , 6 ;--nuage-- <br><br>"

    expected = """Je me suis mis à faire des nuages de tags pour être dans l'air du temps ... On en pense ce qu'on veut, mais ça change de temps en temps. Soit donc le nuage des principales personnalités du jour :<br><br> 

<notextile>
 <script type="text/javascript">
  var word_array1 = [ 		{text: "Carter", weight: 64, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Al-Assad", weight: 35, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Milanovic", weight: 22, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Aliev", weight: 21, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Bayrou", weight: 20, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Trump", weight: 18, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Kavelachvili", weight: 18, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Zourabichvili", weight: 16, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Darmanin", weight: 14, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Al-Chareh", weight: 11, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Musk", weight: 11, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Coste", weight: 10, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Primorac", weight: 10, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Macron", weight: 9, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Jacobelli", weight: 9, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Allemand", weight: 8, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Al-Charaa", weight: 8, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Dimanche", weight: 7, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Poutine", weight: 7, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
 		{text: "Rahmane", weight: 6, color: "#"+("000000"+Math.random().toString(16).slice(2, 8).toUpperCase()).slice(-6)},
  ];
  $(function() { $("#cloud_1").jQCloud(word_array1);});
 </script>
</notextile>

<div id="cloud_1" style="width: 700px; height: 350px;"></div>

 <br><br>"""

    drawer = CloudDrawer(block, 1)

    assert drawer.cloud == expected

