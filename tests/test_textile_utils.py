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
