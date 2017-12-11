import os
import shutil
import sys

homeFolder = os.path.expanduser('~')
thisFilePath = os.path.split(os.path.abspath(__file__))[0]

try:
    import regmaxsn
    utilsDir = os.path.join(os.path.abspath(regmaxsn.__path__[0]), 'scripts', 'utils')
except ImportError as e:
    raise(ImportError('The package regmaxsn must be installed before this script can be used.'))
whereToCreate = raw_input("Enter where the workspace must be created (using {} "
                          "if nothing is specifed):".format(homeFolder))
if whereToCreate == "":
    whereToCreate = homeFolder
assert os.path.exists(whereToCreate), "Specified path {} does not exist".format(whereToCreate)

pkgParFilesDir = os.path.join(thisFilePath, "ParFiles")
pkgTestFilesDir = os.path.join(thisFilePath, "TestFiles")

assert os.path.isdir(pkgParFilesDir) and os.path.isdir(pkgTestFilesDir), "Folders 'ParFiles' and 'TestFiles' that " \
                                                                         "came along with this script were not found!" \
                                                                         "Aborting!"

workSpace = os.path.join(whereToCreate, 'RegMaxSN_WorkSpace')
try:
    if os.path.exists(workSpace):
        ch = raw_input('A RegMaxSN Workspace already exists. Delete it and all files in it and create new one?(y/n):')
        if ch == "y":
            shutil.rmtree(workSpace)
        else:
            sys.exit('User Abort')
    os.mkdir(workSpace)
except IOError as e:
    raise(IOError('Error writing into {}. Please make sure its writable'.format(workSpace)))

parFilesDir = os.path.join(workSpace, "ParFiles")
shutil.copytree(pkgParFilesDir, parFilesDir)
testFilesDir = os.path.join(workSpace, "TestFiles")
shutil.copytree(pkgTestFilesDir, testFilesDir)
utilScriptsDir = os.path.join(workSpace, "utilityScripts")
shutil.copytree(utilsDir, utilScriptsDir)

resDir = os.path.join(workSpace, "Results")
os.mkdir(resDir)
os.mkdir(os.path.join(resDir, "Tests"))
os.mkdir(os.path.join(resDir, "Reg-MaxS"))
os.mkdir(os.path.join(resDir, "Reg-MaxS-N"))
os.mkdir(os.path.join(resDir, "PCABased"))

print("Succesfullly created Work Space at {}".format(workSpace))




