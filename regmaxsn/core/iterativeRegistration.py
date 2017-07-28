import os
import numpy as np
from .swcFuncs import transSWC, transSWC_rotAboutPoint
from .SWCTransforms import SWCTranslate, objFun
import shutil
import json
import subprocess

def transPreference(x, y):
    """
    Given two transforms x and y, returns if x is preferred over y. Preferences are scaling > translation,
    scaling > rotation, translation > rotation.
    :param x:
    :param y:
    :return:
    """
    if x == 'scale':
        return 0
    elif y == 'scale':
        return 1
    elif x == 'rot':
        return 0
    else:
        return 1


def getRemainderScale(scale, oldScale):
    """
    Elementwise divides oldScale by scale, effectively removing scale from old scale. The first entry is bounded
    above by 1 and the second entry is bounded below by 1.
    :param scale: 3 member list of 2 member float lists.
    :param oldScale: 3 member list of 2 member float lists.
    :return: 3 member list of 2 member float lists.
    """
    toReturn = []
    for s, oldS in zip(scale, oldScale):

        toReturn.append([min(oldS[0] / s, 1), max(oldS[1] / s, 1)])

    return toReturn


class IterativeRegistration(object):
    """
    This class is used to run basic Reg-MaxS algorithm.
    """
    def __init__(self, refSWC, gridSizes, rotBounds, transBounds,
                 transMinRes, scaleMinRes, rotMinRes, nCPU):
        """
        Initialization
        :param refSWC: valid file path to a valid SWC file, reference SWC
        :param gridSizes: list of three floats, the voxel sizes over which estimations are run, in micrometer
        :param rotBounds: three member list of two member float lists, the bounds for rotation euler angles abour XYZ
                            axes, in radians
        :param transBounds: three member list of two member float lists, the bounds for translations along XYZ axes.
        :param transMinRes: float, minimum resolution of exhaustive search for translation parameters in micrometer.
        :param scaleMinRes: float. minimum (multiplicative) resolution of exhuasitve search for scaling paramers.
        :param rotMinRes: float. minimum resolution of exhuastive search for rotation euler angle parameters in radians.
        :param nCPU: int, number of processes to use
        """
        super(IterativeRegistration, self).__init__()

        self.refSWC = refSWC
        self.gridSizes = gridSizes
        self.rotBounds = rotBounds
        self.transBounds = transBounds
        self.rotBounds = rotBounds
        self.transMinRes = transMinRes
        self.rotMinRes = rotMinRes
        self.scaleMinRes = scaleMinRes
        self.nCPU = nCPU
        self.allFuncs = {'trans': self.transOnce, 'rot': self.rotOnce, 'scale': self.scaleOnce}



    def rotOnce(self, SWC2Align, outFiles, ipParFile):
        """
        Runs exhaustive search to find the best rotation euler angles about XYZ axes that maximize the volume overlap
        between SWC2Align and self.refSWC. Results are written in the two file paths of outFiles.
        If solution found is no better than doing nothing or if the angles found are lower than minimum resolution,
        zero angles are returned with done as true
        :param SWC2Align: valid file path to a valid SWC file
        :param outFiles: list of two valid file paths. SWC2Align rotated with optimum parameters is written to
        outFiles[0], a log file of the process is written into ouFiles[1].
        :param ipParFile: valid file path. Temporary file used.
        :return: bestSol, bestVal, done
                bestSol: list of three floats, best Euler angles in radians
                bestVal: float, best value of dissimilarity between SWC2Align and refSWC at the lowest voxel size
                done: boolean, see above.
        """
        pars = [self.refSWC, SWC2Align, outFiles,
                self.gridSizes, self.rotBounds, self.rotMinRes, self.nCPU]

        with open(ipParFile, 'w') as fle:
            json.dump(pars, fle)

        f2call = os.path.join(os.path.split(__file__)[0], 'rotOnce.py')
        subprocess.call(['python', f2call, ipParFile])

        with open(outFiles[1], 'r') as fle:
            out = json.load(fle)
            bestSol = out['bestSol']
            done = out['done']
            bestVal = out['bestVal']
            print(bestSol, bestVal, done)

        return bestSol, bestVal, done

    def transOnce(self, SWC2Align, outFiles, ipParFile):
        """
        Runs exhaustive search to find the best translations along XYZ axes that maximize the volume overlap between
        SWC2Align and self.refSWC. Results are written in the two file paths of outFiles.
        If solution found is no better than doing nothing or if the translations found are lower than
        the minimum resolution, zero translations are returned with done set to true
        :param SWC2Align: valid file path to a valid SWC file
        :param outFiles: list of two valid file paths. SWC2Align translated with optimum parameters is written to
        outFiles[0], a log file of the process is written into ouFiles[1].
        :param ipParFile: valid file path. Temporary file used.
        :return: bestSol, bestVal, done
                bestSol: list of three floats, best translations in micrometer
                bestVal: float, best value of dissimilarity between SWC2Align and refSWC at the lowest voxel size
                done: boolean, see above.
        """
        pars = [self.refSWC, SWC2Align, outFiles,
                self.gridSizes, self.transBounds, self.transMinRes, self.nCPU]

        with open(ipParFile, 'w') as fle:
            json.dump(pars, fle)

        f2call = os.path.join(os.path.split(__file__)[0], 'transOnce.py')
        subprocess.call(['python', f2call, ipParFile])

        with open(outFiles[1], 'r') as fle:
            out = json.load(fle)
            bestSol = out['bestSol']
            done = out['done']
            bestVal = out['bestVal']
            print(bestSol, bestVal, done)

        return bestSol, bestVal, done

    def scaleOnce(self, SWC2Align, outFiles, ipParFile, scaleBounds):
        """
        Runs exhaustive search to find the best scaling parameters along XYZ axes that maximize the volume overlap
        between SWC2Align and self.refSWC. Results are written in the two file paths of outFiles.
        If solution found is no better than doing nothing or if the scaling parameters found are lower than
        the minimum resolution, unity scaling parameters are returned with done set to true
        :param SWC2Align: valid file path to a valid SWC file
        :param outFiles: list of two valid file paths. SWC2Align scaled with optimum parameters is written to
        outFiles[0], a log file of the process is written into ouFiles[1].
        :param ipParFile: valid file path. Temporary file used.
        :return: bestSol, bestVal, done
                bestSol: list of three floats, best scaling parameters
                bestVal: float, best value of dissimilarity between SWC2Align and refSWC at the lowest voxel size
                done: boolean, see above.
        """
        pars = [self.refSWC, SWC2Align, outFiles,
                self.gridSizes, scaleBounds, self.scaleMinRes, self.nCPU]

        with open(ipParFile, 'w') as fle:
            json.dump(pars, fle)

        f2call = os.path.join(os.path.split(__file__)[0], 'scaleOnce.py')
        subprocess.call(['python', f2call, ipParFile])

        with open(outFiles[1], 'r') as fle:
            out = json.load(fle)
            bestSol = out['bestSol']
            done = out['done']
            bestVal = out['bestVal']
            print(bestSol, bestVal, done)

        return bestSol, bestVal, done

    def compare(self, srts, SWC2Align, tempOutFiles, ipParFile, scaleBounds):
        """
        Runs the exhaustive searchs for the transforms in srts and returns some info about the searches
        :param srts: list of strings, valid entries are 'scale', 'trans' and 'rot'
        :param SWC2Align: valid file path of valid SWC file.
        :param tempOutFiles: list of two valid file paths, for temporary internal use.
        :param ipParFile: valid file path, for temporary internal use.
        :param scaleBounds: three member list of two member float lists, the bounds for scaling parameters
         along XYZ axes.
        :return: tempDones, presBestSol, presBestVal, presBestDone, presBestTrans
                 tempDones: list of booleans, same size as srts, contains the value of 'done' of respective exhaustive
                 searches
                 presBestTrans: transform among srts leading to the lowest dissimilarity
                 presBestSol: list of three floats, correspong transform parameters
                 presBestDone: boolean, 'done' value of presBestTrans
        """
        presBestVal = 1e6
        presBestTrans = 'trans'
        presBestSol = [0, 0, 0]
        presBestDone = False

        tempDones = {}

        for g in srts:

            if g == 'scale':
                bestSol, bestVal, done = self.scaleOnce(SWC2Align, tempOutFiles[g], ipParFile, scaleBounds)
            elif g == 'rot':
                bestSol, bestVal, done = self.rotOnce(SWC2Align, tempOutFiles[g], ipParFile)
            elif g == 'trans':
                bestSol, bestVal, done = self.transOnce(SWC2Align, tempOutFiles[g], ipParFile)
            else:
                raise('Invalid transformation type ' + g)


            tempDones[g] = done

            if (bestVal == presBestVal and transPreference(presBestTrans, g)) or (bestVal < presBestVal):

                presBestTrans = g
                presBestVal = bestVal
                presBestSol = bestSol
                presBestDone = done


        return tempDones, presBestSol, presBestVal, presBestDone, presBestTrans





    def performReg(self, SWC2Align, resFile, scaleBounds,
                   inPartsDir=None, outPartsDir=None,
                   initGuessType='just_centroids',
                   retainTempFiles=False):
        """
        Repeatedly applies translation, rotation and scaling transforms to SWC2Align to maximize its volume overlap
        with self.refSWC. See Reg-MaxS-N manuscript for more info.

        :param SWC2Align: valid file path of a valid SWC file, the SWC that is registered to self.refSWC
        :param resFile: valid file path, where SWC2Align registered to self.refSWC is written
        :param scaleBounds: three member list of two member float lists, the bounds for scaling parameters
        :param inPartsDir: valid directory path, any swc files with this will be transformed exactly same as
                            SWC2Align and written in to outPartsDir
        :param outPartsDir: valid directory path
        :param initGuessType: string, valid values are 'just centroids' and 'nothing'. If 'just centroids', the
        centroids are initially matched, if 'nothing' they are not.
        :param retainTempFiles: boolean, whether to retain the intermediate files.
        :return: finalFile, finalSolFile
                 finalFile: same as resFile
                 finalSolFile: a file at <resFile name>Sol.txt where results of the process are logged.
        """

        resDir, expName = os.path.split(resFile[:-4])

        ipParFile = os.path.join(resDir, 'tmp.json')
        vals = ['trans', 'rot', 'scale']
        tempOutFiles = {}
        for val in vals:
            fle1 = os.path.join(resDir, val + '.swc')
            fle2 = os.path.join(resDir, val + 'bestSol.json')
            tempOutFiles[val] = [fle1, fle2]

        refMean = np.loadtxt(self.refSWC)[:, 2:5].mean(axis=0)
        iterationNo = 0

        tempOutPath = os.path.join(resDir, expName + 'trans')
        if not os.path.isdir(tempOutPath):
            os.mkdir(tempOutPath)

        SWC2AlignLocal = os.path.join(tempOutPath, str(iterationNo) + '.swc')
        SWC2AlignMean = np.loadtxt(SWC2Align)[:, 2:5].mean(axis=0)

        if initGuessType == 'just_centroids':

            transSWC(SWC2Align, np.eye(3), refMean - SWC2AlignMean, SWC2AlignLocal)
            totalTransform = np.eye(4)
            totalTransform[:3, 3] = -SWC2AlignMean
            totalTranslation = refMean

        elif initGuessType == 'nothing':

            shutil.copy(SWC2Align, SWC2AlignLocal)
            totalTransform = np.eye(4)
            totalTransform[:3, 3] = -SWC2AlignMean
            totalTranslation = SWC2AlignMean

        else:
            raise(ValueError('Unknown value for argument \'initGuessType\''))


        SWC2AlignT = SWC2AlignLocal

        scaleDone = False
        bestVals = {}

        while not scaleDone:

            done = False
            srts = ['rot', 'trans']


            while not done:

                tempDones, bestSol, bestVal, lDone, g = self.compare(srts, SWC2AlignT, tempOutFiles, ipParFile, None)

                outFile = os.path.join(tempOutPath, str(iterationNo) + g[0] + '.swc')

                outFileSol = os.path.join(tempOutPath, 'bestSol' + str(iterationNo) + g[0] + '.txt')

                shutil.copyfile(tempOutFiles[g][0], outFile)
                shutil.copyfile(tempOutFiles[g][1], outFileSol)

                with open(outFileSol, 'r') as fle:
                    pars = json.load(fle)
                    presTrans = np.array(pars['transMat'])
                    if g == 'trans':
                        totalTranslation += presTrans[:3, 3]
                    else:
                        totalTransform = np.dot(presTrans, totalTransform)

                print(str(iterationNo) + g)

                bestVals[bestVal] = {"outFile": outFile, "outFileSol": outFileSol,
                                     "totalTransform": totalTransform,
                                     "totalTranslation": totalTranslation,
                                     "iterationIndicator": str(iterationNo) + g
                                     }

                iterationNo += 1

                done = lDone

                SWC2AlignT = outFile


            bestSol, bestVal, sDone = self.scaleOnce(SWC2AlignT, tempOutFiles['scale'], ipParFile, scaleBounds)

            outFile = os.path.join(tempOutPath, str(iterationNo) + 's.swc')

            outFileSol = os.path.join(tempOutPath, 'bestSol' + str(iterationNo) + 's.txt')

            shutil.copyfile(tempOutFiles['scale'][0], outFile)
            shutil.copyfile(tempOutFiles['scale'][1], outFileSol)

            with open(outFileSol, 'r') as fle:
                pars = json.load(fle)
                presTrans = np.array(pars['transMat'])
                totalTransform = np.dot(presTrans, totalTransform)

            print(str(iterationNo) + 's')

            bestVals[bestVal] = {"outFile": outFile, "outFileSol": outFileSol,
                                 "totalTransform": totalTransform,
                                 "totalTranslation": totalTranslation,
                                 "iterationIndicator": str(iterationNo) + 's'
                                 }

            iterationNo += 1

            SWC2AlignT = outFile


            tempDones, bestSol, bestVal, lDone, g = self.compare(vals, SWC2AlignT, tempOutFiles, ipParFile, scaleBounds)
            scaleDone = all(tempDones.values())

            if not scaleDone:
                with open(tempOutFiles['rot'][1], 'r') as fle:
                    pars = json.load(fle)
                    rBestVal = pars['bestVal']

                with open(tempOutFiles['trans'][1], 'r') as fle:
                    pars = json.load(fle)
                    tBestVal = pars['bestVal']

                if rBestVal < tBestVal:
                    g = 'rot'
                else:
                    g = 'trans'

                outFile = os.path.join(tempOutPath, str(iterationNo) + g[0] + '.swc')

                outFileSol = os.path.join(tempOutPath, 'bestSol' + str(iterationNo) + g[0] + '.txt')

                shutil.copyfile(tempOutFiles[g][0], outFile)
                shutil.copyfile(tempOutFiles[g][1], outFileSol)

                with open(outFileSol, 'r') as fle:
                    pars = json.load(fle)
                    presTrans = np.array(pars['transMat'])
                    if g == 'trans':
                        totalTranslation += presTrans[:3, 3]
                    else:
                        totalTransform = np.dot(presTrans, totalTransform)

                print(str(iterationNo) + g)

                bestVals[bestVal] = {"outFile": outFile, "outFileSol": outFileSol,
                                     "totalTransform": totalTransform,
                                     "totalTranslation": totalTranslation,
                                     "iterationIndicator": str(iterationNo) + g
                                     }

                iterationNo += 1

                SWC2AlignT = outFile

        championBestVal = min(bestVals.keys())
        totalTransform = bestVals[championBestVal]["totalTransform"]
        totalTranslation = bestVals[championBestVal]["totalTranslation"]
        bestIterIndicator = bestVals[championBestVal]["iterationIndicator"]

        print("bestIter: {}, bestVal: {}".format(bestIterIndicator, championBestVal))

        totalTransform[:3, 3] += totalTranslation

        for g in vals:
            [os.remove(x) for x in tempOutFiles[g]]
        os.remove(ipParFile)

        if not retainTempFiles:
            shutil.rmtree(tempOutPath)

        finalFile = os.path.join(resDir, expName + '.swc')
        transSWC_rotAboutPoint(SWC2Align,
                               totalTransform[:3, :3], totalTransform[:3, 3],
                               finalFile,
                               [0, 0, 0]
                               )
        trans = SWCTranslate(self.refSWC, finalFile, self.gridSizes[-1])
        finalVal = objFun(([0, 0, 0], trans))
        finalSolFile = os.path.join(resDir, expName + 'Sol.txt')

        with open(finalSolFile, 'w') as fle:
            json.dump({'finalVal': finalVal, 'finalTransMat': totalTransform.tolist(), 'refSWC': self.refSWC,
                       'SWC2Align': SWC2Align, 'bestIteration': bestIterIndicator}, fle)

        if inPartsDir is not None:

            if os.path.isdir(inPartsDir):

                dirList = os.listdir(inPartsDir)
                dirList = [x for x in dirList if x.endswith('.swc')]

                if not os.path.isdir(outPartsDir):
                    os.mkdir(outPartsDir)

                for entry in dirList:
                    transSWC_rotAboutPoint(os.path.join(inPartsDir, entry),
                                           totalTransform[:3, :3], totalTransform[:3, 3],
                                           os.path.join(outPartsDir, entry),
                                           [0, 0, 0]
                                           )

            else:
                print('Specified partsDir {} not found'.format(inPartsDir))


        return finalFile, finalSolFile


