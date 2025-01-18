import textile_utils


def test_format_links():
    content = 'any link https://any.link/something can do'
    expected = 'any link "https://any.link/something":https://any.link/something can do'

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_does_not_change_when_no_link():
    content = "no link"

    result = textile_utils.format_links(content)

    assert result == content


def test_format_links_change_multiple_links():
    content = "Voici deux liens http://bla.com et https://blabla.fr/something à consulter."
    expected = ('Voici deux liens "http://bla.com":http://bla.com et '
                '"https://blabla.fr/something":https://blabla.fr/something à consulter.')

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_images():
    content = "This is an https://www.poetsgraves.co.uk/images/borgesgrave.jpg image"
    expected = 'This is an !https://www.poetsgraves.co.uk/images/borgesgrave.jpg! image'

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_youtube():
    content = "This is a https://www.youtube.com/watch?v=FK-KC2aQpcI video"
    expected = ("This is a\n\n<iframe frameborder='0' width='500' height='352' "
                "src='http://www.youtube.com/embed/FK-KC2aQpcI' "
                "allowfullscreen='allowfullscreen'></iframe>\n\n video")

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_youtu_be():
    content = "This is a https://youtu.be/watch?v=FK-KC2aQpcI video"
    expected = ("This is a\n\n<iframe frameborder='0' width='500' height='352' "
                "src='http://www.youtube.com/embed/watch?v=FK-KC2aQpcI' "
                "allowfullscreen='allowfullscreen'></iframe>\n\n video")

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_pdf():
    content = "This is a https://gspr-ehess.com/documents/ObsEnv2003.pdf pdf"
    expected = ('This is '
                'a"https://gspr-ehess.com/documents/ObsEnv2003.pdf":https://gspr-ehess.com/documents/ObsEnv2003.pdf\n'
                '\n'
                '<object '
                'data="https://gspr-ehess.com/documents/ObsEnv2003.pdf#toolbar=0&navpanes=0&view=Fit" '
                'width="500" height="650" type="application/pdf"></object> pdf')

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_daily_embed():
    content = "This is a http://www.dailymotion.com/embed/video/xiwwfd video"
    expected = ('This is a\n'
                '\n'
                '<iframe frameborder="0" width="500" height="352" '
                'src="http://www.dailymotion.com/embed/video/xiwwfd"></iframe>\n'
                '\n'
                ' video')
    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_daily_video():
    content = "This is a http://www.dailymotion.com/video/x387ig4 video"
    expected = ('This is a\n'
                '\n'
                '<iframe frameborder="0" width="500" height="352" '
                'src="http://www.dailymotion.com/embed/video/x387ig4"></iframe>\n'
                '\n'
                ' video')

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_vimeo():
    content = "This is a http://vimeo.com/7021433 video"
    expected = ('This is a\n'
                '\n'
                '<iframe frameborder="0" width="500" height="352" '
                'src="https://player.vimeo.com/video/7021433" webkitAllowFullScreen '
                'mozallowfullscreen allowFullScreen></iframe>\n'
                '\n'
                ' video')

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_links_change_canal_u():
    content = "This is a http://www.canal-u.tv/video/iap/exoplanetes_la_surprenante_diversite_des_autres_mondes_du_cosmos.18397 video"
    expected = ('This is a\n'
                '\n'
                '<iframe '
                'src="https://www.canal-u.tv/video/iap/embed.1/exoplanetes_la_surprenante_diversite_des_autres_mondes_du_cosmos.18397" '
                'width="550" height="306" frameborder="0" allowfullscreen '
                'scrolling="no"></iframe> video')

    result = textile_utils.format_links(content)

    assert result == expected


