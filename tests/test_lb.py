import sys
sys.path.append('.')

from wusn.commons import WusnOutput
from wusn.yuan.lbsna import lbsna2


if __name__ == '__main__':
    out1 = WusnOutput.from_text_file('tests/001_lu.out')

    out2 = lbsna2.lbsna2(out1)
    out2.to_text_file('data/001.test', 'tests/001_lb.out')
