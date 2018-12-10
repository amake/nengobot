import sys
import os
from xml.etree import ElementTree

ns_svg = 'http://www.w3.org/2000/svg'
ns_ink = 'http://www.inkscape.org/namespaces/inkscape'
ns = {'svg': ns_svg,
      'ink': ns_ink}


def enable_layers(svg, layers):
    for layer in svg.iterfind('.//svg:g[@ink:groupmode="layer"]', namespaces=ns):
        enable = layer.get('{%s}label' % ns_ink) in layers
        style = 'display:inline' if enable else 'display:none'
        layer.set('style', style)


def main():
    args = sys.argv[1:]
    if not args:
        print('usage: svg layername [layername...]')
        sys.exit(1)
    if os.path.isfile(args[0]):
        svg_file = args[0]
        layers = args[1:]
    elif args[0] == '-':
        svg_file = sys.stdin
        layers = args[1:]
    else:
        svg_file = sys.stdin
        layers = args
    svg = ElementTree.parse(svg_file)
    enable_layers(svg, layers)
    svg.write(sys.stdout, encoding='unicode')


if __name__ == '__main__':
    main()
