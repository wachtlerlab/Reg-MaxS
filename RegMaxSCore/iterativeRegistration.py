import os
import numpy as np
from swcFuncs import transSWC, transSWC_rotAboutPoint, getPCADetails
from SWCTransforms import SWCTranslate, objFun
import shutil
import json
import subprocess
from itertools import product


def transPreference(x, y):

    if x == 'scale':
        return 0
    elif y == 'scale':
        return 1
    elif x == 'rot':
        return 0
    else:
        return 1


def getRemainderScale(scale, oldScale):

    toReturn = []
    for s, oldS in zip(scale, oldScale):

        toReturn.append([min(oldS[0] / s, 1), max(oldS[1] / s, 1)])

    return toReturn


class IterativeRegistration(object):

    def __init__(self, refSWC, gridSizes, rotBounds, transBounds,
                 transMinRes, scaleMinRes, rotMinRes, nCPU):

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


    def pca_based(self, SWC2Align, outFiles, tempOPath, gridSize):


        allPossList = [[1, 2, 3]]

        refPts = np.loadtxt(self.refSWC)[:, 2:5]
        refMean = refPts.mean(axis=0)
        SWC2AlignPts = np.loadtxt(SWC2Align)[:, 2:5]
        SWC2AlignMean = SWC2AlignPts.mean(axis=0)

        refEvecs, refNStds = getPCADetails(self.refSWC)
        STAEvecs, STANStds = getPCADetails(SWC2Align)

        scales = [x / y for x, y in zip(refNStds, STANStds)]
        # print scales


        funcVals = []
        totalTranss = []
        for possInd, poss in enumerate(allPossList):

            totalTransform = np.eye(4)
            totalTransform[:3, 3] = -SWC2AlignMean

            poss = np.array(poss)
            possSTAEvecs = np.dot(STAEvecs[:, np.abs(poss) - 1], np.diag(np.sign(poss)))


            temp = np.eye(4)
            temp[:3, :3] = possSTAEvecs.T
            totalTransform = np.dot(temp, totalTransform)

            temp = np.eye(4)
            temp[:3, :3] = np.diag(scales)
            totalTransform = np.dot(temp, totalTransform)

            temp = np.eye(4)
            temp[:3, :3] = refEvecs
            totalTransform = np.dot(temp, totalTransform)

            totalTranslation = refMean

            totalTransform[:3, 3] += totalTranslation

            totalTranss.append(totalTransform)

            SWCPoss = os.path.join(tempOPath, 'poss' + str(possInd) + '.swc')

            transSWC(SWC2Align, totalTransform[:3, :3], totalTransform[:3, 3], SWCPoss)

            trans = SWCTranslate(self.refSWC, SWCPoss, gridSize)
            funcVals.append(objFun(([0, 0, 0], trans)))

        # print(zip(allPossList, funcVals))
        minimum = min(funcVals)
        minimizers = [y for x, y in enumerate(allPossList) if funcVals[x] == minimum]
        minimizerInds = [x for x, y in enumerate(allPossList) if funcVals[x] == minimum]
        numberReflections = [sum([x < 0 for x in y]) for y in minimizers]
        bestSolInd = np.argmin(numberReflections)
        if numberReflections[bestSolInd]:
            print('Reflecting!')
        # bestSol = minimizers[bestSolInd]
        # print(scales[bestSolInd])

        bestTransform = totalTranss[minimizerInds[bestSolInd]]
        transSWC(SWC2Align, bestTransform[:3, :3], bestTransform[:3, 3], outFiles[0])



        # for tFile in tempFiles:
        #     os.remove(tFile)

        with open(outFiles[1], 'w') as fle:
            json.dump({'transMat': bestTransform.tolist(), 'bestVal': minimum}, fle)

        return bestTransform


    def performReg(self, SWC2Align, expName, resDir, scaleBounds, partsDir=None, initGuessType='just_centroids'):

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
            raise(ValueError('Unknown value for arguement \'initGuessType\''))


        SWC2AlignT = SWC2AlignLocal

        scaleDone = False

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
                iterationNo += 1

                SWC2AlignT = outFile

        totalTransform[:3, 3] += totalTranslation

        for g in vals:
            [os.remove(x) for x in tempOutFiles[g]]
        os.remove(ipParFile)

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
                       'SWC2Align': SWC2Align}, fle)

        if partsDir is not None:

            if os.path.isdir(partsDir):

                dirList = os.listdir(partsDir)
                dirList = [x for x in dirList if x.endswith('swc')]

                resPartsDir = os.path.join(resDir, expName)
                if not os.path.isdir(resPartsDir):
                    os.mkdir(resPartsDir)

                for entry in dirList:
                    transSWC_rotAboutPoint(os.path.join(partsDir, entry),
                                           totalTransform[:3, :3], totalTransform[:3, 3],
                                           os.path.join(resPartsDir, entry),
                                           [0, 0, 0]
                                           )




        return finalFile, finalSolFile


def composeRefSWC(alignedSWCs, newRefSWC, gridSize):

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

    trans = SWCTranslate(refSWC, SWC2Align, gridSize)

    return objFun(([0, 0, 0], trans))



def writeFakeSWC(data, fName, extraCol=None):

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