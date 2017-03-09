from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import patches as mpatches
import colorsys
plt.ion()
import os
homeFolder = os.path.expanduser('~')
mplPars = { 'text.usetex'       :    True,
            'axes.labelsize'    :   'large',
            'axes.titlesize'    :   'large',
            'font.family'       :   'sans-serif',
            'font.sans-serif'   :   'computer modern roman',
            'font.size'         :    48,
            'font.weight'       :   'black',
            'xtick.labelsize'   :    40,
            'ytick.labelsize'   :    40,
            }
sns.set(rc=mplPars)

def getLighterColor(col, saturation):
    '''
    Returns a color with the same hue and value as the color `col', but with the given saturation
    :param col: 3 member iterable with values in [0, 1]
    :param saturation: float in [0, 1]
    :return:
    '''

    assert len(col) == 3, 'col must be a 3 member iterable'
    assert all([0 <= x <= 1 for x in col]), 'col can only contain values in [0, 1]'
    assert 0 <= saturation <= 1, 'saturation must be in [0, 1]'

    hsv = colorsys.rgb_to_hsv(*col)
    return colorsys.hsv_to_rgb(hsv[0], saturation, hsv[2])




swcFiles = [
            os.path.join(homeFolder,
                         'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2D.swc'),
            os.path.join(homeFolder,
                                'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandRot.swc')
            # os.path.join(homeFolder,
            #              'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandRot1.swc'),
            # os.path.join(homeFolder,
            #         'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNGNoiseStd42DRandRot1.swc'),
            # os.path.join(homeFolder,
            #              'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandTranslate1.swc'),
            # os.path.join(homeFolder,
            #              'DataAndResults/morphology/OriginalData/borstHSN2D/HSN-fluoro01.CNG2DRandScale.swc'),
           ]
# gridSize = 20.0
# gridSize = 40.0
gridSize = 10.0
minMarkerSize = 5
maxMarkerSize = 10

minRad = 1
maxRad = 5

cols = plt.cm.rainbow(np.linspace(0, 1, len(swcFiles)))

xDis = []
yDis = []
with sns.axes_style('whitegrid'):
    fig, ax = plt.subplots(figsize=(14, 10))

for swcInd, swcFile in enumerate(swcFiles):
    data = np.loadtxt(swcFile)

    slope = (maxMarkerSize - minMarkerSize) / (maxRad - minRad)

    rad2MarkerSize = lambda rad: minMarkerSize + slope * (rad - minRad)

    xs = []
    ys = []
    rads = data[:, 5]
    for ind in range(1, data.shape[0]):

        xs.append([data[ind, 3], data[int(data[ind, 6]) - 1, 3]])
        ys.append([data[ind, 2], data[int(data[ind, 6]) - 1, 2]])


    xs = np.array(xs).T
    ys = np.array(ys).T

    xyDis = gridSize * np.array(np.around(data[:, 3:1:-1] / gridSize), np.intp)
    xDis += xyDis[:, 0].tolist()
    yDis += xyDis[:, 1].tolist()

    xySet = set(map(tuple, xyDis))

    with sns.axes_style('whitegrid'):
        col = cols[swcInd]
        lightCol = getLighterColor(col[:3], 0.5)
        for xy in xySet:

            ax.add_patch(
                mpatches.Rectangle((xy[0] - 0.5 * gridSize, xy[1] - 0.5 * gridSize), width=gridSize, height=gridSize,
                                   fc=lightCol))

        ax.plot(xs, ys, color=col, ls='-', ms=3)

    for x, y, r in zip(xs[0, :], ys[0, :], rads):
        with sns.axes_style('whitegrid'):
            ax.plot(x, y, color=col, marker='o', ms=rad2MarkerSize(r))

ax.axis('square')


xmax = max(xDis) + 0.5 * gridSize
xmin = min(xDis) - 0.5 * gridSize
width = xmax - xmin

ymax = max(yDis) + 0.5 * gridSize
ymin = min(yDis) - 0.5 * gridSize
height = ymax - ymin

ax.set_xlim(xmin - gridSize, xmax + gridSize)
ax.set_ylim(ymin - gridSize, ymax + gridSize)

xticks = np.arange(xmin, xmax + gridSize, gridSize)
yticks = np.arange(ymin, ymax + gridSize, gridSize)

ax.set_xticks(xticks)
ax.set_yticks(yticks)

# xticklabels = ['' if x % 5 else str(y) for x, y in enumerate(xticks)]
# yticklabels = ['' if x % 5 else str(y) for x, y in enumerate(yticks)]

xticklabels = []
yticklabels = []

ax.set_xticklabels(xticklabels, rotation=90)
ax.set_yticklabels(yticklabels)

# ax.set_xlabel(r'X in $\mu$m')
# ax.set_ylabel(r'Y in $\mu$m')
ax.grid(True)

fig.tight_layout()
fig.canvas.draw()


