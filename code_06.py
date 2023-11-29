"""code_06 (code 1 + 3 + 5 + 6)
* Some redundant parts have been commented out
"""
# This code is dedicated to the public domain under the Creative Commons CC0 public domain dedication.
# You are free to use, modify, distribute, and reproduce this code without any restrictions.
# For more information, refer to the Creative Commons CC0 1.0 Universal Public Domain Dedication:
# https://creativecommons.org/publicdomain/zero/1.0/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# code 1
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv', index_col=False)
else:
    df = pd.read_excel(
        r"https://dataverse.nl/api/access/datafile/354095", sheet_name='Data')
    df.to_csv('data.csv', index=False)

df = df.set_index(['countrycode', 'year'])
cgdpopl = df['cgdpo']/(df['emp']*df['avh'])
df['yius'] = cgdpopl/cgdpopl.loc['USA']
df['qius'] = df['yius']/df['ctfp']
# df[['yius', 'ctfp', 'qius']].dropna().describe().to_clipboard()

# # code 2
# df[['yius', 'qius']].dropna().groupby(level=1).apply(
#     lambda g: np.log(g['qius']).var()/np.log(g['yius']).var()).plot(title='measure of success')
# plt.show()

# code 3
_rgdpnapl = df['rgdpna']/(df['emp']*df['avh'])
df['yt2017'] = _rgdpnapl.groupby(level=0, group_keys=False).apply(
    lambda g: g/g.loc[(slice(None), 2017)])
df['qt2017'] = df['yt2017']/df['rtfpna']
# print(df[['yt2017', 'rtfpna', 'qt2017']].dropna().describe())

# # code 4
# gb = df[['yt2017', 'rtfpna', 'qt2017']].loc[['USA', 'JPN', 'DEU']].dropna()
# print(gb.groupby(level=0).apply(lambda g: (np.log(g.iloc[-1]) - np.log(g.iloc[0]))*100))

# code 5
labsh_mean = df['labsh'].groupby(level=1).transform(lambda g: g.mean())
lab_contrib = df['hc']**labsh_mean
c_cap_contrib = (df['cn']/(df['emp']*df['avh']))**(1-labsh_mean)
r_cap_contrib = (df['rnna']/(df['emp']*df['avh']))**(1-labsh_mean)
df['qius_calc'] = \
(c_cap_contrib/c_cap_contrib.loc['USA'])*(lab_contrib/lab_contrib.loc['USA'])
df['ctfp_calc'] = df['yius']/df['qius_calc']
df['kt2017'] = r_cap_contrib.groupby(level=0, group_keys=False)\
.apply(lambda g: g/g.loc[(slice(None), 2017)])
df['hct2017'] = lab_contrib.groupby(level=0, group_keys=False)\
.apply(lambda g: g/g.loc[(slice(None), 2017)])
df['qt2017_calc'] = df['kt2017'] * df['hct2017']
df['rtfpna_calc'] = df['yt2017']/df['qt2017_calc']

# code 6 (in chart 6)
countries = ['BGD', 'KHM', 'PAK', 'MMR', 'VNM']
df.groupby(level=1).apply(
    lambda df: np.log(df['qius_calc']).var()/np.log(df['yius']).var()
    ).plot(title='measure of success: all countries')
plt.show()
df.loc[list(countries)].groupby(level=1).apply(
    lambda df: np.log(df['qius_calc']).var()/np.log(df['yius']).var()
    ).plot(title='measure of success: five countries')
plt.show()
