from js.HistogramDrawer import HistogramDrawer, compute


def test_can_compute():
    values = "2004 , 0 ; 2005 , 259 ;"

    series, ticks = compute(values)

    assert series == [' 0 ', ' 259 ']
    assert ticks == ['2004 ', ' 2005 ']


def test_can_histogram():
    values = "2004 , 0 ; 2005 , 259 ; 2006 , 279 ; 2007 , 320 ; 2008 , 318 ; 2009 , 315 ; 2010 , 287 ; 2011 , 267 ; 2012 , 291 ; 2013 , 312 ; 2014 , 308 ; 2015 , 357 ; 2016 , 361 ; 2017 , 348 ; 2018 , 342 ; 2019 , 306 ; 2020 , 280 ; 2021 , 220 ; 2022 , 272 ; 2023 , 205 ; 2024 , 228 ; 2025 , 4 ;"
    count = 1
    color = '#00749F'

    expected = """<notextile>
 <script class="code" type="text/javascript">
$(document).ready(function(){ 
var s = [ 0 , 259 , 279 , 320 , 318 , 315 , 287 , 267 , 291 , 312 , 308 , 357 , 361 , 348 , 342 , 306 , 280 , 220 , 272 , 205 , 228 , 4 ];
var ticks = ['2004 ',' 2005 ',' 2006 ',' 2007 ',' 2008 ',' 2009 ',' 2010 ',' 2011 ',' 2012 ',' 2013 ',' 2014 ',' 2015 ',' 2016 ',' 2017 ',' 2018 ',' 2019 ',' 2020 ',' 2021 ',' 2022 ',' 2023 ',' 2024 ',' 2025 '];
var plot = $.jqplot('chart_1', [s,],{
	seriesColors: ['#00749F'], 
	seriesDefaults:{renderer:$.jqplot.BarRenderer, rendererOptions:{fillToZero: true}},
	axes:{
		xaxis:{renderer: $.jqplot.CategoryAxisRenderer, ticks: ticks},
		yaxis: {pad: 1.05, tickOptions: {formatString: '%d'}}
	}
});
});
 </script>
</notextile>

<div id="chart_1" style="width: 700px;"></div>"""

    drawer = HistogramDrawer(values, count, color)
    result = drawer.histogram

    assert result == expected
