# Ajayrama Kumaraswamy, 2017, LMU Munich

"""
The input parameters of different Algorithms
"""

# **********************************************************************************************************************
"""
Parameters of Reg-MaxS.
refSWC:                 string. The reference SWC file, to which testFile is registered.
                        Must be a valid SWC file on the file system.

testSWC:                string. The test SWC file which is registered to refSWC.
                        Must be a valid SWC file on the file system.

resFile:                string. This file will be created and the resulting SWC will be written into it.
                        It needs to be valid file reference.

gridSizes:              list of floats. These are the voxel sizes over which Reg-MaxS is run.
                        Values must be in micrometers.

transBounds:            three member list, each element is a two member list. These members must be floats.
                        They are bounds used for estimating translation parameters along XYZ axes.
                        Values must be in micrometers.

transMinRes:            float. After searching at the three voxel sizes in gridSizes, a further search is carried
                        out at this resolution for translation parameters. Values must be in micrometers.

rotBounds:              three member list, each element is a two member list. These members must be floats.
                        They are bounds used for estimating rotation parameters about XYZ axes.
                        Values must be in radians.

rotMinRes:              float. After refining rotation parameters at the three voxel sizes in gridSizes, a further
                        refinement is carried out at this resolution. Values must be in radians.

scaleBounds:            three member list, each element is a two member list. These members must be floats.
                        They are bounds used for estimating scaling parameters along XYZ axes.

minScaleStepSize:       float. After refining scaling parameters at the three voxel sizes in gridSizes, a further
                        refinement is carried out at this resolution.

nCPU:                   int. Reg-MaxS internally uses multiple processes for exhaustive searches.
                        This specifies the number of processes to use. It can be a maximum of number of
                        processors on the machine being used. Larger this number, faster the execution.

inPartsDir:             string. A file system directory, the swc files in which are transformed exactly the same as
                        testSWC and written into outPartsDir.

outPartsDir:            string. A file system directory into which the transformed swc files of inPartsDir are written.
                        It will be created if it does not exist.

retainTempFiles:        boolean. Reg-MaxS generates some temporary files in the directory where resFile is supposed to
                        be created. If retainTempFiles is True, these are not deleted. Else, they are.


"""
RegMaxSParNames = ['refSWC', 'testSWC', 'resFile',
                   'gridSizes',
                   'transBounds', 'transMinRes',
                   'rotBounds', 'rotMinRes',
                   'scaleBounds', 'minScaleStepSize',
                   'nCPU', 'inPartsDir', 'outPartsDir', 'retainTempFiles']

# **********************************************************************************************************************

"""
Parameters of Reg-MaxS-N. Some parameters are same as of Reg-MaxS above and hence are omitted here.

swcList:                list of strings. Each member must refer to a valid SWC file on the file system.

initRefSWC:             string. The initial reference to use for Reg-MaxS-N, i.e., the reference of the first iteration.
                        Must be a valid SWC file on the file system.

resDir:                 string. The directory into which the results of Reg-MaxS-N are written. Will be created anew
                        or replaced if it exists.

finallyNormalizeWRT:    string. Must be one of the SWCs of swcList. The whole set of SWCs after registration
                        is transformed affinely together so that this SWC is restored to it's final form.

maxIter:                int. The number of iterations for which Reg-MaxS-N runs before stopping and returning the
                        result.

usePartsDir:            boolean. If True, Reg-MaxS-N check if for every SWC in swcList, a folder exists with the
                        same name and path without the '.swc' extention. If such folders exist, the SWCs in them are
                        transformed exactly the same as their corresponding SWCs and written into folders with the same
                        name in resDir.

"""

RegMaxSNParNames = [
                    'swcList', 'initRefSWC', 'resDir', 'finallyNormalizeWRT', 'maxIter',
                    'gridSizes',
                    'transBounds', 'transMinRes',
                    'rotBounds', 'rotMinRes',
                    'scaleBounds', 'minScaleStepSize',
                    'nCPU', 'usePartsDir'
                    ]

# **********************************************************************************************************************

"""
Parameters of the registration PCA-based algorithm. Some parameters have the same meaning as in Reg-MaxS above and
hence have been omitted here.

gridSizes:              list of floats. These are the voxel sizes over which Reg-MaxS is run.
                        Values must be in micrometers. These values are not used in the actual algorithm. The last
                        element of this list is used to calculate a measure of dissimilarity between the reference SWC
                        and the result SWC produced by the 'pcaBased' algorithm.

usePartsDir:            boolean. If True, Reg-MaxS-N check if for every SWC in swcList, a folder exists with the
                        same name and path without the '.swc' extention. If such folders exist, the SWCs in them are
                        transformed exactly the same as their corresponding SWCs and written into folders with the same
                        name in resDir.
"""

pcaBasedParNames = [
                    'refSWC', 'testSWC', 'resFile',
                    'gridSizes', 'usePartsDir'
                    ]
# **********************************************************************************************************************

DensitySaveParNames = ['refSWC', 'resFile']