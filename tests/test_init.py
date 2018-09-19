import sys
sys.path.append('.')

from wusn.commons import WusnInput
from wusn.propose2.init import kmeans_random
from wusn.propose2.utils import ind_to_output


if __name__ == '__main__':
    inp = WusnInput.from_file('small_data/001.test')
    indv = kmeans_random(inp)
    out = ind_to_output(indv, inp)
