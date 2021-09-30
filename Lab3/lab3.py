# Generate process data as data.txt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits import mplot3d

df_bpsk = pd.read_excel('lab3_data.xlsx',sheet_name="Sheet2",index_col=None)
df_qpsk = pd.read_excel('lab3_data.xlsx',sheet_name="Sheet3",index_col=None)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.scatter3D(df_bpsk['Attenuation'],df_bpsk['Noise'],df_bpsk['SER'])
ax.scatter3D(df_qpsk['Attenuation'],df_qpsk['Noise'],df_qpsk['SER'])
ax.legend(['BPSK','QPSK'])
ax.set_title('SER vs Noise vs Attenuation')
ax.set_xlabel('Attenuation')
ax.set_ylabel('Noise')
ax.set_zlabel('SER')