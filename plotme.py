import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, to_hex
try:
    from matplotlib.colors import TwoSlopeNorm as nrm
except:
    from matplotlib.colors import DivergingNorm as nrm

import argparse

import os

import re
import ast

import pandas as pd
import numpy as np
import itertools

from scipy.integrate import simps, trapz


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
                hideSpine = True,
                sd=False,
                auc=False,
                fileExtension='csv',
                comment="#",
                cmd=False ):

        if cmd:
            # if it is called by command line
            self.parseCmd()
        else:
            # if it is called by another program
            self.data = data if isinstance(data, list) else [data]
            self.fileName = ''
            self.Palette = setPalette 
            self.graphType = graphType
            self.output = output 
            self.sep = separator
            if int(x)>0:
                self.x = int(x) - 1
            else:
                 raise Exception(x + " is not a valid column index")
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
            self.hideSpine = hideSpine
            self.sd = sd
            self.auc = auc
            self.extension = fileExtension
            self.comment = comment
        self.colorMap = {"lightblue": -1, "yellow": 0.75, "grey": 0.5, "lightpink": 0.25, "brown": 0.1,
                         "pink": -0.1, "orange": -0.25, "green": -0.5, "dark yellow": -0.75, "blue": -1}


    def parseCmd(self):
        #parses arguments
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="""I can plot 4 types of graphs: Bar, Line, Pie and Scatter""")
        fileHandler = self.parser.add_argument_group("File handling arguments","The arguments that handle the data from the input file")
        fileHandler.add_argument("-f","--fileName", nargs='+', help="Name of the files that contains the data for the graph: name1.extension name2.extension ..., it can be a directory as well, as long as there are csv files in it", required=True)
        fileHandler.add_argument("-sep", "--separator", help="Defines the separator used in the input file, for parsing purposes.\nValid arguments: ' ', '\\t', regular expressions and other file delimiters\nExamples:\n    python3 plotme.py -f file.txt -sep \\t\nDefault: Comma(,)", default=',')
        fileHandler.add_argument("-o","--output", help="Name and/or extension of the output file.\nValid arguments: '.png', 'name', 'name.png'\nExamples:\n    python3 plotme.py -f file -o outputFile\n    python3 plotme.py -f file -o .tiff\n    python3 plotme.py -f file -o export.jpeg\nDefault: .pdf", default=".pdf")
        fileHandler.add_argument("-x", "--x", help="The x-axis of the plot.\nValid arguments: Indexes of columns\nExamples:\n    python3 plotme.py -f file -x 1\nDefault: 1", default=1)
        fileHandler.add_argument("-y", "--y", help="The y-axis of the plot.\nValid arguments: Indexes of columns(value, list [ex: 2,3,4] or sequences [ex: 2-4])\nExamples:\n    python3 plotme.py -f file -y 5-7\n    python3 plotme.py -f file -y 5,6,7\nDefault: 2", default='2')
        fileHandler.add_argument("-g","--graphType", help="Type of graph that will be plotted\nExamples:\n    python3 plotme.py -f file -g bar\nDefault: line", default="line",  choices=['line', 'pie', 'bar', 'scatter'])
        fileHandler.add_argument("-hd", "--header", help="Ignores lines starting with # in the input file (see -f)\nExamples:\n    python3 plotme.py -f file -hd False\nDefault: True", default=True, choices=['True', 'False'])
        fileHandler.add_argument("-sd", "--standardDeviation", help="Makes a plot of the mean and the stand deaviation pointwise over the whole database, the effect is to put a shadow representing the error\nExamples:\n    python3 plotme.py -f file1 file2 file3 [...] -y 2 -sd\n    python3 plotme.py -f file1 file2 file3 -y 2-4,7 -sd\nDefault: False", action='store_true', default=False)
        fileHandler.add_argument("-auc", "--areaUnderCurve", help="Calculate the area under the curve given the file(s) and the y index(es)\nExamples:\n    python3 plotme.py -f file -y 4-6 -auc\n    python3 plotme.py -f file1 file2 file3 [...] -y 3,4 -auc\nDefault: False", action="store_true", default=False)
        fileHandler.add_argument("-aucm", "--areaUnderCurveMethod", type=str, action='store', choices=['simpson', 'trapz', 'mean'], default='simpson', help='The method that is goind to be used for the auc calculation. It can be the simpson rule, the trapezoidal rule or the mean of them.\nExamples:\n    python3 plotme.py -f file -y 2-4 -auc -aucm simpson\n    python3 plotme.py -f file -y 5 -auc -aucm trapz')
        fileHandler.add_argument("-ext", "--fileExtension", type=str, action='store', default='.csv', help="File extension to be chosen if a directory is passed.\nExamples:\n    python3 plotme.py -f dir -y 3-5 -sd -ext txt")
        fileHandler.add_argument("-com", "--comment", type=str, default="#", action="store", help="The character that will indicate if a line should be treated as comment.\nExamples\n    python3 plotme.py -f file -com @")
        markers = self.parser.add_argument_group("Marker arguments","Arguments that handle the markers")
        markers.add_argument("-s", "--symbols", help="Shape of the symbols used.\nValid arguments: Lists [ex: vhD] or values\nExamples:\n    python3 plotme.py -f file -y 2,3 -s vH\n    python3 plotme.py -f file -y 2-6 -s vHddv\n    python3 plotme.py -f file -y 2-6 -s v\nFor valid markers: https://matplotlib.org/stable/api/markers_api.html)\nDefault: o(circle)", default=None)
        markers.add_argument("-d", "--distBetSymbols", help="Distance between each symbol\nValid Arguments: int\nExamples:\n    python3 plotme.py -f file -d 3\nDefault: 1", default=None)
        markers.add_argument("-ss", "--symbolSize", help="Size of each symbol.\nValid arguments: float\nExamples:\n    python3 plotme.py -f file -s v -ss 15\nDefault: 20", default=None)
        aesthetic = self.parser.add_argument_group("Image parameters","Arguments that handle color and other image features")
        aesthetic.add_argument("-p", "--setPalette", help="Graph color palette\nExamples:\n    python3 plotme.py -f file -p deep\nDefault: colorblind", default="colorblind",  choices=['deep', 'pastel', 'muted', 'bright', 'dark', 'colorblind'])
        aesthetic.add_argument("-bgc", "--bgColor", help="Changes the color of the background.\nValid arguments: 'red','black','lightyellow','#abc','#ff701E'\nExamples:\n    python3 plotme.py -f file -bgc black\n    python3 plotme.py -f file -bgc '#ff701E'\nSee https://matplotlib.org/stable/tutorials/colors/colors.html for more examples\nDefault: lightgrey", default="lightgrey")
        aesthetic.add_argument("-gc", "--gColor", help="Changes the color of the graph`s grid.\nValid arguments: 'red','black','lightyellow','#abc','#ff701E'\nExamples:\n    python3 plotme.py -f file '#abc'\nSee https://matplotlib.org/stable/tutorials/colors/colors.html for more examples\nDefault: grey", default="grey")
        aesthetic.add_argument("-c", "--colors", help="Selects the colors of the plotted y-axes in the scatter and line plots.\nValid arguments: 'red','black','lightyellow','#abc','#ff701E'\nExamples:\n    python3 plotme.py -f file -y 2,4 -c yellow,green\n    python3 plotme.py -f file -y 2,4 -c '#ff701E','#abc'\nSee https://matplotlib.org/stable/tutorials/colors/colors.html for more examples\nDefault: cycles colormap", default=None)
        aesthetic.add_argument("-fig", "--figSize", help="Size of the graph and the exported image (Bounding Box).\nValid arguments: (float,float) in inches\nExamples:\n    python3 plotme.py -f file -fig 192,108\nDefault: 6,5", default=None)
        aesthetic.add_argument("-st", "--hideSpine", help="Removes the spines from the graph\nExamples:\n    python3 plotme.py -f file -st True\nDefault: True", default='True', choices=['True', 'False'])
        aesthetic.add_argument("-l", "--lineWidth", help="Size of the line on a Line plot.\nValid arguments: float\nExamples:\n    python3 plotme.py -f file -l 15\nDefault: 1", default=None)
        text = self.parser.add_argument_group("Text/Font arguments", "Parameters that handle the texts in the plot")
        text.add_argument("-pt", "--plotTitle", help="Title that appears at the top of the plot.\nValid arguments: string\nExamples:\n    python3 plotme.py -f file -pt 'Tile of the plot'\nDefault: None", default=None)
        text.add_argument("-xl", "--xLabel", help="Label of the x-axis.\nValid arguments: string\nExamples:\n    python3 plotme.py -f file -xl 'label of x'\nDefault: header of the x-axis", default=None)
        text.add_argument("-yl", "--yLabel", help="Label of the y-axis.\nValid arguments: string\nExamples:\n    python3 plotme.py -f file -yl 'label of y'\nDefault: header of the last y-axis", default=None)
        text.add_argument("-pl", "--pieLabel", help="Labels of the data in the pie plot.\nValid arguments: strings, the number must match the number of y indexes\nExamples:\n    python3 plotme.py -f file -g pie -pl slice1,'another slice',3\nDefault: 0 - (n-1), n = lenght of y-axis", default=None)
        text.add_argument("-fs","--fontSize",help="Size of the font used in the graph itself.\nValid arguments: int\nExamples:\n    python3 plotme.py -f file -fs 14\nDefault: 10", default=None)
        
        # and put the values in the class variables
        args = self.parser.parse_args()
        self.fileName = args.fileName
        self.Palette = args.setPalette 
        self.graphType = args.graphType
        self.output = args.output 
        self.sep = args.separator
        self.extension = args.fileExtension
        if int(args.x)>0:
            self.x = int(args.x) - 1
        else:
            raise Exception(args.x + " is not a valid column index")
        self.y = self.defineAxis(args.y) 
        self.symbols = args.symbols 
        self.distBetSymbols = args.distBetSymbols 
        self.symbolSize = args.symbolSize
        self.figSize = args.figSize
        self.fontSize = args.fontSize
        self.lineWidth = args.lineWidth
        self.plotTitle = args.plotTitle
        self.xLabel = args.xLabel
        self.yLabel = args.yLabel
        self.comment = args.comment
        self.pieLabel = args.pieLabel
        if args.header == 'False':
            self.header = False
        else:
            self.header = True
        self.data = self.openFile( self.fileName )
        self.bgColor = args.bgColor
        self.gColor = args.gColor
        self.colors = args.colors
        if args.hideSpine == 'True':
            self.hideSpine = True
        else:
            self.hideSpine = False
        self.sd = args.standardDeviation
        self.auc = args.areaUnderCurve
        self.aucm = args.areaUnderCurveMethod


    def getAxisName(self, df, y, x):
        columns = df.columns

        if self.graphType == 'pie':
            yColumns = [ str(integer) for integer in y ]
            yColumns = "".join(yColumns)
            yColumns = int(yColumns)
        else:
            yColumns = [ columns[ind] for ind in y ]

        xColumn = columns[x]

        return columns, yColumns, xColumn


    def plotSD(self, data, yInput, ax1):
        # gets all the columns and y-columns name
        cols, yAxis = [], []
        for df in data:
            col, y, _ = self.getAxisName(df, yInput, self.x)
            cols.append(col)
            yAxis.append(y)

        # get all the stats data - the mean and standard deviation
        stats = []
        for y_count in range(len(yInput)):
            col_data = []

            for file_count in range(len(yAxis)):
                col_data.append(data[file_count][yAxis[file_count][y_count]])
            
            df = pd.concat( col_data, axis=1 )
            stats.append( { 
                'mean': df[ df.columns ].mean(axis=1),
                'std': df[ df.columns ].std(axis=1)
             } )
        
        # create all the datasets containing the mean,std and x information        
        df = []
        for i in range(len(stats)):
            df.append(pd.DataFrame.from_dict(stats[i]))
            df[i]['x'] = data[0][ data[0].columns[ self.x ] ]
        
        # gets the arguments
        args = self.getParameters( x='x', y=['mean'] )

        if self.colors:
            colors=self.colors
        else:
            colors=itertools.cycle(args['colormap'].colors)
        args.pop('colormap')
        markers = args['marker'] if 'marker' in args else ['']
        if 'marker' in args:
            args.pop('marker')

        # finally, makes the plot
        for vals in df:
            color=next(colors)

            vals.plot(kind='line', ax=ax1, marker=markers[0], color=color, **args)
            plt.fill_between(vals['x'], vals['mean']+vals['std'], vals['mean']-vals['std'], color=color, alpha=0.15, rasterized=True)
            
            if len(markers)>1:
                markers.pop(0)
        
        # put the legend of the first csv file
        ax1.legend(yAxis[0])


    def checkConditions(self):
        # check if there's the right number of colors
        if self.colors:
            count = self.colors.split(',')
            self.colors = itertools.cycle(count)
            if len(count) != len(self.y):
                raise Exception("The number of declared colors is different than the number of y-axes")

        # if the conditions for a confidence interval plot doesn't fit, show the error
        if len(self.data)>1:
            if self.auc:
                pass
            elif (self.graphType != 'line' or self.sd!=True):
                raise NotImplementedError('More than one file are allowed only for line plots with confidence intervals and for finding the area under the curve')

        # check if all the dfs have the same number of rows
        rows = len(self.data[0].index)
        for df in self.data:
            if len(df.index) != rows:
                raise Exception("The files that were given have differents numbers of rows, which is incoherent for the analysis")


    def plotControl(self):
        # makes sure all the conditions match and are allowed
        self.checkConditions()
        
        if self.auc:
            intg = Integral(
                file=self.data,
                y=self.y,
                x=self.x,
                method=self.aucm
                )
            intg.prettify( intg.integrate_files() )

        # check if it is a confidence interval plot
        else:
            # initialize the figure and ax
            fig, ax1 = plt.subplots(facecolor=self.bgColor, constrained_layout=True)
            if self.sd:
                # plot the confidence interval
                self.plotSD( self.data,  self.y, ax1)
        
            else:
                # this kinds of plots below only accepts one file
                data = self.data[0]

                # call the right kind of graph
                if self.graphType == 'line':
                    self.plotLine( data, fig, ax1 )
                elif self.graphType == 'bar':
                    self.plotBar( data, fig, ax1 )
                elif self.graphType == 'pie':
                    self.plotPie( data, fig, ax1 )
                elif self.graphType == 'scatter':
                    self.plotScatter( data, fig, ax1 )


            # add the extra features to the plot
            self.ImageConfigurations(fig, ax1)

            # default value: shows plot, else: only saves the image
            if self.output == '.pdf':           
                plt.show()
            
            # saves the figure
            self.exportFile(self.output, self.fileName[0], fig)


    def ImageConfigurations(self, fig, ax1):
        ax1.set_facecolor(self.bgColor)
        ax1.set_clip_on(False)
        ax1.tick_params(grid_color=self.gColor)
        if self.hideSpine:
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


    def plotLine(self, data, fig, ax1):
        # get the name of the y, x and all columns
        columns, yColumns, xColumn = self.getAxisName(data, self.y, self.x)

        # get all the arguments
        args = self.getParameters(xColumn)

        if self.colors:
            colors=self.colors
        else:
            colors=itertools.cycle(args['colormap'].colors)
        args.pop('colormap')
        markers = args['marker'] if 'marker' in args else ['']
        if 'marker' in args:
            args.pop('marker')

        for y in yColumns:
            data.plot(kind='line', ax=ax1, y=y, marker=markers[0], color = next(colors), **args)
            if len(markers)>1:
                markers.pop(0)
        ax1.legend()


    def plotPie(self, data, fig, ax1):
        # get the name of the y, x and all columns
        columns, yColumns, xColumn = self.getAxisName(data, self.y, self.x)

        # get all the arguments
        args = self.getParameters(xColumn, y=yColumns)   

        #plot the graph
        data.plot(kind='pie', ax=ax1, **args)


    def plotBar(self,data, fig, ax1):
        # get the name of the y, x and all columns
        columns, yColumns, xColumn = self.getAxisName(data, self.y, self.x)

        # get all the arguments
        args = self.getParameters(xColumn, y=yColumns)

        data.plot(kind='bar', ax=ax1, **args)


    def plotScatter(self,data, fig, ax1):
        # get the name of the y, x and all columns
        columns, yColumns, xColumn = self.getAxisName(data, self.y, self.x)

        # get all the arguments
        args = self.getParameters(xColumn)   

        ys = yColumns.copy()

        symb = 0
        i=0
        if not self.colors:
            color=itertools.cycle( args['colormap'].colors )
        if 'marker' in args:
            symb = args['marker']
            args['marker'] = symb[0]
        dist = 0
        if 'markevery' in args:
            dist = args['markevery']
            args.pop('markevery')
            data = data.loc[::dist,:]
        while yColumns:
            if not self.colors:
                data.plot(kind='scatter', ax=ax1, y=yColumns[0], color=next(color) ,colorbar=False, **args)
            else:
                data.plot(kind='scatter', ax=ax1, y=yColumns[0], c=next(self.colors), colorbar=False, **args)
            yColumns.pop(0)
            if symb:
                if len(symb)>1:
                    symb.pop(0)
                args['marker'] = symb[0]
            i+=1
        ax1.legend(ys)
        if not self.yLabel:
            plt.ylabel("")


    def getParameters(self,x,y = None):
        # dictionary of arguments
        # some types of graphs don`t accept some arguments, so they need to be checked beforehand and evaluated
        args = {}
        
        # if the y needs to be set
        if y:
            args['y'] = y

        if self.graphType != 'pie':
            args['x'] = x

        if self.graphType == 'pie' and self.pieLabel:
            args['labels'] = self.pieLabel.split(',')

        args['colormap'] = self.getPalette()

        if self.figSize:
            args['figsize'] = self.figSize.split(',')
            args['figsize'] = [ int(num) for num in args['figsize'] ]
            
            if len(args['figsize']) > 2:
                raise Exception('Invalid dimension for figSize parameter')
            
            args['figsize'] = tuple(args['figsize'])
        
        if self.graphType == 'line':
            if self.symbols:
                args['marker'] = list(self.symbols)
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
            if self.distBetSymbols and type(self.distBetSymbols) != int and type(self.distBetSymbols) != float:
                args['markevery'] = ast.literal_eval(self.distBetSymbols)
        
        if self.graphType == 'scatter':
            if self.symbols:
                args['marker'] = list(self.symbols)
            if self.symbolSize:
                args['s'] = float(self.symbolSize)

        if self.plotTitle:
            args['title'] = self.plotTitle
        
        if self.fontSize:
            args['fontsize'] = self.fontSize
            
        return args


    def openFile(self, filenames):

        args = {}
        # if the first row is not of labels, include it as actual data
        if not self.header:
            args['header'] = None

        # if the separator is a space, make it work properly
        if self.sep == ' ' or self.sep == '':
            self.sep = '\ '

        # if it a directory is passed as the -f argument
        # store all the csv files in them to afterwards open them
        tmp_f = []
        for fs in filenames:
            if os.path.isdir(fs):
                tmp_f.extend([ f'{fs}/{f}' for f in os.listdir(fs) if self.extension in f ])
            else:
                tmp_f.append(fs)
        filenames = tmp_f

        # make sure there are files to read
        assert len(filenames)>0, "At least one file should be passed"

        # read all the files
        dfs = []
        for fname in filenames:
            dfs.append( pd.read_csv(fname, sep=self.sep, comment=self.comment, engine='python', **args) )
        
        return dfs


    def getPalette(self):
        '''
        deep, muted, pastel, bright, dark, and colorblind
        '''
        return ListedColormap(sns.color_palette(self.Palette))


    def defineAxis(self, y):
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
            elif containsExt.match(outName):
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
                print(f'File {newName}{add}{ext} saved succesfully')
            else:
                raise NameError("Extension not supported")

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