def composeRefSWC(alignedSWCs, newRefSWC, gridSize):
    """
    Given a list of SWCs, it constructs a fake SWC to represent the union of the volumes occupied by the SWCs.
    :param alignedSWCs: list of SWC files
    :param newRefSWC: valid file path, where the resulting SWC is written
    :param gridSize: float, the voxel size at which the volumes are discretized before forming the union.
    :return: dissim: float, 1 - (# of voxels in the intersection of volumes) / (# of voxels in the union of volumes)
    """
    indVoxs = []

    for aswc in alignedSWCs:
        aPts = np.loadtxt(aswc)[:, 2:5]
        aVox = np.array(np.round(aPts / gridSize), np.int32)
        aVoxSet = set(map(tuple, aVox))
        indVoxs.append(aVoxSet)

    # majority = [sum(x in y for y in indVoxs) >= 0.5 * len(indVoxs) for x in aUnion]

    # newRefVoxSet = [y for x, y in enumerate(aUnion) if majority[x]]

    aUnion = reduce(lambda x, y: x.union(y), indVoxs)
    aInt = reduce(lambda x, y: x.intersection(y), indVoxs)

    newRefVoxSet = aUnion


    newRefXYZ = np.array(list(newRefVoxSet)) * gridSize

    writeFakeSWC(newRefXYZ, newRefSWC)
    # print(len(aInt), len(aUnion))

    return 1 - len(aInt) / float(len(aUnion))


