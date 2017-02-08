import numpy as np

#***********************************************************************************************************************


def readSWC_numpy(swcFile):
    '''
    Read the return the header and matrix data in a swcFile
    :param swcFile: filename
    :return: header (string), matrix data (ndarray)
    '''
    headr = ''
    with open(swcFile, 'r') as fle:
        lne = fle.readline()
        while lne[0] == '#':
            headr = headr + lne[1:]
            lne = fle.readline()

    headr = headr.rstrip('\n')

    swcData = np.loadtxt(swcFile)

    return headr, swcData

#***********************************************************************************************************************


def writeSWC_numpy(fName, swcData, headr=''):
    '''
    Write the SWC data in swcData to the file fName with the header headr
    :param fName: string
    :param swcData: 2D numpy.ndarray with 7 or 8 columns
    :param headr: string
    :return:
    '''

    swcData = np.array(swcData)
    assert swcData.shape[1] in [7, 8], 'Width given SWC Matrix data is incompatible.'


    formatStr = '%d %d %0.6f %0.6f %0.6f %0.6f %d'

    if swcData.shape[1] == 8:
         formatStr += ' %0.6f'

    np.savetxt(fName, swcData, formatStr, header=headr, comments='#')

#***********************************************************************************************************************


def transSWC(fName, A, b, destFle):
    '''
    Generate an SWC file at destFle with each point `x' of the morphology in fName transformed Affinely as Ax+b
    :param fName: string
    :param A: 2D numpy.ndarray of shape (3, 3)
    :param b: 3 member iterable
    :param destFle: string
    :return:
    '''

    headr = ''
    with open(fName, 'r') as fle:
        lne = fle.readline()
        while lne[0] == '#':
            headr = headr + lne[1:]
            lne = fle.readline()

    data = np.loadtxt(fName)
    data[:, 2:5] = np.dot(A, data[:, 2:5].T).T + np.array(b)

    if data.shape[1] == 7:
        formatStr = '%d %d %0.3f %0.3f %0.3f %0.3f %d'
    elif data.shape[1] == 8:
        formatStr = '%d %d %0.3f %0.3f %0.3f %0.3f %d %d'
    else:
        raise(TypeError('Data in the input file is of unknown format.'))

    np.savetxt(destFle, data, header=headr, fmt=formatStr)

#***********************************************************************************************************************


def transSWC_rotAboutPoint(fName, A, b, destFle, point):
    '''
    Generate an SWC file at destFle with each point `x' of the morphology in fName transformed Affinely as A(x-mu)+b
    where mu is a specified point.
    Essentially, the morphology is centered at a specified point before being Affinely transformed.
    :param fName: string
    :param A: 2D numpy.ndarray of shape (3, 3)
    :param b: 3 member iterable
    :param destFle: string
    :param point: 3 member iterable
    :return:
    '''

    headr = ''
    with open(fName, 'r') as fle:
        lne = fle.readline()
        while lne[0] == '#':
            headr = headr + lne[1:]
            lne = fle.readline()

    data = np.loadtxt(fName)
    pts = data[:, 2:5]
    rotAbout = np.array(point)
    ptsCentered = pts - rotAbout
    data[:, 2:5] = np.dot(A, ptsCentered.T).T + np.array(b) + rotAbout

    if data.shape[1] == 7:
        formatStr = '%d %d %0.3f %0.3f %0.3f %0.3f %d'
    elif data.shape[1] == 8:
        formatStr = '%d %d %0.3f %0.3f %0.3f %0.3f %d %d'
    else:
        raise(TypeError('Data in the input file is of unknown format.'))

    np.savetxt(destFle, data, header=headr, fmt=formatStr)
#***********************************************************************************************************************

def getPCADetails(swcFileName, center=True, data=None):
    '''
    Returns the principal components and standard deviations along the principal components.
    Ref: http://arxiv.org/pdf/1404.1100.pdf
    :param swcFileName: sting, input SWC file name
    :param center: Boolean,  if True, data is centered before calculating PCA
    :param data: numpy ndarray of shape [<>, 3]
    :return: PC, STDs
    PC: numpy.ndarray with the prinicial components of the data in its columns
    STDs: 3 member float iterable containing the standard variances of the data along the prinicipal components.
    '''

    if data is None:
        data = np.loadtxt(swcFileName)[:, 2:5]
    if center:
        mu = np.mean(data, axis=0)
        data = data - mu
    U, S, V = np.linalg.svd(data.T)
    dataProj = np.dot(U, data.T).T
    newStds = np.std(dataProj, axis=0)
    return U.T, newStds
#***********************************************************************************************************************

# **********************************************************************************************************************

def digitizeSWCXYZ(swcXYZ, gridUnitSizes):

    digSWCXYZ = np.empty_like(swcXYZ, dtype=np.intp)
    for ind in range(3):
        digSWCXYZ[:, ind] = np.array(np.around((swcXYZ[:, ind]) / gridUnitSizes[ind]), np.int)

    return digSWCXYZ

# **********************************************************************************************************************

def resampleSWC(swcFile, resampleLength, mask=None, swcData=None):
    '''
    Resample the SWC points to place points at every resamplelength along the central line of every segment. Radii are interpolated.
    :param swcData: nx4 swc point data
    :param resampleLength: length at with resampling is done.
    :return: totlLen, ndarray of shape (#pts, 4) with each row containing XYZR values
    '''

    if swcData is  None:
        swcData = np.loadtxt(swcFile)
    inds = swcData[:, 0].tolist()

    if mask is None:
        mask = [True] * swcData.shape[0]
    else:
        assert len(mask) == swcData.shape[0], 'Supplied mask is invalid for ' + swcFile
    resampledSWCData = []

    getSegLen = lambda a, b: np.linalg.norm(a - b)

    totalLen = 0
    for pt in swcData:

        if pt[6] < 0:
            if mask[inds.index(int(pt[0]))]:
                resampledSWCData.append(pt[2:6])

        if (pt[6] > 0) and (int(pt[6]) in inds):
            if mask[inds.index(int(pt[0]))]:
                resampledSWCData.append(pt[2:6])


                parentPt = swcData[inds.index(pt[6]), :]
                segLen = getSegLen(pt[2:5], parentPt[2:5])
                totalLen += segLen

                if segLen > resampleLength:

                    temp = parentPt[2:5] - pt[2:5]
                    distTemp = np.linalg.norm(temp)
                    unitDirection = temp / distTemp
                    radGrad = (pt[5] - parentPt[5]) / distTemp

                    for newPtsInd in range(1, int(np.floor(segLen / resampleLength)) + 1):

                        temp = (pt[2:5] + newPtsInd * resampleLength * unitDirection).tolist()
                        temp.append(pt[5] + newPtsInd * radGrad * resampleLength)
                        resampledSWCData.append(temp)

    return totalLen, np.array(resampledSWCData)

# **********************************************************************************************************************