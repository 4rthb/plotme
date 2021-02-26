# plotme
 A module written in Python that plots data from a file or multiple files, outputs the graphs as an image or pdf. 

## Command Line Arguments
| Verbose            | Short    | Default       | Description                                           | Valid Values                                           |
|--------------------|:--------:|:-------------:|:-----------------------------------------------------:|:------------------------------------------------------:|
| _--setPalette_     | _-p_     | colorblind    | Graph color palette                                   | deep, muted, pastel, bright, dark and colorblind       |
| _--graphType_      | _-g_     | line          | Type of graph that will be plotted                    | line, scatter, pie and bar                             |
| _--fileName_       | _-f_     | `required`    | Name of the file that will provide data for the graph | `name with or without path`.`extension`                |
| _--output_         | _-o_     | .pdf          | Name and/or extension of the desired output file      | `string` e.g. "outputFile.pdf", ".png" or "outputName" |
| _--separator_      | _-sep_   | ,             | Separator used in the input file                      | `string`                                               |
| _--x_              | _-x_     | first column  | The abscissa of the graph                             | `int`                                                  |
| _--y_              | _-y_     | second column | The ordinate(s) of the graph                          | `int`                                                  |
| _--symbols_        | _-s_     | point symbol  | Shape of the symbols used                             | https://matplotlib.org/3.1.0/api/markers_api.html      |
| _--distBetSymbols_ | _-d_     | auto          | Distance between each symbol                          | `int`, `float`, `None`, `(int,int,int)` etc            |
| _--symbolSize_     | _-ss_    | auto          | Size of each symbol                                   | `int` or `float`                                       |
| _--figSize_        | _-fig_   | auto          | Size of the graph                                     | `float,float`                                          |
| _--fontSize_       | _-fs_    | auto          | Size of the font used in the graph itself             | `int`                                                  |
| _--lineWidth_      | _-l_     | auto          | Size of the line on a Line graph                      | `int` or `float`                                       |
| _--plotTitle_      | _-plot_  | none          | Title that appears at the top of the graph            | `string`                                               |
| _--xLabel_         | _-xl_    | column name   | Label of the abscissa                                 | `string`                                               |
| _--yLabel_         | _-yl_    | column name   | Label of the ordinate(s)                              | `string`                                               |
| _--pieLabel_       | _-pl_    | none          | Label each slice of the pie                           | `string1,string2,...,stringN`                          |

## Examples
 - Plotting two line graphs: `python3 plotme.py -f (path)filename.extension,(path)filename2.extension -x columnIndex -y columnIndex`
    - The only required argument is the filename 
 - Plotting three scatter graphs with differente output names and plot titles: `python3 plotme.py -f (path)file.ext,(path)file2.ext,(path)file3.ext -plot title,title2,title3 -o export,export2.jpeg,export3.png` 
 - Plotting a bar graph: `python3 plotme.py -f (path)filename.extension`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
 - Plotting a pie graph with labels on each slice while using a tab separated input file: `python3 plotme.py -f (path)filename.extension -sep \t -pl label,label2,...,labelN`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float

### Dependencies: seaborn
