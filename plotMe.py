import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import argparse

class plot:

    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""I can plot 4 types of graphs: Bar, Line, Pie and Scatter""")
        self.parser.add_argument("-f","--fileName", help="Name of the file that will provide data for the graph", required=True)
        self.parser.add_argument("-p", "--setPalette", help="Graph color palette", default="colorblind")
        self.parser.add_argument("-g","--graphType", help="Type of graph that will be plotted", default="line")
        self.parser.add_argument("-o","--output", help="Name and/or extension of the desired output file", default=".pdf")
        self.parser.add_argument("-x", "--x", help="The abscissa of the graph", default=0)
        self.parser.add_argument("-y", "--y", help="The ordinate(s) of the graph", default=(1))
        self.parser.add_argument("-s", "--symbols", help="Shape of the symbols used", default=("ball"))
        self.parser.add_argument("-d", "--distBetSymbols", help="Distance between each symbol", default=None)
        self.parser.add_argument("-ss", "--symbolSize", help="Size of each symbol", default=None)
        self.parser.add_argument("-fig", "--figSize", help="Size of the graph", default=None)
        self.parser.add_argument("-fs","--fontSize",help="Size of the font used in the graph itself", default=None)
        self.parser.add_argument("-lfs", "--legendFontSize", help="Size of the graphs legend", default=None)
        self.parser.add_argument("-l", "--lineWidth", help="Size of the line on a Line graph", default=None)
        self.parser.add_argument("-plot", "--plotTitle", help="Title that appears at the top of the graph", default=None)
        self.parser.add_argument("-xl", "--xLabel", help="Label of the abscissa", default=None)
        self.parser.add_argument("-yl", "--yLabel", help="Label of the ordinate(s)", default=None)
        self.args = self.parser.parse_args()

if __name__ == "__main__":
    plot().main()