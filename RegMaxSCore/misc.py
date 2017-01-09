import json

def parFileCheck(parFile, parNames):

    with open(parFile, 'r') as fle:
        parsList = json.load(fle)
        assert type(parsList) == list, 'Parameter file does not contain a list of dictionaries as is the requirement.'
        for parInd, par in enumerate(parsList):
            assert type(par) == dict, 'Parameter set # {} in {} not a list'.format(parInd, parFile)

            for pn in parNames:
                assert pn in par, 'Parameter {} not found in ' \
                                  'parameter set # {} of {} is improper'.format(pn, parInd, parFile)
    return parsList