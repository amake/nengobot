from PIL import Image, ImageDraw, ImageFont

transparent = (255, 255, 255, 0)
black = (0, 0, 0, 255)

image_heisei = './work/blank.png'
image_party = './work/party.png'
image_reiwa = './work/reiwa.jpg'

text_origin = {image_heisei: (113, 72),
               image_party: (113, 72),
               image_reiwa: (250, 110)}

text_size = {image_heisei: 80,
             image_reiwa: 200}

text_adjust = {image_heisei: [1, -0.1, 0,
                              0.05, 1, 0],
               image_party: [1, -0.1, 0,
                             0.05, 1, 0],
               image_reiwa: [1, -0.1, 0,
                             0.1, 1, 0]}


def fit_frame(img_obj, image):
    return img_obj.transform(img_obj.size,
                             method=Image.AFFINE,
                             data=text_adjust[image],
                             resample=Image.BILINEAR)


def generate(*lines, image=image_reiwa):
    base = Image.open(image).convert('RGBA')
    txt = Image.new('RGBA', base.size, transparent)
    fnt = ImageFont.truetype(
        './work/UtsukushiMincho-FONT/UtsukushiFONT.otf', text_size[image])
    d = ImageDraw.Draw(txt)
    d.text(text_origin[image], '\n'.join(lines), font=fnt, fill=black)
    rot = fit_frame(txt, image)
    return Image.alpha_composite(base, rot)


def generate_emoji(emoji_file):
    base = Image.open(image_party).convert('RGBA')
    emoji = Image.open(emoji_file).convert('RGBA')
    txt = Image.new('RGBA', base.size, transparent)
    txt.paste(emoji, (75, 70))
    rot = fit_frame(txt, image_party)
    return Image.alpha_composite(base, rot)


def main():
    import sys
    import random
    if sys.argv[1:]:
        img = generate(*sys.argv[1])
        img.show()
    img = generate_emoji(
        f'./work/images/160x160/{random.randint(1, 2514)}.png')
    img.show()


if __name__ == '__main__':
    main()
