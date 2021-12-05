import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib as mpl
import matplotlib.pyplot as plt

pdr = pd.read_csv('./results/all.csv', sep=';')

#pdr['encoding'] = pdr.encoding.astype("category", categories=range(8), ordered=True)
# pdr['foffset'] = pdr.foffset.astype(CategoricalDtype(categories=range(7), ordered=True))

#pdr.encoding.cat.categories = [
#        "BPSK 1/2", "BPSK 3/4",
#        "QPSK 1/2", "QPSK 3/4",
#        "16-QAM 1/2", "16-QAM 3/4",
#        "64-QAM 2/3", "64-QAM 3/4"]
# pdr.foffset.cat.categories = ["0.0","0.05","0.10","0.15","0.20","0.25","0.30"]

a = pdr.groupby(['foffset', 'snr'])

b = a.agg({'received': np.mean}).reset_index()
c = b.pivot(index='snr', columns='foffset', values='received')
c.plot()
plt.ylabel('Ratio of received packets')
plt.title('802.11p with Freq Offset')
plt.savefig('pdr.pdf')

# b.to_csv('results.csv')


threedee = plt.figure().gca(projection='3d')
threedee.scatter(b['snr'], b['foffset'], b['received'])

