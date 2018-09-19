import sys

from wusn.commons import WusnOutput


if __name__ == '__main__':
    inp = sys.argv[1]
    out_path = sys.argv[2]

    out = WusnOutput.from_text_file(inp)
    out.plot_to_file(out_path)
