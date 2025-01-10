import re


def format_links(block):
    """format link for textile according to their target type
        including video and images"""

    motif_images = re.compile(r"(https?\S*.(jpg|png|gif|jpeg|JPG|img))")

    fragments = re.split(r'[^:](http\S*)', block)
    block = fragments[0]

    for i, fragment in enumerate(fragments[1:]):
        if i % 2 == 0:
            if motif_images.search(fragment):
                fragment = re.sub(r"(https?\S*.(jpg|png|gif|jpeg|JPG|img))",
                                  " !\\1!", fragment)
            elif re.search("youtube.com/watch", fragment):
                fragment = re.sub(r'https?://www.youtube.com/watch?'
                                  r'\S*v=([^\s&]*)',
                                  "\n\n<iframe frameborder='0'  width='500' "
                                  " height='352' "
                                  "src='http://www.youtube.com/embed/\\1' "
                                  " allowfullscreen='allowfullscreen'>"
                                  "</iframe>\n\n",
                                  fragment)
            elif re.search("youtu.be", fragment):
                fragment = re.sub(r"https?://youtu.be/(.*)",
                                  "\n\n<iframe frameborder='0' width='500' "
                                  "height='352' "
                                  "src='http://www.youtube.com/embed/\\1'  "
                                  "allowfullscreen='allowfullscreen'>"
                                  "</iframe>\n\n",
                                  fragment)
            elif re.search(r"https?://\S*\.pdf", fragment):
                fragment = re.sub(r"(https?://\S*\.pdf)",
                                  '"\\1":\\1\n\n<object '
                                  'data="\\1#toolbar=0&navpanes=0&view=Fit" '
                                  'width="500" height="650" '
                                  'type="application/pdf"></object>',
                                  fragment)
            elif re.search(r"https?://www.dailymotion.com/\S*", fragment):
                if re.search(r"https?://www.dailymotion.com/embed/video/\S*",
                             fragment):
                    fragment = re.sub(r"(https?://www.dailymotion.com/"
                                      r"embed/video/\S*)",
                                      '\n\n<iframe frameborder="0" '
                                      'width="500" height="352" '
                                      'src="\\1"></iframe>\n\n',
                                      fragment)
                elif re.search(r"https?://www.dailymotion.com/video/.*",
                               fragment):
                    fragment = re.sub(r"(https?://www.dailymotion.com/)"
                                      r"(video/[^_]*).*\s*",
                                      '\n\n<iframe frameborder="0" '
                                      'width="500" height="352" '
                                      'src="\\1embed/\\2\"></iframe>\n\n',
                                      fragment)
            elif re.search(r"https?://vimeo.com/\d+", fragment):
                fragment = re.sub(r"https?://vimeo.com/(\d+)",
                                  '\n\n<iframe frameborder="0" '
                                  'width="500" height="352" '
                                  'src="https://player.vimeo.com/video/\\1\" '
                                  'webkitAllowFullScreen mozallowfullscreen '
                                  'allowFullScreen></iframe>\n\n',
                                  fragment)
            elif re.search(r"https?://www.canal-u.tv/video/S*", fragment):
                fragment = re.sub(r"https?://www.canal-u.tv/video/(\S*)"
                                  r"/(\S*)",
                                  '\n\n<iframe src="https://www.canal-u.tv/'
                                  'video/\\1/embed.1/\\2" width="550" '
                                  'height="306" frameborder="0" '
                                  'allowfullscreen scrolling="no"></iframe>',
                                  fragment)
            else:
                fragment = re.sub(r'(https?://\S*)',
                                  ' "\\1":\\1',
                                  fragment)
        block += fragment

    return block
