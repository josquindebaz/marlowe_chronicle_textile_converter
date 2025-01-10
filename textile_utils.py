import re


def format_links(block):
    """format link for textile according to their target type
        including video and images"""

    image_pattern = re.compile(r"(https?\S*.(jpg|png|gif|jpeg|JPG|img))")
    youtube_pattern = re.compile(r'https?://www.youtube.com/watch?\S*v=([^\s&]*)')
    youtu_be_pattern = re.compile(r"https?://youtu.be/(.*)")
    pdf_pattern = re.compile(r"(https?://\S*\.pdf)")
    daily_embed_pattern = re.compile(r"(https?://www.dailymotion.com/embed/video/\S*)")
    daily_video_pattern = re.compile(r"(https?://www.dailymotion.com/)(video/[^_]*).*\s*")
    vimeo_pattern = re.compile(r"https?://vimeo.com/(\d+)")
    canal_u_pattern = re.compile(r"https?://www.canal-u.tv/video/(\S*)/(\S*)")

    fragments = re.split(r'[^:](http\S*)', block)
    block = fragments[0]

    for i, fragment in enumerate(fragments[1:]):
        if i % 2 == 0:
            if image_pattern.search(fragment):
                fragment = image_pattern.sub(" !\\1!", fragment)

            elif youtube_pattern.search(fragment):
                replacement = "\n\n<iframe frameborder='0' width='500' height='352' " \
                              "src='http://www.youtube.com/embed/\\1' allowfullscreen='allowfullscreen'></iframe>\n\n"

                fragment = youtube_pattern.sub(replacement, fragment)

            elif youtu_be_pattern.search(fragment):
                replacement = "\n\n<iframe frameborder='0' width='500' height='352' " \
                              "src='http://www.youtube.com/embed/\\1' allowfullscreen='allowfullscreen'></iframe>\n\n"

                fragment = youtu_be_pattern.sub(replacement, fragment)

            elif pdf_pattern.search(fragment):
                replacement = '"\\1":\\1\n\n<object data="\\1#toolbar=0&navpanes=0&view=Fit" ' \
                              'width="500" height="650" type="application/pdf"></object>'

                fragment = pdf_pattern.sub(replacement, fragment)

            elif daily_embed_pattern.search(fragment):
                replacement = '\n\n<iframe frameborder="0" width="500" height="352" src="\\1"></iframe>\n\n'

                fragment = daily_embed_pattern.sub(replacement, fragment)

            elif daily_video_pattern.search(fragment):
                replacement = '\n\n<iframe frameborder="0" width="500" height="352" src="\\1embed/\\2\"></iframe>\n\n'

                fragment = daily_video_pattern.sub(replacement, fragment)

            elif vimeo_pattern.search(fragment):
                replacement = '\n\n<iframe frameborder="0" width="500" height="352" src="https://player.vimeo.com/video/\\1\" ' \
                              'webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>\n\n'

                fragment = vimeo_pattern.sub(replacement, fragment)

            elif canal_u_pattern.search(fragment):
                replacement = '\n\n<iframe src="https://www.canal-u.tv/video/\\1/embed.1/\\2" width="550" ' \
                              'height="306" frameborder="0" allowfullscreen scrolling="no"></iframe>'

                fragment = canal_u_pattern.sub(replacement, fragment)

            else:
                fragment = re.sub(r'(https?://\S*)',
                                  ' "\\1":\\1',
                                  fragment)
        block += fragment

    return block
