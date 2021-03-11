# plotme
 A module written in Python that plots data from a file or multiple files, outputs the graphs as an image or pdf. 

## Command Line Arguments
| Verbose            | Short    | Default       | Description                                           | Valid Values                                           |
|--------------------|:--------:|:-------------:|:-----------------------------------------------------:|:------------------------------------------------------:|
| _--setPalette_     | _-p_     | colorblind    | Graph color palette                                   | deep, muted, pastel, bright, dark and colorblind       |
| _--graphType_      | _-g_     | line          | Type of plot                                          | line, scatter, pie and bar                             |
| _--fileName_       | _-f_     | `required`    | Name of the file that contains the data for the graph | `name with or without path`.`extension`                |
| _--output_         | _-o_     | .pdf          | Name and/or extension of the output file              | `string` e.g. "outputFile.pdf", ".png" or "outputName" |
| _--separator_      | _-sep_   | ,             | Separator used in the the input file, for parsing purpose | `string`                                           |
| _--x_              | _-x_     | first column  | The x axis of the plot                                | `int`                                                  |
| _--y_              | _-y_     | second column | The y axes (can be one value, a sequence or a list) of the plot | `int`                                        |
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
| _--label_          | _-lab_   | True          | Take the header of your database off                  | `True` or `False`                                      |
| _--bgc_            | _-bgc_   | "lightgrey"   | Change the color of the background                    | https://matplotlib.org/3.3.3/gallery/color/color_demo.html#sphx-glr-gallery-color-color-demo-py |


## Examples
 - Plotting two line graphs: `python3 plotme.py -f (path)filename.extension,(path)filename2.extension -x columnIndex -y columnIndex`
    - The only required argument is the filename 
 - Plotting three scatter graphs with differente output names and plot titles: `python3 plotme.py -f (path)file.ext,(path)file2.ext,(path)file3.ext -plot title,title2,title3 -o export,export2.jpeg,export3.png` 
 - 
 - Plotting a bar graph: `python3 plotme.py -f (path)filename.extension -g bar`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
 
 - Plotting a pie graph with labels on each slice while using a tab separated input file: `python3 plotme.py -f (path)filename.extension -sep \t -pl label,label2,...,labelN`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
 - To plot a database separated by spaces, you can use the separator as "" or " ". If the database is separated by commas, just use the default.
    `python3 plotme.py -f (path)filename.extension -sep ""` or `python3 plotme.py -f (path)filename.extension -sep " "` to the space separated database.
    `python3 plotme.py -f (path)filename.extension` to the comma separated database - using the default.
 
 - To use more than one symbol in the scatter plot, you got to have multiple y values, and multiple symbols in the -s parameter, the symbols must be inside quotes and in a row with no separation between. 
     `python3 plotme.py -f (path)filename.ext -g scatter -y 2,4,5 -s "s3p"`
     
 - More details on the colors for the setPalette parameter are available at this link: https://seaborn.pydata.org/tutorial/color_palettes.html

 
### Dependencies: 

seaborn, pandas, matplotlib, argparse, re, ast
