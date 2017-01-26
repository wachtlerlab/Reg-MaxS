import os
import json
from RegMaxSCore.RegMaxSPars import pcaBasedParNames

temp = os.path.split(os.path.abspath(__file__))[0]
temp1 = os.path.split(temp)[0]


# **********************************************************************************************************************

# Default parameters
# distances in um, angles in radians
gridSizes = [40.0, 20.0, 10.0]
usePartsDir = True

# **********************************************************************************************************************

# # User defined parameters
# # distances in um, angles in radians
# gridSizes = [40.0, 20.0, 10.0]
# usePartsDir = False

# **********************************************************************************************************************

# # Case 1: Default or user defined parameters above, one reference, one test
# # Replace refSWC, testSWC, resFile and parFile as required and run this file to generate parFile
# # Then run python <...>/pcaBased.py parFile
#
# refSWC = os.path.join(temp1, 'TestFiles', 'HSNR', 'HSN-fluoro01.CNG.swc')
# testSWC = os.path.join(temp1, 'TestFiles', 'HSNR', 'HSN-fluoro04.CNG.swc')
# resFile = os.path.join(temp1, 'Results', 'PCABased', 'HSNR', 'HSN-fluoro04.CNG.swc')
# parFile = os.path.join(temp1, 'ExampleParFiles', 'PCABased', 'HSNR1-4.json')
#
#
# ns = vars()
# pars = [{k: ns[k] for k in pcaBasedParNames}]
# **********************************************************************************************************************

# Case 2: Default or user defined parameters above, one reference, many tests, all in same directory
# -----------------------------------------------------------------------------------
# dirPath = os.path.join(temp1, 'TestFiles', 'HSNR')
# refSWC = os.path.join(dirPath, 'HSN-fluoro01.CNG.swc')
# expNames = [
#             'HSN-fluoro01.CNG',
#             'HSN-fluoro04.CNG',
#             'HSN-fluoro05.CNG',
#             'HSN-fluoro07.CNG',
#             'HSN-fluoro09.CNG',
#             ]
# resPath = os.path.join(temp1, 'Results', 'PCABased', 'HSNR')
# parFile = os.path.join(temp1, 'ExampleParFiles', 'PCABased', 'HSNR.json')
#
# pars = []
# for sfr in expNames:
#     testSWC = os.path.join(dirPath, sfr + '.swc')
#     resFile = os.path.join(resPath, sfr + '.swc')
#     ns = vars()
#     pars.append({k: ns[k] for k in pcaBasedParNames})

# -----------------------------------------------------------------------------------
# dirPath = os.path.join(temp1, 'TestFiles', 'HSNL')
# refSWC = os.path.join(dirPath, 'HSN-fluoro02.CNG.swc')
# expNames = [
#             'HSN-fluoro02.CNG',
#             'HSN-fluoro03.CNG',
#             'HSN-fluoro06.CNG',
#             'HSN-fluoro08.CNG',
#             'HSN-fluoro10.CNG',
#             ]
# resPath = os.path.join(temp1, 'Results', 'PCABased', 'HSNL')
# parFile = os.path.join(temp1, 'ExampleParFiles', 'PCABased', 'HSNL.json')
#
# pars = []
# for sfr in expNames:
#     testSWC = os.path.join(dirPath, sfr + '.swc')
#     resFile = os.path.join(resPath, sfr + '.swc')
#     ns = vars()
#     pars.append({k: ns[k] for k in pcaBasedParNames})
# # -----------------------------------------------------------------------------------
dirPath = os.path.join(temp1, 'TestFiles', 'LLC')
refSWC = os.path.join(dirPath, 'Gad1-F-000062.CNG.swc')
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
resPath = os.path.join(temp1, 'Results', 'PCABased', 'LLC')
parFile = os.path.join(temp1, 'ExampleParFiles', 'PCABased', 'LLC.json')

pars = []
for sfr in expNames:
    testSWC = os.path.join(dirPath, sfr + '.swc')
    resFile = os.path.join(resPath, sfr + '.swc')
    ns = vars()
    pars.append({k: ns[k] for k in pcaBasedParNames})
# -----------------------------------------------------------------------------------
# **********************************************************************************************************************

with open(parFile, 'w') as fle:
    json.dump(pars, fle)
