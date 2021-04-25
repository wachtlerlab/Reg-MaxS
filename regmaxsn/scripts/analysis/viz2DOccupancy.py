import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
plt.ion()
import os
from regmaxsn.core.matplotlibRCParams import mplPars
from collections import Counter
import pandas as pd

homeFolder = "/home/aj/"

sns.set(rc=mplPars)

swcFiles = [
            os.path.join(homeFolder,
                         'DataAndResults/morphology/OriginalData/Tests/HSN-fluoro01.CNG.swc'),
            os.path.join(homeFolder,
                         'DataAndResults/morphology/OriginalData/Tests/HSN-fluoro01.CNGRandRotY0.swc'),
            # os.path.join(homeFolder,
            #              'DataAndResults/morphology/OriginalData/Tests/HSN-fluoro01.CNGRandRotY1.swc'),
           ]
# gridSize = 20.0
# gridSize = 40.0
gridSize = 10.0

voxels = []
for swc in swcFiles:
    aPts = np.loadtxt(swc)[:, 2:4]
    aPts[:, 0] *= -1
    aVox = np.array(aPts / gridSize, np.int32)
    aVoxSet = set(map(tuple, aVox))
    voxels.extend(list(aVoxSet))

voxelCounter = Counter(voxels)
df = pd.DataFrame()
for voxel, count in voxelCounter.items():
    tempDict = {"X": voxel[0], "Y": voxel[1], "count": count}
    df = df.append(tempDict, ignore_index=True)

dfIndexed = df.pivot(index='X', columns='Y', values='count')
fig, ax = plt.subplots(figsize=(14, 11.2))
sns.heatmap(data=dfIndexed, xticklabels=50, yticklabels=50, annot=True, fmt="%d",
            square=True, cmap=plt.cm.Dark2, cbar_kws={"ticks": np.arange(1, df["count"].max() + 1)},
            ax=ax)
ax.set_xlabel('X')
ax.set_ylabel('Y')
fig.tight_layout()

