# omnireader

The goal of this python package is an easy interface with the omniweb data available at https://omniweb.gsfc.nasa.gov/.

It makes use of the ```request``` package in python together with the omniweb API which allows to pull data via an HTML request.

The received HTML code is parsed using the ```html``` class in python. 

## To Do

1. Make a dictionnary for the different variables
The omniweb API allows us to fetch the data based on an index. 
Currently, using the ```OMniwebreader.variables_info()```-function, the variables and corresponding index are printed to the terminal, after which the user can select which variable shsould be fetched.
This is not a very intuitive method, as the list must be checked to see which variables you pull. 
__Solution__: consider using a dictionary to link each variable to its respective index