def calcOverlap(refSWC, SWC2Align, gridSize):
    """
    Given two SWCs, it calculates a measure of dissimilarity between them using their discretized volumes.
    It's defined as 1 - size of intersection of the volumes / size of union of the volumes
    :param refSWC: valid file path to a valid SWC file
    :param SWC2Align: valid file path to a valid SWC file
    :param gridSize: float, the voxel size at which the volumes are discretized.
    :return: float, dissimilarity value
    """
    trans = SWCTranslate(refSWC, SWC2Align, gridSize)

    return objFun(([0, 0, 0], trans))



def writeFakeSWC(data, fName, extraCol=None):
    """
    Forms a 7 column SWC data from the 3 column XYZ data in 'data' and writes it to a file at path fName adding
    a '!! Fake SWC !!' warning in the header.
    :param data: numpy.ndarray, 3 column XYZ data
    :param fName: valid file path to write the fake SWC file
    :param extraCol: iterable of the same size as the number of rows of data, will be added as the 8th column
    :return:
    """
    data = np.array(data)

    assert data.shape[1] == 3

    if extraCol is not None:
        extraCol = np.array(extraCol)
        assert extraCol.shape == (data.shape[0], ) or extraCol.shape == (data.shape[0], 1)

        toWrite = np.empty((data.shape[0], 8))
        toWrite[:, 7] = extraCol
    else:
        toWrite = np.empty((data.shape[0], 7))

    toWrite[:, 2:5] = data
    toWrite[:, 0] = range(1, data.shape[0] + 1)
    toWrite[:, 1] = 3
    toWrite[:, 5] = 1
    toWrite[:, 6] = -np.arange(1, data.shape[0] + 1)


    formatStr = '%d %d %0.6f %0.6f %0.6f %0.6f %d'

    if extraCol is not None:
        formatStr += ' %d'
    headr = '!! Fake SWC file !!'
    np.savetxt(fName, toWrite, fmt=formatStr, header=headr)