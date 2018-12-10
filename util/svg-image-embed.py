import sys
import os
import base64
from xml.etree import ElementTree

ns_svg = 'http://www.w3.org/2000/svg'
ns_ink = 'http://www.inkscape.org/namespaces/inkscape'
ns_xlk = 'http://www.w3.org/1999/xlink'
ns = {'svg': ns_svg,
      'ink': ns_ink,
      'xlk': ns_xlk}

media_type = {'.jpg': 'image/jpeg'}


def embed_images(svg, root):
    for image in svg.iterfind('.//svg:image[@xlk:href]', namespaces=ns):
        href = image.get('{%s}href' % ns_xlk)
        if not href.startswith('data:'):
            path = os.path.join(root, href)
            with open(path, 'rb') as in_file:
                b64 = base64.b64encode(in_file.read())
            _, ext = os.path.splitext(href)
            mtype = media_type[ext]
            data_img = f'data:{mtype};base64,{b64.decode("utf-8")}'
            image.set('{%s}href' % ns_xlk, data_img)


def die(message):
    print(message)
    sys.exit(1)


usage = 'usage: svg file [file...]'


def main():
    args = sys.argv[1:]
    if not args or args[0] == '-':
        svg_file = sys.stdin
        root = os.getcwd()
    elif len(args) > 1:
        die(usage)
    elif os.path.isfile(args[0]):
        svg_file = args[0]
        root = os.path.dirname(svg_file)
    else:
        die(usage)
    svg = ElementTree.parse(svg_file)
    embed_images(svg, root)
    svg.write(sys.stdout, encoding='unicode')


if __name__ == '__main__':
    main()
