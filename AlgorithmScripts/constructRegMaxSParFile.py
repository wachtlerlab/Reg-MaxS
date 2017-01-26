from numpy import pi, deg2rad
import os
import json
from RegMaxSCore.RegMaxSPars import RegMaxSParNames

temp = os.path.split(os.path.abspath(__file__))[0]
temp1 = os.path.split(temp)[0]


# **********************************************************************************************************************

# Default parameters
# distances in um, angles in radians
gridSizes = [80.0, 40.0, 20.0, 10.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
rotMinRes = deg2rad(1).round(4)
scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
minScaleStepSize = 1.005
retainTempFiles = False
inPartsDir = None
outPartsDir = None
nCPU = 6

# **********************************************************************************************************************

# # User defined parameters
# # distances in um, angles in radians
# gridSizes = [40.0, 20.0, 10.0]
# transBounds = [[-30, 30], [-30, 30], [-30, 30]]
# transMinRes = 1
# rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
# rotMinRes = deg2rad(1).round(4)
# scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
# minScaleStepSize = 1.005

# **********************************************************************************************************************

# # Case 1: Default or user defined parameters above, one reference, one test
# # Replace refSWC, testSWC, resFile and parFile as required and run this file to generate parFile
# # Then run python <...>/RegMaxS.py parFile
#
# -------------------------------------------
# # Example 1
# refSWC = os.path.join(temp1, 'TestFiles', 'HSN-fluoro01.CNG.swc')
# testSWC = os.path.join(temp1, 'TestFiles', 'HSN-fluoro01.CNGRandTrans1.swc')
# resFile = os.path.join(temp1, 'Results', 'Tests', 'HSN-fluoro01.CNGRandTrans1.swc')
# parFile = os.path.join(temp1, 'ExampleParFiles', 'Reg-MaxS', 'HSN-fluoro01.CNGRandTrans1.json')
# -------------------------------------------
# Example 2
refSWC = os.path.join(temp1, 'TestFiles', 'LLC', 'Gad1-F-000062.CNG.swc')
testSWC = os.path.join(temp1, 'TestFiles', 'LLC', 'Cha-F-400051.CNG.swc')
resFile = os.path.join(temp1, 'Results', 'Tests', 'LLC', 'Cha-F-400051.CNG.swc')
parFile = os.path.join(temp1, 'ExampleParFiles', 'Reg-MaxS', 'LLC1.json')
inPartsDir = os.path.join(temp1, 'TestFiles', 'LLC', 'Cha-F-400051.CNG')
outPartsDir = os.path.join(temp1, 'Results', 'Tests', 'LLC', 'Cha-F-400051.CNG')
#
# -------------------------------------------
ns = vars()
pars = [{k: ns[k] for k in RegMaxSParNames}]
# **********************************************************************************************************************

# # Case 2: Default or user defined parameters above, one reference, many tests, all in same directory
#
# dirPath = os.path.join(temp1, 'TestFiles')
# refSWC = os.path.join(dirPath, 'HSN-fluoro01.CNG.swc')
# testSWCFiles = [
#             'HSN-fluoro01.CNGRandTrans0.swc',
#             'HSN-fluoro01.CNGRandTrans1.swc',
#             'HSN-fluoro01.CNGRandTrans2.swc',
#             'HSN-fluoro01.CNGRandTrans3.swc',
#             'HSN-fluoro01.CNGRandTrans4.swc',
#             'HSN-fluoro01.CNGRandTrans5.swc',
#             'HSN-fluoro01.CNGRandTrans6.swc',
#             'HSN-fluoro01.CNGRandTrans7.swc',
#             'HSN-fluoro01.CNGRandTrans8.swc',
#             'HSN-fluoro01.CNGRandTrans9.swc',
#
#             # 'HSN-fluoro01.CNGNoiseStd1RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd2RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd3RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd4RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd5RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd6RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd7RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd8RandTrans.swc',
#             # 'HSN-fluoro01.CNGNoiseStd9RandTrans.swc',
#             ]
# resPath = os.path.join(temp1, 'Results', 'Tests')
# parFile = os.path.join(temp1, 'ExampleParFiles', 'Reg-MaxS', 'HSN-fluoro01.CNGRandTrans0-9.json')
#
# pars = []
# for sfr in testSWCFiles:
#     testSWC = os.path.join(dirPath, sfr)
#     resFile = os.path.join(resPath, sfr)
#     ns = vars()
#     pars.append({k: ns[k] for k in RegMaxSParNames})

# **********************************************************************************************************************

with open(parFile, 'w') as fle:
    json.dump(pars, fle)

