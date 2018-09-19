import sys
sys.path.append('.')

from wusn.commons import WusnInput
from wusn.yuan.lurns import lurns1, lurns2


if __name__ == '__main__':
    inp = WusnInput.from_file('data/001.test')

    out1 = lurns1.lurns1(inp)
    out1.to_text_file('data/001.test', 'tests/001_lu.out')
    # out2 = lurns2.lurns2(inp)
