import matplotlib.pyplot as plt
import os

from mpl_toolkits.mplot3d import Axes3D
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

from wusn.commons import WusnOutput, WusnInput


if __name__ == '__main__':
    history = InMemoryHistory()
    plt.ioff()

    print('Enter a path to an input/output file to view its plot.')
    print('Ctrl+C or Ctrl+D to exit.')

    try:
        while True:
            path = prompt('> ', history=history)
            if not os.path.exists(path):
                print('No such path exists.')
                continue

            try:
                if path.endswith('.test'):
                    obj = WusnInput.from_file(path)
                else:
                    obj = WusnOutput.from_text_file(path)
            except Exception:
                print('Failed to open file.')
                continue

            fig = plt.figure()
            ax = Axes3D(fig)
            obj.plot(ax, highlight_max=False)
            ax.legend()
            plt.show()
            fig.clf()

    except (KeyboardInterrupt, EOFError):
        print()
