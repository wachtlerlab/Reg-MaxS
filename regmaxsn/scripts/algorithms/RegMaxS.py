import sys
from regmaxsn.core.iterativeRegistration import IterativeRegistration
from regmaxsn.core.misc import parFileCheck
import os
import pathlib as pl


def runRegMaxS(parFile, parNames):
    parsList = parFileCheck(parFile, parNames)

    for pars in parsList:
        print('Current Parameters:')
        for parN, parV in pars.items():
            print(('{}: {}'.format(parN, parV)))

        resFile = pars['resFile']
        refSWC = pars['refSWC']
        testSWC = pars['testSWC']

        res_filepath = pl.Path(resFile)
        if res_filepath.is_file():

            ch = input('File exists: ' + resFile + '\nDelete(y/n)?')
            if ch == 'y':
                res_filepath.unlink()
            else:
                quit()

        res_filepath.parent.mkdir(exist_ok=True)

        assert pl.Path(refSWC).is_file(), 'Could  not find {}'.format(refSWC)
        assert pl.Path(testSWC).is_file(), 'Could  not find {}'.format(testSWC)

        iterReg = IterativeRegistration(refSWC=pars['refSWC'],
                                        gridSizes=pars['gridSizes'],
                                        rotBounds=pars['rotBounds'],
                                        transBounds=pars['transBounds'],
                                        transMinRes=pars['transMinRes'],
                                        scaleMinRes=pars['minScaleStepSize'],
                                        rotMinRes=pars['rotMinRes'],
                                        nCPU=pars['nCPU'])

        iterReg.performReg(SWC2Align=pars['testSWC'],
                           resFile=pars['resFile'],
                           scaleBounds=pars['scaleBounds'],
                           inPartsDir=pars['inPartsDir'],
                           outPartsDir=pars['outPartsDir'],
                           retainTempFiles=pars['retainTempFiles'])


if __name__ == '__main__':

    from regmaxsn.core.RegMaxSPars import RegMaxSParNames
    assert len(sys.argv) == 2, 'Improper usage! Please use as \'python RegMaxS.py parFile\''

    parFile = sys.argv[1]

    runRegMaxS(parFile, RegMaxSParNames)
