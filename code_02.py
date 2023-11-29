"""code_02 (code 1 + code 2)
"""
# This code is dedicated to the public domain under the Creative Commons CC0 public domain dedication.
# You are free to use, modify, distribute, and reproduce this code without any restrictions.
# For more information, refer to the Creative Commons CC0 1.0 Universal Public Domain Dedication:
# https://creativecommons.org/publicdomain/zero/1.0/

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# code 1
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv', index_col=False)
else:
    print("Please be patient. It takes a long time to download the Excel file. "
          "The second execution uses cached data, so it does not take much time.")
    df = pd.read_excel(
        r"https://dataverse.nl/api/access/datafile/354095", sheet_name='Data')
    df.to_csv('data.csv', index=False)

df = df.set_index(['countrycode', 'year'])
cgdpopl = df['cgdpo']/(df['emp']*df['avh'])
df['yius'] = cgdpopl/cgdpopl.loc['USA']
df['qius'] = df['yius']/df['ctfp']
df[['yius', 'ctfp', 'qius']].dropna().describe().to_clipboard()

# code 2
df[['yius', 'qius']].dropna().groupby(level=1).apply(
    lambda g: np.log(g['qius']).var()/np.log(g['yius']).var()).plot(title='measure of success')
plt.show()
