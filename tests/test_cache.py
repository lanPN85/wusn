import sys
sys.path.append('.')

from wusn.commons import WusnInput


if __name__ == '__main__':
    inp1 = WusnInput.from_file('small_data/001.test', ignore_cache=True)
    inp1.cache_losses()
    inp2 = WusnInput.from_file('small_data/001.test', ignore_cache=False)
