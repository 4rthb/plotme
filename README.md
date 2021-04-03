# plotme
 A script written in python that plots data from a file or from a dataframe, outputs that graph as an image or pdf. 

## Command Line Arguments
| Verbose                | Short    | Default       | Description                                           | Valid Values                                                             |
|------------------------|:--------:|:-------------:|:-----------------------------------------------------:|:------------------------------------------------------------------------:|
| _--setPalette_         | _-p_     | colorblind    | Graph color palette                                   | deep, muted, pastel, bright, dark and colorblind                         |
| _--graphType_          | _-g_     | line          | Type of graph that will be plotted                    | line, scatter, pie and bar                                               |
| _--fileName_           | _-f_     | `required`    | Name of the file that will provide data for the graph | `name with or without path`.`extension`                                  |
| _--output_             | _-o_     | .pdf          | Name and/or extension of the desired output file      | `string` e.g. "outputFile.pdf", ".png" or "outputName"                   |
| _--separator_          | _-sep_   | ,             | Separator used in the input file                      | `string` use ' ' for names that contains \ or similar                    | 
| _--x_                  | _-x_     | first column  | The abscissa of the graph                             | `int`                                                                    |
| _--y_                  | _-y_     | second column | The ordinate(s) of the graph                          | `int`                                                                    |
| _--symbols_            | _-s_     | ball symbol   | Shape of the symbols used                             | https://matplotlib.org/3.1.0/api/markers_api.html (no separator between) |
| _--distBetSymbols_     | _-d_     | auto          | Distance between each symbol                          | `int`, `float`, `None`, `(int,int,int)` etc                              |
| _--symbolSize_         | _-ss_    | auto          | Size of each symbol                                   | `int` or `float`                                                         |
| _--figSize_            | _-fig_   | auto          | Size of the graph                                     | `float,float`                                                            |
| _--fontSize_           | _-fs_    | auto          | Size of the font used in the graph itself             | `int`                                                                    |
| _--lineWidth_          | _-l_     | auto          | Size of the line on a Line graph                      | `int` or `float`                                                         |
| _--plotTitle_          | _-plot_  | none          | Title that appears at the top of the graph            | `string`                                                                 |
| _--xLabel_             | _-xl_    | column name   | Label of the abscissa                                 | `string`                                                                 |
| _--yLabel_             | _-yl_    | column name   | Label of the ordinate(s)                              | `string`                                                                 |
| _--pieLabel_           | _-pl_    | none          | Label each slice of the pie                           | `string1,string2,...,stringN`                                            |
| _-label-_              | _-lab_   | true          |  Ignores the # lines in the file                      | `True` or `False`                                                        | 
| _-bgColor-_            | _-bgc_   | lightgrey     | Color of the background                               | red, brown, lightgrey, grey, black, crimson etc                          |
| _-gColor-_             | _-gc_    | grey          | Color of the grid                                     | red, brown, lightgrey, grey, black, crimson etc                          |
| _-spineTran-_          | _-st_    | true          | Transparency of the graph's spine                     | `True` or `False`                                                        |
| _-confidenceInterval-_ | _-ci_    | false         | shadow that represents the error interval             | `True` or `False`                                                        |

## Examples
 - Line plot: `py plotme.py -f (path)filename.extension -x columnIndex -y columnIndex`
    - The only required argument is the filename 
 - Scatter plot with differente output name and plot title: `py plotme.py -f (path)file.ext -g scatter -plot title -o export` 
 - Bar plot: `py plotme.py -f (path)filename.extension`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
 - Pie chart with labels on each slice while using a tab separated input file: `py plotme.py -f (path)filename.extension -sep '\t' -pl label,label2,...,labelN`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
    - Each label corresponds to a single slice in the chart, from 1 to N, every label is assigned a slice following the file order. The number of labels need to be the same as the number of elements in the column.
### Using the module:
 1. Let's read this pokemon.csv file:  

|#|Name|Type 1|Type 2|HP|Attack|Defense|Sp. Atk|Sp. Def|Speed|Generation|Legendary|  
|--|:---|:------|:------|:--|:------|:-------|:-------|:-------|:-----|:----------|:---------|  
| 1 |Bulbasaur|Grass|Poison|45|49|49|65|65|45|1|FALSE|  
|2|Ivysaur|Grass|Poison|60|62|63|80|80|60|1|FALSE|  
|3|Venusaur|Grass|Poison|80|82|83|100|100|80|1|FALSE|  
|3|VenusaurMega Venusaur|Grass|Poison|80|100|123|122|120|80|1|FALSE|  
|4|Charmander|Fire||39|52|43|60|50|65|1|FALSE|  
|5|Charmeleon|Fire||58|64|58|80|65|80|1|FALSE|  

 2. Now let's make a cool scatter plot with a little bit of color: 
 `py plotme.py -f pokemon.csv -g scatter -y 6,7,8 -bgc green -gc darkblue -st False`

![image](https://user-images.githubusercontent.com/57924116/113490775-c6737400-94a2-11eb-82b5-a576e0386568.png)

 3. Beautiful! Now let's put some meaningful labels on these axis, a title and change these markers a little: 
 `py plotme.py -f pokemon.csv -g scatter -y 6,7,8 -bgc green -gc darkblue -st False -xl "Cool Stats" -yl "Numbers" -plot "My very own plot" -s p*+ -ss 80`

![image](https://user-images.githubusercontent.com/57924116/113490953-c2942180-94a3-11eb-8e97-356096522775.png)

4. Objectively better! 

## Using it as an imported module

 1. After importing, you need to make an instance of the `Plot` class while passing, at least, the  `data`(the imported version of fileName) argument with the dataframe, the rest of the arguments have the same names as their CLI counterparts. 
 2. Call the `plotGraph()` method. The file will be exported as `Plot.pdf` if no `output` argument was passed.

### Use python3, as well as pip3 to install the dependencies

### Dependencies: seaborn, matplotlib, pandas, argparse, re, ast
