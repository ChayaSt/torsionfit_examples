import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import torsionfit.backends.sqlite_plus as sqlite

from matplotlib.backends.backend_pdf import PdfPages


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Plot deviance')
    parser.add_argument('-f', '--filename', type=str,
                        help="name of file")
    parser.add_argument('-n', '--dbname', type=str,
                        help="name of database")
    parser.add_argument('-b', '--burn', type=str,
                        help="where to start plotting")
    parser.add_argument('-t', '--thin', type=str,
                        help="how much to thin for plotting")

    args = parser.parse_args()

    with PdfPages(args.filename) as pdf:
        for i in range(2):
            db = sqlite.load('{}_{}/{}_{}.sqlite'.format(args.dbname, i, args.dbname, i))
            plt.plot(db.deviance[int(args.burn)::int(args.thin)], alpha=0.4, linewidth=0.4)
            del db
        plt.xlabel('time')
        plt.ylabel('Deviance')
        pdf.savefig()
