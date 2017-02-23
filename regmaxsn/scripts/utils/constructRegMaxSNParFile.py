# Ajayrama Kumaraswamy, 2017, LMU Munich

"""
Description:        This script is used to generate a parameter file required to run RegMaxSN.py. This parameter file
                    should contain a json string of a list of dictionaries. Each dictionary is one Reg-MaxS-N job
                    that contains Reg-MaxS-N parameters.
                    See core/RegMaxSPars.py for the description of the parameters.

Usage:              python constructRegMaxSNParFile.py

Action:             creates a parameter file for RegMaxSN.py

Usage guidelines:   There are a couple of cases with examples shown below.
                    Read the comments therein.
                    Essentially edit the values of some variables in this script and run it.


"""

from numpy import pi, deg2rad
import os
import json
from regmaxsn.core.RegMaxSPars import RegMaxSNParNames

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
usePartsDir = True
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

# Case 1: Using Default or user defined parameters above and
# swcList: contains the list of SWCs to register together. This is formed using the list expNames and the directory
# swcDir
# initRefSWC: the initial reference SWC. May or may not be one among swcList
# resDir: directory in which the results are to be created when RegMaxSN.py is run with the parameter file generated by
# this script.
# parFile: the parameter file will be generated at this file path by running this script.
# finallyNormalizeWRT: all SWCs are affinely tranformed together by RegMaxSN.py after completing the registration
# so that this SWC is brought back to its original form.

# Usage: Replace initRefSWC, swcDir, expNames, resDir, parFile, finallyNormalizeWRT as required and
# run this file to generate parFile
# Then run python <...>/RegMaxSN.py parFile

# -----------------------------------------------------------------------------------
# # Example 1
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
# parFile = os.path.join(temp1, 'ParFiles', 'Reg-MaxS-N', 'HSNL.json')
# finallyNormalizeWRT = initRefSWC
#
# obtains the list of variables in the current work space
# ns = vars()
# forms the dictionary of parameters to be saved into the parameter file.
# pars = [{k: ns[k] for k in RegMaxSNParNames}]
# -----------------------------------------------------------------------------------
# Example 2
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
parFile = os.path.join(temp1, 'ParFiles', 'Reg-MaxS-N', 'LLC.json')
finallyNormalizeWRT = initRefSWC

# obtains the list of variables in the current work space
ns = vars()
# forms the dictionary of parameters to be saved into the parameter file.
pars = [{k: ns[k] for k in RegMaxSNParNames}]
# -----------------------------------------------------------------------------------
# **********************************************************************************************************************

# # Case 2: Using Default or user defined parameters above, and other parameters below.
# Parameters are same as in Case 1 above, but multiple jobs can be specified in this case.

# Usage: Replace initRefSWC, swcDir, expNames, resDir, parFile, finallyNormalizeWRT as required for each job and
# run this file to generate parFile
# Then run python <...>/RegMaxSN.py parFile
#
# pars = []
# parFile = os.path.join(temp1, 'ParFiles', 'Reg-MaxS-N', 'HSNL-HSNR.json')
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
# obtains the list of variables in the current work space
# ns = vars()
# forms the dictionary of parameters to be saved into the parameter file.
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
# obtains the list of variables in the current work space
# ns = vars()
# forms the dictionary of parameters to be saved into the parameter file.
# pars += [{k: ns[k] for k in RegMaxSNParNames}]

# **********************************************************************************************************************

# write the parameters into the parameter file.
with open(parFile, 'w') as fle:
    json.dump(pars, fle)