def test_format_table():
    block = """Je n'ai pas noté d' " affaire " susceptible de défrayer la chronique (sic). Voici pour mémoire les principales affaires dont on a le plus bavardé entre le 6/12/2004  et le 27/12/2024  : <br> <BR>1400  -  corruption  -  <BR>483  -  Clearstream  -  <BR>465  -  Bettencourt  -  <BR>360  -  Benalla  -  <BR>305  -  Weinstein  -  <BR>298  -  Cahuzac  -  <BR>267  -  pédophilie  -  <BR>264  -  viol  -  <BR>263  -  Fillon  -  <BR>257  -  Bygmalion  -  <BR>253  -  Outreau  -  <BR>235  -  attentats  -  <BR>230  -  emplois fictifs  -  <BR>230  -  meurtre  -  <BR>217  -  Watergate  -  <BR>213  -  dopage  -  <BR>211  -  Karachi  -  <BR>195  -  écoutes  -  <BR>168  -  Mediator  -  <BR>168  -  DSK  -  <BR>167  -  Nuremberg  -  <BR>164  -  fraude  -  <BR>161  -  affaire  -  <BR>153  -  Kerviel  -  <BR>150  -  Merah  -  <BR>149  -  moteurs  -  <BR>148  -  assistants parlementaires  -  <BR>147  -  Grégory  -  <BR>141  -  famille  -  <BR>133  -  Skripal  -  <BR>126  -  moeurs  -  <BR>125  -  Elf  -  <BR>124  -  fraude fiscale  -  <BR>122  -  emplois présumés fictifs  -  <BR>120  -  viols  -  <BR>120  -  masse  -  <BR>119  -  Roe  -  <BR>119  -  Tapie  -  <BR>118  -  Sarkozy  -  <BR>116  -  Carlton  -  <BR>"""
    expected = """Je n'ai pas noté d' " affaire " susceptible de défrayer la chronique (sic). Voici pour mémoire les principales affaires dont on a le plus bavardé entre le 6/12/2004  et le 27/12/2024  : <br> 

table(marloblog).
| 1400 | corruption   |
| 483 | Clearstream   |
| 465 | Bettencourt   |
| 360 | Benalla   |
| 305 | Weinstein   |
| 298 | Cahuzac   |
| 267 | pédophilie   |
| 264 | viol   |
| 263 | Fillon   |
| 257 | Bygmalion   |
| 253 | Outreau   |
| 235 | attentats   |
| 230 | emplois fictifs   |
| 230 | meurtre   |
| 217 | Watergate   |
| 213 | dopage   |
| 211 | Karachi   |
| 195 | écoutes   |
| 168 | Mediator   |
| 168 | DSK   |
| 167 | Nuremberg   |
| 164 | fraude   |
| 161 | affaire   |
| 153 | Kerviel   |
| 150 | Merah   |
| 149 | moteurs   |
| 148 | assistants parlementaires   |
| 147 | Grégory   |
| 141 | famille   |
| 133 | Skripal   |
| 126 | moeurs   |
| 125 | Elf   |
| 124 | fraude fiscale   |
| 122 | emplois présumés fictifs   |
| 120 | viols   |
| 120 | masse   |
| 119 | Roe   |
| 119 | Tapie   |
| 118 | Sarkozy   |
| 116 | Carlton   |"""

    result = textile_utils.format_table(block)

    assert result == expected

