import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import argparse
import re

class Plot:

    def __init__(self, 
                fileName='', 
                setPalette='colorblind', 
                graphType='line',
                output= '.pdf', 
                x=0, 
                y='1', 
                symbols='ball', 
                distBetSymbols=None, 
                symbolSize=None, 
                figSize=None, 
                fontSize=None, 
                legendFontSize=None,
                lineWidth=None,
                plotTitle=None,
                xLabel=None,
                yLabel=None,
                cmd=False ):
        if cmd:
            # if it is called by command line
            self.parseCmd()
        else:
            # if it is called by another program
            self.fileName = fileName
            self.setPalette = setPalette 
            self.graphType = graphType
            self.output = output 
            self.x = x 
            self.y = y 
            self.symbols = symbols 
            self.distBetSymbols = distBetSymbols 
            self.symbolSize = symbolSize
            self.figSize = figSize
            self.fontSize= fontSize
            self.legendFontSize=legendFontSize
            self.lineWidth=lineWidth
            self.plotTitle=plotTitle
            self.xLabel=xLabel
            self.yLabel=yLabel


    def parseCmd(self):
        #parses arguments
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""I can plot 4 types of graphs: Bar, Line, Pie and Scatter""")
        self.parser.add_argument("-f","--fileName", help="Name of the file that will provide data for the graph: name.extension", required=True)
        self.parser.add_argument("-p", "--setPalette", help="Graph color palette", default="colorblind",  choices=['deep', 'pastel', 'muted', 'bright', 'dark', 'colorblind'])
        self.parser.add_argument("-g","--graphType", help="Type of graph that will be plotted", default="line", choices=['line', 'pie', 'bar', 'scatter'])
        self.parser.add_argument("-o","--output", help="Name and/or extension of the desired output file", default=".pdf")
        self.parser.add_argument("-x", "--x", help="The abscissa of the graph", default=0)
        self.parser.add_argument("-y", "--y", help="The ordinate(s) of the graph", default='1')
        self.parser.add_argument("-s", "--symbols", help="Shape of the symbols used", default=("ball" ,))
        self.parser.add_argument("-d", "--distBetSymbols", help="Distance between each symbol", default=None)
        self.parser.add_argument("-ss", "--symbolSize", help="Size of each symbol", default=None)
        self.parser.add_argument("-fig", "--figSize", help="Size of the graph", default=None)
        self.parser.add_argument("-fs","--fontSize",help="Size of the font used in the graph itself", default=None)
        self.parser.add_argument("-lfs", "--legendFontSize", help="Size of the graphs legend", default=None)
        self.parser.add_argument("-l", "--lineWidth", help="Size of the line on a Line graph", default=None)
        self.parser.add_argument("-plot", "--plotTitle", help="Title that appears at the top of the graph", default=None)
        self.parser.add_argument("-xl", "--xLabel", help="Label of the abscissa", default=None)
        self.parser.add_argument("-yl", "--yLabel", help="Label of the ordinate(s)", default=None)
        
        # and put the values in the class variables
        args = self.parser.parse_args()
        self.fileName = args.fileName
        self.setPalette = args.setPalette 
        self.graphType = args.graphType
        self.output = args.output 
        self.x = args.x 
        self.y = args.y 
        self.symbols = args.symbols 
        self.distBetSymbols = args.distBetSymbols 
        self.symbolSize = args.symbolSize
        self.figSize = args.figSize
        self.fontSize = args.fontSize
        self.legendFontSize = args.legendFontSize
        self.lineWidth = args.lineWidth
        self.plotTitle = args.plotTitle
        self.xLabel = args.xLabel
        self.yLabel = args.yLabel


    def importFile(self):
        fileName = self.fileName
        print(fileName)
        
        if type(fileName) == str:
            sep=' '
            if ',' in fileName:
                sep = ','
            
            fileName = fileName.split(sep)

        handlers = []
        for files in fileName:
            name, ext = files.split('.')
            
            if ext:
                # opens a single file
                pass
            else:
                # opens a full directory
                pass
        

    def defineAxis(self):
        y = self.y
        #splits y in every comma, to get every interval/value separated
        y = y.split(',')

        # the set that will store the values
        # the data structure is a set to make sure that there will be no repeated values
        values = set()

        for interval in y:
            # for every value in the list, check if it is an interval or a single value
            val = interval.split('-')
            
            # if it's a list, then it's an interval
            if len(val) > 1:
                # gets the limits
                val = [int(x) for x in val]
                low_limit = min(val)
                high_limit = max(val)
                # adds each value
                for k in range(low_limit, high_limit):
                    values.add(k)
                continue

            #otherwise, it's a single value and just add it to the set
            values.add(int(val[0]))
        
        # transform to a list
        values = list(values)
        # sort the values to get them in order
        values.sort()

        self.y = values


    def exportFile(self):

        outName=self.output
        fName=self.fileName

        #defines regex`s that search specific combinations
        containsExt = re.compile('^\.\w+')
        containsNameExt = re.compile('^.+\.\w+')
        containsPath1 = re.compile('\\.+')
        containsPath2 = re.compile('/')

        #if the variable was used
        if outName != '.pdf':

            path=''
            #if the file name cointains a file path, then it`s separated into a differente variable
            if containsPath1.match(fName) or containsPath2.match(fName):
                removeName = fName
                while removeName[-1] != '/' and removeName[-1] != '\\' and removeName != '':
                    print(removeName)

                    removeName = removeName[:-1]
                if removeName != '':
                    path = removeName

            #if the output name only contains the extension
            if containsExt.match(outName):
                #checks if the fileName contains an extension
                if containsNameExt.match(fName):
                    removeName = fName
                    #removes the extension from filename
                    while removeName[-1] != '.' and removeName != '':
                        removeName = removeName[:-1]
                    if removeName[-1] == '.':
                        removeName = removeName[:-1]
                    if removeName != '':
                        fName = removeName
                newName=fName
                ext=outName.replace(".","")
                add = 'Plot.'

            #if the output name contains an extension and a name
            elif containsNameExt.match(outName):
                [newName, ext] = outName.split('.')
                add = '.'
                newName = path + newName

            #search if given extension is supported
            if re.search("^(eps|jpeg|jpg|pdf|pgf|png|ps|raw|rgba|svg|svgz|tif|tiff)$", ext):
                plt.savefig(newName + add + ext, bbox_inches="tight")
            else:
                print("Extension not supported")

        else:
            #checks if the fileName contains an extension
            if containsNameExt.match(fName):
                #removes the extension from filename
                rmvName = fName
                while rmvName[-1] != '.' and rmvName != '':
                    rmvName = rmvName[:-1]
                if rmvName[-1] == '.':
                    rmvName = rmvName[:-1]
                if rmvName != '':
                    fName=rmvName
            plt.savefig(fName+'Plot'+outName, bbox_inches="tight")


if __name__ == "__main__":
    instance = Plot(cmd=True)
    instance.exportFile()
