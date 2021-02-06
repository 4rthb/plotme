# plotScript
 A script written in python that plots data from a file, can also output that graph as an image or pdf. 

## Command Line Arguments
| Verbose            | Short    | Default       | Description                                           | Valid Values                                           |
|--------------------|:--------:|:-------------:|:-----------------------------------------------------:|:------------------------------------------------------:|
| _--setPalette_     | _-p_     | colorblind    | Graph color palette                                   | deep, muted, pastel, bright, dark and colorblind       |
| _--graphType_      | _-g_     | line          | Type of graph that will be plotted                    | line, scatter, pie and bar                             |
| _--fileName_       | _-f_     | `required`    | Name of the file that will provide data for the graph | `string`                                               |
| _--output_         | _-o_     | .pdf          | Name and/or extension of the desired output file      | `string` e.g. "outputFile.pdf", ".png" or "outputName" |
| _--x_              | _-x_     | first column  | The abscissa of the graph                             | `int`                                                  |
| _--y_              | _-y_     | second column | The ordinate(s) of the graph                          | `int`                                                  |
| _--symbols_        | _-s_     | ball symbol   | Shape of the symbols used                             | https://matplotlib.org/3.1.0/api/markers_api.html      |
| _--distBetSymbols_ | _-d_     | auto          | Distance between each symbol                          | `int` or `float`                                       |
| _--symbolSize_     | _-ss_    | auto          | Size of each symbol                                   | `int` or `float`                                       |
| _--figSize_        | _-fig_   | auto          | Size of the graph                                     | `int` or `float`                                       |
| _--fontSize_       | _-fs_    | auto          | Size of the font used in the graph itself             | `int`                                                  |
| _--legendFontSize_ | _-lfs_   | auto          | Size of the graphs legend                             | `int`                                                  |
| _--lineWidth_      | _-l_     | auto          | Size of the line on a Line graph                      | `int` or `float`                                       |
| _--plotTitle_      | _-plot_  | none          | Title that appears at the top of the graph            | `string`                                               |
| _--xLabel_         | _-xl_    | column name   | Label of the abscissa                                 | `string`                                               |
| _--yLabel_         | _-yl_    | column name   | Label of the ordinate(s)                              | `string`                                               |
