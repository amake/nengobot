from PIL import Image, ImageDraw, ImageFont

transparent = (255, 255, 255, 0)
black = (0, 0, 0, 255)


def fit_frame(img):
    return img.transform(img.size,
                         method=Image.AFFINE,
                         data=[1, -0.1, 0,
                               0.05, 1, 0],
                         resample=Image.BILINEAR)


def generate(*lines):
    base = Image.open('./work/blank.png').convert('RGBA')
    txt = Image.new('RGBA', base.size, transparent)
    fnt = ImageFont.truetype(
        './work/UtsukushiMincho-FONT/UtsukushiFONT.otf', 80)
    d = ImageDraw.Draw(txt)
    d.text((113, 72), '\n'.join(lines), font=fnt, fill=black)
    rot = fit_frame(txt)
    return Image.alpha_composite(base, rot)


def generate_emoji(emoji_file):
    base = Image.open('./work/party.png').convert('RGBA')
    emoji = Image.open(emoji_file).convert('RGBA')
    txt = Image.new('RGBA', base.size, transparent)
    txt.paste(emoji, (75, 70))
    rot = fit_frame(txt)
    return Image.alpha_composite(base, rot)


def main():
    import sys
    import random
    import os
    if sys.argv[1:]:
        img = generate(*sys.argv[1])
        img.show()
    img = generate_emoji(
        f'./work/images/160x160/{random.randint(1, 2514)}.png')
    img.show()


if __name__ == '__main__':
    main()
