import re


def format_links(block):
    """format link for textile according to their target type
        including video and images"""

    image_pattern = re.compile(r"(https?\S*.(jpg|png|gif|jpeg|JPG|img))")

    fragments = re.split(r'[^:](http\S*)', block)
    block = fragments[0]

    for i, fragment in enumerate(fragments[1:]):
        if i % 2 == 0:
            if image_pattern.search(fragment):
                fragment = re.sub(r"(https?\S*.(jpg|png|gif|jpeg|JPG|img))",
                                  " !\\1!", fragment)

            elif re.search("youtube.com/watch", fragment):
                replacement = "\n\n<iframe frameborder='0' width='500' height='352' " \
                              "src='http://www.youtube.com/embed/\\1' allowfullscreen='allowfullscreen'></iframe>\n\n"

                fragment = re.sub(r'https?://www.youtube.com/watch?\S*v=([^\s&]*)',
                                  replacement,
                                  fragment)

            elif re.search("youtu.be", fragment):
                replacement = "\n\n<iframe frameborder='0' width='500' height='352' " \
                              "src='http://www.youtube.com/embed/\\1' allowfullscreen='allowfullscreen'></iframe>\n\n"

                fragment = re.sub(r"https?://youtu.be/(.*)",
                                  replacement,
                                  fragment)

            elif re.search(r"https?://\S*\.pdf", fragment):
                replacement = '"\\1":\\1\n\n<object data="\\1#toolbar=0&navpanes=0&view=Fit" ' \
                              'width="500" height="650" type="application/pdf"></object>'

                fragment = re.sub(r"(https?://\S*\.pdf)",
                                  replacement,
                                  fragment)

            elif re.search(r"https?://www.dailymotion.com/\S*", fragment):
                if re.search(r"https?://www.dailymotion.com/embed/video/\S*",
                             fragment):
                    replacement = '\n\n<iframe frameborder="0" width="500" height="352" src="\\1"></iframe>\n\n'

                    fragment = re.sub(r"(https?://www.dailymotion.com/"
                                      r"embed/video/\S*)",
                                      replacement,
                                      fragment)
                elif re.search(r"https?://www.dailymotion.com/video/.*", fragment):
                    replacement = '\n\n<iframe frameborder="0" width="500" height="352" src="\\1embed/\\2\"></iframe>\n\n'

                    fragment = re.sub(r"(https?://www.dailymotion.com/)(video/[^_]*).*\s*",
                                      replacement,
                                      fragment)

            elif re.search(r"https?://vimeo.com/\d+", fragment):
                replacement = '\n\n<iframe frameborder="0" width="500" height="352" src="https://player.vimeo.com/video/\\1\" ' \
                              'webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>\n\n'

                fragment = re.sub(r"https?://vimeo.com/(\d+)",
                                  replacement,
                                  fragment)

            elif re.search(r"https?://www.canal-u.tv/video/S*", fragment):
                replacement = '\n\n<iframe src="https://www.canal-u.tv/video/\\1/embed.1/\\2" width="550" ' \
                              'height="306" frameborder="0" allowfullscreen scrolling="no"></iframe>'

                fragment = re.sub(r"https?://www.canal-u.tv/video/(\S*)/(\S*)",
                                  replacement,
                                  fragment)
            else:
                fragment = re.sub(r'(https?://\S*)',
                                  ' "\\1":\\1',
                                  fragment)
        block += fragment

    return block
