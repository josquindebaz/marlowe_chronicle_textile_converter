import datetime

import mrlw_chron_2_textile


def test_entire_chronicle():
    with open("source_samples/2024-12-28-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    assert parser.date == datetime.datetime(2024, 12, 28, 23, 4, 53)
    assert parser.title == "Now, I'm taking the head out of the jumble, the mayhem, the mess ..."
    assert parser.logs == "Saturday 28 December 2024 23:04:53\nchronicle text size: 171446 chars\nfound 22 blocks\nNow, I'm taking the head out of the jumble, the mayhem, the mess ...\n"

    with open("source_samples/2024-12-29-chronique_mrlw.txt", 'rb') as c:
        chronicle_content = c.read()

    parser = mrlw_chron_2_textile.ChroniqueParser(chronicle_content)

    assert parser.date == datetime.datetime(2024, 12, 29, 23, 6, 3)
    assert parser.title == ("Bonsoir. Un internaute m'a adressé une série d'insultes sur Aliev ... Je les "
                            'ai détruites... Bien sûr, un procès me rendrait très inoubliable , mais '
                            'devant des juges, outre que je serais réduit à des lignes de code indigestes '
                            'et ausculté par des experts, je ne ferais pas le malin ! Merci de modérer '
                            'vos propos chers interlocuteurs ')

    assert parser.logs == ('Sunday 29 December 2024 23:06:03\n'
                           'chronicle text size: 30219 chars\n'
                           'found 23 blocks\n'
                           "Bonsoir. Un internaute m'a adressé une série d'insultes sur Aliev ... Je les "
                           'ai détruites... Bien sûr, un procès me rendrait très inoubliable , mais '
                           'devant des juges, outre que je serais réduit à des lignes de code indigestes '
                           'et ausculté par des experts, je ne ferais pas le malin ! Merci de modérer '
                           'vos propos chers interlocuteurs \n')

######## static methods

def test_format_sigles_returns_block_if_no_sigles():
    block = "Non rien de rien, je ne relève rien. \r\n\r\r\n"

    result = mrlw_chron_2_textile.format_sigles(block)

    assert result == block + "- "
    # strip that "- "

def test_format_sigles_can_handle_acronyms():
    block = 'Voici le contenu des "nouveaux" sigles : <br> <br> <BR> TGC : taxe générale sur la consommation, <BR> SALT : Strategic Arms Limitation Talks, <BR> BSAOM : bâtiment de soutien et d \' assistance outre-mer\r\n\r\r\n'

    result = mrlw_chron_2_textile.format_sigles(block)

    assert result == 'Voici le contenu des "nouveaux" sigles : \n\n- TGC  := taxe générale sur la consommation,\n- SALT  := Strategic Arms Limitation Talks,\n- BSAOM  := bâtiment de soutien et d \' assistance outre-mer'


# def test_format_links():
#     assert False

# def test_format_numbered_list():
#     assert False
#
#
# def test_table_or_barplot():
#     assert False
#
#
# def test_format_table():
#     assert False
#
#
# def test_format_barplot():
#     assert False
#
#
# def test_format_histo():
#     assert False
#
#
# def test_format_graphe():
#     assert False
#
#
# def test_format_cloud():
#     assert False
#
#
# def test_format_map():
#     assert False
#
#
# def test_format_quotes():
#     assert False
#
#
# def test_protect_quotes():
#     assert False
#
#
# def test_format_date():
#     assert False
#
#
# def test_format_marks():
#     assert False


# TownCoordinates
# def test_read_file():
#     assert False
#
#
# def test_get_coord():
#     assert False
#
#
# def test_save_coord():
#     assert False

# ChroniqueParser

# def test_type_sentences():
#     assert False
#
#
# def test_prepare_blocks():
#     assert False
#
#
# def test_generate_blocks():
#     assert False
#
#
# def test_generate_citations():
#     assert False
#
#
# def test_format_citation():
#     assert False
#
#
# def test_get_date():
#     assert False
#
#
# def test_generate_preambule():
#     assert False
#
#
# def test_write_textile():
#     assert False

# Referencer
# def test_get_url():
#     assert False

# NetworkGraphe

# def test_intro():
#     assert False
#
#
# def test_end():
#     assert False
#
#
# def test_set_lists():
#     assert False
#
#
# def test_set_edges():
#     assert False