def test_format_table_when_double():
    block = "La directive Brun - du nom d'un fidèle, et notoire lecteur de mes chroniques , m'incite à distinguer deux palmarès. Celui qui est le résultat entassé de l'ensemble des chroniques, et celui de la période plus récente - que j'ai fixée au pif à 60 jours. J'affiche donc en premier lieu le palmarès global, couvrant la période du 14/ 9/2004  au 27/12/2024  : <br> <br> <BR>3348  -  Sarkozy  -  <BR>2971  -  Macron  -  <BR>2540  -  Trump  -  <BR>2086  -  Poutine  -  <BR>2070  -  Hollande  -  <BR>1832  -  Obama  -  <BR>1523  -  Le Pen  -  <BR>1318  -  Biden  -  <BR>1054  -  Fillon  -  <BR>1001  -  Mélenchon  -  <BR>958  -  Merkel  -  <BR>922  -  Royal  -  <BR>903  -  Valls  -  <BR>871  -  Bush  -  <BR>860  -  Chirac  -  <BR>715  -  Clinton  -  <BR>553  -  Erdogan  -  <BR>545  -  Villepin  -  <BR>523  -  Netanyahu  -  <BR>513  -  Bayrou  -  <BR>498  -  Johnson  -  <BR>456  -  Zelensky  -  <BR>384  -  Assange  -  <BR>383  -  Maduro  -  <BR>372  -  Darmanin  -  <BR>367  -  Aubry  -  <BR>366  -  Abbas  -  <BR>360  -  Kerry  -  <BR>339  -  Le Maire  -  <BR>337  -  Ayrault  -  <BR> <br> <br> Et pour y voir plus clair sur les déplacements récents, j'affiche maintenant le palmarès des personnalités du 29/10/2024  au 27/12/2024  : <br> <br> <BR>60  -  Trump  -  <BR>59  -  Macron  -  <BR>50  -  Barnier  -  <BR>49  -  Poutine  -  <BR>39  -  Le Pen  -  <BR>38  -  Biden  -  <BR>27  -  Zelensky  -  <BR>25  -  Retailleau  -  <BR>24  -  Al-Assad  -  <BR>23  -  Bayrou  -  <BR>21  -  Musk  -  <BR>20  -  Scholz  -  <BR>16  -  Harris  -  <BR>14  -  Meloni  -  <BR>13  -  Netanyahu  -  <BR>13  -  Pelicot  -  <BR>12  -  Bardella  -  <BR>11  -  Yoon  -  <BR>11  -  Faure  -  <BR>9  -  Attal  -  <BR>9  -  Paty  -  <BR>9  -  Mélenchon  -  <BR>9  -  Barrot  -  <BR>8  -  Darmanin  -  <BR>8  -  Sánchez  -  <BR>8  -  Nétanyahou  -  <BR>7  -  Orbán  -  <BR>6  -  Tusk  -  <BR>6  -  Wauquiez  -  <BR>6  -  Washington  -  <BR>"

    expected = """La directive Brun - du nom d'un fidèle, et notoire lecteur de mes chroniques , m'incite à distinguer deux palmarès. Celui qui est le résultat entassé de l'ensemble des chroniques, et celui de la période plus récente - que j'ai fixée au pif à 60 jours. J'affiche donc en premier lieu le palmarès global, couvrant la période du 14/ 9/2004  au 27/12/2024  : <br> <br> 

table(marloblog).
| 3348 | Sarkozy   |
| 2971 | Macron   |
| 2540 | Trump   |
| 2086 | Poutine   |
| 2070 | Hollande   |
| 1832 | Obama   |
| 1523 | Le Pen   |
| 1318 | Biden   |
| 1054 | Fillon   |
| 1001 | Mélenchon   |
| 958 | Merkel   |
| 922 | Royal   |
| 903 | Valls   |
| 871 | Bush   |
| 860 | Chirac   |
| 715 | Clinton   |
| 553 | Erdogan   |
| 545 | Villepin   |
| 523 | Netanyahu   |
| 513 | Bayrou   |
| 498 | Johnson   |
| 456 | Zelensky   |
| 384 | Assange   |
| 383 | Maduro   |
| 372 | Darmanin   |
| 367 | Aubry   |
| 366 | Abbas   |
| 360 | Kerry   |
| 339 | Le Maire   |
| 337 | Ayrault   |

p. Et pour y voir plus clair sur les déplacements récents, j'affiche maintenant le palmarès des personnalités du 29/10/2024  au 27/12/2024  :

table(marloblog).
| 60 | Trump   |
| 59 | Macron   |
| 50 | Barnier   |
| 49 | Poutine   |
| 39 | Le Pen   |
| 38 | Biden   |
| 27 | Zelensky   |
| 25 | Retailleau   |
| 24 | Al-Assad   |
| 23 | Bayrou   |
| 21 | Musk   |
| 20 | Scholz   |
| 16 | Harris   |
| 14 | Meloni   |
| 13 | Netanyahu   |
| 13 | Pelicot   |
| 12 | Bardella   |
| 11 | Yoon   |
| 11 | Faure   |
| 9 | Attal   |
| 9 | Paty   |
| 9 | Mélenchon   |
| 9 | Barrot   |
| 8 | Darmanin   |
| 8 | Sánchez   |
| 8 | Nétanyahou   |
| 7 | Orbán   |
| 6 | Tusk   |
| 6 | Wauquiez   |
| 6 | Washington   |"""

    result = textile_utils.format_table(block)

    assert result == expected