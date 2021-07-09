# plotme
 A script written in python that plots data from a file or from a dataframe, outputs that graph as an image or pdf. 

## Command Line Arguments
| Verbose                | Short    | Default       | Description                                           | Valid Values                                                             |
|------------------------|:--------:|:-------------:|:-----------------------------------------------------:|:------------------------------------------------------------------------:|
| _--setPalette_     | _-p_     | colorblind    | Graph color palette                                   | deep, muted, pastel, bright, dark and colorblind       |
| _--graphType_      | _-g_     | line          | Type of graph that will be plotted                    | line, scatter, pie and bar                             |
| _--fileName_       | _-f_     | `required`    | Name of the file that contains the data for the graph | `name with or without path`.`extension`                |
| _--output_         | _-o_     | .pdf          | Name and/or extension of the output file              | '.png', 'name', 'name.png'                             |
| _--separator_   | _-sep_ | , | Defines the separator used in the input file, for parsing purposes. | ' ', '\\t', regular expressions and other file delimiters |
| _--x_              | _-x_     | first column  | The x axis of the plot                                | Indexes of columns                                     |
| _--y_              | _-y_     | second column | The y axis of the plot                     | Indexes of columns(value, list [ex: 2,3,4] or sequences [ex: 2-4] |
| _--symbols_        | _-s_     | point symbol  | Shape of the symbols used     | Lists [ex: vhD] or values in https://matplotlib.org/3.1.0/api/markers_api.html |
| _--distBetSymbols_ | _-d_    | auto | Distance between each symbol | None, `int`, `float`, `(int,int)`, `[float,float]`, `[int,int,int]`,`(float,float,float)` |
| _--symbolSize_     | _-ss_    | auto          | Size of each symbol                                   | `float`                                                |
| _--figSize_        | _-fig_   | auto          | Size of the graph and the exported image              | `float,float`                                          |
| _--fontSize_       | _-fs_    | auto          | Size of the font used in the graph itself             | `int`                                                  |
| _--lineWidth_      | _-l_     | auto          | Size of the line on a Line plot                       | `int` or `float`                                       |
| _--plotTitle_      | _-pt_    | none          | Title that appears at the top of the plot             | `string`                                               |
| _--xLabel_         | _-xl_    | column name   | Label of the abscissa                                 | `string`                                               |
| _--yLabel_         | _-yl_    | column name   | Label of the ordinate(s)                              | `string`                                               |
| _--pieLabel_       | _-pl_    | none          | Label each slice of the pie                           | `string1,string2,...,stringN`                          |
| _--header_         | _-hd_    | True          | Ignores the # lines in the file                       | `True` or `False`                                      |
| _-bgColor-_        | _-bgc_   | lightgrey     | Changes the color of the background                   | 'red','black','lightyellow','#abc','#ff701E'   ***     |
| _-gColor-_         | _-gc_    | grey          | Color of the grid                                     | 'red','black','lightyellow','#abc','#ff701E'   ***     |
| _-spineTran-_      | _-st_    | True          | Removes the spines from the graph                     | `True` or `False`                                      |
|_-confidenceInterval-_|_-ci_|False|Makes a confidence interval over the whole database, the effect is to put a shadow representing the error | `True` or `False`|

*** See https://matplotlib.org/stable/tutorials/colors/colors.html for more examples

## Examples
 - Line plot: `py plotme.py -f (path)filename.extension -x columnIndex -y columnIndex`
    - The only required argument is the filename 
 - Scatter plot with differente output name and plot title: `py plotme.py -f (path)file.ext -g scatter -pt title -o export` 
 - Bar plot: `py plotme.py -f (path)filename.extension`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
 - Pie chart with labels on each slice while using a tab separated input file: `py plotme.py -f (path)filename.extension -sep '\t' -pl label,label2,...,labelN`
    - The first item in the column is interpreted as the label of the axis, the subsequent itens in that column **NEED** to be of type int or float
    - Each label corresponds to a single slice in the chart, from 1 to N, every label is assigned a slice following the file order. The number of labels need to be the same as the number of elements in the column.
### Using the module:
 1. Let's read this pok.csv file:  

|#|Name|Type 1|Type 2|HP|Attack|Defense|Sp. Atk|Sp. Def|Speed|Generation|Legendary|  
|--|:---|:------|:------|:--|:------|:-------|:-------|:-------|:-----|:----------|:---------|  
| 1 |Bulbasaur|Grass|Poison|45|49|49|65|65|45|1|FALSE|  
|2|Ivysaur|Grass|Poison|60|62|63|80|80|60|1|FALSE|  
|3|Venusaur|Grass|Poison|80|82|83|100|100|80|1|FALSE|  
|3|VenusaurMega Venusaur|Grass|Poison|80|100|123|122|120|80|1|FALSE|  
|4|Charmander|Fire||39|52|43|60|50|65|1|FALSE|  
|5|Charmeleon|Fire||58|64|58|80|65|80|1|FALSE|  

 2. Now let's plot colunms 5 to 7 and put color the background: `python3 plotme.py -f pok.csv -y 5-7 -bgc '#abc'`
 ![image](https://user-images.githubusercontent.com/57924116/125137485-23567a00-e0e3-11eb-84e6-44b244ba44a2.png)

 3. To change the color pallete so that the lines are better shown and make the grid color a little stronger: `python3 plotme.py -f pok.csv -y 5-7 -bgc '#abc' -p bright -gc black`
 ![image](https://user-images.githubusercontent.com/57924116/125137414-04f07e80-e0e3-11eb-87b4-db53d2cc5bbd.png)
 
 4. We are ignoring the header from this file, so some values are used as labels, let's fix that and show the spines of the plot: `python3 plotme.py -f pok.csv -y 5-7 -bgc '#abc' -p bright -gc black -hd False -st False`
 ![image](https://user-images.githubusercontent.com/57924116/125137750-b2fc2880-e0e3-11eb-8691-8cc58ad24c5e.png)
 
 5. If we want to put better labels in the graph, titles and change the font: `python3 plotme.py -f pok.csv -y 5-7 -bgc '#abc' -p bright -gc black -hd False -st False -xl Pokemons -yl Stats -pt PokemonsXStats -fs 6`
 ![image](https://user-images.githubusercontent.com/57924116/125137931-0cfcee00-e0e4-11eb-85b9-b3369a137421.png)
 
 6. Rolling back a little, let's just change the line width and put some markers in the plot and choose their sizes: `python3 plotme.py -f pok.csv -y 5-7 -s v -ss 9 -l 3`
 ![image](https://user-images.githubusercontent.com/57924116/125138229-a62c0480-e0e4-11eb-8f82-9a6a5307b53c.png)
 
 7. And if we need to skip one marker after another? And output a file with '.tiff'? Then: `python3 plotme.py -f pok.csv -y 5-7 -s v -ss 9 -l 3 -d 1 -o .tiff`
 ![image](https://user-images.githubusercontent.com/57924116/125138573-42eea200-e0e5-11eb-9673-8d1111950cbf.png)

 8. Last, let's try the pie plot, change the labels and ouput it in pdf with another name: `python3 plotme.py -f pok.csv -y 5 -g pie -hd False -pl Bulb,Ivy,Ven,VenMega,Char,Charme -yl 'poke stats' -o pokepie`
 ![image](https://user-images.githubusercontent.com/57924116/125138961-02435880-e0e6-11eb-939b-c59a5628fcc0.png)
 

## Using it as an imported module

 1. After importing, you need to make an instance of the `Plot` class while passing, at least, the  `data`(the imported version of fileName) argument with the dataframe, the rest of the arguments have the same names as their CLI counterparts. 
 2. Call the `plotGraph()` method. The file will be exported as `Plot.pdf` if no `output` argument was passed.

### Use python3, as well as pip3 to install the dependencies

### Dependencies: seaborn, matplotlib, pandas, argparse, re, ast
