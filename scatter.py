#!/usr/bin/env python

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='performance info scatter')
parser.add_argument('filepath', nargs='?')
args = parser.parse_args()

filepath = args.filepath or sys.stdin

df = pd.read_csv(filepath, index_col='time')
pca = PCA(n_components=2)

coords = pca.fit_transform(df.transpose())
x = [v[0] for v in coords]
y = [v[1] for v in coords]

plt.scatter(x, y)

for i, txt in enumerate(df.columns):
  plt.annotate(txt, (x[i], y[i]))

plt.show()

