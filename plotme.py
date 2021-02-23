import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import re
import ast

class Plot:

    def __init__(self, 
                fileName='', 
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
                cmd=False ):
        if cmd:
            # if it is called by command line
            self.parseCmd()
        else:
            # if it is called by another program
            self.fileName = fileName
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
        self.parser.add_argument("-s", "--symbols", help="Shape of the symbols used", default=(".",))
        self.parser.add_argument("-d", "--distBetSymbols", help="Distance between each symbol", default=None)
        self.parser.add_argument("-ss", "--symbolSize", help="Size of each symbol", default=(2,))
        self.parser.add_argument("-fig", "--figSize", help="Size of the graph", default=None)
        self.parser.add_argument("-fs","--fontSize",help="Size of the font used in the graph itself", default=None)
        self.parser.add_argument("-l", "--lineWidth", help="Size of the line on a Line graph", default=(1,))
        self.parser.add_argument("-plot", "--plotTitle", help="Title that appears at the top of the graph", default=None)
        self.parser.add_argument("-xl", "--xLabel", help="Label of the abscissa", default=None)
        self.parser.add_argument("-yl", "--yLabel", help="Label of the ordinate(s)", default=None)
        self.parser.add_argument("-pl", "--pieLabel", help="Labels of the data in the pie plot", default=None)
        
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


    def plotGraph(self):
        # get the files to be plot
        files = self.importFile()
        # get the name of the files
        inputNames = self.parseInput()
        # get the color palette
        colors = self.getPalette()
        # get the output names
        outputNames = self.parseOutput(len(files))
        # get the graph types
        graphTypes = self.parseGraph(len(files))
        # get the widths of the line graphs
        lineWidths = self.parseLines(len(files))
        # get the symbols and symbol sizes of the scatter graphs
        markers, mrkrSizes, mrkrDist = self.parseSymbols(len(files))
        # get the axis
        yInput = self.defineAxis()
        # parses plotTitle, fontsize, legendFontsize, ylabel, xlabel and pieLabels
        plotTitle = self.parseIn(self.plotTitle)
        fontSizes = self.parseIn( self.fontSize, ftype=int)
        pieLabels = self.parseIn(self.pieLabel)
        yLabels = self.parseIn(self.yLabel)
        xLabels = self.parseIn(self.xLabel)


        # plot each file individually
        for count, f in enumerate(files):

            columns = f.columns
            if graphTypes[count] != 'pie':
                yAxis = [ columns[ind] for ind in yInput ]
            else:
                yAxis = [str(integer) for integer in yInput]
                yAxis = "".join(yAxis)
                yAxis = int(yAxis)

            # get the list of the parameters
            args = self.getParameters(yAxis, self.x, colors, lineWidths, markers, mrkrSizes, mrkrDist, graphTypes[count], plotTitle, fontSizes, yLabels, xLabels, pieLabels)

            # make the correct type of graph
            if graphTypes[count] == 'line':
                f.plot(kind='line', **args)
            elif graphTypes[count] == 'pie':
                f.plot(kind='pie', **args)
            elif graphTypes[count] == 'bar':
                f.plot(kind='bar', **args)
            elif graphTypes[count] == 'scatter':
                f.plot(kind='scatter', **args)
            
            # finally, export the files
            self.exportFile(outputNames[count], inputNames[count])


    def getParameters(self, y, x, color, lineWidths, markers, mrkrSizes, mrkrDist, graphType, plotTitle, fontSizes, yLabels, xLabels, pieLabels):
        # dictionary of arguments
        # some types of graphs don`t accept some arguments, so they need to be checked beforehand and evaluated
        args = {}

        args['y'] = y
        if graphType != 'pie':
            args['x'] = x

        if graphType == 'pie' and pieLabels:
            args['labels'] = pieLabels

        if graphType != 'scatter' and graphType != 'pie':
            args['color'] = color
        elif graphType != 'pie':
            col = tuple([ int( 255*n ) for n in color[0] ]) 
            args['c'] = '#%02x%02x%02x' % col

        if self.figSize:
            args['figsize'] = self.figSize.split(',')
            args['figsize'] = [ int(num) for num in args['figsize'] ]
            
            if len(args['figsize']) > 2:
                raise Exception('Invalid dimension for figSize parameter')
            
            args['figsize'] = tuple(args['figsize'])
        
        if graphType == 'line':
            if lineWidths and len(lineWidths)!=1:
                args['linewidth'] = lineWidths.pop(0)
            if mrkrSizes and len(mrkrSizes)!=1:
                args['markersize'] = mrkrSizes.pop(0)
            if mrkrDist and len(mrkrDist)!=1 and type(mrkrDist) != int and type(mrkrDist) != float:
                args['markevery'] = mrkrDist.pop(0)

        if graphType == 'line' or graphType == 'scatter':
            if markers and len(markers)!=1:
                args['marker'] = markers.pop(0)
        
        if graphType == 'scatter':
            if mrkrSizes and len(mrkrSizes)!=1:
                args['s'] = mrkrSizes.pop(0)

        if plotTitle:
            args['title'] = plotTitle.pop(0)
        
        if fontSizes and len(fontSizes)!=1:
            args['fontsize'] = fontSizes.pop(0)

        if yLabels and len(yLabels)!=1:
            args['ylabel'] = yLabels.pop(0)
        if xLabels and len(xLabels)!=1:
            args['xlabel'] = xLabels.pop(0)

        return args


    def openFile(self, name):
        df = pd.read_csv(name, sep=self.sep, comment='#', engine='python')
        return df


    def getPalette(self):
        '''
        deep, muted, pastel, bright, dark, and colorblind
        '''
        return sns.color_palette(self.Palette)


    def parseInput(self):
        fileName = self.fileName

        # if the fileName came from the command line, transform it to a list
        if type(fileName) == str:
            fileName = fileName.split(',')
        
        # otherwise, there's nothing to be done
        return fileName


    def parseOutput(self, arrayLen):
        # get the output names that are given
        name = self.output

        # split in order to separate, if it comes from the command line
        if type(name) == str:
            name = name.split(',')

        # if output names given are less than files to be plot, append the default (.pdf) until both have the same length
        while len(name) < arrayLen:
            name.append('.pdf')

        # if there are more outputs than files, return only the ones that can be used
        return name[:arrayLen]


    def parseIn(self, arg, ftype=str):
        # Generic parse function
        if not arg:
            return []

        if type(arg) == str:
            arg = arg.split(',')
        
        if ftype == int:
            arg = [ int(x) for x in arg ]

        return arg


    def parseGraph(self, arrayLen):
        # get the graph types that are given
        typeG = self.graphType

        # split in order to separate, if it comes from the command line
        if type(typeG) == str:
            typeG = typeG.split(',')

        # removes blank spaces
        for graph in typeG:
            graph = graph.strip()

        # if graph types given are less than files to be plot, append the last type until both have the same length
        while len(typeG) < arrayLen:
            typeG.append(typeG[-1])

        # if there are more outputs than files, return only the ones that can be used
        return typeG[:arrayLen]


    def parseSymbols(self, arrayLen):
        # get the symbols properties that are given
        markers = list(self.symbols)
        mrkrSizes = self.symbolSize
        mrkrDist = self.distBetSymbols

        # split in order to separate, if it comes from the command line
        if type(markers) == str:
            markers = markers.split(',')
            mrkrSizes = mrkrSizes.split(',')

        # gets the correct values
        mrkrSizes = [float(nm) for nm in mrkrSizes]

        # evens the lengths of the lists
        while len(markers) != len(mrkrSizes):
            if len(markers) > len(mrkrSizes):
                mrkrSizes.append(mrkrSizes[-1])
            else:
                markers.append(markers[-1])
        # checks if the distance between arguments was passed, so that there are no problems dealing with iteration on
        # type None
        if mrkrDist:
            mrkrDist = ast.literal_eval(mrkrDist)
            if type(mrkrDist) != int and type(mrkrDist) != float:
                mrkrDist = list(mrkrDist)
                while len(markers) != len(mrkrDist):
                    if len(markers) > len(mrkrDist):
                        mrkrDist.append(mrkrDist[-1])
                    else:
                        markers.append(markers[-1])
            # if there are more symbols than files, return only the ones that can be used
                return markers[:arrayLen], mrkrSizes[:arrayLen], mrkrDist[:arrayLen]
            return markers[:arrayLen], mrkrSizes[:arrayLen], mrkrDist

        # if there are more symbols than files, return only the ones that can be used
        return markers[:arrayLen], mrkrSizes[:arrayLen], mrkrDist


    def parseLines(self, arrayLen):
        # get the line widths that are given
        lineW = self.lineWidth

        # split in order to separate, if it comes from the command line
        if type(lineW) == str:
            lineW = lineW.split(',')

        # gets the float values
        lineW = [float(n) for n in lineW]

        # if there are more outputs than files, return only the ones that can be used
        return lineW[:arrayLen]


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


    def importFile(self):
        
        fileName = self.parseInput()

        # for every file in the list, open it 
        handlers = []
        for files in fileName:

            handlers.append( self.openFile(files) )

        return handlers


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


if __name__ == "__main__":
    instance = Plot(cmd=True)
    sns.set()
    instance.plotGraph()