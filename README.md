# plotme
 A script written in python that plots data from a file or from a dataframe, outputs that graph as an image or pdf. 

## Command Line Arguments
| Verbose            | Short    | Default       | Description                                           | Valid Values                                           |
|--------------------|:--------:|:-------------:|:-----------------------------------------------------:|:------------------------------------------------------:|
| _--fileName_       | _-f_     | `required`    | Name of the file that contains the data for the graph | `name with or without path`.`extension`                |
| _--separator_ | _-sep_ | ,(comma) | Defines the separator used in the input file, for parsing purposes. | ' ', '\\t', regular expressions and other file delimiters |
| _--output_         | _-o_     | .pdf          | Name and/or extension of the output file              | '.png', 'name', 'name.png'                             |
| _--x_              | _-x_     | first column  | The x-axis of the plot                                | Indexes of columns                             *       |
| _--y_              | _-y_     | second column | The y-axis of the plot             | Indexes of columns(value, list [ex: 2,3,4] or sequences [ex: 2-4] *       |
| _--graphType_      | _-g_     | line          | Type of graph that will be plotted                    | line, scatter, pie and bar                             |
| _--header_         | _-hd_    | True       | Ignores lines starting with # in the input file (see -f) | `True` or `False`                                      |
| _--symbols_        | _-s_     | point symbol  | Shape of the symbols used     | Lists [ex: vhD] or values in https://matplotlib.org/3.1.0/api/markers_api.html |
| _--distBetSymbols_ | _-d_     | auto          | Distance between each symbol                          | `int`                                                  |
| _--symbolSize_     | _-ss_    | auto          | Size of each symbol                                   | `float`                                                |
| _--setPalette_     | _-p_     | colorblind    | Graph color palette                                   | deep, muted, pastel, bright, dark and colorblind       |
| _--bgColor_        | _-bgc_   | lightgrey     | Changes the color of the background                   | 'red','black','lightyellow','#abc','#ff701E'   **      |
| _--gColor_         | _-gc_    | grey          | Color of the grid                                     | 'red','black','lightyellow','#abc','#ff701E'   **      |
| _--colors_ | _-c_ | cycles default colors | Selects the colors of the plotted abscissa(s) in the scatter and line plots | 'red','black','lightyellow','#abc','#ff701E'   ** |
| _--figSize_        | _-fig_   | auto        | Size of the graph and the exported image (Bounding Box) | `float,float`                                          |
| _--hideSpine_      | _-st_    | True          | Removes the spines from the graph                     | `True` or `False`                                      |
| _--lineWidth_      | _-l_     | auto          | Size of the line on a Line plot                       | `int` or `float`                                       |
| _--plotTitle_      | _-pt_    | none          | Title that appears at the top of the plot             | `string`                                               |
| _--xLabel_         | _-xl_    | column name   | Label of the abscissa                                 | `string`                                               |
| _--yLabel_         | _-yl_    | column name   | Label of the ordinate(s)                              | `string`                                               |
| _--pieLabel_       | _-pl_    | none          | Label each slice of the pie                           | `string1,string2,...,stringN`                          |
| _--fontSize_       | _-fs_    | auto          | Size of the font used in the graph itself             | `int`                                                  |

* Column indexes begin at 1, not 0
** See https://matplotlib.org/stable/tutorials/colors/colors.html for more examples
*** 'lightblue', 'yellow', 'grey', 'lightpink', 'brown', 'pink', 'orange', 'green', 'dark yellow', 'blue'

## Examples
 - Line plot: `py plotme.py -f (path)filename.extension -x columnIndex -y columnIndex`
    - The only required argument is the filename 
 - Scatter plot with differente output name and plot title: `py plotme.py -f (path)file.ext -g scatter -pt title -o export` 
 - Bar plot: `py plotme.py -f (path)filename.extension`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
 - Pie chart with labels on each slice while using a tab separated input file: `py plotme.py -f (path)filename.extension -sep '\t' -pl label,label2,...,labelN`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
    - Each label corresponds to a single slice in the chart, from 1 to N, every label is assigned a slice following the file order. The number of labels need to be the same as the number of elements in the column.
### Parameters examples  
   - f:              `python3 plotme.py -f 'name with spaces.csv'`
   - separator:      `python3 plotme.py -f file.txt -sep \t`
                     `python3 plotme.py -f file.csv -sep ,`
   - output:         `python3 plotme.py -f file -o outputFile`
                     `python3 plotme.py -f file -o .tiff`
                     `python3 plotme.py -f file -o export.jpeg`
   - x:              `python3 plotme.py -f file -x 1`            
   - y:              `python3 plotme.py -f file -y 5-7`
                     `python3 plotme.py -f file -y 5,6,7`
   - graphType       `python3 plotme.py -f file -g bar`   
   - header          `python3 plotme.py -f file -hd False`   
   - symbols         `python3 plotme.py -f file -y 2,3 -s vH`  
                     `python3 plotme.py -f file -y 2-6 -s vHddv`
                     `python3 plotme.py -f file -y 2-6 -s v` 
   - distBetSymbols  `python3 plotme.py -f file -d 3`
   - symbolSize      `python3 plotme.py -f file -s v -ss 15`
   - setPalette      `python3 plotme.py -f file -p deep`
   - bgColor         `python3 plotme.py -f file -bgc black`
                     `python3 plotme.py -f file -bgc '#ff701E'`
   - gColor          `python3 plotme.py -f file '#abc'`
   - colors          `python3 plotme.py -f file -y 2,4 -c yellow,green`
                     `python3 plotme.py -f file -y 2,4 -c '#ff701E','#abc'`
   - figSize         `python3 plotme.py -f file -fig 192,108`
   - hideSpine       `python3 plotme.py -f file -st True`
   - lineWidth       `python3 plotme.py -f file -l 15`
   - plotTitle       `python3 plotme.py -f file -pt 'Tile of the plot'`
   - xLabel          `python3 plotme.py -f file -xl 'label of x'`
   - yLabel          `python3 plotme.py -f file -yl 'label of y'`
   - pieLabel        `python3 plotme.py -f file -g pie -pl slice1,'another slice',3`
   - fontSize        `python3 plotme.py -f file -fs 14`

## Using it as an imported module

 1. After importing, you need to make an instance of the `Plot` class while passing, at least, the  `data`(the imported version of fileName) argument with the dataframe, the rest of the arguments have the same names as their CLI counterparts. 
 2. Call the `plotGraph()` method. The file will be exported as `Plot.pdf` if no `output` argument was passed.

### Use python3, as well as pip3 to install the dependencies

### Dependencies: seaborn, matplotlib, pandas, argparse, re, ast, itertools
