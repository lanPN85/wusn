import sys
sys.path.append('.')

from wusn.exact import solve
from wusn.commons import WusnInput


if __name__ == '__main__':
    inp = WusnInput.from_file('small_data/test/001.test')
    prob = solve.model_lp(inp)
    out = solve.solve_lp(prob, inp)
    print(out.valid)
    out.plot_to_file('tests/test.png')
