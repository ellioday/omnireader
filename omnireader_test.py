#%%

from omnireader import Omniwebreader
import pandas as pd
import numpy as np

# Initialize the class
reader = Omniwebreader()

print("Check out which number corresponds to which variable.")
reader.variables_info()
var = [3, 8] # Pull Bartels rotation number and the scalar B

#%%
pdout = "pandas_out"
reader.fetch_to_file(start=20170101,stop=20170102,variables=var,output_file=pdout, style="pandas")
print("Reading the pandas output...")
df = pd.read_csv(pdout + ".lst", delim_whitespace=True)
print(df.head())

#%%
npout = "numpy_out"
reader.fetch_to_file(start=20170101,stop=20170102,variables=var,output_file=npout, style="numpy")
print("Reading the numpy output...")
a = np.loadtxt(npout + ".lst")
print(a)




