import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import re
import ast
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
try:
    from matplotlib.colors import TwoSlopeNorm as nrm
except:
    from matplotlib.colors import DivergingNorm as nrm

class Plot:
    def __init__(self, 
                data=None, 
                setPalette='colorblind', 
                graphType='line',
                output= '.pdf', 
                separator = ',',
                x='1',
                y='2',
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
                bgColor = 'lightgrey',
                gColor = "grey",
                colors = None,
                showSpine = True,
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
            if int(x)>0:
                self.x = int(x) - 1
            else:
                 raise ValueError(x + " is not a valid column index")
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
            self.bgColor = bgColor
            self.gColor = gColor
            self.colors = colors
            self.showSpine = showSpine
        self.colorMap = {"lightblue": -1, "yellow": 0.75, "grey": 0.5, "lightpink": 0.25, "brown": 0.1,
                         "pink": -0.1, "orange": -0.25, "green": -0.5, "dark yellow": -0.75, "blue": -1}

    def parseCmd(self):
        #parses arguments
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="""I can plot 4 types of graphs: Bar, Line, Pie and Scatter""")
        fileHandler = self.parser.add_argument_group("File handling arguments","The arguments that handle the data from the input file")
        fileHandler.add_argument("-f","--fileName", help="Name of the file that contains the data for the graph: name.extension", required=True)
        fileHandler.add_argument("-sep", "--separator", help="Defines the separator used in the input file, for parsing purposes.\nValid arguments: ' ', '\\t', regular expressions and other file delimiters", default=',')
        fileHandler.add_argument("-o","--output", help="Name and/or extension of the output file.\nValid arguments: '.png', 'name', 'name.png'", default=".pdf")
        fileHandler.add_argument("-x", "--x", help="The x axis of the plot.\nValid arguments: Indexes of columns", default=1)
        fileHandler.add_argument("-y", "--y", help="The y axis of the plot.\nValid arguments: Indexes of columns(value, list [ex: 2,3,4] or sequences [ex: 2-4])", default='2')
        fileHandler.add_argument("-g","--graphType", help="Type of graph that will be plotted", default="line",  choices=['line', 'pie', 'bar', 'scatter'])
        fileHandler.add_argument("-hd", "--header", help="Ignores the # lines in the file", default=True, choices=['True', 'False'])
        markers = self.parser.add_argument_group("Marker arguments","Arguments that handle the markers")
        markers.add_argument("-s", "--symbols", help="Shape of the symbols used.\nValid arguments: Lists [ex: vhD] or values\nFor valid markers: https://matplotlib.org/stable/api/markers_api.html)", default=None)
        markers.add_argument("-d", "--distBetSymbols", help="Distance between each symbol\nValid Arguments: None, int, float, (int,int), [float,float], [int,int,int],(float,float,float)", default=None)
        markers.add_argument("-ss", "--symbolSize", help="Size of each symbol.\nValid arguments: float", default=None)
        aesthetic = self.parser.add_argument_group("Image parameters","Arguments that handle color and other image features")
        aesthetic.add_argument("-p", "--setPalette", help="Graph color palette", default="colorblind",  choices=['deep', 'pastel', 'muted', 'bright', 'dark', 'colorblind'])
        aesthetic.add_argument("-bgc", "--bgColor", help="Changes the color of the background.\nValid arguments: 'red','black','lightyellow','#abc','#ff701E'\nSee https://matplotlib.org/stable/tutorials/colors/colors.html for more examples", default="lightgrey")
        aesthetic.add_argument("-gc", "--gColor", help="Changes the color of the graph`s grid.\nValid arguments: 'red','black','lightyellow','#abc','#ff701E'\nSee https://matplotlib.org/stable/tutorials/colors/colors.html for more examples", default="grey")
        aesthetic.add_argument("-c", "--colors", help="Selects the colors of the plotted abscissa(s).\nValid arguments: ", default=None)
        aesthetic.add_argument("-fig", "--figSize", help="Size of the graph and the exported image .\nValid arguments: (float,float) in inches", default=None)
        aesthetic.add_argument("-st", "--showSpine", help="Removes the spines from the graph", default='True', choices=['True', 'False'])
        self.writing = self.parser.add_argument_group("Writing arguments", "Parameters that handle the written words in the plot")
        self.writing.add_argument("-l", "--lineWidth", help="Size of the line on a Line plot.\nValid arguments: float", default=None)
        self.writing.add_argument("-pt", "--plotTitle", help="Title that appears at the top of the plot.\nValid arguments: string", default=None)
        self.writing.add_argument("-xl", "--xLabel", help="Label of the abscissa.\nValid arguments: string", default=None)
        self.writing.add_argument("-yl", "--yLabel", help="Label of the ordinate(s).\nValid arguments: string", default=None)
        self.writing.add_argument("-pl", "--pieLabel", help="Labels of the data in the pie plot.\nValid arguments: strings, the number must match the number of y indexes", default=None)
        self.writing.add_argument("-fs","--fontSize",help="Size of the font used in the graph itself.\nValid arguments: int", default=None)
        
        # and put the values in the class variables
        args = self.parser.parse_args()
        self.fileName = args.fileName
        self.Palette = args.setPalette 
        self.graphType = args.graphType
        self.output = args.output 
        self.sep = args.separator
        if int(args.x)>0:
            self.x = int(args.x) - 1
        else:
            raise ValueError(args.x + " is not a valid column index")
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
        if args.header == 'False':
            self.header = False
        else:
            self.header = True
        self.data = self.openFile( self.fileName )
        self.bgColor = args.bgColor
        self.gColor = args.gColor
        self.colors = args.colors
        if args.showSpine == 'True':
            self.showSpine = True
        else:
            self.showSpine = False

    def plotGraph(self):
        data = self.data
        # get the color palette
        cmap = self.getPalette()
        # get the symbols and symbol sizes of the scatter graphs
        yInput = self.defineAxis()
    
        columns = data.columns
        if self.graphType != 'pie':
            yAxis = [ columns[ind] for ind in yInput ]
        else:
            yAxis = [str(integer) for integer in yInput]
            yAxis = "".join(yAxis)
            yAxis = int(yAxis)

        if self.colors:
            self.colors = self.colors.split(',')
            if len(self.colors) != len(yAxis):
                raise ValueError("The number of declared colors is different than the number of abscissas")

        # get the list of the parameters
        args = self.getParameters(yAxis, cmap, columns[self.x])

        fig, ax1 = plt.subplots(facecolor=self.bgColor, constrained_layout=True)
        # make the correct type of graph
        if self.graphType == 'line':
            data.plot(kind='line', ax=ax1, **args)
        elif self.graphType == 'pie':
            data.plot(kind='pie', ax=ax1, **args)
        elif self.graphType == 'bar':
            data.plot(kind='bar', ax=ax1, **args)
        elif self.graphType == 'scatter':
            yAx = args['y']
            args.pop('y')
            symb = 0
            i=0
            norm = nrm(vmin=-1,vmax=1,vcenter=0)
            if 'marker' in args:
                symb = args['marker']
                args['marker'] = symb[0]
            dist = 0
            if 'markevery' in args:
                dist = args['markevery']
                args.pop('markevery')
                data.drop(data.loc[::dist,:].index, inplace=True)
            color=-1.1
            while yAx:
                if not self.colors:
                    color+=0.2
                    if color>1:
                        color-=2
                else:
                    if self.colors[i] not in self.colorMap:
                        raise ValueError('Color not compatible')
                    color=self.colorMap[self.colors[i]]
                data.plot(kind='scatter', ax=ax1, y=yAx[0], c=np.repeat(color,len(data)), norm=norm, **args)
                fig.delaxes(fig.axes[-1])
                yAx.pop(0)
                if symb:
                    if len(symb)>1:
                        symb.pop(0)
                    args['marker'] = symb[0]
                i+=1

        # finally, export the file
        ax1.set_facecolor(self.bgColor)
        ax1.set_clip_on(False)
        ax1.tick_params(grid_color=self.gColor)
        if self.showSpine:
            ax1.spines['bottom'].set_visible(False)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['left'].set_visible(False)
        else:
            ax1.spines['bottom'].set_color(self.gColor)
            ax1.spines['top'].set_color(self.gColor)
            ax1.spines['right'].set_color(self.gColor)
            ax1.spines['left'].set_color(self.gColor)
        if self.xLabel:
            ax1.set_xlabel(self.xLabel)
        if self.yLabel:
            ax1.set_ylabel(self.yLabel)
        plt.show()
        self.exportFile(self.output, self.fileName, fig)

    def getParameters(self, y, cmap, x):
        # dictionary of arguments
        # some types of graphs don`t accept some arguments, so they need to be checked beforehand and evaluated
        args = {}

        args['y'] = y
        if self.graphType != 'pie':
            args['x'] = self.x

        if self.graphType == 'pie' and self.pieLabel:
            args['labels'] = self.pieLabel.split(',')

        args['colormap'] = cmap

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

        if self.graphType == 'line' or self.graphType == 'scatter':
            if self.symbols:
                args['marker'] = self.symbols
            if self.graphType == 'scatter' and self.symbols:
                args['marker'] = re.findall(r"\w{1}|[^\w\s]", args['marker'])
            if self.distBetSymbols and type(self.distBetSymbols) != int and type(self.distBetSymbols) != float:
                args['markevery'] = ast.literal_eval(self.distBetSymbols)
        
        if self.graphType == 'scatter':
            if self.symbolSize:
                args['s'] = float(self.symbolSize)

        if self.plotTitle:
            args['title'] = self.plotTitle
        
        if self.fontSize:
            args['fontsize'] = self.fontSize
            
        return args

    def openFile(self, name):

        args = {}
        if not self.header:

            args['header'] = None

        if self.sep == ' ' or self.sep == '':
            self.sep = '\ '

        df = pd.read_csv(name, sep=self.sep, comment='#', engine='python', **args)
        
        return df

    def getPalette(self):
        '''
        deep, muted, pastel, bright, dark, and colorblind
        '''
        return ListedColormap(sns.color_palette(self.Palette))

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
                for k in range(low_limit, high_limit+1):
                    # we put k-1 in order to get the correct index
                    # because the user considers our 0 as 1.
                    values.add(k-1)
                continue

            #otherwise, it's a single value and just add it to the set
            values.add(int(val[0])-1)

        # transform to a list
        values = list(values)
        # sort the values to get them in order
        values.sort()

        return values

    def exportFile(self, outName, fName, fig):

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
            
            #if there is no extension in the output name
            else:
                newName = path = outName
                ext = "pdf"
                add = "."

            #search if given extension is supported
            if re.search("^(eps|jpeg|jpg|pdf|pgf|png|ps|raw|rgba|svg|svgz|tif|tiff)$", ext):
                fig.savefig(newName + add + ext, bbox_inches="tight", facecolor=fig.get_facecolor(), transparent=True)
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
            fig.savefig(fName+'Plot'+outName, bbox_inches="tight", facecolor=fig.get_facecolor(), transparent=True)

            print(f'File {fName}Plot{outName} saved succesfully')

if __name__ == "__main__":
    instance = Plot(cmd=True)
    sns.set()
    instance.plotGraph()