class Integral:

    def __init__(self, file=None, y=1, x=0, method='simpson',cmd=False) -> None:
        if cmd:
            self.prs = argparse.ArgumentParser(description='Integrate Module - For calculating the area under the curve.')
            
            # set all the arguments
            self.prs.add_argument('-f', '--files', nargs='+', type=str, required=True, help='Path to the data file. It can be multiple files.')
            self.prs.add_argument('-y', '--yAxis', nargs='+', type=int, default=[2], help='Index for the y-axis. Can be more than 1 value (Index starting in 1).')
            self.prs.add_argument('-x', '--xAxis', type=int, default=1, help='Index for the x-axis.')
            self.prs.add_argument('-m', '--method', action='store', choices=['simpson', 'trapz', 'mean'], default='simpson', help='The method that is goind to be used for the calculation. It can be the simpson rule or the trapezoidal rule.')
            # parse
            self.args = self.prs.parse_args()

            self.files = self.open_files( self.args.files )
            self.y = self._convert_human_indexing(self.args.yAxis)
            self.x = self._convert_human_indexing(self.args.xAxis)
            self.method = self.args.method
        else:
            # if the software is being used as a module
            self.files = file if isinstance(file, list) else [file]
            self.y = y if isinstance(y,list) else [y]
            self.y = self.y
            self.x = x
            self.method = method


    def _convert_human_indexing(self, val):
        if isinstance(val, int):
            # if the value is less than 1, it means the index doesn't exist
            if val<1:
                raise ValueError('Invalid Value. The indexing start in 1, make sure your value can be an index.')
            # otherwise, return the human like indexing
            return val-1
        elif isinstance(val, list):
            # if it's a list, iterate over all the values, doing elementwise the same as above
            for index in range(len(val)):
                if val[index]<1:
                    raise ValueError('Invalid Value. The indexing start in 1, make sure your value can be an index.')
                val[index] -= 1
            return val
        else:
            raise TypeError('Invalid Type.\nThe type for y-axis or x-axis is invalid')
        

    def open_files(self, files):
        handlers = []
        # stores all the dataframes in handlers array
        for fs in files:
            handlers.append( pd.read_csv( fs ) )
        
        return handlers


    def _calculate(self, file, y, x):
        # sets the arguments
        args = {
            'y': file[ file.columns[y] ] * 5,
            'x': file[ file.columns[x] ]
        }
        # the result is calculated using the method chosen before
        if self.method == 'simpson':
            return simps(**args)
        elif self.method == 'trapz':
            return trapz(**args)
        else:
            return (simps(**args) + trapz(**args) ) / 2


    def integrate_files( self ):
        file_areas = []
        # for every file, calculate the area and store in the file_areas array, to be returned afterwards
        for file in self.files:
            area = []
            for y in self.y:
                # calculate the result
                result = self._calculate( file, y, self.x )
                # check if the result is nan, if so, raise an exception
                if np.isnan(result):
                    raise ValueError('Some column have unsuported values to calculate the Area Under the Curve.')
                # otherwise, append the result
                area.append( result )
            
            file_areas.append( area[:] )
            area.clear()

        return file_areas


    def stats(self):
        # return the pandas description
        for file in self.files:
            return file.describe()


    def prettify(self, int_arrs):
        try:
            fname = self.args.files
        except:
            fname = [f'File {str(i)}' for i in range(len(self.files))]
        for i, file in enumerate(fname):
            print( f'\n{f"VALUES FOR {file}":^30}' )
            for j, y in enumerate(self.y):
                print(f'Y[{y+1}]: {int_arrs[i][j]}')


if __name__ == "__main__":
    instance = Plot(cmd=True)
    sns.set()
    instance.plotControl()