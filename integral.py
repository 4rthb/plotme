from scipy.integrate import simps, trapz

import pandas as pd
import numpy as np

import argparse

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


if __name__ == '__main__':

    integ_cls = Integral(cmd=True)
    vals = integ_cls.integrate_files()
    integ_cls.prettify(vals)
