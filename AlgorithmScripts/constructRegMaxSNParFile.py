from numpy import pi, deg2rad
import os
import json
from RegMaxSCore.RegMaxSPars import RegMaxSNParNames

temp = os.path.split(os.path.abspath(__file__))[0]
temp1 = os.path.split(temp)[0]


# **********************************************************************************************************************

# Default parameters
# distances in um, angles in radians
gridSizes = [40.0, 20.0, 10.0]
transBounds = [[-30, 30], [-30, 30], [-30, 30]]
transMinRes = 1
rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
rotMinRes = deg2rad(1).round(4)
scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
minScaleStepSize = 1.005
usePartsDir = False
nCPU = 6
maxIter = 100

# **********************************************************************************************************************

# # User defined parameters. Change these if required
# # distances in um, angles in radians
# gridSizes = [40.0, 20.0, 10.0]
# transBounds = [[-30, 30], [-30, 30], [-30, 30]]
# transMinRes = 1
# rotBounds = [[-pi / 6, pi / 6], [-pi / 6, pi / 6], [-pi / 6, pi / 6]]
# rotMinRes = deg2rad(1).round(4)
# scaleBounds = [[0.5, 1 / 0.5], [0.5, 1 / 0.5], [0.5, 1 / 0.5]]
# minScaleStepSize = 1.005
# nCPU = 6
# maxIter = 100

# **********************************************************************************************************************

# Case 1: Default or user defined parameters above, one reference, one test
# Replace initRefSWC, swcDir, expNames, resDir, parFile, finallyNormalizeWRT as required and
# run this file to generate parFile
# Then run python <...>/Reg-MaxS-N.py parFile

# -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(temp1, 'TestFiles', 'HSNL', 'HSN-fluoro02.CNG.swc')
# swcDir = os.path.join(temp1, 'TestFiles', 'HSNL')
# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(temp1, 'Results', 'Reg-MaxS-N', 'HSNL')
# parFile = os.path.join(temp1, 'ExampleParFiles', 'Reg-MaxS-N', 'HSNL.json')
# finallyNormalizeWRT = initRefSWC
#
# ns = vars()
# pars = [{k: ns[k] for k in RegMaxSNParNames}]
# -----------------------------------------------------------------------------------
initRefSWC = os.path.join(temp1, 'TestFiles', 'LLC', 'Gad1-F-000062.CNG.swc')
swcDir = os.path.join(temp1, 'TestFiles', 'LLC')
expNames = [
            'Gad1-F-000062.CNG',
            'Cha-F-000012.CNG',
            'Cha-F-300331.CNG',
            'Gad1-F-600000.CNG',
            'Cha-F-000018.CNG',
            'Cha-F-300051.CNG',
            'Cha-F-400051.CNG',
            'Cha-F-200000.CNG'
            ]
swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
resDir = os.path.join(temp1, 'Results', 'Reg-MaxS-N', 'LLC')
parFile = os.path.join(temp1, 'ExampleParFiles', 'Reg-MaxS-N', 'LLC.json')
finallyNormalizeWRT = initRefSWC

ns = vars()
pars = [{k: ns[k] for k in RegMaxSNParNames}]
# -----------------------------------------------------------------------------------
# **********************************************************************************************************************

# # Case 2: Default or user defined parameters above, multiple jobs. Each job is a dictionary of parameters
# # that is put together in pars and written into the parFile
#
# pars = []
# parFile = os.path.join(temp1, 'ExampleParFiles', 'Reg-MaxS-N', 'HSNL-HSNR.json')
# # -----------------------------------------------------------------------------------
# # job 1
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(temp1, 'TestFiles', 'HSNL', 'HSN-fluoro02.CNG.swc')
# swcDir = os.path.join(temp1, 'TestFiles', 'HSNL')
# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(temp1, 'Results', 'Reg-MaxS-N', 'HSNL')
# finallyNormalizeWRT = initRefSWC
#
# ns = vars()
# pars += [{k: ns[k] for k in RegMaxSNParNames}]
#
# # -----------------------------------------------------------------------------------
# # job 2
# # -----------------------------------------------------------------------------------
# initRefSWC = os.path.join(temp1, 'TestFiles', 'HSNR', 'HSN-fluoro01.CNG.swc')
# swcDir = os.path.join(temp1, 'TestFiles', 'HSNR')
# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro09.CNG',
#             ]
# swcList = [os.path.join(swcDir, expName + '.swc') for expName in expNames]
# resDir = os.path.join(temp1, 'Results', 'Reg-MaxS-N', 'HSNR')
# finallyNormalizeWRT = initRefSWC
#
# ns = vars()
# pars += [{k: ns[k] for k in RegMaxSNParNames}]

# **********************************************************************************************************************

with open(parFile, 'w') as fle:
    json.dump(pars, fle)

