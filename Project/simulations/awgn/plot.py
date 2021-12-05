import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib as mpl
import matplotlib.pyplot as plt

pdr = pd.read_csv('./results/all.csv', sep=';')

#pdr['encoding'] = pdr.encoding.astype("category", categories=range(8), ordered=True)
pdr['noise'] = pdr.noise.astype(CategoricalDtype(categories=range(11), ordered=True))

#pdr.encoding.cat.categories = [
#        "BPSK 1/2", "BPSK 3/4",
#        "QPSK 1/2", "QPSK 3/4",
#        "16-QAM 1/2", "16-QAM 3/4",
#        "64-QAM 2/3", "64-QAM 3/4"]

pdr.noise.cat.categories = ["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7",
                            "0.8","0.9","10.0"]

a = pdr.groupby(['noise', 'snr'])

b = a.agg({'received': np.mean}).reset_index()
c = b.pivot(index='snr', columns='noise', values='received')
c.plot()
plt.ylabel('Ratio of received packets')
plt.title('802.11p with AWGN model')
plt.savefig('pdr.pdf')

