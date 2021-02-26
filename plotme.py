import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import re
import ast

class Plot:
    def __init__(self, 
                data=None, 
                setPalette='colorblind', 
                graphType='line',
                output= '.pdf', 
                separator = ',',
                x='0', 
                y='1',
                symbols='.',
                distBetSymbols=None, 
                symbolSize=(2,),
                figSize=None, 
                fontSize=None,
                lineWidth=(1,),
                plotTitle=None,
                xLabel=None,
                yLabel=None,
                pieLabel=None,
                label=True,
                cmd=False ):

        if cmd:
            # if it is called by command line
            self.parseCmd()
        else:
            # if it is called by another program
            self.data = data
            self.fileName = ''
            self.Palette = setPalette 
            self.graphType = graphType
            self.output = output 
            self.sep = separator
            self.x = int(x) 
            self.y = y 
            self.symbols = symbols 
            self.distBetSymbols = distBetSymbols 
            self.symbolSize = symbolSize
            self.figSize = figSize
            self.fontSize= fontSize
            self.lineWidth=lineWidth
            self.plotTitle=plotTitle
            self.xLabel=xLabel
            self.yLabel=yLabel
            self.pieLabel=pieLabel
            self.label = label

    def parseCmd(self):
        #parses arguments
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="""I can plot 4 types of graphs: Bar, Line, Pie and Scatter""")
        self.parser.add_argument("-f","--fileName", help="Name of the file that will provide data for the graph: name.extension", required=True)
        self.parser.add_argument("-p", "--setPalette", help="Graph color palette", default="colorblind",  choices=['deep', 'pastel', 'muted', 'bright', 'dark', 'colorblind'])
        self.parser.add_argument("-g","--graphType", help="Type of graph that will be plotted", default="line")
        self.parser.add_argument("-o","--output", help="Name and/or extension of the desired output file", default=".pdf")
        self.parser.add_argument("-sep", "--separator", help="Defines the separator used in the file parse", default=',')
        self.parser.add_argument("-x", "--x", help="The abscisse of the graph", default=0)
        self.parser.add_argument("-y", "--y", help="The ordinate(s) of the graph", default='1')
        self.parser.add_argument("-s", "--symbols", help="Shape of the symbols used", default=None)
        self.parser.add_argument("-d", "--distBetSymbols", help="Distance between each symbol", default=None)
        self.parser.add_argument("-ss", "--symbolSize", help="Size of each symbol", default=None)
        self.parser.add_argument("-fig", "--figSize", help="Size of the graph", default=None)
        self.parser.add_argument("-fs","--fontSize",help="Size of the font used in the graph itself", default=None)
        self.parser.add_argument("-l", "--lineWidth", help="Size of the line on a Line graph", default=None)
        self.parser.add_argument("-plot", "--plotTitle", help="Title that appears at the top of the graph", default=None)
        self.parser.add_argument("-xl", "--xLabel", help="Label of the abscissa", default=None)
        self.parser.add_argument("-yl", "--yLabel", help="Label of the ordinate(s)", default=None)
        self.parser.add_argument("-pl", "--pieLabel", help="Labels of the data in the pie plot", default=None)
        self.parser.add_argument("-lab", "--label", help="Label to be put as a description in the plot", default=True, choices=['True', 'False'])

        # and put the values in the class variables
        args = self.parser.parse_args()
        self.fileName = args.fileName
        self.Palette = args.setPalette 
        self.graphType = args.graphType
        self.output = args.output 
        self.sep = args.separator
        self.x = int(args.x) 
        self.y = args.y 
        self.symbols = args.symbols 
        self.distBetSymbols = args.distBetSymbols 
        self.symbolSize = args.symbolSize
        self.figSize = args.figSize
        self.fontSize = args.fontSize
        self.lineWidth = args.lineWidth
        self.plotTitle = args.plotTitle
        self.xLabel = args.xLabel
        self.yLabel = args.yLabel
        self.pieLabel = args.pieLabel
        if args.label == 'False':
            self.label = False
        else:
            self.label = True

        self.data = self.openFile( self.fileName )

    def plotGraph(self):
        data = self.data
        # get the color palette
        color = self.getPalette()
        # get the symbols and symbol sizes of the scatter graphs
        yInput = self.defineAxis()
    
        columns = data.columns
        if self.graphType != 'pie':
            yAxis = [ columns[ind] for ind in yInput ]
        else:
            yAxis = [str(integer) for integer in yInput]
            yAxis = "".join(yAxis)
            yAxis = int(yAxis)

        # get the list of the parameters
        args = self.getParameters(yAxis, color)

        # make the correct type of graph
        if self.graphType == 'line':
            data.plot(kind='line', **args)
        elif self.graphType == 'pie':
            data.plot(kind='pie', **args)
        elif self.graphType == 'bar':
            data.plot(kind='bar', **args)
        elif self.graphType == 'scatter':
            data.plot(kind='scatter', **args)
            
        # finally, export the file
        self.exportFile(self.output, self.fileName)

    def getParameters(self, y, color):
        # dictionary of arguments
        # some types of graphs don`t accept some arguments, so they need to be checked beforehand and evaluated
        args = {}

        args['y'] = y
        if self.graphType != 'pie':
            args['x'] = self.x

        if self.graphType == 'pie' and self.pieLabel:
            args['labels'] = self.pieLabel

        if self.graphType != 'scatter' and self.graphType != 'pie':
            args['color'] = color
        elif self.graphType == 'scatter':
            col = tuple([ int( 255*n ) for n in color[0] ]) 
            args['c'] = '#%02x%02x%02x' % col

        if self.figSize:
            args['figsize'] = self.figSize.split(',')
            args['figsize'] = [ int(num) for num in args['figsize'] ]
            
            if len(args['figsize']) > 2:
                raise Exception('Invalid dimension for figSize parameter')
            
            args['figsize'] = tuple(args['figsize'])
        
        if self.graphType == 'line':
            if self.lineWidth:
                self.lineWidth = [str(width) for width in self.lineWidth]
                self.lineWidth = "".join(self.lineWidth)
                args['linewidth'] = self.lineWidth
            if self.symbolSize:
                if self.symbolSize != float and self.symbolSize != float:
                    self.symbolSize = [str(floatpoint) for floatpoint in self.symbolSize]
                    self.symbolSize = "".join(self.symbolSize)
                args['markersize'] = float(self.symbolSize)
            if self.distBetSymbols and type(self.distBetSymbols) != int and type(self.distBetSymbols) != float:
                args['markevery'] = ast.literal_eval(self.distBetSymbols)
                args['markevery'] = self.distBetSymbols

        if self.graphType == 'line' or self.graphType == 'scatter':
            if self.symbols:
                args['marker'] = self.symbols
        
        if self.graphType == 'scatter':
            if self.symbolSize:
                args['s'] = self.symbolSize

        if self.plotTitle:
            args['title'] = self.plotTitle
        
        if self.fontSize:
            args['fontsize'] = self.fontSize

        if self.yLabel:
            args['ylabel'] = self.yLabel
        if self.xLabel:
            args['xlabel'] = self.xLabel

        return args

    def openFile(self, name):

        args = {}
        if not self.label:

            args['header'] = None

        df = pd.read_csv(name, sep=self.sep, comment='#', engine='python', **args)
        
        return df

    def getPalette(self):
        '''
        deep, muted, pastel, bright, dark, and colorblind
        '''
        return sns.color_palette(self.Palette)

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

        return values

    def exportFile(self, outName, fName):

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

            print(f'File {fName}Plot{outName} saved succesfully')

if __name__ == "__main__":
    instance = Plot(cmd=True)
    sns.set()
    instance.plotGraph()