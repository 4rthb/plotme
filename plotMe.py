import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import argparse
import re

class plot:

    def __init__(self):
        #parses arguments
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""I can plot 4 types of graphs: Bar, Line, Pie and Scatter""")
        self.parser.add_argument("-f","--fileName", help="Name of the file that will provide data for the graph: name.extension", required=True)
        self.parser.add_argument("-p", "--setPalette", help="Graph color palette", default="colorblind",  choices=['deep', 'pastel', 'muted', 'bright', 'dark', 'colorblind'])
        self.parser.add_argument("-g","--graphType", help="Type of graph that will be plotted", default="line", choices=['line', 'pie', 'bar', 'scatter'])
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

    def fileWise(self):
        outName = self.args.output
        fName = self.args.fileName

        def exportFile(outName,fName):
            pattern1 = re.compile('^\.\w+')
            pattern2 = re.compile('^.+\.\w+')

            if pattern1.match(outName):
                #only the extension
                if pattern2.match(fName):
                    #checks if the fileName contains an extension
                    [fName, ext] = fName.split('.')

                outName=outName.replace(".","")

                if re.search("^(eps|jpeg|jpg|pdf|pgf|png|ps|raw|rgba|svg|svgz|tif|tiff)",outName):
                    #search if given extension is supported
                    plt.savefig(fName+'Plot.'+outName, bbox_inches="tight")
                else:
                    print("Extension not supported")

            elif pattern2.match(outName):
                #extension and name
                [outName, ext] = outName.split('.')
                if re.search("^(eps|jpeg|jpg|pdf|pgf|png|ps|raw|rgba|svg|svgz|tif|tiff)",ext):
                    #search if given extension is supported
                    plt.savefig(outName+'.'+ext, bbox_inches="tight")
                else:
                    print("Extension not supported")

            else:
                plt.savefig(outName+'.pdf', bbox_inches="tight")



        exportFile(outName,fName)

if __name__ == "__main__":
    instance = plot()
    print(instance.fileWise())
